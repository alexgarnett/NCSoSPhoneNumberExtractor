# North Carolina New Business Phone Number Extractor

This is a tool for extracting the phone number for newly registered businesses on the North Carolina Secretary of State 
website.

## About

This tool was built for my client in order to get in contact with the registered agent of newly created 
businesses. All information used or extracted by this tool is public record.

It uses information provided by the user in a CSV downloaded from the NC SoS business registration database to find a 
unique ID associated with the business registration. That ID is then used to locate the new business filing paperwork 
associated with that business, and download it. The tool then uses Optical Character Recognition on the downloaded 
document to extract the business's primary phone number.

This tool automates a very tedious and time-consuming task that my client was performing by hand so that he 
could find the phone number for new businesses and contact them about financing opportunities.

## Installation

First, clone the repo
```commandline
git clone
```

Next, install dependencies
```commandline
pip install requirements.txt
```

Then, you'll need to install the Tesseract engine and set up your tessdata directory. You can find detailed instructions 
about how to install Tesseract for your operating system at https://github.com/tesseract-ocr/tessdoc, but I've provided 
an overview below. 

#### Ubuntu

Install Tesseract
```commandline
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```

The app sets the environment variable _TESSDATA_PREFIX_ to "Tesseract-OCR/tessdata". Use the following commands to 
create the appropriate directory and move the Tesseract data there. 
```commandline
mkdir root/ez-scanner/Tesseract-OCR
cp -r usr/share/tesseract-ocr/4.00/tessdata/ root/ez-scanner/Tesseract-OCR/tessdata/
```

#### Windows

The tool looks for the executable file "tesseract.exe" in the "Tesseract-OCR" directory. For this reason, it is 
recommended to specify the Phone Number Extractor project directory as the install location during installation, or 
simply move the entire Tesseract folder into the project directory after installing. For convenience, I have included 
the tesseract setup executable in the root of this project.

The app sets the environment variable _TESSDATA_PREFIX_ to "Tesseract-OCR/tessdata". Upon successful installation of 
Tesseract, please locate the Tesseract trained data folder called "tessdata" and place it in a directory named 
"Tesseract-OCR" in the root directory of this project. Refer to the tessdoc README for details regarding where to 
locate the "tessdata" folder.

#### Mac OS

Please follow the installation instructions in the README at https://github.com/tesseract-ocr/tessdoc.

## Usage

In order to use the tool, first navigate to the NC SoS search tool for newly registered businesses using the link below:
https://www.sosnc.gov/online_services/search/by_title/_Business_Registration_Changes

You can then use the search parameters to search by date of registration, business type, and county, before downloading 
the search results as a CSV. I have also included a short example input file named "input.csv" that the tool can be 
tested with. 

After downloading the CSV, move it into the root directory of the project and name it "input.csv", being sure to 
overwrite any old instances of "input.csv." 

Then simply run the tool using 
```commandline
python3 main.py
```
The tool will take a few seconds per business to fetch and process the documents. Once finished, the results are saved 
in "output.csv" with the newly extracted phone numbers. If the tool was not able to extract a phone number, as they are 
often omitted from the filing paperwork, it will not include the record of the business in the output file.
