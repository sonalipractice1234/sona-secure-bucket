# Assignment 3: Monitor Unencrypted S3 Buckets Using AWS Lambda and Boto3

## Objective

The objective of this project is to improve AWS security by automatically detecting Amazon S3 buckets that do not have Server-Side Encryption (SSE) enabled using AWS Lambda and Boto3.

---

## Project Overview

This solution uses an AWS Lambda function to:

* List all S3 buckets in the AWS account.
* Check each bucket's encryption configuration.
* Identify buckets without Server-Side Encryption.
* Log unencrypted bucket names to Amazon CloudWatch.
* Return a list of unencrypted buckets.

---

## AWS Services Used

* Amazon S3
* AWS Lambda
* AWS IAM
* Amazon CloudWatch Logs
* Boto3 (AWS SDK for Python)

---

## Architecture

```text
+-------------------+
|   Amazon S3       |
|     Buckets       |
+---------+---------+
          |
          |
          v
+-------------------+
|   AWS Lambda      |
| Encryption Check  |
+---------+---------+
          |
          |
          v
+-------------------+
| CloudWatch Logs   |
| Security Findings |
+-------------------+
```

---

## Prerequisites

Before starting, ensure you have:

* AWS Account
* IAM permissions to create roles and Lambda functions
* Python 3.x Runtime
* Access to Amazon S3

---

## Step 1: Create S3 Buckets

Create multiple S3 buckets for testing.

Example:

```text
sona-secure-bucket
sona-unsecure-bucket1
sona-unsecure-bucket2
sona-test-unencrypted
```

---

## Step 2: Create IAM Role

### Create Role

1. Open IAM Console
2. Navigate to Roles
3. Click Create Role
4. Select AWS Service → Lambda

### Attach Policy

```text
AmazonS3ReadOnlyAccess
```

### Role Name

```text
LambdaS3EncryptionMonitorRole
```

---

## Step 3: Create Lambda Function

### Function Details

| Setting        | Value                         |
| -------------- | ----------------------------- |
| Function Name  | S3EncryptionMonitor           |
| Runtime        | Python 3.12                   |
| Architecture   | x86_64                        |
| Execution Role | LambdaS3EncryptionMonitorRole |

---

## Lambda Code

```python
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def lambda_handler(event, context):

    buckets = s3.list_buckets()

    unencrypted_buckets = []

    for bucket in buckets['Buckets']:

        bucket_name = bucket['Name']

        try:
            s3.get_bucket_encryption(
                Bucket=bucket_name
            )

        except ClientError as e:

            if e.response['Error']['Code'] == \
               'ServerSideEncryptionConfigurationNotFoundError':

                unencrypted_buckets.append(bucket_name)

                print(
                    f"UNENCRYPTED BUCKET: {bucket_name}"
                )

    return {
        'statusCode': 200,
        'unencrypted_buckets': unencrypted_buckets
    }
```

---

## Deployment

1. Paste the code into Lambda.
2. Click Deploy.
3. Create a Test Event.

Example:

```json
{}
```

4. Click Test.

---

## Sample Output

### If Unencrypted Buckets Exist

```json
{
  "statusCode": 200,
  "unencrypted_buckets": [
    "sona-unsecure-bucket1",
    "sona-unsecure-bucket2"
  ]
}
```

### If All Buckets Are Encrypted

```json
{
  "statusCode": 200,
  "unencrypted_buckets": []
}
```

---

## CloudWatch Logs Example

```text
Checking bucket: sona-secure-bucket
Encryption Enabled: sona-secure-bucket

Checking bucket: sona-unsecure-bucket1
UNENCRYPTED BUCKET: sona-unsecure-bucket1

Checking bucket: sona-unsecure-bucket2
UNENCRYPTED BUCKET: sona-unsecure-bucket2
```

---

## Project Result

In this implementation, all S3 buckets were found to have encryption enabled.

Example Encryption Configuration:

```text
Server-side encryption with Amazon S3 managed keys (SSE-S3)
SSEAlgorithm: AES256
```

Therefore, the Lambda function returned:

```json
{
  "statusCode": 200,
  "unencrypted_buckets": []
}
```

This confirms that no unencrypted buckets were present in the AWS account.

---

## Security Benefits

* Detects non-compliant S3 buckets.
* Improves data protection.
* Supports AWS security audits.
* Helps enforce encryption-at-rest policies.
* Provides centralized monitoring through CloudWatch Logs.

---

## Learning Outcomes

After completing this project, the following concepts were learned:

* AWS Lambda Automation
* Amazon S3 Security
* Server-Side Encryption (SSE-S3)
* IAM Roles and Permissions
* Boto3 S3 APIs
* CloudWatch Logging
* Security Monitoring in AWS

---

## Screenshots Included

1. S3 Buckets Created
2. IAM Role Creation
3. Lambda Function Configuration
4. Lambda Python Code
5. Successful Lambda Execution
6. CloudWatch Logs
7. Bucket Encryption Configuration

---

## Author

Sonali Patil

AWS Security Monitoring Project – Detect Unencrypted S3 Buckets Using AWS Lambda and Boto3
