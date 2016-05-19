import argparse

parser = argparse.ArgumentParser(description='Create snap edge tables')
parser.add_argument('input_file', help='input file name. File should contain a list of protein interactions, as outputted by extract_protein_edges.py')
parser.add_argument('db_file', help='name of file that contains the db specific snap_id to db protein id mapping')
parser.add_argument('protein_edge_file', help='output file name; outputs a list of snap ids and db ids; note that this file is appended to')
parser.add_argument('db_edge_file', help='output file name; output contains mapping of snap ids to db ids for node ids')
parser.add_argument('snap_id_counter_start', type=int, help='where to start assigning snap ids')
parser.add_argument('db_id', type=int, help='int id for this database')
parser.add_argument('src_db_id', type=int, help='int id for the source node database')
parser.add_argument('dst_db_id', type=int, help='int id for the dest node database')
args = parser.parse_args()


inFNm = args.input_file

mapping = {}
map_file = args.db_file
with open(map_file, 'r') as inF:
  for line in inF:
    (snap_id, string_id) = line.strip().split('\t')
    mapping[string_id] = int(snap_id)

outFNm = args.protein_edge_file
outFNm2 = args.db_edge_file
counter = args.snap_id_counter_start
with open(inFNm, 'r') as inF:
  with open(outFNm, 'w') as map:
    with open(outFNm2, 'w') as string:
      for line in inF:
        if line[0] == '#':
          continue
        (id1, id2) = line.strip().split('\t')
        map.write('%d\t%d\t%d\t%d\n' % (counter, args.db_id, mapping[id1], mapping[id2]))
        string.write('%d\t%d\t%d\n' % (counter, args.src_db_id, args.dst_db_id))
        counter += 1
