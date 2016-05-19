import argparse

parser = argparse.ArgumentParser(description='Create snap node tables')
parser.add_argument('input_file', help='input file name. File should be of the format of extract_fields.py')
parser.add_argument('gene_node_file', help='output file name; outputs a list of snap ids and db ids; note that this file is appended to')
parser.add_argument('db_node_file', help='output file name; output contains mapping of snap ids to db gene ids')
parser.add_argument('snap_id_counter_start', type=int, help='where to start assigning snap ids')
parser.add_argument('db_id', type=int, help='int id for this database')
args = parser.parse_args()

fileIn = args.input_file
fileOut1 = args.gene_node_file
fileOut = args.db_node_file
values = set()
counter = args.snap_id_counter_start
db_id = args.db_id
with open(fileIn, 'r') as inF:
  with open(fileOut1, 'w') as snapMap: # snap id, db id
    with open(fileOut, 'w') as uniprotMap: # snap id, uniprot
      for line in inF:
        if line[0] == '#':
          continue
        vals = line.strip().split('\t')
        uniprot = vals[0]
        if uniprot in values:
          continue
        snapMap.write('%d\t%d\n' % (counter, db_id))
        uniprotMap.write('%d\t%s\n' % (counter, uniprot))
        values.add(uniprot)
        counter += 1