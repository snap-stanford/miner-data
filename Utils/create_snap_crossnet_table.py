'''
file: create_snap_crossnet_table.py
author: Sheila Ramaswamy(@sramas15)

Script that creates snap tables for a given crossnet.

Usage:
python create_snap_crossnet_table.py <input_file_path> <src_file_path> <dst_file_path> <dataset_name> <dataset_id>

Positional Arguments:
input_file_path:         Path to the input file; Input file should be a tsv.
src_file_path:           Path to a dataset specific file, as outputted by create_snap_mode_table.py,
                         corresponding to the source mode. File name MUST MATCH FORMAT:
                         miner-<mode_name>-<dataset_id>-<dataset>-<date>.tsv
dst_file_path:           Path to a dataset specific file, as outputted by create_snap_mode_table.py,
                         corresponding to the destination mode. File name MUST MATCH FORMAT:
                         miner-<mode_name>-<dataset_id>-<dataset>-<date>.tsv
dataset_name:            Name of dataset being used to create the snap crossnet tables i.e. the 
                         dataset the input file comes from. e.g. STRING
dataset_id:              unique integer id for this dataset.


Optional arguments:
--src_node_index:        If there are multiple columns in the input tsv, the index of the column with the src node id.
                         Defaults to 0.
--dst_node_index:        If there are multiple columns in the input tsv, the index of the column with the dst node id.
                         Defaults to 1.
--output_dir:            Directory to create output files. Defaults to the current working directory.
--full_crossnet_file:    Name of output file tsv containing a list of <snap_id>\t<dataset_id>.
                         Defaults to output_dir/miner-<src_mode_name>-<dst_mode_name>-<date>.tsv
--db_edge_file:          Name of output file tsv for a specific dataset; contains a list of <snap id>\t<dataset_specific_entity_id>
                         Defaults to output_dir/miner-<src_mode_name>-<dst_mode_name>-<dataset_id>-<dataset>-<date>.tsv
--snap_id_counter_start  Start assigning snap ids from this integer value; this number MUST be greater
                         than any id found in the full crossnet file. If not specified, finds the max id in the
                         full_crossnet_file.
--skip_missing_ids       Flag; If any of the ids in the input tsv do not have snap ids (which are fetched from
                         the src and dst files), skip the line and continue parsing the data.

Example usage:
Creating files for genes-function relationships using GeneOntology:

Input files: go.tsv, miner-gene-0-GO-20160520.tsv, miner-function-0-GO-20160520.tsv

Output directory: outputs/genes-functions/

Output files: miner-gene-function-20160520.tsv, miner-gene-function-0-GO-20160520.tsv

Workflow:

python create_snap_crossnet_table.py go.tsv miner-gene-0-GO-20160520.tsv miner-function-0-GO-20160520.tsv GO 0 --output_dir outputs/genes-functions/
'''

import argparse
import utils
import os

parser = argparse.ArgumentParser(description='Create snap edge tables')
parser.add_argument('input_file', help='input file name. File should be a tsv, containing interactions between ids found in src_file_name and ids found in dst_file_name')
parser.add_argument('src_file', help='input file name. Should be a file outputted by create_snap_mode_table (with properly formatted name).')
parser.add_argument('dst_file', help='input file name. Should be a file outputted by create_snap_mode_table (with properly formatted name).')
parser.add_argument('dataset_name', type=str, help='name of dataset')
parser.add_argument('db_id', type=int, help='int id for this dataset')
parser.add_argument('--src_node_index', type=int, help='column index that contains src node ids (NOT snap ids, from src_input_file)', default=0)
parser.add_argument('--dst_node_index', type=int, help='column index that contains dst node ids (NOT snap ids, from dst_input_file)', default=1)
parser.add_argument('--output_dir', help='directory to output files; either this argument or full_crossnet_file and db_edge_file MUST be specified', default='.')
parser.add_argument('--full_crossnet_file', help='output file name; outputs a list of snap ids, the db ids (db the snap id was derived from), and source and destination snap node ids;' \
  + 'note that this file is appended to; OVERRIDES output_dir argument', default=None)
parser.add_argument('--db_edge_file', help='output file name; output contains mapping of snap ids to dataset ids; OVERRIDES output dir argument', default=None)
parser.add_argument('--skip_missing_ids', action='store_true', help='don\'t throw an error if ids in input_file not found in src or dst file.')
parser.add_argument('--snap_id_counter_start', type=int, help='where to start assigning snap ids', default=-1)
args = parser.parse_args()


inFNm = args.input_file
srcFile = args.src_file
dstFile = args.dst_file
dataset = args.dataset_name
db_id = args.db_id

srcIdx = args.src_node_index
dstIdx = args.dst_node_index

src_db_id = utils.parse_dataset_id_from_name(os.path.basename(srcFile))
dst_db_id = utils.parse_dataset_id_from_name(os.path.basename(dstFile))

output_dir = args.output_dir
outFNm = args.full_crossnet_file
if outFNm is None:
  mode_name1 = utils.parse_mode_name_from_name(os.path.basename(srcFile))
  mode_name2 = utils.parse_mode_name_from_name(os.path.basename(dstFile))
  outFNm = os.path.join(args.output_dir, utils.get_full_cross_file_name(mode_name1, mode_name2))
outFNm2 = args.db_edge_file
if outFNm2 is None:
  mode_name1 = utils.parse_mode_name_from_name(os.path.basename(srcFile))
  mode_name2 = utils.parse_mode_name_from_name(os.path.basename(dstFile))
  outFNm2 = os.path.join(args.output_dir, utils.get_cross_file_name(mode_name1, mode_name2, db_id, dataset))


src_mapping = utils.read_mode_file(srcFile)
if os.path.samefile(srcFile, dstFile):
  dst_mapping = src_mapping
else:
  dst_mapping = utils.read_mode_file(dstFile)

counter = args.snap_id_counter_start
if counter == -1:
  counter = utils.get_max_id(outFNm)
print 'Starting at snap id: %d' % counter
with open(inFNm, 'r') as inF:
  with open(outFNm, 'a') as fullF:
    with open(outFNm2, 'w') as dbF:
      for line in inF:
        if line[0] == '#' or line[0] == '\n':
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
