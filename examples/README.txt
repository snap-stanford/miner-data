------------------------------
Example : Load Miner Dataset
------------------------------

This folder contains two simple scripts to 
1. Load the miner data set into a multi-modal network which is then saved to disk. 
2. Read the saved graph from disk and print basic statistics about the miner dataset. 

Sample workflow:
1. Generate the network and save to disk
python miner_load_tables.py config.txt --loglevel info

2. Read the saved network and print statistics
python miner_get_stats.py ./miner.graph

Usage of the scripts used:

----------------------------
file : miner_load_tables.py
----------------------------

Example to illustrate how to load the miner dataset into a multi-modal network. 

Usage: miner_load_tables.py <config_file>

Config File : 
The config files contains the path to all tsv to load modes and cross-nets. 

Positional Arguments:
config_file  : Path to the config file. The config file contatins the path to all the modes and cross-net tsv files.

Optional Arguments: 
--output_dir : Directory to create output files. Defaults to the current working directory.
--loglevel   : Enable logging. Defaults to warning level. 

Example Usage: 
Input File   : Config.txt

Command Line : 
python miner_load_tables.py config.txt --loglevel info 

Output: 
miner.graph

Note:
Due to 32 bit limitation we can't fully load the Protein-Protein edges.
Only edges with confidence level greater than 200 are used. When SNAP supports
64 bit make the following change in config file:
Protein-Protein = /dfs/ilfs2/0/MINER-BIO/types/Protein-Protein/20160418/snap-tables/miner-protein-protein-20160607.tsv

---------------------------
file   : miner_get_stats.py
---------------------------

Script to print basic statistics of the miner dataset.

Usage: 
python miner_get_stats.py <input_file>

Positional Arguments:
input_file : Path to the multi-modal network

Example Usage: 
Input file : miner.graph

Command line: 
python miner_get_stats.py ./miner.graph

