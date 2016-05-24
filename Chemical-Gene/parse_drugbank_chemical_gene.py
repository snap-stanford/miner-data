'''
file : parse_drugbank_chemical_gene.py
author: Agrim Gupta

XML parser to parse the drugbank database for chemical gene interactions. 
Outputs a tab separated .tsv file with the following coloumn headers:
DrugbankId Gene1 Gene2 ...
Currently UniportID is used for genes.

Usage:
python parse_drugbank_chemical_gene.py <input_file_path>

Positional Arguments:
input_file   : Path to the durgbank.xml file.

Optional Arugments: 
--output_dir : Directory to create output files. Defaults to the current working directory.

Example Usage:
Input File: drugbank.xml

Output directory : outputs/chemical/

Comamnd line:
python parse_drugbank_chemical_gene.py drugbank.xml --output_dir outputs/chemicals/

Output: 
drugbank_parsed_chemical_gene.tsv
'''

from bs4 import BeautifulSoup
import os
import argparse

parser = argparse.ArgumentParser(description='Parse Durgbank database for drug gene interaction')
parser.add_argument('input_file', help='input file path. File should be the drugbank.xml file.')
parser.add_argument('--output_dir', help='directory to output files', default='.')
args = parser.parse_args()
outputFile = os.path.join(args.output_dir, "drugbank_parsed_chemical_gene.tsv")
soup = BeautifulSoup(open(args.input_file),"xml")
sep = "\t"
empty = "NULL"
#geneIdentifier = "HUGO Gene Nomenclature Committee (HGNC)"
geneIdentifier = "UniProtKB"
with open(outputFile, 'w') as f:
    for drug in soup.findAll("drug"):
        toPrint = ""
        toPrint += drug.find("drugbank-id").text + sep
        # Get target Genes
        targets = drug.findAll("target")
        targetGene = []
        if targets:
            for target in targets:
                externIden = target.findAll("external-identifier")
                if not externIden:
                    continue
                for iden in externIden:
                    if iden.find("resource").text == geneIdentifier:
                        targetGene.append(iden.find("identifier").text)
        # Get Enzyme Gene
        enzymes = drug.findAll("enzyme")
        enzymeGene = []
        if enzymes:
            for enzyme in enzymes:
                externIden = enzyme.findAll("external-identifier")
                if not externIden:
                    continue
                for iden in externIden:
                    if iden.find("resource").text == geneIdentifier:
                        enzymeGene.append(iden.find("identifier").text)
        allGene = targetGene + enzymeGene
        if len(allGene) == 0:
            toPrint += empty
        else:
            toPrint += ','.join(allGene)
        f.write(toPrint.encode('utf-8') + '\n')
