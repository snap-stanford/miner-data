'''
file: fetch_ensembl_id_mapping.py
author: Sheila Ramaswamy(@sramas15)

Connects to ENSEMBL server to fetch id mapping, using the biomart python library.

Dependencies:
biomart python library (https://pypi.python.org/pypi/biomart/0.9.0)

Usage:
python parse_obo_for_functions.py <output_file_path>

Positional Arguments:
output_file_path:        Path to the output file; Will be a tsv with the following schema:
               <gene_id>\\t<protein_id>


Example usage:

Input files: None

Output files: /path/to/output/gene-protein-mapping.tsv

Workflow:

python fetch_ensembl_id_mapping.py /path/to/output/gene-protein-mapping.tsv
'''
import argparse
from biomart import BiomartServer

parser = argparse.ArgumentParser(description='Get ensembl gene and peptide mapping from biomart')
parser.add_argument('output_file', help='output file name. Will be a tsv')
args = parser.parse_args()

def main(newfile):
  atts = ['ensembl_gene_id', 'ensembl_peptide_id']
  url = 'http://www.ensembl.org/biomart'
  server = BiomartServer(url)
  hge = server.datasets['hsapiens_gene_ensembl']
  with open(newfile, 'w') as outF:
    s = hge.search({'attributes': atts}, header=0)
    for l in s.iter_lines():
      (gene_id, peptide_id) = l.split('\t')
      if len(peptide_id) > 0:
        outF.write('%s\t%s\n' % (gene_id.strip(), peptide_id.strip()))

main(args.output_file)
