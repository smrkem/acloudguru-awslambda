## Lab 1: Parsing a csv file uploaded to S3

Create a bucket using the cli
```
aws s3 mb ms-awslamba-lab0
```
and upload the sample csv file to it.
```
aws s3 cp sample.csv s3://ms-awslambda-lab0
```

### Version 1
Next I created a lambda function (python 3) using the console called `awslambda-lab1`.
Leaving the sample generated code alone - I wrote the `csv_read.py` file:
```
import boto3

s3 = boto3.resource('s3')


def lambda_handler(event, context):
    src_bucket = event['Records'][0]['s3']['bucket']['name']
    src_key = event['Records'][0]['s3']['object']['key']

    obj = s3.Object(src_bucket, src_key)
    contents = obj.get()['Body'].read().decode('utf-8')
    print("Raw CSV: {}".format(contents))
    return contents
```
 and zipped it up:
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
aws lambda update-function-code --zip-file=fileb://csv_parse.zip --function-name awslambda-lab1 --publish
```
and in the console I can see the new version and create an alias "PROD" which points to it.

### Version 2
Next step is to update the lambda so it outputs the Net revenue totals for the day. The csv looks like:  

|Day       |Customers|Gross|Expenses|
|----------|---------|-----|--------|
|2016-05-25|       45|  500|     273|
|2016-05-26|       90| 9240|    3947|
|2016-05-27|       20|  200|     250|

So for each csv file I'd like to sum up the 'gross' - 'expenses' value from each line. I'm not going to bother checking that those columns exist. I also want to add some output to make looking at the cloudwatch logs nicer.

The course uses a whole new file and function-handler for the new version, but I'm just going to update csv_read to

```
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
        total_net += (row["Gross"] - row["Expenses"])
    return "Total Net: ${0}".format(total_net)
```
and rezip and publish the file.
```
$ zip -r csv_parse.zip *.py
$ aws lambda update-function-code --zip-file=fileb://csv_parse.zip --function-name awslambda-lab1 --publish
```

I can see in the console that version 2 is there and is $LATEST. What will happen now if I upload a new csv to s3? I change a couple values in sample3.csv and copy it to my bucket?
```
aws s3 cp sample3.csv s3://ms-awslamba-lab0
```
Shoot - An error!!
```
Traceback (most recent call last):
File "/var/task/csv_read.py", line 18, in lambda_handler
total_net += (row["Gross"] - row["Expenses"])
TypeError: unsupported operand type(s) for -: 'str' and 'str'
```
lol - stupid me. An easy fix which I'll upload *without* publishing a new version. Converting the strings to floats:
```
for row in csv.DictReader(contents.split()):
    print(row)
    total_net += (float(row["Gross"]) - float(row["Expenses"]))
return "Total Net: ${0}".format(total_net)
```
I then save, rezip and reupload - this time without the `--publish` flag.
```
$ zip -r csv_parse.zip *.py
$ aws lambda update-function-code --zip-file=fileb://csv_parse.zip --function-name awslambda-lab1
```
and in the returned output I see it's uploaded to $LATEST.
