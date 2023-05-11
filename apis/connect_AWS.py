import boto3
import os

accessKey = 'AKIAVWCJ7IWM3E2ZUVIU'
""": str = os.environ.get("awsAccessKey")"""
secretKey = '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'
""": str = os.environ.get("awsSecretKey")"""

session = boto3.Session(
    aws_access_key_id=accessKey,
    aws_secret_access_key=secretKey,
    region_name= 'ap-southeast-1'
)

s3 = session.resource('s3')

buckets = [bucket.name for bucket in s3.buckets.all()]
print(buckets)