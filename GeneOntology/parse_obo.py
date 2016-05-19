import argparse

parser = argparse.ArgumentParser(description='Create snap node and edge tables.')
parser.add_argument('input_file', help='input file name. Should be an obo file')
parser.add_argument('func_node_file', help='node output file name; outputs a list of snap ids and db ids; note that this file is appended to')
parser.add_argument('db_node_file', help='node output file name; output contains mapping of snap ids to db function ids(GO ids)')
parser.add_argument('func_edge_file', help='edge output file name; outputs a list of snap ids (edge id and node ids) and db ids; note that this file is appended to')
parser.add_argument('db_edge_file', help='edge output file name; output contains mapping of snap ids to src/dst node db ids')
parser.add_argument('node_snap_id_counter_start', type=int, help='where to start assigning snap ids')
parser.add_argument('edge_snap_id_counter_start', type=int, help='where to start assigning snap ids')
parser.add_argument('node_db_id', type=int, help='int id for this database')
parser.add_argument('edge_db_id', type=int, help='int id for this database')

args = parser.parse_args()


edge_terms = ['disjoint_from',  'consider', 'alt_id', 'id', 'relationship', 'intersection_of', 'is_a', 'replaced_by']

with open(args.input_file, 'r') as inF:
	with open(args.func_edge_file, 'a') as map_file:
		with open(args.db_edge_file, 'w') as db_file:
			inTerm = False
			node_ids = {}
			edge_ids = {}
			node_counter = args.node_snap_id_counter_start
			edge_counter = args.edge_snap_id_counter_start
			currNode = None
			for line in inF:
				line = line.strip()
				if line == '[Term]':
					inTerm = True
					continue
				if len(line) == 0:
					inTerm = False
					currNode = None
					continue
				if inTerm:
					if line[0:3] == 'id:':
						node_id = line.split(':')[1].strip()
						if node_id not in node_ids:
							node_ids[node_id] = node_counter
							node_counter += 1
						currNode = node_ids[node_id]
					else:
						for term in edge_terms:
							if line.split(':')[0] == term:
								new_line = line[len(term)+1:].strip()
								if new_line[0:3] == 'GO:':
									attr = '-'
									dst_id = new_line.split(' ')[0]
								else:
									(attr, edge_id) = new_line.split('!')[0].split('GO:')
									attr = attr.strip()
									dst_id = 'GO:' + edge_id.strip()
								if dst_id not in node_ids:
									node_ids[dst_id] = node_counter
									node_counter += 1
								dst_node = node_ids[dst_id]
								map_file.write('%d\t%d\t%d\t%d\n' % (edge_counter, args.edge_db_id, currNode, dst_node))
								db_file.write('%d\t%d\t%d\n' % (edge_counter, args.node_db_id, args.node_db_id))
								edge_counter += 1

with open(args.func_node_file, 'a') as map_file:
	with open(args.db_node_file, 'w') as db_file:
		for node_id in node_ids:
			snap_id = node_ids[node_id]
			map_file.write('%d\t%d\n' % (snap_id, args.node_db_id))
			db_file.write('%d\t%s\n' % (snap_id, node_id))


