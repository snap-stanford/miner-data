Current datasets containing disease information:
- DiseaseOntology (has DOID ids, as well as cross-references to the MESH and
  OMIM ids)
- CTD (uses MESH ids for some diseases, and OMIM ids for others)
- OMIM

Workflow for creating mode tables for diseases:

Input files/directories:
/path/to/input/doid.obo  (from DOID)
/path/to/input/CTD_diseases.tsv (from CTD)
/path/to/input/OMIM/ (from OMIM. Note that this is the entire directory, since
multiple files are required to identify diseases)

Intermediate files:
/path/to/intermediate/doid_parsed.tsv
/path/to/intermediate/ctd_mesh_parsed.tsv
/path/to/intermediate/ctd_omim_parsed.tsv
/path/to/intermediate/omim_parsed.tsv
/path/to/intermediate/doid_mesh_equiv.tsv
/path/to/intermediate/doid_omim_equiv.tsv

Output files:
/path/to/output/miner-disease-20160521.tsv
/path/to/output/miner-disease-0-DOID-20160521.tsv
/path/to/output/miner-disease-1-CTD_MESH-20160521.tsv
/path/to/output/miner-disease-3-OMIM-20160525.tsv
/path/to/output/miner-disease-equiv-20160525.tsv

# Create intermediate files
python parse_do_diseases.tsv /path/to/input/doid.obo --output_dir /path/to/intermediate/
python parse_ctd_diseases.tsv /path/to/input/CTD_diseases.tsv --output_dir /path/to/intermediate/
python parse_omim_diseases.tsv /path/to/input/OMIM/ --output_dir /path/to/intermediate/


# Create mode files
python ../Utils/create_snap_mode_table.py /path/to/intermediate/doid_parsed.tsv disease DOID 0 --output_dir /path/to/output/
python ../Utils/create_snap_mode_table.py /path/to/intermediate/ctd_mesh_parsed.tsv disease CTD_MESH 1 --output_dir /path/to/output/
python ../Utils/create_snap_mode_table.py /path/to/intermediate/ctd_omim_parsed.tsv disease CTD_OMIM 2 --output_dir /path/to/output/
python ../Utils/create_snap_mode_table.py /path/to/intermediate/omim_parsed.tsv disease OMIM 3 --output_dir /path/to/output/

# Create mode equivalence table
python ../Utils/create_snap_mode_equiv_table.py /path/to/output/miner-disease-0-DOID-20160521.tsv /path/to/output/miner-disease-1-CTD_MESH-20160521.tsv --output_dir /path/to/output/ --mapping_file /path/to/intermediate/doid_mesh_equiv.tsv --skip_missing_ids
python ../Utils/create_snap_mode_equiv_table.py /path/to/output/miner-disease-0-DOID-20160521.tsv /path/to/output/miner-disease-2-CTD_OMIM-20160521.tsv --output_dir /path/to/output/ --mapping_file /path/to/intermediate/doid_omim_equiv.tsv --skip_missing_ids
python ../Utils/create_snap_mode_equiv_table.py /path/to/output/miner-disease-0-DOID-20160521.tsv /path/to/output/miner-disease-3-OMIM-20160521.tsv --output_dir /path/to/output/ --mapping_file /path/to/intermediate/doid_omim_equiv.tsv --skip_missing_ids
