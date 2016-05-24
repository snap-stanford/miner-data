Current datasets containing chemical-gene information:
- drugbank

Workflow:

Input Files:
/path/to/input/drugbank.xml
/path/to/input/miner-chemical-0-drugbank-20160523.tsv
/path/to/input/miner-gene-0-20160523.tsv

Intermediate Files:
/path/to/intermediate/drugbank_parsed_chemical_gene.tsv

Output Files:
/path/to/output/miner-chemical-gene-20160423.tsv
/path/to/output/miner-chemical-gene-0-drugbank-20160423.tsv

# Parse data
python parse_drugbank_chemical_gene.py /path/to/input/drugbank.xml --output_dir /path/to/intermediate/

# Create crossnet tables
python make_drugbank_chemical_gene.py /path/to/intermediate/drugbank_parsed_chemical_gene.tsv ./../nodes/miner-chemical-0-drugbank-20160523.tsv miner-genes-0-go-20160523.tsv --output_dir /path/to/output/


Usage of the scripts used:

--------------------------------------
file : parse_drugbank_chemical_gene.py
--------------------------------------

XML parser to parse the drugbank database for chemical gene interactions. 
Outputs a tab separated .tsv file with the following coloumn headers:
DrugbankId Gene1 Gene2 ...
Currently UniportID is used for genes.

Usage:
python parse_drugbank_chemical_gene.py <input_file_path>

Positional Arguments:
input_file   : Path to the durgbank.xml file.

Optional Arugments: 
--output_dir : Directory to create output files. Defaults to the current working directory.

Example Usage:
Input File: drugbank.xml

Output directory : outputs/chemical/

Comamnd line:
python parse_drugbank_chemical_gene.py drugbank.xml --output_dir outputs/chemicals/

Output: 
drugbank_parsed_chemical_gene.tsv

-------------------------------------
file : make_drugbank_chemical_gene.py
-------------------------------------

Script to output chemical gene interactions.

Usage:
python make_drugbank_chemical_gene.py <input_file> <chemical_mode> <gene_mode>

Positional Arguments:
input_file       : Path to chemical chemical interaction file (drugbank_parsed_chemical_gene.tsv)
chemical_mode    : Path to chemical mode file (miner-chemical-0-drugbank-20160523.tsv)
gene_mode        : Path to gene mode file (miner-genes-0-go-20160523.tsv) 

Optional Arugments: 
--output_dir : Directory to create output files. Defaults to the current working directory.

Example Usage:
Input File: drugbank_parsed_chemical_gene.tsv, miner-chemical-0-drugbank-20160523.tsv

Output directory : outputs/chemical/

Comamnd line:
python make_drugbank_chemical_gene.py drugbank_parsed_chemical_gene.tsv ./../nodes/miner-chemical-0-drugbank-20160523.tsv miner-genes-0-go-20160523.tsv --output_dir outputs/chemicals/

Output: 
miner-chemical-gene-20160423.tsv, miner-chemical-gene-0-drugbank-20160423.tsv

