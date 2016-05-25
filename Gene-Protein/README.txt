Current datasets containing gene-protein interaction information:
- ENSEMBL/BioMart server (data NOT on ilfs2)

Workflow:

Input Files:
/path/to/input/hgnc_complete_set.txt
/path/to/input/protein.links.full.v10.txt

Output Files:
/path/to/output/miner-gene-20160521.tsv
/path/to/output/miner-gene-2-HUGO_ENSEMBL-20160521.tsv
/path/to/output/miner-protein-20160521.tsv
/path/to/output/miner-protein-0-STRING-20160521.tsv
/path/to/output/miner-gene-protein-20160521.tsv
/path/to/output/miner-gene-protein-0-ENSEMBL-20160521.tsv

Intermediate Files:
/path/to/intermediate/ensembl_mapping.tsv
/path/to/intermediate/protein-STRING-edgelist.tsv
/path/to/intermediate/protein-STRING-nodelist.tsv

# Get the mapping file from biomart
python fetch_ensembl_id_mapping /path/to/intermediate/ensembl_mapping.tsv

# Get the gene mode table
python ../Utils/create_snap_mode_table.py /path/to/input/hgnc_complete_set.txt gene HUGO_ENSEMBL 2 --output_dir /path/to/output/ --node_index 19

# Extract the edge list from the full protein interactions file; potentially may have to change
# the divider default value in the script (assume src and dst columns are 1 and 5)
python ../Utils/extract_edge_list.py /path/to/input/protein.links.full.v10.txt /path/to/intermediate/protein-STRING-edgelist.tsv STRING 1 5

# Extract the unique protein ids from the edge list (columns 0 and 1)
python ../Utils/extract_unique_node_ids.py /path/to/intermediate/protein-STRING-edgelist.tsv /path/to/intermediate/protein-STRING-nodelist.tsv STRING 0 1

# Create the protein mode files
python ../Utils/create_snap_mode_table.py /path/to/intermediate/protein-STRING-nodelist.tsv protein STRING 0 --output_dir /path/to/output/

# Create the CrossNet tables
python ../Utils/create_snap_crossnet_table.py /path/to/intermediate/ensembl_mapping.tsv /path/to/output/miner-gene-2-HUGO_ENSEMBL-20160521.tsv /path/to/output/miner-protein-0-STRING-20160521.tsv ENSEMBL 0 --output_dir /path/to/output/ --skip_missing_ids --dst_mode_filter add_species_id


Scripts Included:

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


