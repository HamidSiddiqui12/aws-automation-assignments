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

![SNS Topic](screenshots/01-sns-topic.png)

---

## Step 2 - Subscribe an Email Address

Subscribed an email address to the SNS topic and confirmed the subscription through the confirmation email sent by AWS.

Without confirming the subscription, SNS cannot send notifications.

![Email Subscription](screenshots/02-email-subscription.png)

---

## Step 3 - Create the IAM Role

Created an IAM Role for AWS Lambda.

Attached the managed policy:

- AWSLambdaBasicExecutionRole

Created an inline least-privilege policy allowing:

- s3:ListAllMyBuckets
- s3:GetBucketPublicAccessBlock
- s3:GetBucketPolicyStatus
- s3:GetBucketAcl
- sns:Publish

![IAM Role](screenshots/03-iam-role.png)

![Inline IAM Policy](screenshots/04-inline-policy.png)

---

## Step 4 - Create the Lambda Function

Created a Lambda function using:

- Runtime: Python 3.12
- Architecture: x86_64
- Execution Role: S3-Public-Audit-Lambda-Role

The Lambda function audits every S3 bucket in the account.

![Lambda Configuration](screenshots/05-lambda-configuration.png)

---

## Step 5 - Deploy the Python Code

The Lambda function performs the following actions:

1. Lists every S3 bucket.
2. Checks Block Public Access configuration.
3. Checks Bucket Policy Status.
4. Checks Bucket ACL.
5. Identifies publicly accessible buckets.
6. Sends an SNS email notification if any bucket is public.
7. Logs all actions to CloudWatch Logs.

---

## Step 6 - Test the Lambda Function

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

![Lambda Test Output](screenshots/06-lambda-test.png)

![Public Bucket Policy](screenshots/08-public-bucket-policy.png)

![SNS Email Alert](screenshots/09-sns-email.png)

---

## Step 7 - Verify CloudWatch Logs

Verified that CloudWatch Logs recorded:

- Bucket names being checked.
- Public bucket detection.
- SNS notification sent successfully.

![CloudWatch Logs](screenshots/07-cloudwatch-logs.png)