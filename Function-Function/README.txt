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