Current datasets containing gene information:
- GeneOntology (Uniprot ids *)
- HUGO (contains ENSEMBL gene ids and Uniprot ids *)

* Uniprot ids technically protein ids, but they seem to be used interchangeably in these datasets.

Note that all the relevant tables can be generated using scripts found in the Utils directory.

Workflow for creating mode tables for genes

Input files:
/path/to/input/hgnc_complete_set.txt  (from HUGO)
/path/to/input/gene_association.goa_human (from GO)

Output files:
/path/to/output/miner-gene-20160521.tsv
/path/to/output/miner-gene-0-GO-20160521.tsv
/path/to/output/miner-gene-1-HUGO_Uniprot-20160521.tsv
/path/to/output/miner-gene-2-HUGO_ENSEMBL-20160521.tsv


# Create mode files
python ../Utils/create_snap_mode_table.py /path/to/input/gene_association.goa_human gene GO 0 --output_dir /path/to/output/ --node_index 1
python ../Utils/create_snap_mode_table.py /path/to/input/hgnc_complete_set.txt gene HUGO_Uniprot 1 --output_dir /path/to/output/ --node_index 25
python ../Utils/create_snap_mode_table.py /path/to/input/hgnc_complete_set.txt gene HUGO_ENSEMBL 2 --output_dir /path/to/output/ --node_index 19

# Create mode equivalence table
python../Utils/create_snap_mode_equiv_table.py /path/to/output/miner-gene-0-GO-20160521.tsv /path/to/output/miner-gene-1-HUGO_Uniprot-20160521.tsv --output_dir /path/to/output/

python../Utils/create_snap_mode_equiv_table.py /path/to/output/miner-gene-2-HUGO_ENSEMBL-20160521.tsv /path/to/output/miner-gene-1-HUGO_Uniprot-20160521.tsv --output_dir /path/to/output/ --mapping_file_path /path/to/input/hgnc_complete_set.txt --ds1_node_index 19 --ds2_node_index 25