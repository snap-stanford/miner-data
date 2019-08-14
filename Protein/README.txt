Current datasets relevant for getting protein ids:

- STRING v10; uses ENSEMBL peptide ids

Note that all the relevant tables can be generated using scripts found in the Utils directory.

How to create mode tables from the STRING database:

Input Files (from STRING):
/path/to/input/protein.links.full.v10.txt

Output Files:
/path/to/output/miner-protein-20160521.tsv
/path/to/output/miner-protein-0-STRING-20160521.tsv

Intermediate Files:
/path/to/intermediate/protein-STRING-edgelist.tsv
/path/to/intermediate/protein-STRING-nodelist.tsv

# Extract the edge list from the full protein interactions file; potentially may have to change
# the divider default value in the script (assume src and dst columns are 0 and 1)
python ../Utils/extract_edge_list.py /path/to/input/protein.links.full.v10.txt /path/to/intermediate/protein-STRING-edgelist.tsv STRING 0 1 --divider " "

# Extract the unique protein ids from the edge list (columns 0 and 1)
python ../Utils/extract_unique_node_ids.py /path/to/intermediate/protein-STRING-edgelist.tsv /path/to/intermediate/protein-STRING-nodelist.tsv STRING 0 1

# Create the mode files
python ../Utils/create_snap_mode_table.py /path/to/intermediate/protein-STRING-nodelist.tsv protein STRING 0 --output_dir /path/to/output/

# If multiple datasets used, and there is a mapping between the ids, please use the
# create_snap_mode_equiv_table.py script.

