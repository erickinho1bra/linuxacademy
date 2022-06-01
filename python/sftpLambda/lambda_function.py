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

#s3Bucket = "xelima-test-bucket"
s3Bucket = os.environ['s3Bucket']


def checkIfFileInBucket(bucket, key, file, sftpclient):
    # check if file is in S3 bucket
    s3 = boto3.resource('s3')
    try:
        # command that tries to check for object existence in bucket
        s3.Object(bucket, key).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            # The object does not exist in the bucket.
            print("File does not exist in bucket, downloading file: " + file)
            # change directory to /tmp/ since Lambda has Read-only file system
            local_path = "/tmp/" + file
            # command to download file from SFTP server

            sftpclient.get(file, local_path, None)
    else:
        # The object does exist.
        print("File already exists in bucket, you SHOULD NOT download file: " + file)


# Use getDirListRemote() to get a list of remote files to see if they are in the S3 bucket
def downloadFilesNotInBucket():
    host = 'ftp.s6.exacttarget.com'
    port = 22
    username = '6419404'
    password = 'nelle@20170828'

    # Create SFTP connection
    sftpclient = create_sftp_client(host, port, username, password)

    # Get a list of the files that are on th SFTP server
    sftpclient.chdir('/Import')
    dirlistRemote = sftpclient.listdir('.')

    for file in sorted(dirlistRemote):
            # We only want files ending in .csv
            if fnmatch.fnmatch(file, '*.csv'):
                if fnmatch.fnmatch(file, '*Game*.csv'):
                    print("Not downloading: " + file)
                else:
                    # Look for Giveaways.csv files
                    if fnmatch.fnmatch(file, 'Giveaways*.csv'):
                        objectKey = "giveaways/" + file
                        checkIfFileInBucket(s3Bucket, objectKey, file, sftpclient)
                        # Below is only necessary on your local computer not on Lambda
                        #os.remove(file)
                        #print("Deleted file from directory:" + file)
                    # Look for NewSubscriber.csv files
                    if fnmatch.fnmatch(file, 'NewSubscribers*.csv'):
                        objectKey = "newsletters/" + file
                        checkIfFileInBucket(s3Bucket, objectKey, file, sftpclient)
                        # Below is only necessary on your local computer not on Lambda
                        #os.remove(file)
                        #print("Deleted file from directory:" + file)
                    # Look for EllenCampaignsNewsletter.csv files
                    if fnmatch.fnmatch(file, 'EllenCampaignsNewsletter*.csv'):
                        objectKey = "campaign-newsletters/" + file
                        checkIfFileInBucket(s3Bucket, objectKey, file, sftpclient)
                        # Below is only necessary on your local computer not on Lambda
                        #os.remove(file)
                        #print("Deleted file from directory:" + file)
    # close SFTP connection
    sftpclient.close()



# Upload the .csv files to the S3 bucket
def upload_to_aws(local_file, bucket, key):

    s3 = boto3.resource('s3')
    try:
        s3.Object(bucket, key).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            # The object does not exist.
            print("File does not exist in bucket, will upload file: " + local_file)

            try:
                s3C = boto3.client('s3')    
                s3C.upload_file(local_file, bucket, key)
                print("Upload Successful")
                return True
            except FileNotFoundError:
                print("The file was not found")
                return False
            except NoCredentialsError:
                print("Credentials not available")
                return False

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

    downloadFilesNotInBucket()

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

