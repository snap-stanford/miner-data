import os
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser(description='Parse Durgbank database for chemicals')
parser.add_argument('input_file', help='input file path. File should be the drugbank.xml file.')
parser.add_argument('--output_dir', help='directory to output files', default='.')
args = parser.parse_args()
outputFile = os.path.join(args.output_dir, "drugbank_parse_test1.tsv")
soup = BeautifulSoup(open(args.input_file),"xml")
sep = "\t"
empty = "NULL"
fields = ["name", "description", "general-references", "synthesis-reference",
          "protein-binding", "classification", "salts", "synonyms", "products", "international-brands", "mixtures",
          "manufacturers", "prices", "categories", "dosages", "atc-codes", "food-interactions", "pathways","reactions",
          "snp-effects","snp-adverse-drug-reactions"]
header = ["drugbankID", "pc_Compund", "pc_substance"] + fields;

with open(outputFile, 'w') as f:
    f.write("# " + sep.join(header) + '\n')
    counter = 0 
    drugs = soup.findAll("drug")
    for drug in drugs:
        drugline = ''
        if not drug.find("name"):
            name = empty
	else:
            name = drug.find("name").text
        counter += 1
        drugline += (str(counter)+" ")
	drugline += (str(name) + " ")
        #drugline += drug.find('drugbank-id').text + sep
        drugline = drugline.encode('utf-8')
        f.write(drugline+'\n')
