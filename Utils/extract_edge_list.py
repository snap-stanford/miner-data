'''
file: extract_edge_list.py
author: Sheila Ramaswamy(@sramas15)

Script that creates an edge list given the input file.

Usage:
python extract_edge_list.py <input_file_path> <output_file_path> <dataset_name> <src_node_column> <dst_node_column>

Positional Arguments:
input_file:              Path to the input file; Input file should be a tsv.
output_file:             Path to the output file; Output file will be a tsv.
dataset_name:            Name of dataset nodes are being extracted from e.g. STRING
src_node_column:         Column containing source node(s)
dst_node_column:         Column containing destination node(s)

Optional arguments:
--src_node_name:         String indicating how to refer to the src node ids in the file scheme. Defaults to node_id1.
--dst_node_name:         String indicating how to refer to the dst node ids in the file scheme. Defaults to node_id2.
--has_title:             If provided, skips over the first line of the file.
--verbose:               If provided, prints to the console for every million lines of the input file processed.
--src_node_sep:          If the column containing the src node actually contains a list of nodes, the character separater
                         used to split the text into the different node ids. Relevant for many-to-one relationships.
                         By default assumes only one node id specified.
--dst_node_sep:          If the column containing the dst node actually contains a list of nodes, the character separater
                         used to split the text into the different node ids. Relevant for one-to-many relationships.
                         By default assumes only one node id specified.

Example usage:
Extracting edge list from a STRING protein-protein interactions file, which contains many other fields.

Input files: STRING.tsv; assume protein 1 at index 1 and protein 2 at index 5.

Output file: STRING-edges.tsv

Workflow:

python extract_edge_list.py STRING.tsv STRING-edges.tsv STRING 1 5 --src_node_name protein_1 --dst_node_name protein_2
'''
import argparse
import utils

parser = argparse.ArgumentParser(description='Extract edges and additional data from a file')
parser.add_argument('input_file', help='input file name.')
parser.add_argument('output_file', help='output file name.')
parser.add_argument('dataset_name', help='Name of the dataset')
parser.add_argument('src_node_col', help='column index containing source nodes')
parser.add_argument('dst_node_col', help='column index containing destination nodes')
parser.add_argument('--src_node_sep', help='if multiple ids are specified in this column,' \
                  + ' character used to split them', default=None)
parser.add_argument('--dst_node_sep', help='if multiple ids are specified in this column,' \
                  + ' character used to split them', default=None)
parser.add_argument('--has_title', action='store_true',
                    help='has a title line')
parser.add_argument('--verbose', action='store_true',
                    help='Print every 1,000,000 lines processed')
parser.add_argument('--divider', default='\t', type=str, help='separator')
parser.add_argument('--src_node_name', default='node_id1', type=str, help='how to identify the src nodes in the header for tsv')
parser.add_argument('--dst_node_name', default='node_id2', type=str, help='how to identify the dst nodes in the header for tsv')

if __name__ == '__main__':
    args = parser.parse_args()
    #print(args)
    with open(args.input_file, 'r') as inF:
        with open(args.output_file, 'w') as outF:
            outF.write('# Dataset: %s\n' % args.dataset_name)
            outF.write('# %s\t%s\n' % (args.src_node_name, args.dst_node_name))
            for i, line in enumerate(inF):
                if args.verbose and i%1000000 == 0:
                    print 'Finished processing line %d in the original input file' % i
                if line[0] == '#' or line[0] == '!' or line[0] == '\n' or (i==0 and args.has_title):
                    continue
                vals = utils.split_then_strip(line, args.divider)
		#print(vals)
                src_nodes = [vals[int(args.src_node_col)]]
                dst_nodes = [vals[int(args.dst_node_col)]]
                if args.src_node_sep is not None:
                    src_nodes = src_nodes[0].split(args.src_node_sep)
                if args.dst_node_sep is not None:
                    dst_nodes = dst_nodes[0].split(args.dst_node_sep)
                for src_node in src_nodes:
                    if src_node == '':
                        continue
                    for dst_node in dst_nodes:
                        if dst_node != '':
                            outF.write('%s\t%s\n' % (src_node, dst_node))
