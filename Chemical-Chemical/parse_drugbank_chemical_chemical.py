'''
file : parse_drugbank_chemical_chemical.py
author: Agrim Gupta

XML parser to parse the drugbank database for chemical chemical interactions. 
Outputs a tab separated .tsv file with the following coloumn headers:
DrugbankId DrugbankId

Usage:
python parse_drugbank_chemical_chemical.py <input_file_path>

Positional Arguments:
input_file   : Path to the durgbank.xml file.

Optional Arugments: 
--output_dir : Directory to create output files. Defaults to the current working directory.

Example Usage:
Input File: drugbank.xml

Output directory : outputs/chemical/

Comamnd line:
python parse_drugbank_chemical_chemical.py drugbank.xml --output_dir outputs/chemicals/

Output: 
drugbank_parsed_chemical_chemical.tsv
'''

from bs4 import BeautifulSoup
import os
import argparse

parser = argparse.ArgumentParser(description='Parse Durgbank database for drug drug interaction')
parser.add_argument('input_file', help='input file path. File should be the drugbank.xml file.')
parser.add_argument('--output_dir', help='directory to output files', default='.')
args = parser.parse_args()
outputFile = os.path.join(args.output_dir, "drugbank_parsed_chemical_chemical.tsv")
soup = BeautifulSoup(open(args.input_file),"xml")
sep = "\t"
empty = "NULL"
with open(outputFile, 'w') as f:
    for drug in soup.findAll("drug"):
        drugName = drug.find("drugbank-id").text 
        interactions = drug.findAll("drug-interaction")
        if not interactions:
            continue
        for i in interactions:
            toPrint = drugName + sep + i.find("drugbank-id").text + sep + i.find("description").text
            f.write(toPrint.encode('utf-8') + '\n')
