import logging
import os
import pandas as pd
import pickle
import uuid
import boto3.session

from cryptography.fernet import Fernet
from io import BytesIO


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@staticmethod
def list_files(session: boto3.session, s3_bucket: str, s3_key: str = ""):

    try:
        s3 = session.resource('s3')
        s3_bucket = s3.Bucket(s3_bucket)

        for obj in s3_bucket.objects.all():
            logger.info(obj.key)
    except Exception as e:
        logger.error(e)

@staticmethod
def upload_file(session: boto3.session, s3_bucket: str, s3_key: str, source_file: str,
                encryption=False, encryption_key=None):
    """
    Specifying S3 path:
    Example: s3://BucketName/Project/WordFiles/123.txt
        bucket = "BucketName"
        prefix = “BucketName/Project/WordFiles/”
        key = "Project/WordFiles/123.txt"
    Example: s3://BucketName/123.txt
        bucket = "BucketName"
        prefix = “BucketName/”
        key = "123.txt"
    """

    if encryption:
        fk = Fernet(encryption_key)

        with open(source_file, "rb") as file:
            # read all file data
            file_data = file.read()

        # encrypt data
        encrypted_data = fk.encrypt(file_data)

        # close file
        file.close()

        # name the encrypted file
        x, y = os.path.splitext(source_file)
        upload_file = '{0}-{1}{2}'.format(x, 'encrypted', y)

        # write the encrypted file
        with open(upload_file, "wb") as file:
            file.write(encrypted_data)

        file.close()

    else:
        upload_file = source_file

    # Upload the file to S3
    s3_hook.load_file(filename=upload_file, key=s3_key, bucket_name=s3_bucket, replace=True, encrypt=False)

if __name__=='__main__':
    print(10)
    session = boto3.session.Session(profile_name='default', region_name='us-east-1')
    list_files(session, 'pam-airflow-qa-staging')
    # upload_file(session, 'pam-airflow-qa-staging', 'test_dir')