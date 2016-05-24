Current datasets containing chemical-chemical information:
- drugbank

Workflow:

Input Files:
/path/to/input/drugbank.xml
/path/to/input/miner-chemical-0-drugbank-20160523.tsv

Intermediate Files:
/path/to/intermediate/drugbank_parsed_chemical_chemical.tsv

Output Files:
/path/to/output/miner-chemical-chemical-20160423.tsv
/path/to/output/miner-chemical-chemical-0-drugbank-20160423.tsv

# Parse data
python parse_drugbank_chemical_chemical.py /path/to/input/drugbank.xml --output_dir /path/to/intermediate/

# Create crossnet tables
python make_drugbank_chemical_chemical.py /path/to/intermediate/drugbank_parsed_chemical_chemical.tsv ./../Chemical/miner-chemical-0-drugbank-20160523.tsv --output_dir /path/to/output/

Usage of the scripts used:

------------------------------------------
file : parse_drugbank_chemical_chemical.py
------------------------------------------

XML parser to parse the drugbank database for chemical chemical interactions. 
Outputs a tab separated .tsv file with the following coloumn headers:
DrugbankId DrugbankId

Usage:
python parse_drugbank_chemical_chemical.py <input_file_path>

Positional Arguments:
input_file   : Path to the durgbank.xml file.

Optional Arugments: 
--output_dir : Directory to create output files. Defaults to the current working directory.

Example Usage:
Input File: drugbank.xml

Output directory : outputs/chemical/

Comamnd line:
python parse_drugbank_chemical_chemical.py drugbank.xml --output_dir outputs/chemicals/

Output: 
drugbank_parsed_chemical_chemical.tsv

------------------------------------------
file : make_drugbank_chemical_chemical.py
------------------------------------------

Script to output chemical chemical interactions.

Usage:
python make_drugbank_chemical_chemical.py <input_file> <mode_file>

Positional Arguments:
input_file   : Path to chemical chemical interaction file (drugbank_parsed_chemical_chemical.tsv)
mode_file    : Path to chemical mode file (miner-chemical-0-drugbank-20160523.tsv)

Optional Arugments: 
--output_dir : Directory to create output files. Defaults to the current working directory.

Example Usage:
Input File: drugbank_parsed_chemical_chemical.tsv, miner-chemical-0-drugbank-20160523.tsv

Output directory : outputs/chemical/

Comamnd line:
python make_drugbank_chemical_chemical.py drugbank_parsed_chemical_chemical.tsv ./../nodes/miner-chemical-0-drugbank-20160523.tsv --output_dir outputs/chemicals/

Output: 
miner-chemical-chemical-20160423.tsv, miner-chemical-chemical-0-drugbank-20160423.tsv


