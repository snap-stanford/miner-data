'''
file : make_disease_chem_ctd.py
author: Viswajith Venugopal

Parses CTD to find disease chemical links.

Usage:
python make_disease_chem_ctd <input_dir> [--output_dir OUTPUT_DIR]

Positional Arguments:
input_dir  : The directory of the CTD files.

Optional Arugments: 
--output_dir : Directory to create output files. Defaults to the current working directory.

Example Usage:
Input File: CTD/0416_CTD

Output directory : outputs/disease-chemical/

Comamnd line:
python parse_do_diseases.py CTD/0416_CTD --output_dir outputs/disease-chemical/

Output: 
ctd_disease_chemical_parsed.tsv
'''

from collections import defaultdict
import os
import argparse

def get_chem_to_db(ctd_dir):
    ctd_chem_node_fname = os.path.join(ctd_dir, 'CTD_chemicals.tsv')
    chem_to_db_dict = {}
    # First, we load uniprot ids.
    with open(ctd_chem_node_fname, 'r') as ctd_gene_node_f:
        for line in ctd_gene_node_f:
            if line.startswith('#'):
                continue
            sp_line = line.strip('\n').split('\t')
            chem_id = sp_line[1]
            db_ids = sp_line[8]
            if len(db_ids) > 0:
                db_ids = db_ids.split('|')
                chem_to_db_dict[chem_id] = db_ids

    return chem_to_db_dict

def parse_ctd_chem_diseases(ctd_dir):
    
    chem_to_db_dict = get_chem_to_db(ctd_dir)
    disease_chem_list = []
    ctd_chem_dis_fname = os.path.join(ctd_dir, 'CTD_chemicals_diseases.tsv')
    with open(ctd_chem_dis_fname) as in_f:
        for line in in_f:
            if line.startswith('#'):
                continue
            sp_line = line.strip('\n').split('\t')
            chem_id = 'MESH:' + sp_line[1]
            if chem_id not in chem_to_db_dict:
                continue
            db_id = chem_to_db_dict[chem_id][0]
            disease_id = sp_line[4]
            inference_score = sp_line[7]
            if inference_score == "":
                inference_score = "0"
            disease_chem_list.append((disease_id, db_id,inference_score))

    return disease_chem_list
     

parser = argparse.ArgumentParser(description='Parse CTD to find disease-chemical links.')
parser.add_argument('input_dir', help='Input files directory. This should be the directory with all the CTD TSVs.')
parser.add_argument('--output_dir', help='Directory to output files', default='.')
args = parser.parse_args()

output_fname = os.path.join(args.output_dir, "ctd_disease_chem_parsed.tsv")

disease_chem_list = parse_ctd_chem_diseases(args.input_dir)

with open(output_fname, 'w') as out_f:
    out_f.write('#Disease Chemical links from CTD.\n')
    for (disease_id, db_id, iscore) in disease_chem_list:
        out_f.write('\t'.join([disease_id, db_id,iscore]))
        out_f.write('\n')
