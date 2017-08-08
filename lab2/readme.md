## Lab 2: Kinesis

This will set up a lambda function to operate on records as they are put into a Kinesis stream. First I'll set up a Kinesis stream in the console - `acloudguru-awslambda-lab2`.

Setting up the function was trickier than I anticipated. I selected my stream as a trigger, but there was no policy template for Kinesis, and my experience in the console wasn't matching the course demo. I ended up creating the default lambda execution role, and manually adding the Kinesis read access policy to it.

**cloudguru-awslambda-lab2**

The code for this function will be pretty simple. Input records will be the same as in lab1. Kinesis batches up multiple records in the event sent to lambda.

It took me several tries to get the bytes to string decoding right :(

```
import base64


def lambda_handler(event, context):
    net_profit = 0
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        print("Decoded Payload: {}".format(payload))
        row = payload.split(',')
        net_profit += (float(row[2]) - float(row[3]))
    print("Net Profits: ${}".format(net_profit))
    return net_profit
```

Once again I zip this up and upload it as the code in my lambda function.
```
$ zip -r kinesis_sums.zip *.py
$ aws lambda update-function-code --zip-file=fileb://kinesis_sums.zip --function-name cloudguru-awslambda-lab2
$ aws lambda update-function-configuration --function-name cloudguru-awslambda-lab2 --handler sum_records.lambda_handler
$ aws lambda update-function-code --zip-file=fileb://kinesis_sums.zip --function-name cloudguru-awslambda-lab2 --publish
```
