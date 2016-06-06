'''
file: create_snap_mode_equiv_table.py
author: Sheila Ramaswamy(@sramas15)

Script that creates snap equivalence table between two datasets for a given mode.

Usage:
python create_snap_mode_equiv_table.py <dataset1_file_path> <dataset2_file_path>

Positional Arguments:
dataset1_file:           Path to a dataset specific file, as outputted by create_snap_mode_table.py,
                         corresponding to the source mode. File name MUST MATCH FORMAT:
                         miner-<mode_name>-<dataset_id>-<dataset>-<date>.tsv
dataset2_file:           Path to a dataset specific file, as outputted by create_snap_mode_table.py,
                         corresponding to the destination mode. File name MUST MATCH FORMAT:
                         miner-<mode_name>-<dataset_id>-<dataset>-<date>.tsv


Optional arguments:
--mapping_file:          Path to a tsv file containing the mapping between the two datasets.
--ds1_node_index:        If there are multiple columns in the input tsv, the index of the column with the dataset1 entity id.
                         Defaults to 0.
--ds2_node_index:        If there are multiple columns in the input tsv, the index of the column with the dataset2 entity id.
                         Defaults to 1.
--output_dir:            Directory to create output files. Defaults to the current working directory.
--equiv_file:            Name of output file tsv containing a list of <snap_id>\t<snap_id>.
                         Defaults to output_dir/miner-<mode_name>-equiv-<date>.tsv
--skip_missing_ids       Flag; If any of the ids in the input tsv do not have snap ids (which are fetched from
                         the src and dst files), skip the line and continue parsing the data.

Example usage:
Creating equivalence file for genes using GeneOntoloty and HUGO

Input files: hugo.tsv, miner-gene-0-GO-20160520.tsv, miner-gene-1-HUGO-20160520.tsv

Output directory: outputs/genes/

Output files: miner-gene-equiv-20160520.tsv

Workflow:

python create_snap_mode_equiv_table.py miner-gene-0-GO-20160520.tsv miner-gene-1-HUGO-20160520.tsv --mapping_file_path hugo.tsv --output_dir outputs/genes/
'''

import argparse
import utils
import os

parser = argparse.ArgumentParser(description='Create snap edge tables')
parser.add_argument('dataset1_file', help='input file name. Should be a file outputted by create_snap_mode_table (with properly formatted name).')
parser.add_argument('dataset2_file', help='input file name. Should be a file outputted by create_snap_mode_table (with properly formatted name).')
parser.add_argument('--mapping_file', help='path to a tsv file giving a mapping between the dataset specific ids in dataset1 and dataset2 files.', default=None)
parser.add_argument('--ds1_node_index', type=int, help='column index that contains ds1 node ids (NOT snap ids, from src_input_file)', default=0)
parser.add_argument('--ds2_node_index', type=int, help='column index that contains ds2 node ids (NOT snap ids, from dst_input_file)', default=1)
parser.add_argument('--output_dir', help='directory to output files; either this argument or full_crossnet_file and db_edge_file MUST be specified', default='.')
parser.add_argument('--equiv_file', help='output file name; outputs a equivalence table of snap ids' \
  + 'note that this file is appended to; OVERRIDES output_dir argument', default=None)
parser.add_argument('--skip_missing_ids', action='store_true', help='don\'t throw an error if ids in input_file not found in src or dst file.')
args = parser.parse_args()


inFNm = args.mapping_file
dsFile1 = args.dataset1_file
dsFile2 = args.dataset2_file

ds1Idx = args.ds1_node_index
ds2Idx = args.ds2_node_index

output_dir = args.output_dir
outFNm = args.equiv_file
mode_name = 'Unknown'
if outFNm is None:
  mode_name1 = utils.parse_mode_name_from_name(os.path.basename(dsFile1))
  mode_name2 = utils.parse_mode_name_from_name(os.path.basename(dsFile2))
  mode_name = mode_name1
  assert mode_name1 == mode_name2
  outFNm = os.path.join(args.output_dir, utils.get_equiv_mode_file_name(mode_name1))

ds1_mapping = utils.read_mode_file(dsFile1)
if os.path.samefile(dsFile1, dsFile2):
  ds2_mapping = ds1_mapping
else:
  ds2_mapping = utils.read_mode_file(dsFile2)

add_header = True
if os.path.isfile(outFNm):
  add_header = False


with open(outFNm, 'a') as equivF:
  if add_header:
    equivF.write('# Equivalence table for mode %s\n' % mode_name)
    equivF.write('# File generated on: %s\n' % utils.get_current_date())
    equivF.write('# snap_nid_1\tsnap_nid_2\n')
  if inFNm is not None:
    with open(inFNm, 'r') as inF:
      for line in inF:
        if line[0] == '#' or line[0] == '\n':
          continue
        vals = utils.split_then_strip(line, '\t')
        id1 = vals[ds1Idx]
        id2 = vals[ds2Idx]
        if id1 == '' or id2 == '':
          continue
        if args.skip_missing_ids and (id1 not in ds1_mapping or id2 not in ds2_mapping):
          continue
        equivF.write('%d\t%d\n' % (ds1_mapping[id1], ds2_mapping[id2]))
  else:
    for id1 in ds1_mapping:
      if id1 in ds2_mapping:
        equivF.write('%d\t%d\n' % (ds1_mapping[id1], ds2_mapping[id1]))
