import boto3

s3 = boto3.resource('s3')


def lambda_handler(event, context):
    src_bucket = event['Records'][0]['s3']['bucket']['name']
    src_key = event['Records'][0]['s3']['object']['key']

    obj = s3.Object(src_bucket, src_key)
    contents = obj.get()['Body'].read().decode('utf-8')
    print("Raw CSV: {}".format(contents))
    return contents
