Current datasets containing chemical information:
- Drugbank

Workflow for creating mode tables for chemicals:

Input files:
/path/to/input/drugbank.xml

Intermediate files:
/path/to/intermediate/drugbank_parsed.tsv
Output files:
/path/to/output/miner-chemical-20160523.tsv
/path/to/output/miner-chemical-0-drugbank-20160523.tsv
/path/to/output/miner-chemical-1-PubChemCompound-20160523.tsv 
/path/to/output/miner-chemical-2-PubChemSubstance-20160523.tsv
/path/to/output/miner-chemical-equiv-20160523.tsv

# Parse Data
# Beautiful Soup is required for this, use pipenv to install if you lack permissions
python parse_drugbank_chemicals.py /path/to/input/drugbank.xml --output-dir /path/to/intermediate/

# Create Mode tables
python make_snap_chemical_mode.py /path/to/intermediate/drugbank_parsed.tsv --output_dir /path/to/intermediate

Usage of the scripts used:

----------------------------------
file : parse_drugbank_chemicals.py
----------------------------------

XML parser to parse the drugbank database and output a tsv file 
containting the following coloumn headers:
DrugbankID PubChem_Compound PubChem_Substance

Usage:
python parse_drugbank_chemicals.py <input_file_path>

Positional Arguments:
input_file   : Path to the durgbank.xml file.

Optional Arugments: 
--output_dir : Directory to create output files. Defaults to the current working directory.

Example Usage:
Input File: drugbank.xml

Output directory : outputs/chemical/

Comamnd line:
python parse_drugbank_chemicals.py drugbank.xml --output_dir outputs/chemicals/

Output: 
drugbank_parsed.tsv

---------------------------------------
file : make_snap_chemical_mode_table.py
---------------------------------------

Takes input parsed durgbank.xml with the following coloumn headers:
DrugbankID PubChem_Compound PubChem_Substance. Outputs snap tables for 
chemical mode.

Usage:
python make_snap_chemical_mode.py <input_file_path>

Positional Arguments:
input_file   : Path to parsed drugbank.xml.

Optional Arugments: 
--output_dir : Directory to create output files. Defaults to the current working directory.

Example Usage:
Input File: drugbank_parsed.tsv 

Output directory : outputs/chemical/

Comamnd line:
python make_snap_chemical_mode.py drugbank_parsed.tsv --output_dir outputs/chemicals/

Output:
miner-chemical-20160523.tsv, miner-chemical-0-drugbank-20160523.tsv,
miner-chemical-1-PubChemCompound-20160523.tsv, miner-chemical-2-PubChemSubstance-20160523.tsv,
miner-chemical-equiv-20160523.tsv


