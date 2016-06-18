'''
file : make_snap_chemical_mode_table.py
author: Agrim Gupta

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
'''
import itertools
import os
from datetime import datetime
import argparse

sep = "\t"
empty = "NULL"
snapIdPrefix = ""
idNum = 0
format = '%Y%m%d'
dateStr = datetime.now().strftime(format)

parser = argparse.ArgumentParser(description='Make mode tables for chemical')
parser.add_argument('input_file', help='input file path. File should be the parsed drugbank.xml')
parser.add_argument('--output_dir', help='directory to output files', default='.')
args = parser.parse_args()

#output files
masterTable = os.path.join(args.output_dir,"miner-chemical-" + dateStr + ".tsv")
drugbankTable = os.path.join(args.output_dir, "miner-chemical-0-drugbank-" + dateStr + ".tsv")
pubCompundTable = os.path.join(args.output_dir, "miner-chemical-1-PubChemCompound-" + dateStr + ".tsv")
pubSubTable = os.path.join(args.output_dir, "miner-chemical-2-PubChemSubstance-" + dateStr + ".tsv")
eqTable = os.path.join(args.output_dir, "miner-chemical-equiv-" + dateStr + ".tsv")

subTable = [drugbankTable, pubCompundTable, pubSubTable]
databases = ["drugbank", "PubChemCompound" , "PubChemSubstance"]
subHandle = [open(subTable[i], 'w') for i in xrange(len(subTable))]
# Add Header
for i in xrange(len((subHandle))):
    subHandle[i].write('# snap_id\t%s specific id\n' % databases[i])

with open(args.input_file, 'r') as input, open(masterTable, 'w') as master,open(eqTable, 'w') as eqTable:
    master.write('# snap_id\tdataset_id\n')
    eqTable.write('# Equivalence table for mode chemical\n')
    eqTable.write('# snap_id_1\tsnap_id_2\n')
    for line in input:
        if line.startswith('#'):
            continue
        line = line.strip().split(sep)
        currId = []
        # Only first three fields are relavant
        for num,id in enumerate(line):
            if num > 2:
                break
            if id == "NULL":
                continue
            snapId = snapIdPrefix + str(idNum)
            idNum += 1
            master.write(snapId + sep + str(num) + '\n')
            subHandle[num].write(snapId + sep + id + '\n')
            currId.append(snapId)
        allPerms = list(itertools.permutations(currId,2))
        for perm in allPerms:
            toWrite = ' '.join(perm)
            eqTable.write(toWrite + '\n')

[handle.close() for handle in subHandle]
