'''
file : parse_do_disease_disease.py
author: Viswajith Venugopal

Parses the disease ontology OBO to create the 
edge table using the is_a relationship.

Usage:
python parse_do_disease_disease.py <input_file> [--output_dir OUTPUT_DIR]

Positional Arguments:
input_file   : The doid.obo file which contains the disease ontology.

Optional Arugments: 
--output_dir : Directory to create output files. Defaults to the current working directory.

Example Usage:
Input File: doid.obo

Output directory : outputs/disease-disease/

Comamnd line:
python parse_do_disease_disease.py doid.obo --output_dir outputs/disease-disease/

Output: 
doid_disease_disease_parsed.tsv
'''

from collections import defaultdict
import os
import argparse
import pickle


# In[79]:

def parse_do_file_to_list(fname):
    """
    Reads the disease ontology in obo format from file
    given by fname, and returns the ontology as a list
    of dictionaries, one dictionary per entry.
    The dictionary for each entry is structured with
    the following fields
    {
        'id' (The disease ontology id)
        'name'
        'def'
        'synonym'
        'alt_id' (A list of alternate DOID ids)
        'xref' (A list of xrefs to MESH/OMIM ids)
        'is_a' (A DOID of what this disease is)
    
    }
    """
    f = open(fname, 'r')

    preamble = True # If we're in the top part of the file
    global_list = []
    curr_node_dict = {}
    for line in f:
        if preamble:
            if line.startswith('[Term]'):
                preamble = False
            continue
        spline = line.strip().split()
        if len(spline) == 0:
            global_list.append(curr_node_dict)
            curr_node_dict = {}
            continue
        if spline[0] == 'id:':
            if not spline[1].startswith('DOID'): # This means we've reached the bottom part of the file.
                break
            curr_node_dict['id'] = spline[1]
        elif spline[0] == 'name:':
            curr_node_dict['name'] = ' '.join(spline[1:])
        elif spline[0] == 'def:':
            curr_node_dict['def'] = ' '.join(spline[1:])
        elif spline[0] == 'synonym:':
            curr_node_dict['synonym'] = ' '.join(spline[1:])
        elif spline[0] == 'alt_id:':
            if 'alt_id' in curr_node_dict:
                curr_node_dict['alt_id'].append(spline[1])
            else:
                curr_node_dict['alt_id'] = [spline[1]]
        elif spline[0] == 'is_a:':
            curr_node_dict['is_a'] = spline[1]
        elif spline[0] == 'xref:':
            if 'xref' in curr_node_dict:
                curr_node_dict['xref'].append(spline[1])
            else:
                curr_node_dict['xref'] = [spline[1]]

                
    return global_list

doid_to_mesh_dict = defaultdict(list)
mesh_to_doid_dict = defaultdict(list)
omim_to_doid_dict = defaultdict(list)
doid_to_omim_dict = defaultdict(list)
doid_equiv_dict = defaultdict(list)


parser = argparse.ArgumentParser(description='Parse DOID to find disease-disease is-a edges.')
parser.add_argument('input_file', help='Input file path. File should be the doid.obo file.')
parser.add_argument('--output_dir', help='Directory to output files', default='.')
args = parser.parse_args()

output_fname = os.path.join(args.output_dir, "doid_disease_disease_parsed.tsv")

# Get the Disease Ontology as a list of one dictionary per entry.
do_list = parse_do_file_to_list(args.input_file)

with open(output_fname, 'w') as out_f:
    out_f.write('# Parsed DOID file.\n# Columns are source id, dest id.\n')
    for entry in do_list:
        if 'is_a' in entry:
            out_f.write('\t'.join([entry['id'], entry['is_a']]))
            out_f.write('\n')
