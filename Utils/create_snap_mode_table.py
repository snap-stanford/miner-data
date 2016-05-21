import argparse
import utils
import os

parser = argparse.ArgumentParser(description='Create snap node tables')
parser.add_argument('input_file', help='input file name. File should be a tsv, with one mode-specific id per line (unless --node_index specified)')
parser.add_argument('mode_name', type=str, help='mode name')
parser.add_argument('dataset_name', type=str, help='name of dataset')
parser.add_argument('db_id', type=int, help='int id for this dataset')
parser.add_argument('--node_index', type=int, help='column index that contains node ids', default=0)
parser.add_argument('--output_dir', help='directory to output files; either this argument or full_mode_file and db_node_file MUST be specified', default='.')
parser.add_argument('--full_mode_file', help='output file name; outputs a list of snap ids and the db ids (db the snap id was derived from);' \
  + 'note that this file is appended to; OVERRIDES output_dir argument', default=None)
parser.add_argument('--db_node_file', help='output file name; output contains mapping of snap ids to db protein ids; OVERRIDES output dir argument', default=None)
parser.add_argument('--snap_id_counter_start', type=int, help='where to start assigning snap ids', default=-1)
args = parser.parse_args()


inFNm = args.input_file
db_id = args.db_id
mode_name = args.mode_name
dataset = args.dataset_name
outFNm = args.full_mode_file
if outFNm is None:
  outFNm = os.path.join(args.output_dir, utils.get_full_mode_file_name(mode_name))
dbFNm = args.db_node_file
if dbFNm is None:
  dbFNm = os.path.join(args.output_dir, utils.get_mode_file_name(mode_name, db_id, dataset))

counter = args.snap_id_counter_start
if counter == -1:
  counter = utils.get_file_len(outFNm)
node_index = args.node_index


seen = set()
with open(inFNm, 'r') as inF:
  with open(outFNm, 'a') as outF:
    with open(dbFNm, 'w') as dbF:
      if counter == 0:
        outF.write('# snap_id\tdataset id\n')
      outF.write('# Adding mapping for mode %s with dataset %s\n' % (mode_name, dataset))
      dbF.write('# Mapping for mode %s from dataset %s\n' % (mode_name, dataset))
      dbF.write('# snap_id\t%s specific id\n' % dataset)
      for line in inF:
        if line[0] == '#':
          continue
        node_id = line.strip().split('\t')[node_index]
        if node_id in seen:
          continue
        outF.write('%d\t%d\n' % (counter, db_id))
        dbF.write('%d\t%s\n' % (counter, node_id))
        seen.add(node_id)
        counter += 1
