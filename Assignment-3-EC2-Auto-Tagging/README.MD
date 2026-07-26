# Auto-Tagging EC2 Instances on Launch

# Architecture

```text
EC2 Instance Launch
        │
        ▼
EC2 Instance enters Running state
        │
        ▼
Amazon EventBridge
        │
        ▼
AWS Lambda
        │
        ▼
Apply Tags
        │
        ▼
Amazon EC2
        │
        ▼
CloudWatch Logs
```

# Implementation Steps

## Step 1 – Create the IAM Role

Created an IAM role for AWS Lambda using **Lambda** as the trusted entity.

### Screenshot

![IAM Role](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-3-EC2-Auto-Tagging/Snapshots/Screenshot%202026-07-23%20090107.png)

---

## Step 2 – Attach IAM Permissions

Created a least-privilege inline IAM policy with the following permissions:

- ec2:CreateTags
- ec2:DescribeInstances

Also attached the AWS managed policy:

- AWSLambdaBasicExecutionRole

### Screenshot

![Inline Policy](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-3-EC2-Auto-Tagging/Snapshots/Screenshot%202026-07-23%20090139.png)

![Inline Policy](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-3-EC2-Auto-Tagging/Snapshots/Screenshot%202026-07-23%20090209.png)

![Inline Policy](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-3-EC2-Auto-Tagging/Snapshots/Screenshot%202026-07-23%20090321.png)

---

## Step 3 – Create the Lambda Function

Created a Lambda function named **EC2-Auto-Tagging** using the Python 3.12 runtime and assigned the IAM execution role.

### Screenshot

![Lambda Configuration](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-3-EC2-Auto-Tagging/Snapshots/Screenshot%202026-07-23%20090744.png)

![Lambda Configuration](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-3-EC2-Auto-Tagging/Snapshots/Screenshot%202026-07-23%20091651.png)


## Step 4 – Configure the EventBridge Rule

Created an EventBridge rule to listen for EC2 instance state-change events.

## Step 5 – Configure the Event Pattern

Configured the event pattern with the following settings:

- AWS Service: EC2
- Event Type: EC2 Instance State-change Notification
- State: Running
- Instance: Any instance

### Screenshot

![EventBridge Rule](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-3-EC2-Auto-Tagging/Snapshots/Screenshot%202026-07-23%20091659.png)

---

## Step 6 – Launch a Test EC2 Instance

Launched a t3.micro EC2 instance named **AutoTag-Test** to verify the automation.

### Screenshot

![EC2 Instance](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-3-EC2-Auto-Tagging/Snapshots/Screenshot%202026-07-23%20092002.png)

---

## Step 7 – Verify Automatic Tagging

After the EC2 instance entered the **Running** state, EventBridge automatically triggered the Lambda function, which added the following tags:

- LaunchDate
- Environment = Development

### Screenshot

![Tags Added](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-3-EC2-Auto-Tagging/Snapshots/Screenshot%202026-07-23%20092014.png)

---

## Step 8 – Verify CloudWatch Logs

Verified successful Lambda execution in Amazon CloudWatch Logs. The logs confirm that the instance was tagged successfully.

### Screenshot

![CloudWatch Logs](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-3-EC2-Auto-Tagging/Snapshots/Screenshot%202026-07-23%20092526.png)

---

## Step 9 – Final Result

Confirmed that the EC2 instance was automatically tagged without manual intervention.

### Screenshot

![Final Result](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-3-EC2-Auto-Tagging/Snapshots/Screenshot%202026-07-23%20093205.png)
![Final Result](https://github.com/HamidSiddiqui12/aws-automation-assignments/blob/main/Assignment-3-EC2-Auto-Tagging/Snapshots/Screenshot%202026-07-23%20093216.png)
