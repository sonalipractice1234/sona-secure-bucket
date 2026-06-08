import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def lambda_handler(event, context):

    buckets = s3.list_buckets()
    unencrypted_buckets = []

    for bucket in buckets['Buckets']:

        bucket_name = bucket['Name']

        try:
            s3.get_bucket_encryption(Bucket=bucket_name)

        except ClientError as e:

            if e.response['Error']['Code'] == \
               'ServerSideEncryptionConfigurationNotFoundError':

                unencrypted_buckets.append(bucket_name)
                print(f"UNENCRYPTED BUCKET: {bucket_name}")

    return {
        'statusCode': 200,
        'unencrypted_buckets': unencrypted_buckets
    }