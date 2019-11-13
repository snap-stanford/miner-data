'''
file : make_disease_gene_ctd.py
author: Viswajith Venugopal

Parses CTD to find disease-gene edges.

Usage:
python make_disease_gene_ctd.py <input_file>

Positional Arguments:
input_dir   : The directory to the CTD folder.

Optional Arugments: 
--output_dir : Directory to create output files. Defaults to the current working directory.

Example Usage:
Input File: CTD/0416_CTD

Output directory : outputs/disease-gene/

Comamnd line:
python make_disease_gene_ctd.py --output_dir outputs/disease-gene/

Output: 
ctd_disease_gene_parsed.tsv
'''

from collections import defaultdict
import os
import argparse

def get_ncbi_to_uniprot(ctd_dir):
    ctd_gene_node_fname = os.path.join(ctd_dir, 'CTD_genes.tsv')
    ncbi_to_uniprot_dict = {}
    # First, we load uniprot ids.
    with open(ctd_gene_node_fname, 'r') as ctd_gene_node_f:
        for line in ctd_gene_node_f:
            if line.startswith('#'):
                continue
            sp_line = line.strip('\n').split('\t')
            ncbi_id = sp_line[2]
            uniprot_ids = sp_line[7]
            if len(uniprot_ids) > 0:
                uniprot_ids = uniprot_ids.split('|')
                ncbi_to_uniprot_dict[ncbi_id] = uniprot_ids

    return ncbi_to_uniprot_dict

def parse_ctd_gene_diseases(ctd_dir):
    
    ncbi_to_uniprot_dict = get_ncbi_to_uniprot(ctd_dir)
    disease_gene_list = []
    ctd_gene_dis_fname = os.path.join(ctd_dir, 'CTD_genes_diseases.tsv')
    with open(ctd_gene_dis_fname) as in_f:
        i = 0
        for line in in_f:
            i += 1
            if i % 100000 == 0:
                pass
                #print i
            if line.startswith('#'):
                continue
            sp_line = line.strip('\n').split('\t')
            ncbi_id = sp_line[1]
            if ncbi_id not in ncbi_to_uniprot_dict:
                continue
            disease_id = sp_line[3]
            iscore = sp_line[6]
            if iscore=="":
                iscore = 0
            for uniprot_id in ncbi_to_uniprot_dict[ncbi_id]:
                yield (disease_id, uniprot_id,iscore)
     

parser = argparse.ArgumentParser(description='Parse CTD to find disease-gene links.')
parser.add_argument('input_dir', help='Input files directory. This should be the directory with all the CTD TSVs.')
parser.add_argument('--output_dir', help='Directory to output files', default='.')
args = parser.parse_args()

output_fname = os.path.join(args.output_dir, "ctd_disease_gene_parsed.tsv")


with open(output_fname, 'w') as out_f:
    out_f.write('#Disease Gene links from CTD.\n')
    for (disease_id, uni_id,iscore) in parse_ctd_gene_diseases(args.input_dir):
        out_f.write('\t'.join([disease_id, uni_id,iscore]))
        out_f.write('\n')
