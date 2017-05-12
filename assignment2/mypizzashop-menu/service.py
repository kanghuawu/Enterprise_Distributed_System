from __future__ import print_function
import boto3
import boto
import json

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else res,
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def menu_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    try:
        table = boto3.resource('dynamodb', region_name='us-west-1', endpoint_url = 'http://127.0.0.1:8000').Table('menu')
    	# table = boto3.resource('dynamodb', region_name='us-west-1').Table('menu')
    except Exception as not_found:
        print("Table doesn't exist.")

    operation = event['method']
    if operation == 'GET':
        return respond(None, table.get_item(Key=event['param']).get('Item'))
    elif operation == 'POST':
        
        return respond(None, table.put_item(Item=event['body']))
    elif operation == 'PUT':
        res = table.update_item(
            Key=event['param'],
            UpdateExpression='SET selection = :val1',
            ExpressionAttributeValues={':val1': event['body']['selection']})
        return respond(None, res)
    elif operation == 'DELETE':
        return respond(None, table.delete_item(Key=event['param']))
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))


'''
from __future__ import print_function

import boto3
import json

print('Loading function')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):

    #print("Received event: " + json.dumps(event, indent=2))

    operations = {
        'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
        'GET': lambda dynamo, x: dynamo.scan(**x),
        'POST': lambda dynamo, x: dynamo.put_item(**x),
        'PUT': lambda dynamo, x: dynamo.update_item(**x),
    }

    operation = event['httpMethod']
    if operation in operations:
        payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
        dynamo = boto3.resource('dynamodb').Table(payload['TableName'])
        return respond(None, operations[operation](dynamo, payload))
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))


'''