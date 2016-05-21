Current datasets containing gene-function information:
- GeneOntology (Uniprot ids to GO ids)

Note that all the relevant tables can be generated using scripts found in the Utils directory.

Workflow:

Input files:
/path/to/input/gene_association.goa_human (from GO)
/path/to/input/go.obo

Output files:
/path/to/output/miner-gene-20160521.tsv
/path/to/output/miner-gene-0-GO-20160521.tsv
/path/to/output/miner-function-20160521.tsv
/path/to/output/miner-function-0-GO-20160521.tsv
/path/to/output/miner-gene-function-20160521.tsv
/path/to/output/miner-gene-function-0-GO-20160521.tsv

Intermediate files:
/path/to/intermediate/go_parsed.tsv
/path/to/intermediate/go_nodes.tsv

# First create all the gene mode files

python ../Utils/create_snap_mode_table.py /path/to/input/gene_association.goa_human gene GO 0 --output_dir /path/to/output/ --node_index 1


# Second create all the function mode files
python ../Function-Function/parse_obo_for_functions.py /path/to/input/go.obo /path/to/intermediate/go_parsed.tsv

python ../Utils/extract_unique_node_ids.py /path/to/intermediate/go_parsed.tsv /path/to/intermediate/go_nodes.tsv GO 0 1

python ../Utils/create_snap_mode_table.py /path/to/intermediate/go_nodes.tsv function GO 0 --output_dir /path/to/output/

# Create crossnet files
python ../Utils/create_snap_crossnet_table.py /path/to/input/gene_association.goa_human /path/to/output/miner-gene-0-GO-20160521.tsv /path/to/output/miner-function-0-GO-20160521.tsv GO 0 --output_dir /path/to/output/ --src_node_index 1 --dst_node_index 4

