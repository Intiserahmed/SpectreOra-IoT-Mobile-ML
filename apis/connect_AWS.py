accessKey = 'accessKeyHere'
secretKey = 'SecretKeyHere'
bucketName = 'userdatastrokeprediction'
session = boto3.Session(
    aws_access_key_id=accessKey,
    aws_secret_access_key=secretKey,
    region_name= 'ap-southeast-1'
)
s3 = session.resource('s3')
for bucket in s3.buckets.all():
    print(bucket.name)
