import argparse

parser = argparse.ArgumentParser(description='Create snap node tables')
parser.add_argument('input_file', help='input file name. File should be of the format of extract_fields.py')
parser.add_argument('src_db_file', help='name of file that contains the db specific snap_id to uniprot id mapping')
parser.add_argument('dst_db_file', help='name of file that contains the db specific snap_id to GO id mapping')
parser.add_argument('edge_file', help='output file name; outputs a list of snap ids and db ids; note that this file is appended to')
parser.add_argument('db_edge_file', help='output file name; output contains mapping of snap ids to db ids for node ids')
parser.add_argument('snap_id_counter_start', type=int, help='where to start assigning snap ids')
parser.add_argument('db_id', type=int, help='int id for this database')
parser.add_argument('src_db_id', type=int, help='int id for uniprot id database')
parser.add_argument('dst_db_id', type=int, help='int id for go id database')
args = parser.parse_args()


src_mapping = {}
src_map_file = args.src_db_file
with open(src_map_file, 'r') as inF:
  for line in inF:
    (snap_id, uniprot_id) = line.strip().split('\t')
    src_mapping[uniprot_id] = int(snap_id)

dst_mapping = {}
dst_map_file = args.dst_db_file
with open(dst_map_file, 'r') as inF:
  for line in inF:
    (snap_id, go_id) = line.strip().split('\t')
    dst_mapping[go_id] = int(snap_id)



fileIn = args.input_file
fileOut1 = args.edge_file
fileOut = args.db_edge_file
counter = args.snap_id_counter_start
db_id = args.db_id
src_db_id = args.src_db_id
dst_db_id = args.dst_db_id
with open(fileIn, 'r') as inF:
  with open(fileOut1, 'w') as snapMap: # snap id, db id
    with open(fileOut, 'w') as uniprotMap: # snap id, uniprot
      for line in inF:
        if line[0] == '#':
          continue
        vals = line.strip().split('\t')
        uniprot = vals[0]
        go_id = vals[3]
        snapMap.write('%d\t%d\t%d\t%d\n' % (counter, db_id, src_mapping[uniprot], dst_mapping[go_id]))
        uniprotMap.write('%d\t%d\t%d\n' % (counter, src_db_id, dst_db_id))
        counter += 1