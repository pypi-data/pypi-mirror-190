__all__ = ["s3"]

import boto3.session
from de_pytools.aws import *

def session(profile_name='default', region_name='us-east-1'):
    return boto3.session.Session(profile_name, region_name)
