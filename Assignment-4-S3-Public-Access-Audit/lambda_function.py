import boto3
from botocore.exceptions import ClientError

# Create AWS clients
s3 = boto3.client("s3")
sns = boto3.client("sns")

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:097466312208:BucketAuditAlerts"


def lambda_handler(event, context):
    public_buckets = []

    # Get all S3 buckets
    response = s3.list_buckets()

    for bucket in response["Buckets"]:
        bucket_name = bucket["Name"]

        print(f"Checking bucket: {bucket_name}")

        block_public = False
        policy_public = False
        acl_public = False

        # Check Public Access
        try:
            bpa = s3.get_public_access_block(Bucket=bucket_name)

            config = bpa["PublicAccessBlockConfiguration"]

            if not all(config.values()):
                block_public = True

        except ClientError as e:
            error_code = e.response["Error"]["Code"]

            # If configuration doesn't exist
            if error_code == "NoSuchPublicAccessBlockConfiguration":
                block_public = True
            else:
                print(f"Error checking Block Public Access for {bucket_name}: {e}")

        # Check Bucket Policy Status
        try:
            policy = s3.get_bucket_policy_status(Bucket=bucket_name)

            if policy["PolicyStatus"]["IsPublic"]:
                policy_public = True

        except ClientError as e:
            print(f"No public bucket policy for {bucket_name}")

        # Check Bucket ACL
        try:
            acl = s3.get_bucket_acl(Bucket=bucket_name)

            for grant in acl["Grants"]:
                grantee = grant.get("Grantee", {})

                if (
                    grantee.get("Type") == "Group"
                    and "AllUsers" in grantee.get("URI", "")
                ):
                    acl_public = True

        except ClientError as e:
            print(f"Unable to read ACL for {bucket_name}: {e}")

        if block_public or policy_public or acl_public:

            public_buckets.append(bucket_name)

            print(f"Public bucket found: {bucket_name}")

    # Send SNS notification if any public buckets exist
    if public_buckets:

        message = (
            "The following S3 bucket(s) may be publicly accessible:\n\n"
            + "\n".join(public_buckets)
        )

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="S3 Public Bucket Alert",
            Message=message,
        )

        print("SNS notification sent.")

    else:
        print("No public buckets found.")

    return {
        "statusCode": 200,
        "body": {
            "public_buckets": public_buckets
        }
    }