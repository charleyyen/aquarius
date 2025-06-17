#!/usr/bin/python3
import re
import pytesseract
import argparse
from PIL import Image
from typing import List, Dict
import pprint

def extract_options_data_from_image(image_path: str) -> List[Dict[str, str]]:
    """
    Extracts options chain data from an image into a list of dictionaries.
    """
    try:
        with Image.open(image_path) as img:
            text_data = pytesseract.image_to_string(img, config='--psm 6')
    except FileNotFoundError:
        print(f"Error: The file at '{image_path}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred while processing the image: {e}")
        return []

    lines = text_data.strip().split('\n')
    result_list = []
    options_type = None
    exp_date = None

    for line in lines:
        match = re.search(r'(CALLS|PUTS)\s+((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+\'\d{2})', line)
        if match:
            options_type = match.group(1)
            exp_date = match.group(2)
            break

    full_headers_for_parsing = [
        'Last', 'Change', '% Change', 'Bid', 'Bid Size', 'Ask', 'Ask Size',
        'Volume', 'Open Int', 'Imp Vol', 'Delta', 'Gamma', 'Action', 'Strike'
    ]

    for line in lines:
        line = line.strip()
        
        if re.search(r'\d+\.\d+', line):
            processed_line = re.sub(r'(\+?\d+\.\d+)\s+%', r'\1%', line)
            
            # --- THE FIX IS HERE ---
            # Changed from re.split() to the standard string .split() method, 
            # which correctly handles columns separated by single spaces.
            values = processed_line.split()

            if len(values) == len(full_headers_for_parsing) - 1:
                values.insert(-1, '')

            if len(values) == len(full_headers_for_parsing):
                temp_row_data = dict(zip(full_headers_for_parsing, values))
                final_dict = {
                    'Type': options_type,
                    'Exp Date': exp_date
                }
                
                for key, value in temp_row_data.items():
                    if key != 'Action':
                        final_dict[key] = value

                result_list.append(final_dict)

    print("--- Final Extracted Data ---")
    if not result_list:
        print("(Result list is empty)")
    else:
        pprint.pprint(result_list)
    print("----------------------------")

    return result_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Extract options data from an image file."
    )
    
    parser.add_argument(
        '-i', 
        dest='image_file', 
        type=str, 
        required=True, 
        help="The full path to the input image file."
    )
    
    args = parser.parse_args()
    
    extracted_data = extract_options_data_from_image(args.image_file)
    
    if extracted_data:
        print(f"\nSuccessfully extracted {len(extracted_data)} data row(s).")
    else:
        print("\nNo data was extracted. Please check the image file.")
