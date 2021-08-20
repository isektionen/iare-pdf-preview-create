import boto3
import logging
from botocore.config import Config
from os import getenv, path

from botocore.exceptions import ClientError


def upload(objectname):
    client = boto3.client(
        "s3",
        aws_access_key_id=getenv("ACCESS_KEY"),
        aws_secret_access_key=getenv("SECRET_KEY"),
        region_name=getenv("REGION"),
    )
    bucket = getenv("BUCKET_NAME")
    try:
        print("Attempting to upload:", objectname, path.basename(objectname))
        response = client.upload_file(objectname, bucket, path.basename(objectname))
        print("upload response:", response)
        return True
    except ClientError as e:
        print(e)
        return False


def url(objectname):
    return f"https://{getenv('BUCKET_NAME')}.{getenv('REGION')}.amazonaws.com/{objectname}"