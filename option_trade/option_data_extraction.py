import re
import pytesseract
import easyocr
import argparse
from PIL import Image
from typing import List, Dict
import pprint
import cv2
import os
import csv

# --- Helper Functions for Data Correction and Formatting ---

def post_process_and_correct_data(row_data: Dict[str, str]) -> Dict[str, str]:
    """Corrects predictable OCR errors in a single row of extracted data."""
    corrected_data = row_data.copy()
    two_decimal_columns = ['Last', 'Change', 'Bid', 'Ask']
    # Rule 1: Fix missing decimals
    for key, value in corrected_data.items():
        if key in two_decimal_columns and '.' not in value:
            sign = ''
            num_part = value
            if value.startswith(('+', '-')):
                sign = value[0]
                num_part = value[1:]
            if num_part.isdigit() and len(num_part) >= 2:
                new_num = num_part[:-2] + '.' + num_part[-2:]
                corrected_data[key] = sign + new_num
    # Rule 2: Fix 'Change' column '+' read as '4'
    change_val = corrected_data.get('Change', '')
    if change_val.startswith('40.'):
        corrected_data['Change'] = '+' + change_val[1:]
    # Rule 3: Fix '% Change' column '+' read as '4'
    pct_change_val = corrected_data.get('% Change', '')
    if pct_change_val and pct_change_val.startswith('4'):
        corrected_data['% Change'] = '+' + pct_change_val[1:]
    # Rule 4 & 5: Fix 'Gamma' and 'Delta' missing decimals
    gamma_val = corrected_data.get('Gamma', '')
    if '.' not in gamma_val and gamma_val.startswith('0') and len(gamma_val) > 1:
        corrected_data['Gamma'] = gamma_val[0] + '.' + gamma_val[1:]
    delta_val = corrected_data.get('Delta', '')
    if '.' not in delta_val and delta_val.replace('-', '').isdigit():
        sign = ''
        num_part = delta_val
        if delta_val.startswith('-'):
            sign = '-'
            num_part = delta_val[1:]
        num_part = num_part.lstrip('0')
        corrected_data['Delta'] = sign + '0.' + num_part
    return corrected_data

def format_currency_columns(row_data: Dict[str, str]) -> Dict[str, str]:
    """Adds a '$' prefix to specified currency columns."""
    formatted_data = row_data.copy()
    currency_columns = ['Last', 'Bid', 'Ask']
    for key in currency_columns:
        if key in formatted_data and not formatted_data[key].startswith('$'):
            formatted_data[key] = '$' + formatted_data[key]
    return formatted_data

def clean_percentage_columns(row_data: Dict[str, str]) -> Dict[str, str]:
    """Removes the '%' symbol from specified percentage columns."""
    cleaned_data = row_data.copy()
    percentage_columns = ['% Change', 'Imp Vol']
    for key in percentage_columns:
        if key in cleaned_data:
            cleaned_data[key] = cleaned_data[key].replace('%', '')
    return cleaned_data

def format_exp_date(date_str: str) -> str:
    """Converts a date string from "Mon Day 'YY" format to "MM/DD/YY"."""
    month_map = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
        'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }
    try:
        parts = date_str.split()
        month_abbr, day, year_part = parts[0], parts[1], parts[2]
        year = year_part.replace("'", "")
        month_num = month_map.get(month_abbr, "00")
        return f"{month_num}/{day}/{year}"
    except (IndexError, KeyError):
        return date_str

def remove_commas_from_numbers(row_data: Dict[str, str]) -> Dict[str, str]:
    """Removes commas from all values in the data dictionary."""
    cleaned_data = {}
    for key, value in row_data.items():
        cleaned_data[key] = str(value).replace(',', '')
    return cleaned_data

def format_decimal_places(row_data: Dict[str, str]) -> Dict[str, str]:
    """Formats specified columns to a fixed number of decimal places."""
    formatted_data = row_data.copy()
    two_places_cols = ['Last', 'Change', '% Change', 'Bid', 'Ask', 'Imp Vol', 'Spread %']
    three_places_cols = ['Mean']
    four_places_cols = ['Delta', 'Gamma']
    all_cols_to_format = two_places_cols + three_places_cols + four_places_cols

    for key, value in formatted_data.items():
        if key not in all_cols_to_format: continue
        try:
            sign = ''
            num_str = str(value)
            if num_str.startswith(('+', '-')):
                sign = num_str[0]
                num_str = num_str[1:]
            
            float_val = float(num_str)
            
            if key in two_places_cols: formatted_num = f"{float_val:.2f}"
            elif key in three_places_cols: formatted_num = f"{float_val:.3f}"
            elif key in four_places_cols: formatted_num = f"{float_val:.4f}"
            else: formatted_num = str(float_val)

            formatted_data[key] = sign + formatted_num
        except (ValueError, TypeError):
            continue
    return formatted_data

def calculate_new_columns(row_data: Dict[str, str]) -> Dict[str, str]:
    """Calculates 'Mean' and 'Spread %' from Bid and Ask prices."""
    calcs = {}
    try:
        bid_str = str(row_data.get('Bid', '0'))
        ask_str = str(row_data.get('Ask', '0'))
        bid = float(bid_str)
        ask = float(ask_str)

        if bid > 0 and ask > 0:
            mean = (bid + ask) / 2
            spread = ask - bid
            spread_pct = (spread / mean) * 100 if mean != 0 else 0
            calcs['Mean'] = mean
            calcs['Spread %'] = spread_pct
        else:
            calcs['Mean'] = 0.0
            calcs['Spread %'] = 0.0
    except (ValueError, TypeError):
        calcs['Mean'] = 0.0
        calcs['Spread %'] = 0.0
    return calcs

# --- NEW ENHANCEMENT: QUALITY CONTROL FLAGS ---
def add_quality_control_flags(row_data: Dict[str, str]) -> Dict[str, str]:
    """Adds a QC_FLAG column based on data validation rules."""
    flagged_data = row_data.copy()
    flagged_data['QC_FLAG'] = '' # Initialize with no flag

    # As requested, the benchmark is hardcoded here for easy editing.
    SPREAD_THRESHOLD = 30.0

    try:
        # Check 1: Bid price should not be greater than Ask price.
        bid = float(str(row_data.get('Bid', '0.0')))
        ask = float(str(row_data.get('Ask', '0.0')))
        if bid > ask:
            flagged_data['QC_FLAG'] = 'INVALID_BID_ASK'
            return flagged_data # Exit early, as this is a critical error

        # Check 2: Flag if spread percentage is too high.
        spread_pct = float(str(row_data.get('Spread %', '0.0')))
        if spread_pct > SPREAD_THRESHOLD:
            flagged_data['QC_FLAG'] = 'HIGH_SPREAD_PCT'

    except (ValueError, TypeError):
        # If data can't be converted to float, flag it as invalid.
        flagged_data['QC_FLAG'] = 'INVALID_NUMERIC_DATA'

    return flagged_data

def write_data_to_csv(data_list: List[Dict], output_path: str, final_headers: List[str]):
    """Writes the final list of dictionaries to a CSV file."""
    if not data_list:
        print("No data to write to CSV.")
        return
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=final_headers, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(data_list)
        print(f"\nSuccessfully saved data to: {output_path}")
    except IOError as e:
        print(f"\nError writing to CSV file: {e}")

# --- Main Extraction and Processing Function ---
def extract_and_process_data(image_path: str, debug: bool = False, engine: str = 'tesseract') -> List[Dict[str, str]]:
    """Main function to extract, process, and format options data from an image."""
    try:
        original_img = cv2.imread(image_path)
        if original_img is None: raise FileNotFoundError(f"Could not read image: {image_path}")
        upscaled_img = cv2.resize(original_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        gray_img = cv2.cvtColor(upscaled_img, cv2.COLOR_BGR2GRAY)
        _, thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        print(f"Using '{engine}' OCR engine...")
        if engine == 'easyocr':
            reader = easyocr.Reader(['en'])
            text_data = '\n'.join(reader.readtext(thresh_img, detail=0, paragraph=True))
        else:
            text_data = pytesseract.image_to_string(thresh_img, config='--psm 4')
    except Exception as e:
        print(f"An error occurred during image processing or OCR: {e}")
        return []
    
    if debug: print("\n--- RAW OCR OUTPUT ---\n" + text_data + "\n---------------------\n")
    
    lines = text_data.strip().split('\n')
    result_list = []
    current_options_type, current_exp_date = None, None
    raw_headers = ['Last', 'Change', '% Change', 'Bid', 'Bid Size', 'Ask', 'Ask Size', 'Volume', 'Open Int', 'Imp Vol', 'Delta', 'Gamma', 'Action', 'Strike']
    data_pattern = r"([+-]?\d[\d,.]*%?)"

    for line in lines:
        line = line.strip()
        header_match = re.search(r'(CALLS|PUTS)\s+.*?(Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+[\'‘]\d{2}', line)
        if header_match:
            current_options_type = header_match.group(1)
            date_str_match = re.search(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+[\'‘]\d{2})', line)
            if date_str_match: current_exp_date = format_exp_date(date_str_match.group(1).replace("‘", "'"))
            continue

        values = re.findall(data_pattern, line.encode("ascii", "ignore").decode())
        
        VOLUME_COL_INDEX = 7
        if len(values) == 12 and len(values[VOLUME_COL_INDEX]) == 2 and values[VOLUME_COL_INDEX].startswith('0'):
            merged_val = values[VOLUME_COL_INDEX]
            values[VOLUME_COL_INDEX] = '0'
            values.insert(VOLUME_COL_INDEX + 1, merged_val[1])
        
        if current_exp_date and len(values) > 5:
            if len(values) == len(raw_headers) - 1: values.insert(-1, '')
            if len(values) == len(raw_headers):
                temp_row_data = dict(zip(raw_headers, values))
                
                # --- START OF PROCESSING PIPELINE ---
                corrected_data = post_process_and_correct_data(temp_row_data)
                
                base_dict = {'Type': current_options_type, 'Exp Date': current_exp_date}
                base_dict.update(corrected_data)
                
                percent_cleaned = clean_percentage_columns(base_dict)
                comma_cleaned = remove_commas_from_numbers(percent_cleaned)
                
                new_calcs = calculate_new_columns(comma_cleaned)
                comma_cleaned.update(new_calcs)

                qc_flagged = add_quality_control_flags(comma_cleaned)
                
                rename_map = {'% Change': 'Change %', 'Imp Vol': 'Imp Vol %'}
                renamed_data = {rename_map.get(k, k): v for k, v in qc_flagged.items()}
                
                decimal_formatted = format_decimal_places(renamed_data)
                fully_formatted = format_currency_columns(decimal_formatted)
                # --- END OF PROCESSING PIPELINE ---

                result_list.append(fully_formatted)
    
    return result_list

# --- Main Execution Block ---
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract options data from an image file and save it to a CSV.", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', dest='image_file', type=str, required=True, help="The full path to the input image file.")
    parser.add_argument('-o', dest='output_file', type=str, help="Path for the output CSV file. (default: uses input name)")
    parser.add_argument('-e', '--engine', dest='engine', choices=['tesseract', 'easyocr'], default='tesseract', help="Specify the OCR engine to use. (default: tesseract)")
    parser.add_argument('-d', '--debug', dest='debug_mode', action='store_true', help="Enable debug mode to print raw OCR text.")
    
    args = parser.parse_args()
    
    if args.output_file: output_csv_path = args.output_file
    else:
        base_name = os.path.splitext(os.path.basename(args.image_file))[0]
        output_csv_path = f"{base_name}.csv"
        
    processed_data = extract_and_process_data(args.image_file, debug=args.debug_mode, engine=args.engine)
    
    final_csv_headers = [
        'Type', 'Strike', 'Volume', 'Open Int', 'Bid', 'Bid Size', 'Ask', 'Ask Size', 
        'Last', 'Change', 'Change %', 'Mean', 'Spread %', 'Imp Vol %', 'Delta', 'Gamma', 
        'QC_FLAG', 'Exp Date' # Added new QC_FLAG column
    ]
    
    write_data_to_csv(processed_data, output_csv_path, final_csv_headers)
