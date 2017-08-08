import boto3
import csv

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    src_bucket = event['Records'][0]['s3']['bucket']['name']
    src_key = event['Records'][0]['s3']['object']['key']

    print("Triggered by file: {}".format(src_key))
    obj = s3.Object(src_bucket, src_key)
    contents = obj.get()['Body'].read().decode('utf-8')


    total_net = 0
    for row in csv.DictReader(contents.split()):
        print(row)
        total_net += (float(row["Gross"]) - float(row["Expenses"]))
    return "Total Net: ${0}".format(total_net)
