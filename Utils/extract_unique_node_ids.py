'''
file: extract_unique_node_ids.py
author: Sheila Ramaswamy(@sramas15)

Script that creates a tsv containing all the unique node ids from a given input file.

Usage:
python extract_unique_node_ids.py <input_file_path> <output_file_path> <dataset_name> <column_1> <column_2> ... <column_N>

Positional Arguments:
input_file:              Path to the input file; Input file should be a tsv.
output_file:             Path to the output file; Output file will be a tsv.
dataset_name:            Name of dataset nodes are being extracted from e.g. STRING
columns:                 Columns containing node ids. Can specify many.


Optional arguments:
--node_name:             String indicating how to refer to the node ids in the file scheme. Defaults to node_id.
--has_title:             If provided, skips over the first line of the file.
--verbose:               If provided, prints to the console for every million lines of the input file processed.

Example usage:
Extracting node ids from a STRING edgelist file, consisting of <src_node_id>\t<dst_node_id>

Input files: STRING.tsv

Output file: STRING-nodes.tsv

Workflow:

python extract_unique_node_ids.py STRING.tsv STRING-nodes.tsv STRING 0 1 --node_name ENSEMBL_peptide_id --verbose 
'''


import argparse
import utils

parser = argparse.ArgumentParser(description='Extract unique node ids from file.')
parser.add_argument('input_file', help='input file name.')
parser.add_argument('output_file', help='output file name.')
parser.add_argument('dataset_name', help='Name of the dataset')
parser.add_argument('columns', metavar='N', type=int, nargs='+',
                    help='columnswith node ids')
parser.add_argument('--has_title', action='store_true',
                    help='has a title line that is not prefixed with a #')
parser.add_argument('--verbose', action='store_true',
                    help='Print every 1,000,000 lines processed')
parser.add_argument('--divider', default='\t', type=str, help='column separator, by default a tab')
parser.add_argument('--node_name', default='node_id', type=str, help='how to identify the nodes in the header for tsv')

if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.input_file, 'r') as inF:
        unique_ids = set()
        with open(args.output_file, 'w') as outF:
            outF.write('# Dataset: %s\n' % args.dataset_name)
            outF.write('# %s\n' % args.node_name)
            for i, line in enumerate(inF):
                if args.verbose and i%1000000 == 0:
                    print 'Finished processing line %d in the original input file' % i
                if line[0] == '#' or line[0] == '!' or line[0] == '\n' or (i==0 and args.has_title):
                    continue
                vals = utils.split_then_strip(line, args.divider)
                for column in args.columns:
                    if vals[column] not in unique_ids and len(vals[column]) > 0:
                        unique_ids.add(vals[column])
                        new_line = '%s\n' % vals[column]
                        outF.write(new_line)
