#!/usr/bin/env python3
# https://www.sosnc.gov/online_services/search/by_title/_Business_Registration_Changes
import pytesseract.pytesseract
import requests
from bs4 import BeautifulSoup
import urllib.request
from pdf2image import convert_from_path
import time
import os

os.environ['TESSDATA_PREFIX'] = 'Tesseract-OCR'
pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
POPPLER_PATH = r'poppler-23.11.0/Library/bin'


def filing_page(_sos_id: str):
    url = "https://sosnc.gov/online_services/search/_profile_filings"
    data = {
        "Id": _sos_id
    }
    response = requests.post(url, data=data)
    return response.content


def extract_pdf_id(_filing_page_html):
    soup = BeautifulSoup(_filing_page_html, features="html.parser")
    tag = soup.a
    if tag:
        return tag['id']
    else:
        return False


def download_pdf(_pdf_id: str):
    vault_url = "https://sosnc.gov/online_services/imaging/download_ivault_pdf"
    vault_data = {
        "Id": _pdf_id
    }
    vault_response = requests.post(vault_url, vault_data)
    file_name = vault_response.json()['fileName']
    _pdf_name, headers = urllib.request.urlretrieve(f"https://sosnc.gov/online_services/imaging/download/{file_name}", f"{file_name}.pdf")
    return _pdf_name


def extract_phone_number(_pdf_name: str):
    pages = convert_from_path(_pdf_name, dpi=300, poppler_path=POPPLER_PATH)
    pages[0].save(f'{_pdf_name[:-4]}.jpg', 'JPEG')
    page_text = pytesseract.image_to_string(f'{_pdf_name[:-4]}.jpg', lang='eng')
    index = page_text.find('telephone number:')
    if index == -1:
        return False
    else:
        beginning = index + len('telephone number:')
        number = ''
        i = 0
        while i < 20:
            character = page_text[beginning + i]
            if character.isnumeric():
                number += character
            i += 1
        return number


def clean_up(_pdf_name):
    os.remove(f'{_pdf_name[:-4]}.pdf')
    os.remove(f'{_pdf_name[:-4]}.jpg')


def main():
    start = time.time()
    input_file = open("input.csv", "r+")
    output_file = open("output.csv", "w")
    first_line = True
    for line in input_file:
        if first_line:
            line_text = "CorpName,PhoneNum,DateFormed,Citizenship,Type,Status,SOSID,RegAgent,RegAddr1,RegAddr2,RegCity,RegState,RegZip,RegCounty,PitemId,PrinAddr1,PrinAddr2,PrinCity,PrinState,PrinZip,PrinCounty"
            output_file.write(line_text)
            first_line = False
        else:
            fields = line.split(',')
            item_id = fields[13]
            filing_page_html = filing_page(item_id)
            pdf_id = extract_pdf_id(filing_page_html)
            if pdf_id:
                pdf_name = download_pdf(pdf_id)
                phone_number = extract_phone_number(pdf_name)
                clean_up(pdf_name)
                if phone_number:
                    new_line = f"{fields[0]}, {phone_number}"
                    for field in fields[1:]:
                        new_line += f', {field}'
                    output_file.write(new_line)

    print("Time elapsed: " + str(time.time() - start))

if __name__ == '__main__':
    main()
