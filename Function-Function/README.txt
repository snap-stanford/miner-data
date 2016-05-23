Current datasets containing function-function interaction information:
- GeneOntology (GO ids)

Note that all the relevant tables can be generated using scripts found in the Utils directory.

Workflow:

Input files:
/path/to/input/go.obo

Output files:
/path/to/output/miner-function-20160521.tsv
/path/to/output/miner-function-0-GO-20160521.tsv
/path/to/output/miner-function-function-20160521.tsv
/path/to/output/miner-function-function-0-GO-20160521.tsv

Intermediate files:
/path/to/intermediate/go_parsed.tsv
/path/to/intermediate/go_nodes.tsv

# Create all the function mode files
python ../Function-Function/parse_obo_for_functions.py /path/to/input/go.obo /path/to/intermediate/go_parsed.tsv

python ../Utils/extract_unique_node_ids.py /path/to/intermediate/go_parsed.tsv /path/to/intermediate/go_nodes.tsv GO 0 1

python ../Utils/create_snap_mode_table.py /path/to/intermediate/go_nodes.tsv function GO 0 --output_dir /path/to/output/


# Create crossnet files
python ../Utils/create_snap_crossnet_table.py /path/to/input/go_parsed.tsv /path/to/output/miner-function-0-GO-20160521.tsv /path/to/output/miner-function-0-GO-20160521.tsv GO 0 --output_dir /path/to/output/

Scripts included:

file: parse_obo_for_functions.py
author: Sheila Ramaswamy(@sramas15)

Script that parses the gene ontology obo file for the function-function edge list.

Usage:
python parse_obo_for_functions.py <input_file_path> <output_file_path>

Positional Arguments:
input_file_path:         Path to the input file; Input file should be the GO obo file.
output_file_path:        Path to the output file; Will be a tsv with the following schema:
					     <go_id1>\\t<go_id2>\\t<optional_edge_attr>



Example usage:
Creating files for function-function relationships using GeneOntology:

Input files: /path/to/input/go.obo

Output files: /path/to/output/functions.tsv

Workflow:

python parse_obo_for_functions.py /path/to/input/go.obo /path/to/output/functions.tsv


