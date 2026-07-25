# Assignment 1 - Automated S3 Bucket Cleanup (Objects Older Than 30 Days)

# Architecture

```text
                  Amazon EventBridge
                         │
                         │
                         ▼
                AWS Lambda Function
                         │
                         ▼
                List Objects in S3 Bucket
                         │
                         ▼
             Compare Object LastModified Date
                         │
              ┌──────────┴──────────┐
              │                     │
          Older than 30 Days?      No
              │                     │
             Yes                    │
              │                     │
              ▼                     ▼
      Delete Object          Keep Object
              │
              ▼
      CloudWatch Logs
```

# Project Structure

```text
Assignment-1-S3-Cleanup
│
├── lambda_function.py
├── README.md
└── screenshots
    ├── 01-s3-bucket.png
    ├── 02-iam-role.png
    ├── 03-inline-policy.png
    ├── 04-lambda-configuration.png
    ├── 05-lambda-test.png
    ├── 06-cloudwatch-logs.png
    └── 07-final-bucket.png
```

---

# Implementation Steps

## Step 1 - Create an Amazon S3 Bucket

Created an Amazon S3 bucket named **hamid-s3-cleanup** and uploaded sample files for testing.

For testing purposes, the object age threshold was temporarily reduced so that deletion could be verified without waiting 30 days.

![S3 Bucket](screenshots/01-s3-bucket.png)

---

## Step 2 - Create the IAM Role

Created an IAM role for AWS Lambda.

Attached the managed policy:

- AWSLambdaBasicExecutionRole

Created an inline least-privilege policy with permissions:

- s3:ListBucket
- s3:DeleteObject

The permissions were scoped only to the target S3 bucket.

![IAM Role](screenshots/02-iam-role.png)

![Inline IAM Policy](screenshots/03-inline-policy.png)

---

## Step 3 - Create the Lambda Function

Created an AWS Lambda function using:

- Runtime: Python 3.12+
- Architecture: x86_64
- Execution Role: S3-Cleanup-Lambda-Role

The Lambda function scans the bucket and removes stale objects.

![Lambda Configuration](screenshots/04-lambda-configuration.png)

---

## Step 4 - Deploy the Python Code

The Lambda function performs the following actions:

1. Connects to Amazon S3 using Boto3.
2. Uses a paginator to retrieve all objects in the bucket.
3. Compares each object's `LastModified` timestamp with the current UTC time.
4. Deletes objects older than the configured retention period.
5. Prints the names of deleted objects.
6. Logs all actions to Amazon CloudWatch Logs.

---

## Step 5 - Test the Lambda Function

Triggered the Lambda function manually.

Verified that:

- Objects older than the configured threshold were deleted.
- Newer objects remained in the bucket.
- Deleted object names were logged successfully.

![Lambda Test Output](screenshots/05-lambda-test.png)

---

## Step 6 - Verify CloudWatch Logs

Verified that CloudWatch Logs displayed:

- Bucket being scanned
- Objects evaluated
- Objects deleted
- Completion status

![CloudWatch Logs](screenshots/06-cloudwatch-logs.png)

---

## Step 7 - Verify Final Bucket Contents

Confirmed that only the newer objects remained in the bucket after the cleanup process.

![Final Bucket](screenshots/07-final-bucket.png)

---

# Sample Output

```text
Scanning bucket: hamid-s3-cleanup

Deleted:
old-file-1.txt
old-file-2.jpg

Cleanup completed successfully.
```