import argparse

parser = argparse.ArgumentParser(description='Create snap edge tables')
parser.add_argument('go_gene_node_file', help='db specific snap table file generated from GO annotations file; mapping of snap id to GO gene ids (in this case ensembl gene ids)')
parser.add_argument('input_file', help='input file name; should be HUGO file')
parser.add_argument('gene_node_file', help='output file name; outputs a list of snap ids and db ids; note that this file is appended to')
parser.add_argument('gene_equiv_file', help='output file name; equivalence table for snap node ids; note that this file is appended to')
parser.add_argument('db_uniprot_node_file', help='output file name; output contains mapping of snap ids to db ids for node ids')
parser.add_argument('db_ensembl_node_file', help='output file name; output contains mapping of snap ids to db ids for node ids')
parser.add_argument('db_uniprot_id', type=int, help='int id for this database')
parser.add_argument('db_ensembl_id', type=int, help='int id for this database')
parser.add_argument('snap_id_counter_start', type=int, help='where to start assigning snap ids')

args = parser.parse_args()



def load_mapping(inFile):
  mapping = {}
  with open(inFile, 'r') as inF:
    for line in inF:
      vals = line.strip().split('\t')
      mapping[vals[1]] = int(vals[0])
  return mapping


def clean_line(line):
	old_str = None
	curr_str = line.strip()
	while old_str!=curr_str:
		old_str = curr_str
		curr_str = curr_str.replace('\t\t', '\t-\t')
	return curr_str


go_mapping = load_mapping(args.go_gene_node_file)
fileOut1 = args.gene_node_file
fileOut2 = args.db_uniprot_node_file
fileOut3 = args.db_ensembl_node_file
fileOut4 = args.gene_equiv_file
fileIn = args.input_file
UNIPROT = 25
ENSEMBL = 19
values = {}
counter = args.snap_id_counter_start
with open(fileOut1, 'a') as geneMap: # snap_id db_id
  with open(fileOut2, 'w') as uniMap: # snap_id uniprot
    with open(fileOut3, 'w') as ensMap: # snap_id ensembl id
      with open(fileOut4, 'a') as equiv: # snap_id snap_id
        with open(fileIn, 'r') as inF:
          for line in inF:
            if line[0] == '#':
              continue
            line = clean_line(line)
            vals = line.strip().split('\t')
            uniprot = vals[UNIPROT]
            ensembl = vals[ENSEMBL]
            if uniprot != '-':
              if uniprot not in values:
                values[uniprot] = counter
                geneMap.write('%d\t%d\n' % (counter, args.db_uniprot_id))
                uniMap.write('%d\t%s\n' % (counter, uniprot))
                counter += 1
              uni_id = values[uniprot]
            if ensembl != '-':
              if ensembl not in values:
                values[ensembl] = counter
                geneMap.write('%d\t%d\n' % (counter, args.db_ensembl_id))
                ensMap.write('%d\t%s\n' % (counter, ensembl))
                counter += 1
              ens_id = values[ensembl]
            if uniprot != '-' and ensembl != '-':
              equiv.write('%d\t%d\n' % (uni_id, ens_id))
            if uniprot != '-' and uniprot in go_mapping:
              equiv.write('%d\t%d\n' % (uni_id, go_mapping[uniprot]))
