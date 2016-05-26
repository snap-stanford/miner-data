Current datasets containing disease-function information:
- CTD

Workflow for creating crossnet tables for disease-function relationships:

Pre-requisites:
Must have the disease modes table from CTD (MESH), and the function mode table from
GO.
/path/to/disease_mode/miner-disease-1-CTD_MESH-20160521.tsv
/path/to/function_mode/miner-function-0-GO-20160521.tsv

Input files/directories:
/path/to/input/CTD_dir  (from CTD)

Intermediate files:
/path/to/intermediate/ctd_disease_func_parsed.tsv

Output files:
/path/to/output/miner-disease-function-20160521.tsv
/path/to/output/miner-disease-function-0-CTD-20160521.tsv

# Create intermediate files
python make_disease_func_ctd.py /path/to/input/CTD_dir --output_dir /path/to/intermediate/

# Create cross net files
python ../Utils/create_snap_crossnet_table.py /path/to/intermediate/ctd_disease_func_parsed.tsv /path/to/disease_mode/miner-disease-1-CTD_MESH-20160521.tsv /path/to/function_mode/miner-function-0-GO-20160521.tsv CTD 0 --output_dir /path/to/output/ --skip_missing_ids
