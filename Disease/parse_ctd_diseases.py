'''
file : parse_ctd_diseases.py
author: Viswajith Venugopal

Parses the CTD disease node table into a TSV we can use to build our SNAP mode table
Creates two separate files, one for CTD diseases with a MESH id, and another for 
CTD diseases with an OMIM id.

Usage:
python parse_ctd_diseases.py <input_file> [--output_dir OUTPUT_DIR]

Positional Arguments:
input_file   : The CTD_diseases.tsv file which ships with CTD.

Optional Arugments: 
--output_dir : Directory to create output files. Defaults to the current working directory.

Example Usage:
Input File: CTD_diseases.tsv

Output directory : outputs/diseases/

Comamnd line:
python parse_ctd_diseases.py CTD_diseases.tsv --output_dir outputs/diseases/

Output: 
ctd_mesh_parsed.tsv
ctd_omim_parsed.tsv
'''

import os
import argparse

def parse_ctd_file_to_list(fname):
   """
   Parses the ctd_diseases.tsv file, and returns it as a list
   of entries, each entry represented as a dictionary with structure:
   {
       'name'
       'id'
       'alt_ids' (list of alternate disease ids)
       'defs'
       'parents' (list of parent ids)
       'syns'
   }
   """
   f = open(fname,'r')
   ctd_list = []
   for line in f:
       if line.startswith('#'):
           continue
       spline = line.strip('\n').split('\t')
       name = spline[0]
       disease_id = spline[1]
       alt_ids = spline[2]
       defs = spline[3]
       parents = spline[4]
       syns = spline[7]
       if len(alt_ids) > 0:
           alt_ids = alt_ids.split('|')
       else:
           alt_ids = []
       if len(parents) > 0:
           parents = parents.split('|')
       else:
           parents = []
       ctd_list.append({
               'name': name,
               'id': disease_id,
               'alt_ids': alt_ids,
               'defs': defs,
               'parents': parents,
               'syns': syns
           })
               
   return ctd_list

parser = argparse.ArgumentParser(description='Parse CTD to find diseases.')
parser.add_argument('input_file', help='Input file path. File should be the CTD_diseases.tsv file.')
parser.add_argument('--output_dir', help='Directory to output files', default='.')
args = parser.parse_args()

ctd_list = parse_ctd_file_to_list(args.input_file)
mesh_output_fname = os.path.join(args.output_dir, "ctd_mesh_parsed.tsv")
omim_output_fname = os.path.join(args.output_dir, "ctd_omim_parsed.tsv")


with open(mesh_output_fname, 'w') as mesh_out_f:
    with open(omim_output_fname, 'w') as omim_out_f:
        mesh_out_f.write('# Parsed CTD diseases file with MESH ids.\n# Columns: id, name, definitions, synonyms.\n')
        omim_out_f.write('# Parsed CTD diseases file with OMIM ids.\n# Columns: id, name, definitions, synonyms.\n')

        for entry in ctd_list:
            
            # The string to write into the output file.
            str_to_write = '\t'.join([entry['id'], entry['name'], 
                                      entry['defs'], entry['syns']])
            
            # Find the id; in CTD, it can be either an OMIM or a MESH id.
            if entry['id'].startswith('MESH'):
                mesh_out_f.write(str_to_write + '\n')
            elif entry['id'].startswith('OMIM'):
                omim_out_f.write(str_to_write + '\n')
