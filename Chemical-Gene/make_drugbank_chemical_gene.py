'''
file : make_drugbank_chemical_gene.py
author: Agrim Gupta

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
'''
from collections import defaultdict
import os
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description='Output crossnet for chemical chemical interaction')
parser.add_argument('input_file', help='input file path. File should be parsed chemical-gene interaction')
parser.add_argument('chemical_mode', help='chemical mode file path. File should be the chemical mode file')
parser.add_argument('gene_mode', help='gene mode file path. File should be the gene mode file')
parser.add_argument('--output_dir', help='directory to output files', default='.')
args = parser.parse_args()
sep = "\t"
empty = "NULL"
format = '%Y%m%d'
dateStr = datetime.now().strftime(format)
snapIdPrefix = ""

edgeFile = args.input_file
nodeMap = args.chemical_mode
geneMap = args.gene_mode
masterTable = os.path.join(args.output_dir, "miner-chemical-gene-" + dateStr + ".tsv")
subTable = os.path.join(args.output_dir, "miner-chemical-gene-0-drugbank-" + dateStr + ".tsv")
idNum = 0
# Make a dict mapping from drugbankId to snapChemId
drugbankSnap = {}
with open(nodeMap, 'r') as f:
    for line in f:
        if line.startswith('#'):
            continue
        line = line.strip().split(sep)
        drugbankSnap[line[1]] = line[0]

# Make a dict mapping from UniProtKB to snapGeneId
geneSnap = {}
with open(geneMap, 'r') as f:
    for line in f:
        if line.startswith('#'):
            continue
        line = line.strip().split('\t')
        geneSnap[line[1]] = line[0]

with open(edgeFile, 'r') as f, open(masterTable, 'w') as master, open(subTable, 'w') as sub: 
    master.write('# snap_edge_id\tdataset_id\tsnap_source_id\tsnap_dst_id\n')
    sub.write('# snap_edge_id\tdataset_source_id\tdataset_dst_id\n')
    for line in f:
        if line.startswith('#'):
            continue
        line = line.strip().split(sep)
        if line[0] not in drugbankSnap:
            continue
        geneList = line[1].split(",")
        if geneList[0] == "NULL":
            continue
        for gene in geneList:
            snapId = snapIdPrefix + str(idNum)
            idNum += 1
            if gene not in geneSnap:
                print gene
                continue
            master.write(snapId + sep + "0" + sep + drugbankSnap[line[0]] + sep + geneSnap[gene] + '\n')
            sub.write(snapId + sep + line[0] + sep + gene + '\n')


