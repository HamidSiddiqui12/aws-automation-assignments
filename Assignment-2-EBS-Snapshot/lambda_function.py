import boto3
from datetime import datetime, timezone, timedelta

# Create EC2 client
ec2 = boto3.client("ec2")

# Replace with your EBS Volume ID
VOLUME_ID = "vol-0c52bdf84e1a6ce6c"

# Keep snapshots for 30 days
RETENTION_DAYS = 30


def lambda_handler(event, context):

    # Create snapshot
    response = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description="Automated Lambda Backup"
    )

    snapshot_id = response["SnapshotId"]

    print(f"Created Snapshot: {snapshot_id}")

    # Tag snapshot
    ec2.create_tags(
        Resources=[snapshot_id],
        Tags=[
            {
                "Key": "CreatedBy",
                "Value": "Lambda-Backup"
            }
        ]
    )

    print("Tag added successfully")

    # Get all snapshots created by Lambda
    snapshots = ec2.describe_snapshots(
        OwnerIds=["self"],
        Filters=[
            {
                "Name": "tag:CreatedBy",
                "Values": ["Lambda-Backup"]
            }
        ]
    )["Snapshots"]

    now = datetime.now(timezone.utc)

    # Delete old snapshots
    for snapshot in snapshots:

        age = now - snapshot["StartTime"]

        if age > timedelta(days=RETENTION_DAYS):  #Here we can use minutes=5-any for testing purpose.

            ec2.delete_snapshot(
                SnapshotId=snapshot["SnapshotId"]
            )

            print(f"Deleted Snapshot: {snapshot['SnapshotId']}")

    return {
        "statusCode": 200,
        "body": "Snapshot creation and cleanup completed."
    }