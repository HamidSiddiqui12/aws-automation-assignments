# Automated EBS Snapshot Creation and Cleanup

# Architecture

```
Amazon EventBridge
        │
        ▼
AWS Lambda
        │
        ▼
Amazon EBS Volume
        │
        ▼
Create Snapshot
        │
        ▼
Tag Snapshot
        │
        ▼
Delete Old Snapshots
        │
        ▼
CloudWatch Logs
```

# Implementation Steps

## Step 1: Create an EC2 Instance

A t3.micro Amazon EC2 instance was launched in the **us-east-1** region. AWS automatically created and attached a root EBS volume to the instance.

### Screenshot

![EC2 Instance](screenshots/01-ec2-instance.png)

---

## Step 2: Verify the EBS Volume

The attached root EBS volume was verified from the EC2 console. The Volume ID was noted because it is required by the Lambda function for snapshot creation.

### Screenshot

![EBS Volume](screenshots/02-ebs-volume.png)

---

## Step 3: Create the IAM Role

An IAM role for AWS Lambda was created with **Lambda** as the trusted entity.

### Screenshot

![IAM Role](screenshots/03-iam-role.png)

---

## Step 4: Attach the Inline IAM Policy

A least-privilege inline IAM policy was attached to the Lambda execution role with the following permissions:

- ec2:CreateSnapshot
- ec2:DescribeSnapshots
- ec2:DeleteSnapshot
- ec2:CreateTags

### Screenshot

![IAM Policy](screenshots/04-inline-policy.png)

---

## Step 5: Create the Lambda Function

A Lambda function named **EBS-Snapshot-Cleanup** was created using the Python 3.14 runtime.
The IAM role created in the previous step was assigned as the execution role.

### Screenshot

![Lambda Configuration](screenshots/05-lambda-configuration.png)

---

## Step 6: Upload the Python Code

The Lambda function was implemented using the Boto3 SDK. The code performs the following tasks:

### Screenshot

![Lambda Code](screenshots/06-lambda-code.png)

---

## Step 7: Test the Lambda Function

The Lambda function was manually invoked using the Test feature to verify successful execution.

### Screenshot

![Lambda Test](screenshots/07-test-event.png)

---

## Step 8: Verify Successful Execution

The Lambda function completed successfully and returned a successful execution status.

### Screenshot

![Lambda Success](screenshots/08-test-success.png)

---

## Step 9: Verify CloudWatch Logs

Amazon CloudWatch Logs automatically recorded the Lambda execution. The logs display the created snapshot ID and any deleted snapshot IDs.

### Screenshot

![CloudWatch Logs](screenshots/09-cloudwatch-logs.png)

---

## Step 10: Verify Snapshot Creation

The EC2 Snapshots page was used to verify that the snapshot was created successfully and tagged with **CreatedBy=Lambda-Backup**.

### Screenshot

![Snapshot](screenshots/10-ebs-snapshot.png)

---

## Step 11: Configure Amazon EventBridge

An Amazon EventBridge rule was created to trigger the Lambda function automatically every week.

Schedule Expression:

```text
rate(7 days)
```

### Screenshot

![EventBridge Rule](screenshots/11-eventbridge-rule.png)

---
