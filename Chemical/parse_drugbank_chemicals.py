'''
file : parse_drugbank_chemicals.py
author: Agrim Gupta

XML parser to parse the drugbank database and output a tsv file 
containting the following coloumn headers:
DrugbankID PubChem_Compound PubChem_Substance

Usage:
python parse_drugbank_chemicals.py <input_file_path>

Positional Arguments:
input_file   : Path to the durgbank.xml file.

Optional Arugments: 
--output_dir : Directory to create output files. Defaults to the current working directory.

Example Usage:
Input File: drugbank.xml

Output directory : outputs/chemical/

Comamnd line:
python parse_drugbank_chemicals.py drugbank.xml --output_dir outputs/chemicals/

Output: 
drugbank_parsed.tsv
'''

from bs4 import BeautifulSoup
import os
import argparse

parser = argparse.ArgumentParser(description='Parse Durgbank database for chemicals')
parser.add_argument('input_file', help='input file path. File should be the drugbank.xml file.')
parser.add_argument('--output_dir', help='directory to output files', default='.')
args = parser.parse_args()
outputFile = os.path.join(args.output_dir, "drugbank_parsed.tsv")
soup = BeautifulSoup(open(args.input_file),"xml")
sep = "\t"
empty = "NULL"
with open(outputFile, 'w') as f:
    for drug in soup.findAll("drug"):
        chemFound = False
        toPrint = ""
        toPrint += drug.find("drugbank-id").text + sep
        #toPrint += drug.find("name").text + sep
        identifiers = [i for i in drug.findAll("external-identifier")]
        for i in identifiers:
            database = i.find("resource").text
            if database != "PubChem Compound":
                continue
            value = i.find("identifier").text
            chemFound = True
            toPrint += value + sep
        if not chemFound:
            toPrint += empty + sep
        chemFound = False
        for i in identifiers:
            database = i.find("resource").text
            if database != "PubChem Substance":
                continue
            value = i.find("identifier").text
            chemFound = True
            toPrint += value
        if not chemFound:
            toPrint += empty
        f.write(toPrint.encode('utf-8') + '\n')
    
 
