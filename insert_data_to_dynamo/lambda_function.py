# coding: utf-8
import os
import json
from decimal import Decimal

from boto3.session import Session

from csv_to_json import conv_csv_to_json


def setup_dynamo_table(table_name):
	"""
	Setup dynamo table to insert records.

	Parameters:
	-----------
	table_name: string

	Returns:
	-----------
	dynamo_table: subclass of ServiceResource
	"""
	session = Session(
			region_name='ap-northeast-1'
	)
	dynamodb = session.resource('dynamodb')
	dynamo_table = dynamodb.Table(table_name)
	return dynamo_table


def insert_data_from_json(table, input_file_name):
	"""
	Insert json data to arg dynamo table.

	Parameters:
	-----------
	table: subclass of ServiceResource

	Returns:
	-----------
	input_file_name: json file converted from csv file
	"""
	with open(input_file_name, "r") as f:
		json_data = json.load(f)
		with table.batch_writer() as batch:
			for record in json_data:
				record["transaction_id"] = \
					Decimal("{}".format(record["transaction_id"]))
				record["term"] = \
					Decimal("{}".format(record["term"]))
				record["token_amount"] = \
					Decimal("{}".format(record["token_amount"]))
				batch.put_item(Item=record)
	print('Successfully inserted data.')


def lambda_handler(request, context):
	"""
	lambda handler.

	CAUTION: set envrironment viables.

	Parameters:
	-----------
	request:
	 - no use
	context:
	 - no use
	"""
	target_dynamo_table=os.environ['TARGET_DYNAMO_TABLE']
	target_csv_file=os.environ['CSV_FILE_NAME']
	dynamo_table = \
		setup_dynamo_table(target_dynamo_table)
	target_json_file = \
		conv_csv_to_json(target_csv_file)
	insert_data_from_json(dynamo_table, target_json_file)
