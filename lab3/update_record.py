
import json
import boto3


def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] != "INSERT":
            break

        print(record['dynamodb']['NewImage'])
        print("^^^^^^^^^^^^^^^^^^")
        print(record['eventID'])
        print(record['eventName'])
        print("DynamoDB Record: " + json.dumps(record['dynamodb'], indent=2))
    return 'Successfully processed {} records.'.format(len(event['Records']))
