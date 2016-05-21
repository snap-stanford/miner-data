# Utils
import os
from datetime import datetime

def get_file_len(input_file):
	if os.path.isfile(input_file):
		return sum(1 for line in open(input_file, 'r'))
	return 0

def get_current_date():
	format = '%Y%m%d'
	return datetime.now().strftime(format)

def get_full_mode_file_name(mode_name):
	return 'miner-%s-%s.tsv' % (mode_name, get_current_date())

def get_mode_file_name(mode_name, db_id, dataset):
	return 'miner-%s-%d-%s-%s.tsv' % (mode_name, int(db_id), dataset, get_current_date())

def get_full_cross_file_name(mode_name1, mode_name2):
	return 'miner-%s-%s-%s.tsv' % (mode_name1, mode_name2,  get_current_date())

def get_cross_file_name(mode_name1, mode_name2, db_id, dataset):
	return 'miner-%s-%s-%d-%s-%s.tsv' % (mode_name1, mode_name2, int(db_id), dataset, get_current_date())

def parse_dataset_id_from_name(file_name):
	return int(file_name.split('-')[2])

def parse_dataset_name_from_name(file_name):
	return int(file_name.split('-')[3])

def parse_mode_name_from_name(file_name):
	return int(file_name.split('-')[1])

def read_mode_file(map_file):
	mapping = {}
	with open(map_file, 'r') as inF:
		for line in inF:
			(snap_id, dataset_id) = line.strip().split('\t')
			mapping[dataset_id] = int(snap_id)
	return mapping