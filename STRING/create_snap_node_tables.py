import argparse

parser = argparse.ArgumentParser(description='Create snap node tables')
parser.add_argument('input_file', help='input file name. File should contain a list of protein ids, as outputted by extract_protein_nodes.py')
parser.add_argument('protein_node_file', help='output file name; outputs a list of snap ids and db ids; note that this file is appended to')
parser.add_argument('db_node_file', help='output file name; output contains mapping of snap ids to db protein ids')
parser.add_argument('snap_id_counter_start', type=int, help='where to start assigning snap ids')
parser.add_argument('db_id', type=int, help='int id for this database')
args = parser.parse_args()

inFNm = args.input_file
outFNm = args.protein_node_file
outFNm2 = args.db_node_file
counter = args.snap_id_counter_start
db_id = args.db_id
seen = set()
with open(inFNm, 'r') as inF:
  with open(outFNm, 'a') as map:
    with open(outFNm2, 'w') as string:
      for line in inF:
        if line[0] == '#':
          continue
        string_id = line.strip()
        if string_id in seen:
          print 'duplicate...'
        map.write('%d\t%d\n' % (counter, db_id))
        string.write('%d\t%s\n' % (counter, string_id))
        seen.add(string_id)
        counter += 1
