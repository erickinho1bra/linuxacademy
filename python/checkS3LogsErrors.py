#!/usr/bin/env python3
# Creating file that can be called from other scripts to pull AWS credentials
#import getpass, boto3
#from appscript import *

from getAwsCredentials import *
from sys import stdout
import argparse, json, gzip

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
# Uncomment the bottom lines to know what these color codes look like
print(bcolors.HEADER + "This is bcolors.HEADER" + bcolors.ENDC)
print(bcolors.OKBLUE + "This is bcolors.OKBLUE" + bcolors.ENDC)
print(bcolors.OKCYAN + "This is bcolors.OKCYAN" + bcolors.ENDC)
print(bcolors.OKGREEN + "This is bcolors.OKGREEN" + bcolors.ENDC)
print(bcolors.WARNING + "This is bcolors.WARNING" + bcolors.ENDC)
print(bcolors.FAIL + "This is bcolors.FAIL" + bcolors.ENDC)
print(bcolors.BOLD + "This is bcolors.BOLD" + bcolors.ENDC)
print(bcolors.UNDERLINE + "This is bcolors.UNDERLINE" + bcolors.ENDC)


# Function to print out color coded log error codes
def printLogErrorInfo(httpCodeElement, errorCodeOfLogFilesToCheck):
  # Print log lines for 4XX and 5XX errors if any are present and if errorCodeOfLogFilesToCheck is set
  if httpCodeElement >= 400 and httpCodeElement < 500 and errorCodeOfLogFilesToCheck in ['1', '3']:
    dateElement = bigLogList[logListElementCount][0]
    timeElement = bigLogList[logListElementCount][1]
    httpUrlElement = bigLogList[logListElementCount][7]
    httpCodeElement = bigLogList[logListElementCount][8]
    print("Date: " + str(dateElement) + "  Time: " + str(timeElement) + "\t HTTP URL: " + str(httpUrlElement) + "\t\t\t HTTP Code: " + bcolors.FAIL + str(httpCodeElement) + bcolors.ENDC)
  elif httpCodeElement >= 500 and httpCodeElement < 600 and errorCodeOfLogFilesToCheck in ['2', '3']:
    dateElement = bigLogList[logListElementCount][0]
    timeElement = bigLogList[logListElementCount][1]
    httpUrlElement = bigLogList[logListElementCount][7]
    httpCodeElement = bigLogList[logListElementCount][8]
    print("Date: " + str(dateElement) + "  Time: " + str(timeElement) + "\t HTTP URL: " + str(httpUrlElement) + "\t\t\t HTTP Code: " + bcolors.WARNING + str(httpCodeElement) + bcolors.ENDC)



############################## The Code ##############################

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
  print("Sucessfully pulled the credentials for " + bcolors.OKCYAN + input_arg.local_aws_account_name + bcolors.ENDC)
except Exception as e:
  print("Could not get user credentials and start boto3 session")
  raise e

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

# Ask user what error code they would like to look for and check if what they enter is a valid input (i.e. '1', '2', or '3')
errorCodeOfLogFilesToCheck = input("What error code do you want to check for? \n\t'1' for 4XX errors \n\t'2' for 5XX errors \n\t'3' for both 4XX errors AND 5XX errors \n\t")
while errorCodeOfLogFilesToCheck not in ['1', '2', '3']:
  errorCodeOfLogFilesToCheck = input("You must enter: \n\t'1' for 4XX errors \n\t'2' for 5XX errors \n\t'3' for both 4XX errors AND 5XX errors \n\t")

print("Here are the '" + str(numOfLogFilesToCheck) + "' files we will check: ",s3ObjectsLocalList[-numOfLogFilesToCheck:])
for logFileToCheck in s3ObjectsLocalList[-numOfLogFilesToCheck:]:

  obj = s3.Object(input_arg.s3_bucket, logFileToCheck)
  with gzip.GzipFile(fileobj=obj.get()["Body"]) as gzipfile:
      content = gzipfile.read().decode('utf-8')
  
  # Create list in which the other list will be nested
  # The list nested here will be a list of all the strings in a line in the logs from one particular file
  # This section below will need to live in a for loop that checks multiple files if the user requests for multiple files to be checked
  bigLogList = []
  # Seperate the big string of characters in the log file into multiple lines
  lineNum = 1
  for logLine in content.splitlines():
    # Skip the first two lines in the log file since they are just the headers
    if lineNum > 2:
      # Take each string in each line in the log file and make it an element in a list called logList
      logList = list(logLine.split("\t"))
      # Append this list that contains one Cloudfront log record for one HTTP request
      bigLogList.append(logList)
      #print("logList: ", logList)
      #print("HTTP Code: ", logList[1 ])
    lineNum += 1
  
  bigLogList.sort(key=lambda x: x[1])
  # This is supposed to sort by two elements but it's not working. It's not super important since each log file is usually of the \
  ## same day, but I am leaving this here in case I want to use it in the future
  # sorted(bigLogList, key=lambda x: (-int(x[0]), x[1]))

  # Variable used to iterate the nested list elements in the larger list "bigLogList"
  logListElementCount = 0
  # Go through each log line and show the date, time, HTTP URL, and the HTTP code
  for logListElement in bigLogList:
    # Get HTTP Code element and pass it to the function (i.e. "printLogErrorInfo") that will print it out with the proper color code
    httpCodeElement = int(bigLogList[logListElementCount][8])

    # Function for pringting out the data we all payed to see!
    printLogErrorInfo(httpCodeElement, errorCodeOfLogFilesToCheck)
    logListElementCount += 1

print("Total log lines parsed through in desired section: ", bcolors.HEADER, len(bigLogList), bcolors.ENDC)
print("Showing logs from", bcolors.BOLD, bigLogList[0][0], bcolors.ENDC, bigLogList[0][1], "to", bcolors.BOLD, bigLogList[-1][0], bcolors.ENDC, bigLogList[-1][1],)
