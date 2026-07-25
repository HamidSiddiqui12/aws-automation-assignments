import boto3
from datetime import datetime

# Create EC2 client
ec2 = boto3.client("ec2")

def lambda_handler(event, context):

    # Get EC2 Instance ID from EventBridge event
    instance_id = event["detail"]["instance-id"]

    # Get today's date
    launch_date = datetime.now().strftime("%Y-%m-%d")

    # Add tags to the EC2 instance
    ec2.create_tags(
        Resources=[instance_id],
        Tags=[
            {
                "Key": "LaunchDate",
                "Value": launch_date
            },
            {
                "Key": "Environment",
                "Value": "Development"
            }
        ]
    )

    print(f"Successfully tagged instance: {instance_id}")

    return {
        "statusCode": 200,
        "body": f"Tags added successfully to {instance_id}"
    }