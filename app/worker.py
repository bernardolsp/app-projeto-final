import asyncio
import datetime
from botocore.exceptions import ClientError
from fastapi import HTTPException
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

# Initialize S3 client
s3_client = boto3.client('s3')

S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')


async def upload_to_s3_background(name: str, content: str):
    """
    Asynchronous function to upload content to S3.
    """
    if not S3_BUCKET_NAME:
        print(f"Error: S3 bucket name not configured")
        return

    try:
        now = datetime.datetime.now()
        # Use run_in_executor to run the S3 upload in a separate thread
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, lambda: s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=f"{name}-{now}.txt",  # Add a timestamp to the file name
            Body=content,
            ContentType='text/plain'
        ))
        print(f"Successfully uploaded {name} to S3")
    except ClientError as e:
        print(f"Failed to upload to S3: {str(e)}")

async def list_s3_objects():
    """
    Asynchronous function to list objects in the S3 bucket.
    """
    if not S3_BUCKET_NAME:
        raise HTTPException(status_code=500, detail="S3 bucket name not configured")

    try:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, lambda: s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME))

        objects = response.get('Contents', [])
        return [obj['Key'] for obj in objects]
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Failed to list S3 objects: {str(e)}")