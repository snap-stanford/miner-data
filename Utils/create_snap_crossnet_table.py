import argparse
import utils
import os

parser = argparse.ArgumentParser(description='Create snap edge tables')
parser.add_argument('input_file', help='input file name. File should be a tsv, containing interactions between ids found in src_file_name and ids found in dst_file_name')
parser.add_argument('src_file', help='input file name. Should be a file outputted by create_snap_mode_table (with properly formatted name).')
parser.add_argument('dst_file', help='input file name. Should be a file outputted by create_snap_mode_table (with properly formatted name).')
parser.add_argument('cross_name', type=str, help='cross net name')
parser.add_argument('dataset_name', type=str, help='name of dataset')
parser.add_argument('db_id', type=int, help='int id for this dataset')
parser.add_argument('--src_node_index', type=int, help='column index that contains src node ids (NOT snap ids, from src_input_file)', default=0)
parser.add_argument('--dst_node_index', type=int, help='column index that contains dst node ids (NOT snap ids, from dst_input_file)', default=1)
parser.add_argument('--output_dir', help='directory to output files; either this argument or full_crossnet_file and db_edge_file MUST be specified', default='.')
parser.add_argument('--full_crossnet_file', help='output file name; outputs a list of snap ids, the db ids (db the snap id was derived from), and source and destination snap node ids;' \
  + 'note that this file is appended to; OVERRIDES output_dir argument', default=None)
parser.add_argument('--db_edge_file', help='output file name; output contains mapping of snap ids to dataset ids; OVERRIDES output dir argument', default=None)
parser.add_argument('--skip_missing_ids', action=store_true, help='don\'t throw an error if ids in input_file not found in src or dst file.')
parser.add_argument('--snap_id_counter_start', type=int, help='where to start assigning snap ids', default=-1)
args = parser.parse_args()


inFNm = args.input_file
srcFile = args.src_file
dstFile = args.dst_file
cross_name = args.cross_name
dataset = args.dataset_name
db_id = args.db_id

srcIdx = args.src_node_index
dstIdx = args.dst_node_index

src_db_id = utils.parse_dataset_id_from_name(srcFile)
dst_db_id = utils.parse_dataset_id_from_name(dstFile)

output_dir = args.output_dir
outFNm = args.full_crossnet_file
if outFNm is None:
  mode_name1 = utils.parse_mode_name_from_name(srcFile)
  mode_name2 = utils.parse_mode_name_from_name(dstFile)
  outFNm = os.path.join(args.output_dir, utils.get_full_cross_file_name(mode_name1, mode_name2))
outFNm2 = args.db_edge_file
if outFNm2 is None:
  mode_name1 = utils.parse_mode_name_from_name(srcFile)
  mode_name2 = utils.parse_mode_name_from_name(dstFile)
  outFNm2 = os.path.join(args.output_dir, utils.get_cross_file_name(mode_name1, mode_name2, db_id, dataset))


src_mapping = utils.read_mode_file(srcFile)
if os.path.samefile(srcFile, dstFile):
  dst_mapping = src_mapping
else:
  dst_mapping = utils.read_mode_file(dstFile)

counter = args.snap_id_counter_start
if counter == -1:
  counter = utils.get_file_len(outFNm)
print 'Starting at snap id: %d' % counter
with open(inFNm, 'r') as inF:
  with open(outFNm, 'a') as fullF:
    with open(outFNm2, 'w') as dbF:
      for line in inF:
        if line[0] == '#':
          continue
        vals =  line.strip().split('\t')
        id1 = vals[srcIdx]
        id2 = vals[dstIdx]
        if args.skip_missing_ids and (id1 not in src_mapping or id2 not in dst_mapping):
          continue
        fullF.write('%d\t%d\t%d\t%d\n' % (counter, db_id, src_mapping[id1], dst_mapping[id2]))
        dbF.write('%d\t%d\t%d\n' % (counter, src_db_id, dst_db_id))
        counter += 1
print 'Ending at snap id: %d' % counter
