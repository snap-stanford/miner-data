import argparse

parser = argparse.ArgumentParser(description='Extract unique node ids from file.')
parser.add_argument('input_file', help='input file name.')
parser.add_argument('output_file', help='output file name.')
parser.add_argument('columns', metavar='N', type=int, nargs='+',
                    help='columns to with node ids')
parser.add_argument('--has_title', action='store_true',
                    help='has a title line')
parser.add_argument('--divider', default='\t', type=str, help='separator')
parser.add_argument('--node_name', default='node id', type=str, help='how to identify the nodes in the header for tsv')

if __name__ == '__main__':
        args = parser.parse_args()
        with open(args.input_file, 'r') as inF:
                unique_ids = set()
                with open(args.output_file, 'w') as outF:
                        outF.write('# %s\n' % args.node_name)
                        for i, line in enumerate(inF):
                                if i%1000000 == 0:
                                        print i
                                if line[0] == '#' or (i==0 and args.has_title):
                                    continue
                                vals = line.strip().split(args.divider)
                                for column in args.columns:
                                    if vals[column] not in unique_ids:
                                        unique_ids.add(vals[column])
                                        new_line = '%s\n' % vals[column]
                                        outF.write(new_line)
