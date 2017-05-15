from __future__ import print_function
import boto3
import boto
import json
import datetime

def selectState(order_tb, menu_tb, body):
    order_tb.put_item(Item=body)
    selection = dic(enumerate(menu_tb.get_item(Key={'menu_id': body.get('menu_id')}).get('Item').get('selection'), 1))
    msg = {'message': ', '.join(['{}_{}'.format(k,v) for k,v in selection.iteritems()])}


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def order_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    try:
        order_tb = boto3.resource('dynamodb', region_name='us-west-1').Table('order')
        menu_tb = boto3.resource('dynamodb', region_name='us-west-1').Table('menu')
        # order_tb = boto3.resource('dynamodb', region_name='us-west-1', endpoint_url = 'http://127.0.0.1:8000').Table('order')
        # menu_tb = boto3.resource('dynamodb', region_name='us-west-1', endpoint_url = 'http://127.0.0.1:8000').Table('menu')
    except Exception as not_found:
        print("Table doesn't exist.")

    operation = event['method']
    if operation == 'POST':
        body = event['body']
        order_tb.put_item(Item={
            'menu_id': body['menu_id'],
            'order_id': body['order_id'],
            'customer_name': body['customer_name'],
            "order_status": "selection"
        })
        selection = dict(enumerate(menu_tb.get_item(Key={'menu_id': body.get('menu_id')}).get('Item').get('selection'), 1))
        msg = {
            'message': 'Hi ' + body.get('customer_name') + ', please choose one of these selection:  ' + 
            ', '.join(['{} {}'.format(k,v) for k,v in selection.iteritems()])
        }
        return respond(None, msg)
    elif operation == 'PUT':
        body = event['body']
        order_id = event['param']
        menu_id = order_tb.get_item(Key=order_id).get('Item').get('menu_id')
        selection = dict(enumerate(menu_tb.get_item(Key={'menu_id': menu_id}).get('Item').get('selection'), 1))
        size = dict(enumerate(menu_tb.get_item(Key={'menu_id': menu_id}).get('Item').get('size'), 1))
        price = dict(enumerate(menu_tb.get_item(Key={'menu_id': menu_id}).get('Item').get('price')))
        input = int(event['body'].get('input'))

        if order_tb.get_item(Key=order_id).get('Item').get("order_status") == 'selection':
            order = {}
            order['selection'] = selection.get(input)
            order_tb.update_item(Key=order_id,
                UpdateExpression='SET order_status = :val1, #o = :val2',
                ExpressionAttributeNames={'#o': 'order'},
                ExpressionAttributeValues={
                    ':val1': 'size', 
                    ':val2': order
                })
            msg = {
                'message': 'Which size do you want? ' + ', '.join(['{} {}'.format(k,v) for k,v in size.iteritems()])
            }
        elif order_tb.get_item(Key=order_id).get('Item').get("order_status") == 'size':
            order = order_tb.get_item(Key=order_id).get('Item').get('order')
            order['size'] = size.get(input)
            order['price'] = str(price.get(input-1))
            order['order_time'] = str(datetime.datetime.now().strftime('%m-%d-%Y@%H:%M:%S'))
            order_tb.update_item(Key=order_id,
                UpdateExpression='SET order_status = :val1, #o = :val2',
                ExpressionAttributeNames={'#o': 'order'},
                ExpressionAttributeValues={
                    ':val1': 'processing',
                    ':val2': order,
                })
            msg = {
                'message': 'Your order costs ' + price.get(input-1) + '. We will email you when the order is ready. Thank you!'
            }
        else:
        	msg = {'message': 'Your order is in process. Please wait patiently'}
        return respond(None, msg)
    elif operation == 'GET':
        return respond(None, res=order_tb.get_item(Key=event['param']).get('Item'))
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
