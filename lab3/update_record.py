
import json
import boto3
from datetime import datetime


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('cloudguru-awslambda-lab3-table')

    for record in event['Records']:
        if record['eventName'] != "INSERT":
            break

        item = record['dynamodb']['NewImage']

        net = float(item['gross']['N']) - float(item['costs']['N'])
        table.put_item(
           Item={
               "txid": item['txid']['S'],
               "costs": item['costs']['N'],
               "gross": item['gross']['N'],
               "net": str(net),
               "timestamp": str( datetime.now().date() ),
            }
        )


        print("DynamoDB Record: " + json.dumps(record['dynamodb'], indent=2))
    return 'Successfully processed {} records.'.format(len(event['Records']))
