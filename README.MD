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

---

# AWS Services Used

- Amazon EC2
- AWS Lambda
- Amazon EventBridge
- AWS IAM
- Amazon CloudWatch Logs
- Boto3 (AWS SDK for Python)

# Implementation Steps

## Step 1 – Create the IAM Role

Created an IAM role for AWS Lambda using **Lambda** as the trusted entity.

### Screenshot

![IAM Role](screenshots/01-iam-role.png)

---

## Step 2 – Attach IAM Permissions

Created a least-privilege inline IAM policy with the following permissions:

- ec2:CreateTags
- ec2:DescribeInstances

Also attached the AWS managed policy:

- AWSLambdaBasicExecutionRole

### Screenshot

![Inline Policy](screenshots/02-inline-policy.png)

---

## Step 3 – Create the Lambda Function

Created a Lambda function named **EC2-Auto-Tagging** using the Python 3.12 runtime and assigned the IAM execution role.

### Screenshot

![Lambda Configuration](screenshots/03-lambda-configuration.png)

---

## Step 4 – Upload the Python Code

Implemented the Lambda function using the Boto3 SDK to:

- Read the EC2 instance ID from the EventBridge event.
- Generate the current date.
- Add the `LaunchDate` tag.
- Add the `Environment=Development` tag.
- Print a success message to CloudWatch Logs.

### Screenshot

![Lambda Code](screenshots/04-lambda-code.png)

---

## Step 5 – Configure the EventBridge Rule

Created an EventBridge rule to listen for EC2 instance state-change events.

### Screenshot

![EventBridge Rule](screenshots/05-eventbridge-rule.png)

---

## Step 6 – Configure the Event Pattern

Configured the event pattern with the following settings:

- AWS Service: EC2
- Event Type: EC2 Instance State-change Notification
- State: Running
- Instance: Any instance

### Screenshot

![Event Pattern](screenshots/06-event-pattern.png)

---

## Step 7 – Launch a Test EC2 Instance

Launched a t3.micro EC2 instance named **AutoTag-Test** to verify the automation.

### Screenshot

![EC2 Instance](screenshots/07-ec2-launch.png)

---

## Step 8 – Verify Automatic Tagging

After the EC2 instance entered the **Running** state, EventBridge automatically triggered the Lambda function, which added the following tags:

- LaunchDate
- Environment = Development

### Screenshot

![Tags Added](screenshots/08-tags-added.png)

---

## Step 9 – Verify CloudWatch Logs

Verified successful Lambda execution in Amazon CloudWatch Logs. The logs confirm that the instance was tagged successfully.

### Screenshot

![CloudWatch Logs](screenshots/09-cloudwatch-logs.png)

---

## Step 10 – Final Result

Confirmed that the EC2 instance was automatically tagged without manual intervention.

### Screenshot

![Final Result](screenshots/10-final-result.png)
