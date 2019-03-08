# coding: utf-8
import os
import logging
import socket

import boto3

# Setting for logging
# Environment Variable 'logging_level' allows to control logging level
logger = logging.getLogger()
logLevelTable={'DEBUG': logging.DEBUG, 'INFO': logging.INFO, \
	'WARNING': logging.WARNING, 'ERROR': logging.ERROR, \
	'CRITICAL': logging.CRITICAL}
if 'logging_level' in os.environ and \
	os.environ['logging_level'] in logLevelTable:
	logLevel=logLevelTable[os.environ['logging_level']]
else:
	logLevel=logging.WARNING
logger.setLevel(logLevel)


def lambda_handler(event, context):
	"""
	Create and kick and delete lambda functions from lambda function.

	.
	"""
	ip = socket.gethostbyname(socket.gethostname())
	logger.info(ip)

	client = boto3.client('lambda', 'ap-northeast-1')

	# Create lambda functions
	for i in range(20):
		name_parameter = str(i)
		new_lambda_name = 'lambdaTestIP' + name_parameter + 'nd'
		try:
			response = client.create_function(
				FunctionName=new_lambda_name,
				Runtime='python3.6',
				Role=os.environ['lambda_role'],
				Handler='lambda_get_ip.lambda_handler',
				Code={
					'S3Bucket': 'lambda-sketch-pallet',
					'S3Key': 'lambda_get_ip.py.zip',
				},
				Timeout=123,
				MemorySize=128,
				Publish=False,
				Environment={
					'Variables': {
						'logging_level': 'INFO'
					}
				}
			)
			logger.info(response)
		except Exception as e:
			logger.exception(e)

	# Kick lambda functions with Event type invocation
	for i in range(20):
		name_parameter = str(i)
		lambda_name = 'lambdaTestIP' + name_parameter + 'nd'
		try:
			response = client.invoke(
				FunctionName=lambda_name,
				InvocationType='Event'
			)
			http_status = response['ResponseMetadata']['HTTPStatusCode']
			request_id = response['ResponseMetadata']['RequestId']
			logger.info('HTTPStatusCode: {}, \
				RequestID: {}'.format(http_status, request_id))
		except Exception as e:
			logger.exception(e)

	# Delete lambda functions
	for i in range(20):
		name_parameter = str(i)
		lambda_name = 'lambdaTestIP' + name_parameter + 'nd'
		try:
			response = client.delete_function(
				FunctionName=lambda_name
			)
		except Exception as e:
			logger.exception(e)
