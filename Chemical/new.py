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
with open(args.input_file, 'r') as input, open(masterTable, 'w') as master,open(eqTable, 'w') as eqTable:
    master.write('# snap_id\tdataset_id\n')
    drugbankTable.write('# snap_id\tdataset_id\tname\n')
    eqTable.write('# Equivalence table for mode chemical\n')
    eqTable.write('# snap_id_1\tsnap_id_2\n')
    for line in input:
        if line.startswith('#'):
            continue
        if line.startswith('D'):
            line = line.strip().split(sep)
            id = line[0]
            name = line[1]
            snapId = snapIdPrefix + str(idNum)
            idNum += 1
            master.write(snapId + sep + id + '\n')
            drugbankTable.write(snapId + sep + id + name + '\n')
