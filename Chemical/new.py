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

masterTable = os.path.join(args.output_dir,"miner-chemical-" + dateStr + ".tsv")
drugbankTable = os.path.join(args.output_dir, "miner-chemical-0-drugbank-" + dateStr + ".tsv")
with open(args.input_file, 'r') as input, open(masterTable, 'w') as master, open(drugbankTable,'w') as drugTable:
    master.write('# snap_id\tdataset_id\n')
    drugTable.write('# snap_id\tdataset_id\tname\n')
    #eqTable.write('# Equivalence table for mode chemical\n')
    #eqTable.write('# snap_id_1\tsnap_id_2\n')
    for line in input:
        if line.startswith('#'):
            continue
	spline =line.strip().split(sep)
        if line.startswith('DB') and len(spline)>1:
            line = spline
            id = line[0]
            name = line[1]
            if name == "":
                name = "NULL"
            snapId = snapIdPrefix + str(idNum)
            idNum += 1
            master.write(snapId + sep + id + '\n')
            drugTable.write(snapId + sep + id + sep + name + '\n')
