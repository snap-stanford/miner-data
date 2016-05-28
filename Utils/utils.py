'''
file: utils.py
author: Sheila Ramaswamy (@sramas15)

File containing util functions useful for other scripts.
'''
import os
from datetime import datetime

HUMAN_SPECIES_ID = '9606'

def get_filter(method_name):
	'''Given a function name(string), returns the corresponding function in this file.

	Input:
		method_name: string, function name.
	Output:
		a function in this file or None, if the function doesn't exist.
	'''
	if method_name is None:
		return None
	possibles = globals().copy()
	possibles.update(locals())
	method = possibles.get(method_name)
	return method

def remove_species_id(name):
	'''Filter that removes the species id from a string id. Currently only works
	with the human species id.

	Input:
		name: an ENSEMBL human protein id, prefixed with the species id.
	Output:
		the ENSEMBL human protein id, without the species prefix.
	'''
	vals = split_then_strip(name, '.')
	if len(vals) != 2 or vals[0] != HUMAN_SPECIES_ID:
		return name
	return vals[1]

def add_species_id(name):
	'''Adds the human species id as a prefix to the given ENSEMBL id.

	Input:
		name: the ENSEMBL protein id (string).
	Output:
		a string consisting of the human species id, '.' and name.
	'''
	return '%s.%s' % (HUMAN_SPECIES_ID, name)

def split_then_strip(string, split_char):
	'''Splits the string using the given character and removes whitespace from all
	resulting substrings.

	Input:
		string: string being split
		split_char: character (or multiple characters) used to split string
	Output:
		a list, consisting of the stripped substrings.
	'''
	return [s.strip() for s in string.split(split_char)]


def get_file_len(input_file):
	'''Returns the length of the input_file; Returns 0 if the file does not exist.

	Input:
	    input_file: path to the input file.
	Output:
	    number of lines in the file.
	'''
	if os.path.isfile(input_file):
		return sum(1 for line in open(input_file, 'r'))
	return 0

def get_max_id(input_file):
	'''Returns the max snap id of the input_file; Returns 0 if the file does not exist.
	Assumes file in format of snap mode or crossnet full table tsv file.

	Input:
	    input_file: path to the input file.
	Output:
	    max snap id in input file.
	'''
	max_id = -1
	if os.path.isfile(input_file):
		with open(input_file, 'r') as inF:
			for line in inF:
				if line[0]=='#':
					continue
				new_id = int(line.strip().split('\t')[0])
				if new_id > max_id:
					max_id = new_id
	max_id += 1
	return max_id

def get_current_date():
	'''Returns the current date, formatted as YYYYMMDD

	Input:
	    None
	Output:
	    Current date, as a string.
	'''
	format = '%Y%m%d'
	return datetime.now().strftime(format)

def get_full_mode_file_name(mode_name):
	'''Returns the formatted file name that should contain the full list of snap ids for the mode.

	Input:
	    mode_name: the name of the mode
	Output:
	    the formatted file name.
	'''
	return 'miner-%s-%s.tsv' % (mode_name, get_current_date())

def get_equiv_mode_file_name(mode_name):
	'''Returns the formatted file name that should contain the equivalence table of snap ids for the mode.

	Input:
	    mode_name: the name of the mode
	Output:
	    the formatted file name.
	'''
	return 'miner-%s-equiv-%s.tsv' % (mode_name, get_current_date())

def get_mode_file_name(mode_name, db_id, dataset):
	'''Returns the formatted file name that should contain the snap id to dataset
	specific id mapping.

	Input:
	    mode_name: the name of the mode
	    db_id: dataset id for the given dataset.
	    dataset: the name of the dataset e.g. STRING
	Output:
	    the formatted file name.
	'''
	return 'miner-%s-%d-%s-%s.tsv' % (mode_name, int(db_id), dataset, get_current_date())

def get_full_cross_file_name(mode_name1, mode_name2):
	'''Returns the formatted file name that should contain the full list of snap ids for the cross net.

	Input:
	    mode_name1: the name of the src mode
	    mode_name2: the name of the dst mode
	Output:
	    the formatted file name.
	'''
	return 'miner-%s-%s-%s.tsv' % (mode_name1, mode_name2,  get_current_date())

def get_cross_file_name(mode_name1, mode_name2, db_id, dataset):
	'''Returns the formatted file name that should contain the snap id to the dataset ids
	for the source and destination nodes.

	Input:
	    mode_name1: the name of the src mode
	    mode_name2: the name of the dst mode
	    db_id: dataset id for the given dataset.
	    dataset: the name of the dataset e.g. STRING
	Output:
	    the formatted file name.
	'''
	return 'miner-%s-%s-%d-%s-%s.tsv' % (mode_name1, mode_name2, int(db_id), dataset, get_current_date())

def parse_dataset_id_from_name(file_name):
	'''Extracts the dataset id from the formatted mode file name.

	Input:
	    file_name: mode file name, as returned by get_mode_file_name.
	Output:
	     the integer dataset id.
	'''
	return int(file_name.split('-')[2])

def parse_dataset_name_from_name(file_name):
	'''Extracts the dataset name from the formatted mode file name.

	Input:
	    file_name: mode file name, as returned by get_mode_file_name.
	Output:
	     the string dataset name.
	'''
	return file_name.split('-')[3]

def parse_mode_name_from_name(file_name):
	'''Extracts the mode name from the formatted mode file name.

	Input:
	    file_name: mode file name, as returned by get_mode_file_name.
	Output:
	     the string dataset mode name.
	'''
	return file_name.split('-')[1]

def read_mode_file(map_file):
	'''Reads the mapping between dataset specific ids to snap ids into a dictionary.

	Input:
	    map_file: file containing the mapping.
	Output:
	    dictionary from the dataset specific ids to snap ids.
	'''
	mapping = {}
	with open(map_file, 'r') as inF:
		for line in inF:
			if len(line) == 0 or line[0] == '#':
				continue
			vals = split_then_strip(line, '\t')
			snap_id = vals[0]
			dataset_id = vals[1]
			mapping[dataset_id] = int(snap_id)
	return mapping
