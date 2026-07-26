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

![EC2 Instance](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-2-EBS-Snapshot/Snapshots/Screenshot%202026-07-22%20083948.png)

---

## Step 2: Verify the EBS Volume

The attached root EBS volume was verified from the EC2 console. The Volume ID was noted because it is required by the Lambda function for snapshot creation.

### Screenshot

![EBS Volume](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-2-EBS-Snapshot/Snapshots/Screenshot%202026-07-22%20083939.png)

---

## Step 3: Create the IAM Role

An IAM role for AWS Lambda was created with **Lambda** as the trusted entity.

### Screenshot

![IAM Role](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-2-EBS-Snapshot/Snapshots/Screenshot%202026-07-22%20081334.png)

---

## Step 4: Attach the Inline IAM Policy

A least-privilege inline IAM policy was attached to the Lambda execution role with the following permissions:

- ec2:CreateSnapshot
- ec2:DescribeSnapshots
- ec2:DeleteSnapshot
- ec2:CreateTags

### Screenshot

![IAM Policy](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-2-EBS-Snapshot/Snapshots/Screenshot%202026-07-22%20083857.png)
![IAM Policy](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-2-EBS-Snapshot/Snapshots/Screenshot%202026-07-22%20084851.png)

---

## Step 5: Create the Lambda Function

A Lambda function named **EBS-Snapshot-Cleanup** was created using the Python 3.14 runtime.
The IAM role created in the previous step was assigned as the execution role.

### Screenshot

![Lambda Configuration](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-2-EBS-Snapshot/Snapshots/Screenshot%202026-07-22%20082507.png)

---

### Screenshot

![Lambda Code](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-2-EBS-Snapshot/Snapshots/Screenshot%202026-07-22%20083051.png)

---

## Step 6: Test the Lambda Function

The Lambda function was manually invoked using the Test feature to verify successful execution.

### Screenshot

![Lambda Test](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-2-EBS-Snapshot/Snapshots/Screenshot%202026-07-22%20082730.png)

---

## Step 7: Verify Successful Execution

The Lambda function completed successfully and returned a successful execution status.

### Screenshot

![Lambda Success](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-2-EBS-Snapshot/Snapshots/Screenshot%202026-07-22%20083051.png)
![Lambda Success](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-2-EBS-Snapshot/Snapshots/Screenshot%202026-07-22%20085133.png)
![Lambda Success](screenshots/08-test-success.png)

---

## Step 8: Verify CloudWatch Logs

Amazon CloudWatch Logs automatically recorded the Lambda execution. The logs display the created snapshot ID and any deleted snapshot IDs.

### Screenshot

![CloudWatch Logs](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-2-EBS-Snapshot/Snapshots/Screenshot%202026-07-22%20085247.png)

---

## Step 9: Verify Snapshot Creation

The EC2 Snapshots page was used to verify that the snapshot was created successfully and tagged with **CreatedBy=Lambda-Backup**.

### Screenshot

![Snapshot](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-2-EBS-Snapshot/Snapshots/Screenshot%202026-07-22%20083150.png)
![Snapshot](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-2-EBS-Snapshot/Snapshots/Screenshot%202026-07-22%20082519.png)


---

## Step 10: Configure Amazon EventBridge

An Amazon EventBridge rule was created to trigger the Lambda function automatically every week.

Schedule Expression:

```text
rate(7 days)
```

### Screenshot

![EventBridge Rule](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-2-EBS-Snapshot/Snapshots/Screenshot%202026-07-22%20083558.png)

---
