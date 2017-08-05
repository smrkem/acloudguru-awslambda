### Lab 1: Parsing a csv file uploaded to S3

Create a bucket using the cli
```
aws s3 mb ms-awslamba-lab0
```
and upload the sample csv file to it.
```
aws s3 cp sample.csv s3://ms-awslambda-lab0
```


Next I created a lambda function (python 3) using the console called `awslambda-lab1`.
Leaving the sample generated code alone - I wrote the `csv_read.py` file here and zipped it up:
```
zip -r csv_parse.zip *.py
```
which I can then use to update the code in the lambda function I created.
```
aws lambda update-function-code --zip-file=fileb://csv_parse.zip --function-name awslambda-lab1
```
Afterwards, the function configuration is still wrong and has "Handler": "lambda_function.lambda_handler". I need to correct this to "csv_read.lambda_handler" so
```
aws lambda update-function-configuration --function-name awslambda-lab1 --handler csv_read.lambda_handler
```


Using the S3 Put test trigger in the console, (remembering to change bucket name, arn and object name), everything is working as expected!!


```
import boto3
import csv

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    src_bucket = event['Records'][0]['s3']['bucket']['name']
    src_key = event['Records'][0]['s3']['object']['key']

    obj = s3.Object(src_bucket, src_key)
    contents = obj.get()['Body'].read().decode('utf-8')

    for row in csv.DictReader(contents.split()):
        print(row)
    return "Got {0}: {1}".format(src_bucket, src_key)
```
