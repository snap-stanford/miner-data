'''
file : make_disease_func_ctd.py
author: Viswajith Venugopal

Goes over the disease function file in CTD and creates a table with the disease id
and GO id of the function.

Usage:
python make_disease_func_ctd <input_dir> [--output_dir OUTPUT_DIR]

Positional Arguments:
input_dir   : The directory with all the CTD TSVs

Optional Arugments: 
--output_dir : Directory to create output files. Defaults to the current working directory.

Example Usage:
Input Dir: CTD/0416_CTD

Output directory : outputs/disease_func/

Comamnd line:
python make_disease_func_ctd.py CTD/0416_CTD --output_dir outputs/disease_func/

Output: 
ctd_disease_func_parsed.tsv
'''

from collections import defaultdict
import os
import argparse

def load_disease_functions_ctd(ctd_dir):
    f1 = open(os.path.join(ctd_dir, 'CTD_Phenotype-Disease_biological_process_associations.tsv'), 'r')
    f2 = open(os.path.join(ctd_dir, 'CTD_Phenotype-Disease_cellular_component_associations.tsv'), 'r')
    f3 = open(os.path.join(ctd_dir, 'CTD_Phenotype-Disease_molecular_function_associations.tsv'), 'r')
    global_list = []
    linktype = ""
    for f in [f1, f2, f3]:
        if f==f1:
            linktype = "biological"
        elif f==f2:
            linktype = "cellular"
        else:
            linktype = "molecular"
        for line in f:
            if line.startswith('#'):
                continue
            sp_line = line.strip('\n').split('\t')
            disease_id = sp_line[3]
            go_id = sp_line[1]
            global_list.append((disease_id, go_id, linktype))
    return global_list

parser = argparse.ArgumentParser(description='Parse CTD to find disease-function links.')
parser.add_argument('input_dir', help='Input files directory. This should be the directory with all the CTD TSVs.')
parser.add_argument('--output_dir', help='Directory to output files', default='.')
args = parser.parse_args()

output_fname = os.path.join(args.output_dir, "ctd_disease_func_parsed.tsv")

disease_func_list = load_disease_functions_ctd(args.input_dir)

with open(output_fname, 'w') as out_f:
    out_f.write('#Disease Function links from CTD.\n')
    for (disease_id, go_id,linktype) in disease_func_list:
        out_f.write('\t'.join([disease_id, go_id,linktype]))
        out_f.write('\n')
