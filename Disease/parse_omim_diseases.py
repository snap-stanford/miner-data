'''
file : parse_ctd_diseases.py
author: Farzaan Kaiyom
based on scripts by Viswajith Venugopal

Parses the OMIM latest disease table found in genemap2.txt
^ *This is the latest formatting for OMIM data* ^

Usage:
python parse_ctd_diseases.py <input_file> [--output_dir OUTPUT_DIR]

Positional Arguments:
input_file   : The directory containing all the OMIM files.

Optional Arugments: 
--output_dir : Directory to create output files. Defaults to the current working directory.

Example Usage:
Input File: OMIM/08-2019/

Output directory : ../../output/diseases/

Comamnd line:
python parse_ctd_diseases.py OMIM/08-2019/ --output_dir output/diseases/

Output: 
omim_parsed.tsv
'''

import os
import argparse

def parse_omim_file_to_list(omim_dir):
    """
    Takes the OMIM directory as an argument, and
    returns a list of diseases from OMIM.
    First, it goes over the mim2gene file, and stores
    the OMIM numbers which correspond to diseases (phenotype).
    Then, it goes over the genemap and produces a list of entries
    which correspond to diseases, one dictionary per entry.
    Each dictionary has the following structure:
    {
        'id',
        'cyto_loc',
        'gene_symbols',
        'gene_name',
        'comments',
        'phenotypes',
        'mouse_symb'
    }
    """
    
    mim2gene_f = open(os.path.join(omim_dir, 'mim2gene.txt'), 'r')
    genemap_f = open(os.path.join(omim_dir, 'genemap2.txt'), 'r')
    
    # The set of mim numbers corresponding to diseases.
    disease_mims = set()
    for line in mim2gene_f:
        if line.startswith('#'):
            continue
        sp_line = line.split('\t')
        mim_number = sp_line[0]
        mim_type = sp_line[1]
        if mim_type == 'phenotype':
            disease_mims.add(mim_number)
    
    omim_list = []
    # Now, go over genemap and populate the list.
    for line in genemap_f:
        if line.startswith('#'):
            continue

        sp_line = line.strip('\n').split('\t')
        mim_number = sp_line[5]
        if mim_number not in disease_mims:
            continue
        cyto_loc = sp_line[3]
        gene_symbols = sp_line[6]
        gene_name = sp_line[7]
        
        ensembl_id = sp_line[10]

        comments = sp_line[11]
        phenotypes = sp_line[12]
        mouse_gene_symbol = sp_line[13]
        omim_list.append({
                'id' : 'OMIM:' + mim_number,
                'cyto_loc': cyto_loc,
                'gene_symbols': gene_symbols,
                'gene_name': gene_name,
                'comments': comments,
                'phenotypes': phenotypes,
                'mouse_symb': mouse_gene_symbol
            })
    return omim_list


parser = argparse.ArgumentParser(description='Parse OMIM to find diseases.')
parser.add_argument('input_dir', help='Input file dir. File should be the directory which contains all downloaded OMIM files.')
parser.add_argument('--output_dir', help='Directory to output files', default='.')
args = parser.parse_args()

# Get the OMIM node table as a list of one dictionary per entry.
omim_list = parse_omim_file_to_list(args.input_dir)
output_fname = os.path.join(args.output_dir, "omim_parsed.tsv")

with open(output_fname, 'w') as out_f:
    out_f.write('Parsed OMIM file.\n Columns: id, phenotypes, gene_name, gene_symbols, cyto_loc')
    for entry in omim_list:
        out_f.write('\t'.join([entry['id'], entry['phenotypes'],
                                    entry['gene_name'], entry['gene_symbols'], entry['cyto_loc'],
                                   entry['mouse_symb']]) + '\n')
