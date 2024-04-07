import io
import os
import boto3


from botocore.exceptions import ClientError
from fastapi import HTTPException
from fastapi import status as http_status

from app import S3_BUCKET_NAME


def s3():
    return boto3.resource('s3',
                          endpoint_url=os.environ.get('S3_ENDPOINT_URL', None),
                          aws_access_key_id=os.environ['S3_ACCESS_KEY_ID'],
                          aws_secret_access_key=os.environ['S3_SECRET_ACCESS_KEY_ID']
                          )


async def upload_to_s3(file: bytes, key: str):
    try:
        s3().meta.client.upload_fileobj(Fileobj=io.BytesIO(file), Bucket=S3_BUCKET_NAME, Key=key)
    except Exception:
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="File could not be uploaded")


async def get_from_s3(key: str):
    try:
        obj = s3().Object(S3_BUCKET_NAME, key)
        file = obj.get()['Body'].read()
        return file
    except ClientError as ex:
        if ex.response['Error']['Code'] == 'NoSuchKey':
            # TODO: add logging
            return b''
        else:
            raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="File could not be obtained")
    except Exception:
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="File could not be obtained")


async def delete_from_bucket(key: str):
    try:
        s3().meta.client.delete_object(Bucket=S3_BUCKET_NAME, Key=key)
    except Exception:
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail="File could not be deleted")
