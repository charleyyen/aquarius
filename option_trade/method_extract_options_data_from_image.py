import re
import pytesseract
from PIL import Image
from typing import List, Dict
import pprint

def extract_options_data_from_image(image_path: str) -> List[Dict[str, str]]:
    """
    Extracts options chain data from an image into a list of dictionaries.

    This function performs OCR on the image, finds common data like the option
    type and expiration date, and then parses each data row. It formats the
    output as a list of dictionaries, excluding only the 'Action' column, 
    and prints the result before returning.

    Args:
        image_path: The file path to the input image.

    Returns:
        A list where each element is a dictionary representing a row of data,
        or an empty list if an error occurs or no data is found.
    """
    try:
        with Image.open(image_path) as img:
            text_data = pytesseract.image_to_string(img, config='--psm 6')
    except FileNotFoundError:
        print(f"Error: The file at {image_path} was not found.")
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
        if not line or not re.match(r'^\d+\.\d+', line):
            continue

        processed_line = re.sub(r'(\+?\d+\.\d+)\s+%', r'\1%', line)
        values = re.split(r'\s{2,}', processed_line)

        if len(values) == len(full_headers_for_parsing) - 1:
            values.insert(-1, '')

        if len(values) == len(full_headers_for_parsing):
            temp_row_data = dict(zip(full_headers_for_parsing, values))
            final_dict = {
                'Type': options_type,
                'Exp Date': exp_date
            }
            
            # Add all items from the temporary dict, but EXCLUDE only 'Action'
            for key, value in temp_row_data.items():
                if key != 'Action':
                    final_dict[key] = value

            result_list.append(final_dict)

    print("--- Final Extracted Data ---")
    pprint.pprint(result_list)
    print("----------------------------")

    return result_list

# --- Example Usage for the new image ---
if __name__ == '__main__':
    # Using the new image file you provided
    image_file = 'image_b19930.png' 
    
    extracted_data = extract_options_data_from_image(image_file)
    
    if extracted_data:
        print(f"\nSuccessfully extracted {len(extracted_data)} data row(s).")
