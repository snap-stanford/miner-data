'''
file: parse_obo_for_functions.py
author: Sheila Ramaswamy(@sramas15)

Script that parses the gene ontology obo file for the function-function edge list.

Usage:
python parse_obo_for_functions.py <input_file_path> <output_file_path>

Positional Arguments:
input_file_path:         Path to the input file; Input file should be the GO obo file.
output_file_path:        Path to the output file; Will be a tsv with the following schema:
					     <go_id1>\\t<go_id2>\\t<optional_edge_attr>



Example usage:
Creating files for function-function relationships using GeneOntology:

Input files: /path/to/input/go.obo

Output files: /path/to/output/functions.tsv

Workflow:

python parse_obo_for_functions.py /path/to/input/go.obo /path/to/output/functions.tsv
'''
import argparse

parser = argparse.ArgumentParser(description='Parses and create an edge list for go functions of the form <go_id1>\\t<go_id2>\\t<optional_edge_attr>')
parser.add_argument('input_file', help='input file name. Should be an obo file')
parser.add_argument('output_file', help='output file name. Will be a tsv')

args = parser.parse_args()


edge_terms = ['disjoint_from',  'consider', 'alt_id', 'id', 'relationship', 'intersection_of', 'is_a', 'replaced_by']

lbls = ['name','desc','namespace','synonym']

with open(args.input_file, 'r') as inF:
	with open(args.output_file, 'a') as outF:
		outF.write('# Function-function interactions from GO\n')
		outF.write('# GO_id1\tname\tdesc\tnamespace\tsynonym\n')
		inTerm = True
		currNode = None
		passed = False
		for line in inF:
			line = line.strip()
			#if line == '[Term]':
				#inTerm = True
				#continue
			if len(line) == 0:
				#inTerm = False
				#currNode = None
				continue
			if inTerm:

				if line[0:3] == 'id:':
					if passed:
						for lbl in lbls:
							if lbl not in linedict.keys():
								linedict[lbl]='N/A'
						outF.write('%s\t%s\t%s\t%s\t%s\n' % (linedict['id'], linedict['name'],linedict['desc'],linedict['namespace'],linedict['synonym']))
					linedict = {}
					linedict['id']= line[4:].strip()
					currNode = linedict['id']
					passed = True
				else:
					if line.split(':')[0] in lbls:
						term = line.split(':')[0]
						assert currNode is not None
						new_line = line[len(term)+1:].strip()
						if 'EXACT []' in new_line:
							new_line = new_line.replace('EXACT []','')
						linedict[term] = new_line
							#if new_line[0:3] == 'GO:':
							#	attr = '-'
							#		dst_id = new_line.split(' ')[0]
							#else:
							#	(attr, edge_id) = new_line.split('!')[0].split('GO:')
							#	attr = attr.strip()
							#	dst_id = 'GO:' + edge_id.strip()
				#outF.write('%s\t%s\t%s\n' % (currNode, dst_id, term))
							


