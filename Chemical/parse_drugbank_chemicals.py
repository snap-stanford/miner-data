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
fields = ["name", "description", "general-references", "synthesis-reference",
          "protein-binding", "classification", "salts", "synonyms", "products", "international-brands", "mixtures",
          "manufacturers", "prices", "categories", "dosages", "atc-codes", "food-interactions", "pathways","reactions",
          "snp-effects","snp-adverse-drug-reactions"]
header = ["drugbankID", "pc_Compund", "pc_substance"] + fields;

seenids = set()
seen = set()

def recur(elem,l):
    for e in elem.findChildren():
        if not e.findChildren():
            l.append(e.text.strip())
        else:
            recur(e, l)

with open(outputFile, 'w') as f:
    f.write("# " + sep.join(header) + '\n')
    for drug in soup.findAll("drug"):
        name = drug.find("name").text
        id = drug.find("drugbank-id").text
        if name not in seen or id not in seenids:
                  chemFound = False
                  toPrint = ""
                  toPrint += drug.find("drugbank-id").text + sep
                  seen.add(drug.find("name").text)
                  seenids.add(id)
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
                      toPrint += value + sep
                  if not chemFound:
                      toPrint += empty + sep 
                  attributes = []
                  for field in fields:
                      l = []
                      if not drug.find(field):
                          attributes.append(empty)
                          continue
                      if drug.find(field).findChildren():
                          recur(drug.find(field),l)
                          for i in range(len(l)):
                              if l[i] == "":
                                  l[i] = empty
                          attributes.append("|".join(l).encode('utf-8'))
                      else:
                          if drug.find(field).text != "":
                              genRef = drug.find(field).text
                              genRef = genRef.split("\n")
                              attributes.append("|".join(genRef).encode('utf-8'))
                              #attributes.append(drug.find(field).text.encode('utf-8'))
                          else:
                              attributes.append(empty)
                  toPrint = toPrint.encode('utf-8') + sep.join(attributes)
                  f.write(toPrint + '\n')

