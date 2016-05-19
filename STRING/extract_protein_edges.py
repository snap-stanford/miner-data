import argparse

parser = argparse.ArgumentParser(description='Extract edges and additional data from a file')
parser.add_argument('input_file', help='input file name.')
parser.add_argument('output_file', help='output file name.')
parser.add_argument('columns', metavar='N', type=int, nargs='+',
                    help='columns to extract')
parser.add_argument('--has_title', action='store_true',
                    help='has a title line')
parser.add_argument('--divider', default=' ', type=str, help='separator')

if __name__ == '__main__':
        args = parser.parse_args()
        with open(args.input_file, 'r') as inF:
                with open(args.output_file, 'w') as outF:
                        for i, line in enumerate(inF):
                                if i%1000000 == 0:
                                        print i
                                vals = line.strip().split(args.divider)
                                #print len(vals)
                                new_line_vals = []
                                for column in args.columns:
                                        new_line_vals.append(vals[column])
                                new_line = '\t'.join(new_line_vals) + '\n'
                                if (args.has_title and i==0) or line[0] == '#':
                                        new_line = '#' + new_line
                                outF.write(new_line)
