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
