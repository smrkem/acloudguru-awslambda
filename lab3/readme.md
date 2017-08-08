## Lab 3: DyanmoDb

This lab will trigger a lambda when a record is inserted into a DynamoDb table. The lambda will examine the new record, and add 2 fields to it: net_profit and datestamp.

I set up the DynamoDB table `cloudguru-awslambda-lab3-table` with an example record:
{
  "txid": "abba123",
  "gross": 39,
  "costs": 28
}

And a lambda function `cloudguru-awslambda-lab3` with the above table as a trigger.
For the role I needed to add the AWSLambdaDynamoDBExecute policy.

The `update_record.py` file cas the code, and everything is working as intended. With the test event set up with proper keys, it passes and creates a record in the table. When I add a record to the table through the console, it gets instantly updated with correct 'net' and 'timestamp' fields!
