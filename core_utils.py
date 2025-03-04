import re
import unicodedata
import fitz
import os
import csv
from pdf_typs import pdf_types


def save_text_to_csv(output_directory, extracted_text):
    # Ensure the output directory exists, create it if not
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Created directory: {output_directory}")

    csv_filename = 'output.csv'
    csv_path = os.path.join(output_directory, csv_filename)

    # Extract the data from extracted_text[0]
    extracted_data = extracted_text[0]

    # Check if CSV exists; if not, create it with headers
    file_exists = os.path.exists(csv_path)

    with open(csv_path, mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=extracted_data.keys())

        # If file doesn't exist, write the headers
        if not file_exists:
            writer.writeheader()

        # Write the extracted data (as a row in the CSV)
        writer.writerow(extracted_data)

    print(f"Appended extracted data to {csv_path}")
def delete_pdf(pdf_path):
    try:
        os.remove(pdf_path)
        print(f"Deleted PDF file at {pdf_path}")
    except FileNotFoundError:
        print(f"File {pdf_path} not found, cannot delete.")
    except Exception as e:
        print(f"An error occurred while trying to delete {pdf_path}: {str(e)}")
def split_string(string):

  pattern = r"-"
  matches = re.finditer(pattern, string)
  last_index = len(string)
  for match in matches:
    last_index = match.start()
  return string[last_index:]
def extract_text_by_coordinates(pdf_path, page_num, rect):
    """
    Extracts text from a specified rectangular area on a PDF page.

    :param pdf_path: Path to the PDF file.
    :param page_num: Page number (starting from 0) to extract text from.
    :param rect: Tuple (left, top, right, bottom) representing the rectangular coordinates.
    :return: Extracted text from the specified area.
    """
    pdf_document = fitz.open(pdf_path)
    page = pdf_document[page_num]
    rect_region = fitz.Rect(*rect)
    text = page.get_text("text", clip=rect_region)
    pdf_document.close()
    return text
def is_arabic(text: str) -> bool:
    """
    Checks if the given text contains Arabic characters.

    Parameters
    ----------
    text : str
        The text to check.

    Returns
    -------
    bool
        True if the text contains Arabic characters, False otherwise.
    """
    for char in text:
        if '\u0600' <= char <= '\u06FF' or '\u0750' <= char <= '\u077F' or '\u08A0' <= char <= '\u08FF' or '\uFB50' <= char <= '\uFDFF' or '\uFE70' <= char <= '\uFEFF':
            return True
    return False
def handle_reverse_replace_newline(text):
    return text[::-1].replace('\n', '')
def handle_split_index(text, index):
    parts = text.split('\n')
    if len(parts) > index:
        return unicodedata.normalize('NFKC', parts[index])
    else:
        return None
def handle_replace_newline(text):
    return unicodedata.normalize('NFKC', text.replace('\n', ''))
def handle_reading_type(text):
    out_text = text.replace('\n', '')
    raTy = out_text.split("-")
    if len(raTy) > 1:
        return f"{raTy[0]} - {unicodedata.normalize('NFKC', raTy[1])}"
    else:
        raTy = out_text.split(" ")
        if len(raTy) > 1:
            return f"{raTy[0]} - {unicodedata.normalize('NFKC', raTy[1])}"
        else:
            return unicodedata.normalize('NFKC', out_text)
def extract_text_by_coordinates_new(page, coordinates):
    rect = fitz.Rect(coordinates)
    text = page.get_textbox(rect)
    return text
def determine_pdf_type(page):
    # doc = fitz.open(pdf_file)
    # page_number = 0  # Adjust if necessary
    # page = doc[page_number]
    # Coordinates and checks to determine PDF type
    thabit_coordinates = (16.98, 198.00, 169.96, 306.00)
    #TODO: update this coordinates
    nama_vat_coordinates = (57.11219787597656, 142.0579833984375, 133.68218994140625, 159.81597900390625)
    is_thabit = extract_text_by_coordinates_new(page, thabit_coordinates)
    is_nama_vat = extract_text_by_coordinates_new(page, nama_vat_coordinates)
    # doc.close()
    if "Thabit" in is_thabit:
        return 'new_nama'
    elif ('1100004061' in is_nama_vat) and ("Thabit" not in is_thabit):
        return 'old_nama'
    else:
        return 'dofar'
def extract_pdf_data(pdf_file):
    doc = fitz.open(pdf_file)
    data = {}
    num = 0
    for page_number in range(len(doc)):
        page = doc[page_number]
        pdf_type = determine_pdf_type(page)
        fields = pdf_types[pdf_type]['fields']
        page_data = {}
        for field_name, field_info in fields.items():
            coordinates = field_info['coordinates']
            handler = field_info.get('handler', lambda x: x)
            try:
                extracted_text = extract_text_by_coordinates_new(page, coordinates)
                value = handler(extracted_text)
                page_data[field_name] = value
            except Exception as e:
                print(f"Error processing field '{field_name}': {e}")
                page_data[field_name] = None
        data[num] = page_data
        num += 1
    doc.close()
    return data

def _dummy_data(acc):
    return {0: {
        "Customer": "null",
        "Customer_No": "null",
        "Account_No": f"{acc}",
        "Meter_No": "null",
        "Previous_Reading_Date": "null",
        "Previous_Reading": "null",
        "Current_Reading_Date": "null",
        "Current_Reading": "null",
        "Due_Date": "null",
        "Reading_Type": "null",
        "Tariff_Type": "null",
        "Invoice_Month": "null",
        "Government_Subsidy": "null",
        "Consumption_KWH_1": "null",
        "Rate_1": "null",
        "Consumption_KWH_2": "null",
        "Rate_2": "null",
        "Consumption_KWH_3": "null",
        "Rate_3": "null",
        "Consumption_KWH_4": "null",
        "Rate_4": "null",
        "Consumption_KWH_5": "null",
        "Rate_5": "null",
        "Consumption_KWH_6": "null",
        "Rate_6": "null",
        "Total_Before_VAT": "null",
        "VAT": "null",
        "Total_After_VAT": "null",
        "Total_Payable_Amount": "null"
    }}

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False