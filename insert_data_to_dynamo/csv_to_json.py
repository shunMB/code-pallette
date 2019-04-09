# coding: utf-8
import csv
import json


def conv_csv_to_json(target_csv_file):
	"""
	Convert csv file to json file.

	Parameters:
	-----------
	target_csv_file: csv file
	"""
	json_list = []

	with open(target_csv_file, 'r') as f:
		for line in csv.DictReader(f):
			json_list.append(line)

	with open('NEW_JSON_FILE_NAME.json', 'w') as f:
		json.dump(json_list, f)
