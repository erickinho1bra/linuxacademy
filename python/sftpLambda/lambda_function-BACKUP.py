import json
import _cffi_backend
import paramiko
import os
import fnmatch
import shutil
import boto3
import botocore
from botocore.exceptions import NoCredentialsError

ftpHost = "tp.s6.exacttarget.com"
ftpUsername = "6419404"
myPassword = "nelle@20170828"

s3Bucket = os.environ['s3Bucket']


def upload_to_aws(local_file, bucket, key):
    s3 = boto3.resource('s3')
    try:
        s3.Object(bucket, key).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            # The object does not exist.
            print("File does not exist in bucket, will upload file: " + local_file)
            try:
                s3 = boto3.client('s3')
                s3.put_object(Body=local_file, Bucket=bucket, Key=key)
                print("Successful upload of file: " + local_file)
                return True
            except FileNotFoundError:
                print("The file was not found")
                return False
            except NoCredentialsError:
                print("Credentials not available")
                return False
        else:
            # Something else has gone wrong.
            raise
    else:
        # The object does exist.
            print("File already exists in bucket, skipping file: " + local_file)
    

def create_sftp_client(host, port, username, password):

    sftp = None
    transport = None
    try:
        transport = paramiko.Transport((host, port))
        transport.connect(None, username, password)

        sftp = paramiko.SFTPClient.from_transport(transport)

        return sftp
    except Exception as e:
        print('An error occurred creating SFTP client: %s: %s' % (e.__class__, e))
        if sftp is not None:
            sftp.close()
        if transport is not None:
            transport.close()
        pass



def lambda_handler(event, context):
    host = 'ftp.s6.exacttarget.com'
    port = 22
    username = '6419404'
    password = 'nelle@20170828'
    #s3Bucket = "ellentube-prod-sfmc-data"

    sftpclient = create_sftp_client(host, port, username, password)

    sftpclient.chdir('/Import')
    dirlistRemote = sftpclient.listdir('.')
    for file in sorted(dirlistRemote):
        if fnmatch.fnmatch(file, '*.csv'):
            if fnmatch.fnmatch(file, '*Game*.csv'):
                print("Not downloading: " + file)
            else:
                print("Downloading:" + file)

                local_path = "/tmp/" + file
                
                sftpclient.get(file, local_path, None)

    sftpclient.close()


    os.chdir('/tmp')
    dirlistLocal = os.listdir('.')

    # Upload files in  local directory to the s3 bucket 
    for file in sorted(dirlistLocal):
        # For Giveaway.csv files
        if fnmatch.fnmatch(file, 'Giveaways*.csv'):
            objectKey = "giveaways/" + file
            upload_to_aws(file, s3Bucket, objectKey)
            # Below is only necessary on your local computer not on Lambda
            #os.remove(file)
            #print("Deleted file from directory:" + file)
        # For NewSubscriber.csv files
        if fnmatch.fnmatch(file, 'NewSubscribers*.csv'):
            objectKey = "newsletters/" + file
            upload_to_aws(file, s3Bucket, objectKey)
            # Below is only necessary on your local computer not on Lambda
            #os.remove(file)
            #print("Deleted file from directory:" + file)
        # For EllenCampaignsNewsletter.csv files
        if fnmatch.fnmatch(file, 'EllenCampaignsNewsletter*.csv'):
            objectKey = "campaign-newsletters/" + file
            upload_to_aws(file, s3Bucket, objectKey)
            # Below is only necessary on your local computer not on Lambda
            #os.remove(file)
            #print("Deleted file from directory:" + file)

