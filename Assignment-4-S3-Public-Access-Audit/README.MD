# Assignment 4 - Audit S3 Buckets for Public Access and Notify

# Architecture

```text
                    Amazon EventBridge
                           │
                           │
                           ▼
                  AWS Lambda Function
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
 List S3 Buckets   Check Block Public   Check Bucket
                   Access Settings      Policy & ACL
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼
              Any Public Bucket Found?
                    │              │
                  YES              NO
                    │              │
                    ▼              ▼
             Amazon SNS        End Function
                    │
                    ▼
             Email Notification
```

# Project Structure

```text
Assignment-4-S3-Public-Access-Audit
│
├── lambda_function.py
├── README.md
└── screenshots
    ├── 01-sns-topic.png
    ├── 02-email-subscription.png
    ├── 03-iam-role.png
    ├── 04-inline-policy.png
    ├── 05-lambda-configuration.png
    ├── 06-lambda-test.png
    ├── 07-cloudwatch-logs.png
    ├── 08-public-bucket-policy.png
    └── 09-sns-email.png
```

---

# Implementation Steps

## Step 1 - Create an SNS Topic

Created an Amazon SNS Standard Topic named **BucketAuditAlerts**.

The SNS topic is responsible for sending email notifications whenever the Lambda function detects a public S3 bucket.

![SNS Topic](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-4-S3-Public-Access-Audit/Snapshots/Screenshot%202026-07-25%20224832.png)
![SNS Topic](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-4-S3-Public-Access-Audit/Snapshots/Screenshot%202026-07-25%20225247.png)

---

## Step 2 - Create the IAM Role

Created an IAM Role for AWS Lambda.

Attached the managed policy:

- AWSLambdaBasicExecutionRole

Created an inline least-privilege policy allowing:

- s3:ListAllMyBuckets
- s3:GetBucketPublicAccessBlock
- s3:GetBucketPolicyStatus
- s3:GetBucketAcl
- sns:Publish

![IAM Role](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-4-S3-Public-Access-Audit/Snapshots/Screenshot%202026-07-25%20225550.png)

![Inline IAM Policy](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-4-S3-Public-Access-Audit/Snapshots/Screenshot%202026-07-25%20232042.png)

---

## Step 3 - Create the Lambda Function

Created a Lambda function using:

- Runtime: Python 3.12
- Architecture: x86_64
- Execution Role: S3-Public-Audit-Lambda-Role

The Lambda function audits every S3 bucket in the account.

![Lambda Configuration](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-4-S3-Public-Access-Audit/Snapshots/Screenshot%202026-07-26%20180524.png)

---

## Step 4 - Deploy the Python Code

The Lambda function performs the following actions:

1. Lists every S3 bucket.
2. Checks Block Public Access configuration.
3. Checks Bucket Policy Status.
4. Checks Bucket ACL.
5. Identifies publicly accessible buckets.
6. Sends an SNS email notification if any bucket is public.
7. Logs all actions to CloudWatch Logs.

---

## Step 5 - Test the Lambda Function

Initially, all buckets were private.

The Lambda function returned:

- No public buckets detected.

For testing purposes:

- Created a temporary bucket.
- Disabled Block Public Access.
- Added a public-read bucket policy.

After running the Lambda again:

- The public bucket was detected.
- An SNS email notification was successfully delivered.

![Lambda Test Output](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-4-S3-Public-Access-Audit/Snapshots/Screenshot%202026-07-25%20230604.png)

![Public Bucket Policy](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-4-S3-Public-Access-Audit/Snapshots/Screenshot%202026-07-25%20231244.png)

![SNS Email Alert](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-4-S3-Public-Access-Audit/Snapshots/Screenshot%202026-07-25%20232310.png)

==========

##Invoke Status after deploying code

![Test Code](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-4-S3-Public-Access-Audit/Snapshots/Screenshot%202026-07-25%20231436.png)

![Test Code](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-4-S3-Public-Access-Audit/Snapshots/Screenshot%202026-07-25%20231900.png)

---

## Step 6 - Verify CloudWatch Logs

Verified that CloudWatch Logs recorded:

- Bucket names being checked.
- Public bucket detection.
- SNS notification sent successfully.

![CloudWatch Logs](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-4-S3-Public-Access-Audit/Snapshots/Screenshot%202026-07-25%20232146.png)
====
![CloudWatch Logs](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-4-S3-Public-Access-Audit/Snapshots/Screenshot%202026-07-25%20232208.png)
====
![CloudWatch Logs](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-4-S3-Public-Access-Audit/Snapshots/Screenshot%202026-07-
25%20232226.png)
====
![CloudWatch Logs](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-4-S3-Public-Access-Audit/Snapshots/Screenshot%202026-07-25%20232235.png)
