import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client("s3")

BUCKET_NAME = "hamid-s3-cleanup"

DAYS_TO_KEEP = 30


def lambda_handler(event, context):

    paginator = s3.get_paginator("list_objects_v2")

    pages = paginator.paginate(Bucket=BUCKET_NAME)

    current_time = datetime.now(timezone.utc)

    deleted_files = []

    for page in pages:

        if "Contents" not in page:
            continue

        for obj in page["Contents"]:

            file_name = obj["Key"]

            last_modified = obj["LastModified"]

            file_age = current_time - last_modified

            # Change to days=DAYS_TO_KEEP before final submission
            if file_age > timedelta(minutes=1):

                s3.delete_object(
                    Bucket=BUCKET_NAME,
                    Key=file_name
                )

                deleted_files.append(file_name)

                print(f"Deleted: {file_name}")

    print(f"Total files deleted: {len(deleted_files)}")

    return {
        "statusCode": 200,
        "body": {
            "deleted_files": deleted_files,
            "count": len(deleted_files)
        }
    }