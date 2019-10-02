'''
file : make_drugbank_chemical_chemical.py
author: Agrim Gupta

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
'''
from collections import defaultdict
import os
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description='Output crossnet for chemical chemical interaction')
parser.add_argument('input_file', help='input file path. File should be parsed chemical-chemical interaction')
parser.add_argument('mode_file', help='mode file path. File should be the chemical mode file')
parser.add_argument('--output_dir', help='directory to output files', default='.')
args = parser.parse_args()
sep = "\t"
empty = "NULL"
format = '%Y%m%d'
dateStr = datetime.now().strftime(format)

snapIdPrefix = ""
edgeFile = args.input_file 
nodeMap = args.mode_file
masterTable = os.path.join(args.output_dir, "miner-chemical-chemical-" + dateStr + ".tsv")
subTable = os.path.join(args.output_dir, "miner-chemical-chemical-0-drugbank-" + dateStr + ".tsv")
idNum = 0
# Make a dict mapping from drugbankId to snapChemId
drugbankSnap = {}
with open(nodeMap, 'r') as f:
    for line in f:
        if line.startswith('#'):
            continue
        line = line.strip().split(sep)
        drugbankSnap[line[1]] = line[0]

drugsDone = defaultdict(list)
with open(edgeFile, 'r') as f, open(masterTable, 'w') as master, open(subTable, 'w') as sub:
    master.write('# snap_edge_id\tdataset_id\tsnap_source_id\tsnap_dst_id\n')
    sub.write('# snap_edge_id\tdataset_source_id\tdataset_dst_id\n')
    for line in f:
        if line.startswith('#'):
            continue
        line = line.strip().split(sep)
        if line[1] in drugsDone[line[0]]:
            continue
        if line[0] not in drugbankSnap or line[1] not in drugbankSnap:
            continue
        drugsDone[line[0]].append(line[1])
        snapId = snapIdPrefix + str(idNum)
        idNum += 1
        master.write(snapId + sep + "0" + sep + drugbankSnap[line[0]] + sep + drugbankSnap[line[1]] + sep + line[2] + '\n')
        sub.write(snapId + sep + line[0] + sep + line[1] + sep + line[2] + '\n')


