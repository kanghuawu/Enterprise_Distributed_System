from __future__ import print_function
import boto3
import boto
import sys
import argparse
import json

parser = argparse.ArgumentParser(description='Dynamodb Manager', prog='db_manager.py')
parser.add_argument('--mode', help='Connecto to AWS dynamodb server, or local dynamodb', choices=['local', 'server'], default='local')
parser.add_argument('--name', help='Table name', choices=['menu', 'order'], default='menu')
parser.add_argument('-d', help='Clean database', action='store_true')
parser.add_argument('-s', help='Scan database', action='store_true')
parser.add_argument('-c', help='Create database', action='store_true')

args = parser.parse_args()
if args.mode == 'local':
	db = boto3.resource('dynamodb', endpoint_url = 'http://127.0.0.1:8000', region_name='us-west-1')
elif args.mode == 'server':
	db = boto3.resource('dynamodb', region_name='us-west-1')
else:
	print('Need to choose a mode')
	sys.exit(1)
if args.c:
	try:
		table = db.create_table(
			TableName = args.name,
			KeySchema = [
			{
				'AttributeName': args.name + '_id',
				'KeyType': 'HASH'
			}],
			AttributeDefinitions = [
			{
				'AttributeName': args.name + '_id',
				'AttributeType': 'S'
			}],
			ProvisionedThroughput = {
				'ReadCapacityUnits': 5,
				'WriteCapacityUnits': 5
				}
			)
		table.meta.client.get_waiter('table_exists').wait(TableName=args.name)
	except Exception as in_use:
		print(args.name + ' table exist')
		try:
			table = db.Table(args.name)
		except Exception as e:
			print(args.name + " table doesn't exist.")
else:
	try:
		table = db.Table(args.name)
	except Exception as e:
		print(args.name + " table doesn't exist.")

response = table.scan()
items = response['Items']

if args.s:
	print('Scanning....')
	print(json.dumps(items, indent = 2))

if args.d:
	print('Deleting....')
	for it in items:
		print(json.dumps(it[args.name + '_id'], indent = 2))
		table.delete_item(Key={args.name + '_id':it[args.name + '_id']})