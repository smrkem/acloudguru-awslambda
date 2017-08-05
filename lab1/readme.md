### Lab 1: Parsing a csv file uploaded to S3

Create a bucket using the cli
```
aws s3 mb ms-awslamba-lab0
```
and upload the sample csv file to it.
```
aws s3 cp sample.csv s3://ms-awslambda-lab0
```

##### Version 1
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

To make sure my lambda function is being triggered correctly, I copied the file `sample.csv` over to `sample2.csv` and changed one of the values in it. I uploaded that to s3 and then found the new entry in the cloudwatch logs. woot!



Currently the only version or qualifier I have is $LATEST - nothing is publihsed yet. I create version 1.
```
aws lambda update-function-code --zip-file=fileb://csv_parse.zip --function-name awslambda-lab1
```
and in the console I can see the new version and create an alias "PROD" which points to it.

##### Version 2
Next step is to update the lambda so it outputs the Net revenue totals for the day. The csv looks like:  

|Day       |Customers|Gross|Expenses|
|----------|---------|-----|--------|
|2016-05-25|       45|  500|     273|
|2016-05-26|       90| 9240|    3947|
|2016-05-27|       20|  200|     250|

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
