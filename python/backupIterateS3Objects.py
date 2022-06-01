#!/usr/local/bin/python3
import boto3
import csv
from datetime import datetime, timedelta


#s3 = boto3.client('s3',
#    aws_access_key_id='KEY_ID',
#    aws_secret_access_key='ACCESS_KEY'
#)
s3 = boto3.client('s3')

response = s3.list_buckets()

# print('Existing S3 buckets')

for bucket in response['Buckets']:
    # print("Iterating through:\n", bucket['Name'],"- Created: ", bucket['CreationDate'],"\n")

    #s3_res = boto3.resource('s3',
    #    aws_access_key_id='KEY_ID',
    #    aws_secret_access_key='ACCESS_KEY'
    #)
    s3_res = boto3.resource('s3')

    s3_bucket = s3_res.Bucket(bucket['Name'])

    print("Iterating through bucket", bucket['Name'])

    csvfile = open('s3buckets.csv', 'a')
    fieldnames = ['filename', 'modification_date']
    csvfile.writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    csvfile.writer.writeheader()

    latest_modified_date = datetime(2019,10,1,0)
    latest_modifed_file = ""
    
    for obj in s3_bucket.objects.all():
        # print("file: ", obj.key, "- last modified: ", obj.last_modified)

        if (datetime.strptime(str(obj.last_modified), '%Y-%m-%d %H:%M:%S+00:00') > latest_modified_date):
            latest_modified_date = datetime.strptime(str(obj.last_modified), '%Y-%m-%d %H:%M:%S+00:00')
            latest_modifed_file = str(obj.key)
            break
            

    print("Last modified file:", latest_modifed_file, "- modified on:", latest_modified_date)
    csvfile.writer.writerow({'filename': str(bucket['Name']), 'modification_date': ''})
    csvfile.writer.writerow({'filename': latest_modifed_file, 'modification_date': str(latest_modified_date)})

csvfile.close()
