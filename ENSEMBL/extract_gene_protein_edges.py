import argparse

parser = argparse.ArgumentParser(description='Create snap node tables')
parser.add_argument('input_file', help='input file name. File should be of the format of fetch_gene_protein_mapping.py')
parser.add_argument('src_db_file', help='name of file that contains the db specific snap_id to ensembl protein id mapping (as in STRING, with species id)')
parser.add_argument('dst_db_file', help='name of file that contains the db specific snap_id to ensembl gene id mapping')
parser.add_argument('edge_file', help='output file name; outputs a list of snap ids and db ids; note that this file is appended to')
parser.add_argument('db_edge_file', help='output file name; output contains mapping of snap ids to db ids for node ids')
parser.add_argument('snap_id_counter_start', type=int, help='where to start assigning snap ids')
parser.add_argument('db_id', type=int, help='int id for this database')
parser.add_argument('src_db_id', type=int, help='int id for ensembl protein id database')
parser.add_argument('dst_db_id', type=int, help='int id for ensembl id database')
args = parser.parse_args()


src_mapping = {}
src_map_file = args.src_db_file
with open(src_map_file, 'r') as inF:
  for line in inF:
    (snap_id, protein_id) = line.strip().split('\t')
    src_mapping[protein_id] = int(snap_id)

dst_mapping = {}
dst_map_file = args.dst_db_file
with open(dst_map_file, 'r') as inF:
  for line in inF:
    (snap_id, gene_id) = line.strip().split('\t')
    dst_mapping[gene_id] = int(snap_id)


fileIn = args.input_file
fileOut1 = args.edge_file
fileOut = args.db_edge_file
counter = args.snap_id_counter_start
db_id = args.db_id
src_db_id = args.src_db_id
dst_db_id = args.dst_db_id
with open(fileIn, 'r') as inF:
  with open(fileOut1, 'w') as snapMap: # snap id, db id
    with open(fileOut, 'w') as geneprotMap: # snap id, uniprot
      for line in inF:
        if line[0] == '#':
          continue
        vals = line.strip().split('\t')
        if len(vals) < 5:
          continue
        prot = '9606.%s' % vals[4]
        gene = vals[2]
        if prot not in src_mapping or gene not in dst_mapping:
          continue
        snapMap.write('%d\t%d\t%d\t%d\n' % (counter, db_id, src_mapping[prot], dst_mapping[gene]))
        geneprotMap.write('%d\t%d\t%d\n' % (counter, src_db_id, dst_db_id))
        counter += 1