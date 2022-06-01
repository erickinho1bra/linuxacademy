#!/usr/bin/env python3
# Creating file that can be called from other scripts to pull AWS credentials
#import getpass, boto3
#from appscript import *

from getAwsCredentials import *
import argparse


# Create the parser
try:
  parser = argparse.ArgumentParser()
  parser.add_argument('--local-aws-account-name', '-a', help='AWS account in which the S3 bucket lives', type=str)
  parser.add_argument('--s3-bucket', '-b' , help='The s3 bucket name', type=str)
  parser.add_argument('--s3-bucket-prefix', '-p' , help='The prefix to filter through in the s3 bucket (e.g. "new-logs/")', type=str)
  input_arg = parser.parse_args()
except Exception as e:
  print("Did not get the correct arguments to run script. Need parameters '--local-aws-account-name <LOCAL_AWS_ACCOUNT_NAME>' AND '--s3-bucket <BUCKET_NAME>' ")
  raise e


# Get user credentials using the getCreds.py file in this directory
try:
  credsDict = getCreds(input_arg.local_aws_account_name)
  session = boto3.Session(
  aws_access_key_id=credsDict['aws_access_key_id'],
  aws_secret_access_key=credsDict['aws_secret_access_key'],
  aws_session_token=credsDict['aws_session_token']
  )
  s3 = session.resource('s3')
  my_bucket = s3.Bucket(input_arg.s3_bucket)
except Exception as e:
  print("Could not get user credentials and start boto3 session")
  raise e

s3Objects = []
try:
  for objects in my_bucket.objects.filter(Prefix=input_arg.s3_bucket_prefix):
    print(objects)
except Exception as e:
  print("Could not interate through S3 bucket.")
  raise e 
