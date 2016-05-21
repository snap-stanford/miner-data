Current datasets relevant for getting protein-protein interactions:

- STRING v10; uses ENSEMBL peptide ids

Note that all the relevant tables can be generated using scripts found in the Utils directory.

***** IMPORTANT: STRING v10 contains 1,847,117,370 edges and therefore takes a long time to process.
      when adding interactions from another dataset (to the same miner-protein-protein-20160521.tsv 
      file), please use the snap_id_counter_start argument to set the starting snap id to 
      1,847,117,370; otherwise, we must read through the entire file to get a starting id 
      (based on number of lines).

How to create crossnet tables from the STRING database (assumes mode tables not already created):

Input Files (from STRING):
/path/to/input/protein.links.full.v10.txt

Output Files:
/path/to/output/miner-protein-20160521.tsv
/path/to/output/miner-protein-0-STRING-20160521.tsv
/path/to/output/miner-protein-protein-20160521.tsv
/path/to/output/miner-protein-protein-0-STRING-20160521.tsv

Intermediate Files:
/path/to/intermediate/protein-STRING-edgelist.tsv
/path/to/intermediate/protein-STRING-nodelist.tsv

# Extract the edge list from the full protein interactions file; potentially may have to change
# the divider default value in the script (assume src and dst columns are 1 and 5)
python ../Utils/extract_edge_list.py /path/to/input/protein.links.full.v10.txt /path/to/intermediate/protein-STRING-edgelist.tsv STRING 1 5

# Extract the unique protein ids from the edge list (columns 0 and 1)
python ../Utils/extract_unique_node_ids.py /path/to/intermediate/protein-STRING-edgelist.tsv /path/to/intermediate/protein-STRING-nodelist.tsv STRING 0 1

# Create the mode files
python ../Utils/create_snap_mode_table.py /path/to/intermediate/protein-STRING-nodelist.tsv protein STRING 0 --output_dir /path/to/output/

# Create the crossnet files
python ../Utils/create_snap_crossnet_table.py /path/to/intermediate/protein-STRING-edgelist.tsv /path/to/output/miner-protein-0-STRING-20160521.tsv /path/to/output/miner-protein-0-STRING-20160521.tsv STRING 0 --output_dir /path/to/output/

