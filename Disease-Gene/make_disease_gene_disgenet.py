'''
Title : make_disease_gene_disgenet.py
Author: Farzaan Kaiyom

Parses data from DisGeNET to find disease-gene edges.

Usage:
python make_disease_gene_disgenet.py <input_file>

Positional Arguments:
input_dir   : The directory to the CTD folder.

Optional Arugments: 
--output_dir : Directory to create output files. Defaults to the current working directory.

Example Usage:
Input File: CTD/0819_CTD

Output directory : outputs/disease-gene/

Comamnd line:
python make_disease_gene_disgenet.py --output_dir outputs/disease-gene/

Output: 
ctd_disease_gene_parsed2.tsv
'''

from collections import defaultdict
import os
import argparse

def get_DGN_to_MESH(DGN_dir):
    map_fname = os.path.join(DGN_dir, 'mapping_files.tsv')
    mesh_dict = {}
    with open(map_fname, 'r') as dismap:
        for line in dismap:
            if line.startswith('#'):
                continue
            trgt = line.strip('\n').split('|')
            DGNid = trgt[0]
            vocab = trgt[2]
            if vocab=='MESH'
                code = trgt[3]
                mesh_dict[DGNid]=code
    return mesh_dict

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

def parse_ctd_gene_diseases(ctd_dir,DGN_dir):
    
    ncbi_to_uniprot_dict = get_ncbi_to_uniprot(ctd_dir)
    dgn_dict = get_DGN_to_MESH(DGN_dir)
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
            for uniprot_id in ncbi_to_uniprot_dict[ncbi_id]:
                yield (disease_id, uniprot_id)
     

parser = argparse.ArgumentParser(description='Parse CTD to find disease-gene links.')
parser.add_argument('input_dir1', help='Input files directory. This should be the directory with all the CTD TSVs.')
parser.add_argument('input_dir2', help='Input files directory. This should be the directory with the DGN-MESH mapping.')
parser.add_argument('--output_dir', help='Directory to output files', default='.')
args = parser.parse_args()

output_fname = os.path.join(args.output_dir, "ctd_disease_gene_parsed2.tsv")


with open(output_fname, 'w') as out_f:
    out_f.write('#Disease Gene links from CTD.\n')
    for (disease_id, uni_id) in parse_ctd_gene_diseases(args.input_dir1,args.input_dir2):
        out_f.write('\t'.join([disease_id, uni_id]))
        out_f.write('\n')
