#!/usr/bin/env python3
#### DISCLAIMER ####
# This script works for Cloudfront logs in S3 but I have not checked with other types of logs. I presume it would not work since my script looks for specific lines in the Cloudfront logs that I don't believe appear in ALB logs, for example.

#### Information About Script ####
# This file is to be used to query S3 logs using boto3 to pull s3 logs and then pandasql to make a local database from the logs it pulls
# You must have an AWS session active with a token using okta. You can use aws-gimme-creds for this. I, Erick Lima, use the following command:
## gimme-aws-creds --profile aws-dope-commerce:aws-dope-commerce-devops
### But you may have a different profile set up already. Use whichever one is appropriate and has the sufficient permissions to read s3 logs and possible use KMS when pulling encrypted objects from S3
#
#### How to Run It ####
# Example command to run this script:
## ./checkS3LogsErrorsWithDatabase.py -a aws-dope-commerce:aws-dope-commerce-devops -b dc-shop-prod-cloudfront-logs -p new-logs/ 
### -a is the local AWS profile that I have set up with aws-gimmme-creds (see above)
#### -b is the bucket name that contains your Cloudfront Logs
##### -p is the prefix in S3 that contains your logs. If there is no prefix and the logs are in the root of the bucket then don't include this argument

# Used to parse arguments, authenticate to AWS, and process data

from getAwsCredentials import *
from sys import stdout
import argparse, json, gzip
# For the database
from operator import itemgetter
import pandas as pd
import pandasql as ps

###################################
############ Variables ############
###################################
logHeadersList = ['date', 'time', 'x-edge-location', 'sc-bytes', 'c-ip', 'cs-method', 'cs(Host)', 'cs-uri-stem', 'sc-status', 'cs(Referer)', 'cs(User-Agent)', 'cs-uri-query', 'cs(Cookie)', 'x-edge-result-type', 'x-edge-request-id', 'x-host-header', 'cs-protocol', 'cs-bytes', 'time-taken', 'x-forwarded-for', 'ssl-protocol', 'ssl-cipher', 'x-edge-response-result-type', 'cs-protocol-version', 'fle-status', 'fle-encrypted-fields', 'c-port', 'time-to-first-byte', 'x-edge-detailed-result-type', 'sc-content-type', 'sc-content-len', 'sc-range-start', 'sc-range-end']
databaseTableColumns = list(itemgetter(0, 1, 4, 5, 7, 8, 9)(logHeadersList))
bigLogList = []

#################################
############ Classes ############
#################################
# Class used to print out color coded errors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
## Uncomment the bottom lines to know what these color codes look like
#print(bcolors.HEADER + "This is bcolors.HEADER" + bcolors.ENDC)
#print(bcolors.OKBLUE + "This is bcolors.OKBLUE" + bcolors.ENDC)
#print(bcolors.OKCYAN + "This is bcolors.OKCYAN" + bcolors.ENDC)
#print(bcolors.OKGREEN + "This is bcolors.OKGREEN" + bcolors.ENDC)
#print(bcolors.WARNING + "This is bcolors.WARNING" + bcolors.ENDC)
#print(bcolors.FAIL + "This is bcolors.FAIL" + bcolors.ENDC)
#print(bcolors.BOLD + "This is bcolors.BOLD" + bcolors.ENDC)
#print(bcolors.UNDERLINE + "This is bcolors.UNDERLINE" + bcolors.ENDC)


########################################################################################
####################################### The Code #######################################
########################################################################################

###########################################
############ Create the parser ############
###########################################
try:
  parser = argparse.ArgumentParser()
  parser.add_argument('--local-aws-account-name', '-a', help='AWS account in which the S3 bucket lives', type=str)
  parser.add_argument('--s3-bucket', '-b' , help='The s3 bucket name', type=str)
  parser.add_argument('--s3-bucket-prefix', '-p' , help='The prefix to filter through in the s3 bucket (e.g. "new-logs/")', type=str)
  input_arg = parser.parse_args()
except Exception as e:
  print("Did not get the correct arguments to run script. Need parameters '--local-aws-account-name <LOCAL_AWS_ACCOUNT_NAME>' AND '--s3-bucket <BUCKET_NAME>' ")
  raise e

#############################################
############ Authenticate to AWS ############
#############################################
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
  print("Sucessfully pulled the credentials for " + bcolors.OKCYAN + input_arg.local_aws_account_name + bcolors.ENDC)
except Exception as e:
  print("Could not get user credentials and start boto3 session")
  raise e

#################################################
############ Get List of Log Objects ############
#################################################
# Iterate through the S3 bucket/path and append the objects to a list
s3ObjectsLocalList = []
itemCount = 1
s3ObjectsFromAWSList = my_bucket.objects.filter(Prefix=input_arg.s3_bucket_prefix)
try:
  for objects in s3ObjectsFromAWSList:
    s3ObjectsLocalList.append(objects.key)
    # Only print out line on every 1,000th item so the terminal doesn't get messy
    if itemCount % 1000 == 0:
      updateNotification = "\rFound log file in S3 bucket. Processing item: " + bcolors.HEADER + str(itemCount) + bcolors.ENDC
      #print("Found log file in S3 bucket. Processing item: ", str(itemCount))
      stdout.write("\r%s" % updateNotification)
      stdout.flush()
    itemCount += 1
  stdout.write("\n") # move the cursor to the next line
  print("There are " + bcolors.HEADER + str(len(s3ObjectsLocalList)) + bcolors.ENDC + " log files in this S3 bucket/path.")
except Exception as e:
  print("Could not interate through S3 bucket.")
  raise e

numOfLogFilesToCheck = int(input("How many log files back do you want to check?\t"))
print("Ok, going to check " + str(numOfLogFilesToCheck) + " log files!")
print("Here are the '" + str(numOfLogFilesToCheck) + "' files we will check: ",s3ObjectsLocalList[-numOfLogFilesToCheck:])

########################################
############ Log Processing ############
########################################
# Iterate through list of objects in S3 bucket
# This section will:
#### 1. Get the zipped log file
#### 2. Unzip the file
#### 3. Separate the file into multiple lines. (One line per HTTP request)
#### 4. Make each line in the log file into a list where each data point is an element
#### 5. Append that line to a bigger list called 'bigLogList'
logFileToCheckCount = 1
for logFileToCheck in s3ObjectsLocalList[-numOfLogFilesToCheck:]:

  if logFileToCheckCount % 10 == 0:
    logFileUpdateNotification = "\rProcessing log file: " + bcolors.HEADER + str(logFileToCheckCount) + bcolors.ENDC
    #print("Found log file in S3 bucket. Processing item: ", str(itemCount))
    stdout.write("\r%s" % logFileUpdateNotification)
    stdout.flush()
  logFileToCheckCount += 1
  if logFileToCheckCount == numOfLogFilesToCheck:
    stdout.write("\n") # move the cursor to the next line


  obj = s3.Object(input_arg.s3_bucket, logFileToCheck)
  with gzip.GzipFile(fileobj=obj.get()["Body"]) as gzipfile:
      content = gzipfile.read().decode('utf-8')
  
  # Create list in which the other list will be nested
  # The list nested here will be a list of all the strings in a line in the logs from one particular file
  # This section below will need to live in a for loop that checks multiple files if the user requests for multiple files to be checked
  # Seperate the big string of characters in the log file into multiple lines
  lineNum = 1
  for logLine in content.splitlines():
    # Skip the first two lines in the log file since it is just the version of the logs and the headers
    if lineNum > 2:
      #print("This is the log line lineNum count: ", lineNum)
      #print("This is the log line content: ", logLine)
      # Take each string in each line in the log file and make it an element in a list called logList
      logList = list(logLine.split("\t"))
      #print("This is the logList: ", logList)
      processedLogList = list(itemgetter(0, 1, 4, 5, 7, 8, 9)(logList))
      #print("This is the processedLogList: ", processedLogList)
      # Append this list that contains one Cloudfront log record for one HTTP request
      bigLogList.append(processedLogList)
      #print("This is the length of the bigLogList: ", len(bigLogList))
    # Increment the lineNum varialbe to iterate through each line in the log file
    lineNum += 1

  # Sort the list of lists by the date in the second element place
  #bigLogList.sort(key=lambda x: x[1])
  # This is supposed to sort by two elements but it's not working. It's not super important since each log file is usually of the \
  ## same day, but I am leaving this here in case I want to use it in the future
  # sorted(bigLogList, key=lambda x: (-int(x[0]), x[1]))

#################################################################
############ Create Database and Interact With User ############
#################################################################
df = pd.DataFrame(bigLogList, 
            columns=databaseTableColumns)
# Here is a list of the headers available with example outputs:
##        "date"    "time"          "c-ip"  "cs-method"           "cs-uri-stem"   "sc-status"               "cs(Referer)"
## 0  2022-01-29  02:11:17  162.223.124.26          GET   /en-US/administrator           404    https://shop.dccomics.com/
defaultQuery = """ SELECT * FROM df """
default4xxQuery = """ SELECT date, time, "cs-uri-stem", "sc-status" FROM df WHERE "sc-status" BETWEEN 400 AND 499 """
default5xxQuery = """ SELECT date, time, "cs-uri-stem", "sc-status" FROM df WHERE "sc-status" BETWEEN 500 AND 599 """
query = input(f"Enter in your query below for database called 'df' (default: {defaultQuery} ) \n\tOR \nEnter '1' for default 4XX error query [{default4xxQuery}] \nEnter '2' for default 5XX query [{default5xxQuery}]:\n")

if not query:
    print(f"No query entered! Using the default query: {defaultQuery}\n")
    finalQuery = defaultQuery
elif query in ('1', '2'):
    if query == '1':
        print(f"Option '1' selected! Using the default 4XX query: {default4xxQuery}\n")
        finalQuery = default4xxQuery
    if query == '2':
        print(f"Option '2' selected! Using the default 5XX query: {default5xxQuery}\n")
        finalQuery = default5xxQuery
else:
    print(f"Manual query entered! Using a custom query: {query}\n")
    finalQuery = query

queryResult = ps.sqldf(finalQuery, locals())
queryResultString = queryResult.to_string()
print(queryResultString)

##########################################
############ Post Query Info ############
##########################################
# Remind user how many log files they looked through and tell them how many total lines were processed
print("Total log lines parsed through in desired section consisting of '" + str(numOfLogFilesToCheck) + "' log files: ", bcolors.HEADER, len(bigLogList), bcolors.ENDC)
# Use elements in bigLogList to get the date and time of first line of processed log and the last line
firstDateElement = bigLogList[0][0]
firstTimeElement = bigLogList[0][1]
lastDateElement = bigLogList[-1][0]
lastTimeElement = bigLogList[-1][1]
print("Showing logs from", bcolors.BOLD, firstDateElement, bcolors.ENDC, firstTimeElement, "to", bcolors.BOLD, lastDateElement, bcolors.ENDC, lastTimeElement)