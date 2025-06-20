import re
import pytesseract
import argparse
from PIL import Image
from typing import List, Dict
import pprint
import cv2
import os

def post_process_and_correct_data(row_data: Dict[str, str]) -> Dict[str, str]:
    """
    Corrects predictable OCR errors in a single row of extracted data using a
    set of heuristic rules.
    """
    corrected_data = row_data.copy()
    
    two_decimal_columns = ['Last', 'Change', 'Bid', 'Ask']
    
    # --- RULE 1: Fix missing decimal points for 2-decimal columns ---
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

    # --- RULE 2: Fix the specific OCR error where '+' is read as '4' in the 'Change' column ---
    change_val = corrected_data.get('Change', '')
    if change_val.startswith('40.'):
        corrected_data['Change'] = '+' + change_val[1:]
        
    # --- RULE 3: Fix the specific OCR error where a leading '+' is read as '4' in the '% Change' column ---
    pct_change_val = corrected_data.get('% Change', '')
    if pct_change_val and pct_change_val.startswith('4'):
        corrected_data['% Change'] = '+' + pct_change_val[1:]
        
    # --- RULE 4: Fix Gamma column based on your rules ---
    gamma_val = corrected_data.get('Gamma', '')
    if '.' not in gamma_val and gamma_val.startswith('0') and len(gamma_val) > 1:
        # Insert '.' after the first '0'. e.g., '01048' -> '0.1048'
        corrected_data['Gamma'] = gamma_val[0] + '.' + gamma_val[1:]

    # --- RULE 5: Fix Delta column based on your rules ---
    delta_val = corrected_data.get('Delta', '')
    if '.' not in delta_val and delta_val.replace('-', '').isdigit():
        sign = ''
        num_part = delta_val
        if delta_val.startswith('-'):
            sign = '-'
            num_part = delta_val[1:]
        
        # Format to 0.xxxx or -0.xxxx
        # lstrip('0') handles cases like '01234' -> '1234'
        num_part = num_part.lstrip('0')
        corrected_data['Delta'] = sign + '0.' + num_part
                    
    return corrected_data

def format_currency_columns(row_data: Dict[str, str]) -> Dict[str, str]:
    """
    Adds a '$' prefix to specified currency columns.
    """
    formatted_data = row_data.copy()
    currency_columns = ['Last', 'Bid', 'Ask']
    
    for key in currency_columns:
        if key in formatted_data:
            if not formatted_data[key].startswith('$'):
                formatted_data[key] = '$' + formatted_data[key]
                
    return formatted_data

def clean_percentage_columns(row_data: Dict[str, str]) -> Dict[str, str]:
    """
    Removes the '%' symbol from specified percentage columns.
    """
    cleaned_data = row_data.copy()
    percentage_columns = ['% Change', 'IV %']
    
    for key in percentage_columns:
        if key in cleaned_data:
            cleaned_data[key] = cleaned_data[key].replace('%', '')
            
    return cleaned_data

def format_exp_date(date_str: str) -> str:
    """
    Converts a date string from "Mon Day 'YY" format to "MM/DD/YY".
    """
    month_map = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
        'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }
    try:
        parts = date_str.split()
        month_abbr = parts[0]
        day = parts[1]
        year = parts[2].replace("'", "")
        
        month_num = month_map.get(month_abbr, "00")
        
        return f"{month_num}/{day}/{year}"
    except (IndexError, KeyError):
        return date_str

def remove_commas_from_numbers(row_data: Dict[str, str]) -> Dict[str, str]:
    """
    Removes commas from all values in the data dictionary.
    """
    cleaned_data = {}
    for key, value in row_data.items():
        if isinstance(value, str):
            cleaned_data[key] = value.replace(',', '')
        else:
            cleaned_data[key] = value
            
    return cleaned_data

def format_decimal_places(row_data: Dict[str, str]) -> Dict[str, str]:
    """
    Formats specified columns to a fixed number of decimal places.
    """
    formatted_data = row_data.copy()
    two_places_cols = ['Last', 'Change', '% Change', 'Bid', 'Ask', 'IV %']
    four_places_cols = ['Delta', 'Gamma']

    all_cols_to_format = two_places_cols + four_places_cols

    for key, value in formatted_data.items():
        if key not in all_cols_to_format:
            continue

        try:
            sign = ''
            num_str = value
            # For values that start with a sign, separate the sign so 'float()' works
            if isinstance(num_str, str) and num_str.startswith(('+', '-')):
                sign = num_str[0]
                num_str = num_str[1:]
            
            float_val = float(num_str)
            
            if key in two_places_cols:
                formatted_num = f"{float_val:.2f}"
            elif key in four_places_cols:
                formatted_num = f"{float_val:.4f}"
            else:
                formatted_num = str(float_val)

            formatted_data[key] = sign + formatted_num
        except (ValueError, TypeError):
            continue
            
    return formatted_data


def extract_options_data_from_image(image_path: str, debug: bool = False) -> List[Dict[str, str]]:
    """
    Extracts options chain data from an image into a list of dictionaries.
    """
    try:
        original_img = cv2.imread(image_path)
        if original_img is None:
            raise FileNotFoundError(f"Could not read the image file at '{image_path}'. Check the path.")

        upscaled_img = cv2.resize(original_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        gray_img = cv2.cvtColor(upscaled_img, cv2.COLOR_BGR2GRAY)
        _, thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        dir_name = os.path.dirname(image_path)
        base_name = os.path.basename(image_path)
        new_filename = f"new_{base_name}"
        new_image_path = os.path.join(dir_name, new_filename)
        cv2.imwrite(new_image_path, thresh_img)
        print(f"Saved pre-processed image to: {new_image_path}")

        text_data = pytesseract.image_to_string(thresh_img, config='--psm 4')

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return []
    except Exception as e:
        print(f"An error occurred during image processing or OCR: {e}")
        return []

    if debug:
        print("\n--- RAW OCR OUTPUT (DEBUG MODE) ---")
        print(text_data)
        print("-----------------------------------\n")

    lines = text_data.strip().split('\n')
    result_list = []
    current_options_type = None
    current_exp_date = None

    full_headers_for_parsing = [
        'Last', 'Change', '% Change', 'Bid', 'Bid Size', 'Ask', 'Ask Size',
        'Volume', 'Open Int', 'IV %', 'Delta', 'Gamma', 'Action', 'Strike'
    ]
    
    data_pattern = r"([+-]?\d[\d,.]*%?)"

    for line in lines:
        line = line.strip()
        
        header_match = re.search(r'(CALLS|PUTS)\s+.*?((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+[\'‘]\d{2})', line)
        if header_match:
            current_options_type = header_match.group(1)
            date_from_ocr = header_match.group(2)
            current_exp_date = format_exp_date(date_from_ocr)
            continue

        ascii_line = line.encode("ascii", "ignore").decode()
        values = re.findall(data_pattern, ascii_line)

        VOLUME_COL_INDEX = 7
        if len(values) == 12 and len(values[VOLUME_COL_INDEX]) == 2 and values[VOLUME_COL_INDEX].startswith('0'):
            merged_val = values[VOLUME_COL_INDEX]
            values[VOLUME_COL_INDEX] = '0' 
            values.insert(VOLUME_COL_INDEX + 1, merged_val[1])

        if current_exp_date and len(values) > 5:
            if len(values) == len(full_headers_for_parsing) - 1:
                values.insert(-1, '')

            if len(values) == len(full_headers_for_parsing):
                temp_row_data = dict(zip(full_headers_for_parsing, values))
                
                corrected_row_data = post_process_and_correct_data(temp_row_data)
                
                final_dict = { 'Type': current_options_type, 'Exp Date': current_exp_date }
                for key, value in corrected_row_data.items():
                    if key != 'Action': final_dict[key] = value
                
                percent_cleaned_dict = clean_percentage_columns(final_dict)
                comma_cleaned_dict = remove_commas_from_numbers(percent_cleaned_dict)
                decimal_formatted_dict = format_decimal_places(comma_cleaned_dict)
                fully_formatted_dict = format_currency_columns(decimal_formatted_dict)

                result_list.append(fully_formatted_dict)

    print("\n--- Final Extracted Data ---")
    if not result_list:
        print("(Result list is empty)")
    else:
        pprint.pprint(result_list)
    print("----------------------------")

    return result_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract options data from an image file.")
    parser.add_argument('-i', dest='image_file', type=str, required=True, help="The full path to the input image file.")
    parser.add_argument('-d', '--debug', dest='debug_mode', action='store_true', help="Enable debug mode to print raw OCR text.")
    args = parser.parse_args()
    
    extracted_data = extract_options_data_from_image(args.image_file, debug=args.debug_mode)
    
    if extracted_data:
        print(f"\nSuccessfully extracted {len(extracted_data)} data row(s).")
    else:
        print("\nNo data was extracted. Please check the image file and OCR output.")
