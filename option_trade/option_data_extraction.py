import re
import pytesseract
import argparse
from PIL import Image
from typing import List, Dict
import pprint

def extract_options_data_from_image(image_path: str, debug: bool = False) -> List[Dict[str, str]]:
    """
    Extracts options chain data from an image into a list of dictionaries.
    
    Args:
        image_path (str): The full path to the input image file.
        debug (bool): If True, prints the raw OCR text for debugging.
    """
    try:
        with Image.open(image_path) as img:
            # Using --psm 4 is better for complex layouts with multiple columns.
            text_data = pytesseract.image_to_string(img, config='--psm 4')
    except FileNotFoundError:
        print(f"Error: The file at '{image_path}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred while processing the image: {e}")
        return []

    # If debug mode is enabled, print the raw OCR output
    if debug:
        print("--- RAW OCR OUTPUT (DEBUG MODE) ---")
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

    for line in lines:
        line = line.strip()
        
        header_match = re.search(r'(CALLS|PUTS)\s+.*?((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+[\'‘]\d{2})', line)
        if header_match:
            current_options_type = header_match.group(1)
            current_exp_date = header_match.group(2) 
            continue

        if current_exp_date and re.search(r'\d+\.\d+|,\d{3}', line):
            # Comprehensive cleaning based on all identified garbage characters
            garbage_chars = ['|', '¥', '©', '=', '«']
            cleaned_line = line
            for char in garbage_chars:
                cleaned_line = cleaned_line.replace(char, ' ')
            
            processed_line = re.sub(r'(\+?\d+\.\d+)\s+%', r'\1%', cleaned_line)
            values = processed_line.split()

            if len(values) == len(full_headers_for_parsing) - 1:
                values.insert(-1, '')

            if len(values) == len(full_headers_for_parsing):
                temp_row_data = dict(zip(full_headers_for_parsing, values))
                
                final_dict = {
                    'Type': current_options_type,
                    'Exp Date': current_exp_date
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
    parser = argparse.ArgumentParser(description="Extract options data from an image file.")
    
    parser.add_argument(
        '-i', 
        dest='image_file', 
        type=str, 
        required=True, 
        help="The full path to the input image file."
    )
    
    # New debug flag
    parser.add_argument(
        '-d', 
        '--debug', 
        dest='debug_mode', 
        action='store_true', 
        help="Enable debug mode to print raw OCR text."
    )
    
    args = parser.parse_args()
    
    # Pass the debug flag into the function
    extracted_data = extract_options_data_from_image(args.image_file, debug=args.debug_mode)
    
    if extracted_data:
        print(f"\nSuccessfully extracted {len(extracted_data)} data row(s).")
    else:
        print("\nNo data was extracted. Please check the image file and OCR output.")
