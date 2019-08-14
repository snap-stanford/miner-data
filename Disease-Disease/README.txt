Current datasets containing disease-disease information:
- DiseaseOntology (has edges for the 'is_a' relationship)

Workflow for creating crossnet tables for disease-disease relationships:

Pre-requisites:
Must have the disease mode table from DOID
/path/to/mode/miner-disease-0-DOID-20160521.tsv

Input files/directories:
/path/to/input/doid.obo  (from DOID)

Intermediate files:
/path/to/intermediate/doid_disease_disease_parsed.tsv

Output files:
/path/to/output/miner-disease-disease-20160521.tsv
/path/to/output/miner-disease-disease-0-DOID-20160521.tsv

# Create intermediate files
python parse_do_disease_disease.py /path/to/input/doid.obo --output_dir /path/to/intermediate/

# Create cross net files
python ../Utils/create_snap_crossnet_table.py /path/to/intermediate/doid_disease_disease_parsed.tsv /path/to/mode/miner-disease-0-DOID-20160521.tsv /path/to/mode/miner-disease-0-DOID-20160521.tsv DOID 0 --output_dir /path/to/output/
