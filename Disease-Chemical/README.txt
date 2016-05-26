Current datasets containing disease-chemical information:
- CTD

Workflow for creating crossnet tables for disease-chemical relationships:

Pre-requisites:
Must have the disease modes table from CTD (MESH and OMIM), and the chemical
mode table from Drugbank.
/path/to/disease_mode/miner-disease-1-CTD_MESH-20160521.tsv
/path/to/disease_mode/miner-disease-2-CTD_OMIM-20160521.tsv
/path/to/chemical_mode/miner-chemical-0-drugbank-20160521.tsv

Input files/directories:
/path/to/input/CTD_dir  (from CTD)

Intermediate files:
/path/to/intermediate/ctd_disease_chem_parsed.tsv

Output files:
/path/to/output/miner-disease-chemical-20160521.tsv
/path/to/output/miner-disease-chemical-0-CTD_MESH-20160521.tsv
/path/to/output/miner-disease-chemical-1-CTD_OMIM-20160521.tsv

# Create intermediate files
python make_disease_chem_ctd.py /path/to/input/CTD_dir --output_dir /path/to/intermediate/

# Create cross net files
python ../Utils/create_snap_crossnet_table.py /path/to/intermediate/ctd_disease_chem_parsed.tsv /path/to/disease_mode/miner-disease-1-CTD_MESH-20160521.tsv /path/to/chemical_mode/miner-chemical-0-drugbank-20160521.tsv CTD_MESH 0 --output_dir /path/to/output/ --skip_missing_ids
python ../Utils/create_snap_crossnet_table.py /path/to/intermediate/ctd_disease_chem_parsed.tsv /path/to/disease_mode/miner-disease-2-CTD_OMIM-20160521.tsv /path/to/chemical_mode/miner-chemical-0-drugbank-20160521.tsv CTD_OMIM 1 --output_dir /path/to/output/ --skip_missing_ids
