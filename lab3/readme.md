## Lab 3: DyanmoDb

This lab will trigger a lambda when a record is inserted into a DynamoDb table. The lambda will examine the new record, and add 2 fields to it: net_profit and datestamp.

I set up the DynamoDB table `cloudguru-awslambda-lab3-table` with an example record:
{
  "txid": "abba123",
  "gross": 39,
  "costs": 28
}
