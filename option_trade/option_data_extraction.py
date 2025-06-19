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
    
    # --- RULE 1: Fix missing decimal points ---
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
        # Based on the rule that % Change always has a sign, if it starts with '4',
        # we assume it was a misread '+' sign.
        corrected_data['% Change'] = '+' + pct_change_val[1:]
                    
    return corrected_data


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
        'Volume', 'Open Int', 'Imp Vol', 'Delta', 'Gamma', 'Action', 'Strike'
    ]
    
    data_pattern = r"([+-]?\d[\d,.]*%?)"

    for line in lines:
        line = line.strip()
        
        header_match = re.search(r'(CALLS|PUTS)\s+.*?((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+[\'‘]\d{2})', line)
        if header_match:
            current_options_type = header_match.group(1)
            current_exp_date = header_match.group(2) 
            continue

        ascii_line = line.encode("ascii", "ignore").decode()
        values = re.findall(data_pattern, ascii_line)

        # --- RULE 4: Fix the "merged column" OCR error ---
        # This checks for the specific case where 'Volume' and 'Open Int' are merged.
        # It detects when we have 12 columns and the 'Volume' column looks like a merged value (e.g., '03').
        VOLUME_COL_INDEX = 7 # The 8th column is at index 7
        if len(values) == 12 and len(values[VOLUME_COL_INDEX]) == 2 and values[VOLUME_COL_INDEX].startswith('0'):
            # It's the merged column error, let's split it back into two.
            merged_val = values[VOLUME_COL_INDEX]
            # The first part is always '0' in this error pattern
            values[VOLUME_COL_INDEX] = '0' 
            # The second part is the second digit of the merged value
            values.insert(VOLUME_COL_INDEX + 1, merged_val[1])
            # The 'values' list now has 13 items and is corrected.

        if current_exp_date and len(values) > 5:
            if len(values) == len(full_headers_for_parsing) - 1:
                values.insert(-1, '')

            if len(values) == len(full_headers_for_parsing):
                temp_row_data = dict(zip(full_headers_for_parsing, values))
                
                corrected_row_data = post_process_and_correct_data(temp_row_data)
                
                final_dict = {
                    'Type': current_options_type,
                    'Exp Date': current_exp_date
                }
                
                for key, value in corrected_row_data.items():
                    if key != 'Action':
                        final_dict[key] = value

                result_list.append(final_dict)

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
