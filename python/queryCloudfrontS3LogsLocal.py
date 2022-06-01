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
## ./checkS3LogsErrorsWithDatabase.py -a aws-dope-commerce:aws-dope-commerce-devops -b dc-shop-prod-cloudfront-logs -p new-logs -s 2021-12-24-08 -e 2021-12-24-13/ 
### -a is the local AWS profile that I have set up with aws-gimmme-creds (see above)
#### -b is the bucket name that contains your Cloudfront Logs
##### -p is the prefix in S3 that contains your logs. If there is no prefix and the logs are in the root of the bucket then don't include this argument
###### -s is the start year-month-day-hour of the query you want to run
####### -e is the end year-month-day-hour of the query you want to run
# Used to parse arguments, authenticate to AWS, and process data

print("Importing ALL the packages! *raises fist in the air*")
from getAwsCredentials import *
from sys import stdout
import argparse, json, gzip
# For the databases
from operator import itemgetter
import pandas as pd
import pandasql as ps
from functools import reduce
# To export to CSV
import csv, os
from datetime import datetime
from subprocess import Popen
from time import sleep

###################################
############ Variables ############
###################################
logHeadersList = ['date', 'time', 'x-edge-location', 'sc-bytes', 'c-ip', 'cs-method', 'cs(Host)', 'cs-uri-stem', 'sc-status', 'cs(Referer)', 'cs(User-Agent)', 'cs-uri-query', 'cs(Cookie)', 'x-edge-result-type', 'x-edge-request-id', 'x-host-header', 'cs-protocol', 'cs-bytes', 'time-taken', 'x-forwarded-for', 'ssl-protocol', 'ssl-cipher', 'x-edge-response-result-type', 'cs-protocol-version', 'fle-status', 'fle-encrypted-fields', 'c-port', 'time-to-first-byte', 'x-edge-detailed-result-type', 'sc-content-type', 'sc-content-len', 'sc-range-start', 'sc-range-end']
databaseTableColumns = list(itemgetter(0, 1, 4, 5, 7, 8, 9, 14)(logHeadersList))
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

###################################
############ Functions ############
###################################

def modifyDateTimeToUtc(dateTimeString):
  dateTimeList = list(dateTimeString.split("-"))
  print

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
  parser.add_argument('--start-date-and-hour', '-s' , help='The date and hour you would like to START your query (e.g. "2021-12-24-22")', type=str)
  parser.add_argument('--end-date-and-hour', '-e' , help='The date and hour you would like to END your query (e.g. "2021-12-25-06")', type=str)
  input_arg = parser.parse_args()
except Exception as e:
  print("Did not get the correct arguments to run script. Need parameters '-a <LOCAL_AWS_ACCOUNT_NAME>' AND '-b <BUCKET_NAME>' ")
  raise e

#####################################################
############ Checking For Required Flags ############
#####################################################
if not input_arg.local_aws_account_name or not input_arg.s3_bucket:
  print(bcolors.FAIL + "ERROR" + bcolors.ENDC + ": Either no " + bcolors.HEADER + "AWS account " + bcolors.ENDC + "provided under '-a' flag, no " + bcolors.HEADER + "S3 bucket name" + bcolors.ENDC + " provided under '-b' flag, or both")
  exit()


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
##### s3ObjectsFromAWSList = my_bucket.objects.filter(Prefix=input_arg.s3_bucket_prefix)
try:
  s3ObjectsFromAWSList = my_bucket.objects.filter(Prefix=input_arg.s3_bucket_prefix)
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
  # Remove the first element in the s3ObjectsLocalList since it is just the prefix path
  if input_arg.s3_bucket_prefix:
    s3ObjectsLocalList.pop(0)
  print("There are " + bcolors.HEADER + str(len(s3ObjectsLocalList)) + bcolors.ENDC + " log files in this S3 bucket/path.")
except Exception as e:
  print(f"\n\n{bcolors.FAIL}ERROR{bcolors.ENDC}: Could not interate through S3 bucket. Perhaps your {bcolors.HEADER}AWS account token{bcolors.ENDC} has expired.\n\n")
  raise e

##################################################
############ Inform User On Log Dates ############
##################################################
print("---------------------------------------")
print("---------------------------------------")
earliestLogObjectString = s3ObjectsLocalList[0]
earliestLogDateAndHour = earliestLogObjectString.split(".")[1]
earliestLogDateAndHourList = earliestLogDateAndHour.split("-")
earliestLogYear = str(earliestLogDateAndHourList[0])
earliestLogMonth = str(earliestLogDateAndHourList[1])
earliestLogDay = str(earliestLogDateAndHourList[2])
earliestLogHour = str(earliestLogDateAndHourList[3])
print(f"The {bcolors.OKGREEN}earliest{bcolors.ENDC} log in this bucket/path is from {earliestLogYear}/{earliestLogMonth}/{earliestLogDay} in the {earliestLogHour} hour.")

latestLogObjectString = s3ObjectsLocalList[-1]
latestLogDateAndHour = latestLogObjectString.split(".")[1]
latestLogDateAndHourList = latestLogDateAndHour.split("-")
latestLogYear = str(latestLogDateAndHourList[0])
latestLogMonth = str(latestLogDateAndHourList[1])
latestLogDay = str(latestLogDateAndHourList[2])
latestLogHour = str(latestLogDateAndHourList[3])
print(f"The {bcolors.FAIL}latest {bcolors.ENDC} log in this bucket/path is from {latestLogYear}/{latestLogMonth}/{latestLogDay} in the {latestLogHour} hour.")
print("---------------------------------------")
print("---------------------------------------")

################################################
############ Clean Up Log File List ############
################################################

bigLogObjectList = []
bigLogObjectListColumns = ['yearMonthDayHour', 'fileName']
# Iterate through log file names in s3ObjectsLocalList and create a big list of log file names and their corresponding date and hour
for logObject in s3ObjectsLocalList:
  logObjectDateAndHour = logObject.split(".")[1]
  # Make the object date-hour info into an element in list, i.e. ['<year>-<mont>-<day>']
  logObjectDateAndHourList = [logObjectDateAndHour]
  # Appending the file name to the list needed to create our s3ObjectDatabase, e.g. ['2022-02-02-16', 'new-logs/E2M6LH0LQ7GKZO.2022-02-02-16.fa4282a1.gz']
  logObjectDateAndHourList.append(logObject)
  # Append list to larger list "bigLogObjectList" used to create our s3ObjectDatabase
  bigLogObjectList.append(logObjectDateAndHourList)

####################################################
############ Create the Object Database ############
####################################################
# Create database with list of log objects and the columns list
s3ObjectDatabase = pd.DataFrame(bigLogObjectList, 
            columns=bigLogObjectListColumns)

###################################################
############ Get Query Dates From User ############
###################################################
# Get user input on the dates of logs to check if they have not supplied it in the command line already
if not input_arg.start_date_and_hour and not input_arg.end_date_and_hour:
  queryStartDate = input(f"What is the" + bcolors.OKGREEN + " starting " + bcolors.ENDC + " date of the log you are looking for? (e.g. For Christmas Eve 2021 you would enter: 2021-12-24): ") or "2021-12-24"
  queryStartHour = input(f"What is the" + bcolors.OKGREEN + " starting " + bcolors.ENDC + " hour of the log you are looking for? (e.g. For 9PM you would enter: 21): ") or "21"
  queryStartDateAndHour = queryStartDate + "-" + queryStartHour
  queryEndDate = input(f"What is the" + bcolors.FAIL + " ending " + bcolors.ENDC + " date of the log you are looking for? (e.g. For Christmas Day 2021 you would enter: 2021-12-25): ") or "2021-12-25"
  queryEndHour = input(f"What is the" + bcolors.FAIL + " ending " + bcolors.ENDC + " hour of the log you are looking for? (e.g. For 6AM you would enter: 06): ") or "06"
  queryEndDateAndHour = queryEndDate + "-" + queryEndHour
# If user did not provide an end date for the query when running the script, ask the user if they would like to run it up until the latest log
elif input_arg.start_date_and_hour and not input_arg.end_date_and_hour:
  proceedWithCurrentDateTime = input(f"{bcolors.WARNING} WARNING {bcolors.ENDC} : No end date provided for query. Would you like to use the latest log's date and time {bcolors.UNDERLINE}{latestLogDateAndHour}{bcolors.ENDC} as the ending date? [y] ") or "y"
  if proceedWithCurrentDateTime == "y":
    queryEndDateAndHour = latestLogDateAndHour
    queryStartDateAndHour = input_arg.start_date_and_hour
    print(f"Roger that! Using '{queryStartDateAndHour}' as the query start date '{queryEndDateAndHour}' as the query end date.")
# Set the query date params using the argument values the user used when running the script
else:
  queryStartDateAndHour = input_arg.start_date_and_hour
  queryEndDateAndHour = input_arg.end_date_and_hour
# Create query string and let user know what it is (if they uncomment the line)
s3ObjectDatabaseQuery = f"SELECT fileName FROM s3ObjectDatabase WHERE yearMonthDayHour BETWEEN '{queryStartDateAndHour}' AND '{queryEndDateAndHour}'"
print(f"Pulling log files from" + bcolors.HEADER + f" '{queryStartDateAndHour}'" + bcolors.ENDC + " to" + bcolors.HEADER + f" '{queryEndDateAndHour}'" + bcolors.ENDC)
#print("This is what your query will look like: " + bcolors.OKGREEN + s3ObjectDatabaseQuery + bcolors.ENDC) 

###################################################
############ Run Query and Clean It Up ############
###################################################
# Run the query on the database with all the S3 objects
s3ObjectDatabaseQueryResult = ps.sqldf(s3ObjectDatabaseQuery, locals())
s3ObjectDatabaseQueryResultString = s3ObjectDatabaseQueryResult.to_string()

# Clean up the query result so we can get a final list of log files that we will end up checking
listOfLogObjectsToCheck  =  s3ObjectDatabaseQueryResultString.split("\n")
finalListOfLogObjectsToCheck = []
for rawLogObjectsToCheck in listOfLogObjectsToCheck:
  processedLogObjectsToCheck = rawLogObjectsToCheck.split(" ")
  for processedLogObjectsToCheckElement in processedLogObjectsToCheck:
    if len(processedLogObjectsToCheckElement) > 10:
      finalListOfLogObjectsToCheck.append(processedLogObjectsToCheckElement)

###################################################
############ Get User Input to Proceed ############
###################################################
if len(finalListOfLogObjectsToCheck) == 0:
  print(bcolors.FAIL + "ERROR: No logs found for the given time range!" + bcolors.ENDC)
  exit()
print("Going to check logs on " + bcolors.HEADER + str(len(finalListOfLogObjectsToCheck)) + bcolors.ENDC + " log files")
# Verify the user want to process the number of files they have selected
continueResponse = input("Would you like to proceed? [y]: ") or "y"
if continueResponse == "y":
  pass
else:
  exit

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
#### for logFileToCheck in s3ObjectsLocalList[-numOfLogFilesToCheck:]:
for logFileToCheck in finalListOfLogObjectsToCheck:
  if logFileToCheckCount % 10 == 0 and logFileToCheckCount != len(finalListOfLogObjectsToCheck):
    logFileUpdateNotification = "\rProcessing log file: " + bcolors.HEADER + str(logFileToCheckCount) + bcolors.ENDC
    stdout.write("\r%s" % logFileUpdateNotification)
    stdout.flush()
  logFileToCheckCount += 1
  if logFileToCheckCount == len(finalListOfLogObjectsToCheck):
    logFileUpdateNotification = "\rProcessing log file: " + bcolors.HEADER + str(logFileToCheckCount) + bcolors.ENDC
    stdout.write("\r%s" % logFileUpdateNotification)
    stdout.flush()
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
default4xxQuery = """ SELECT date, time, "cs-uri-stem", "sc-status", "x-edge-request-id" FROM df WHERE "sc-status" BETWEEN 400 AND 499 """
default5xxQuery = """ SELECT date, time, "cs-uri-stem", "sc-status", "x-edge-request-id" FROM df WHERE "sc-status" BETWEEN 500 AND 599 """
print("Here is a sample query you can base yours off of: ")
sampleQuery = "SELECT * FROM df LIMIT 1"
queryResult = ps.sqldf(sampleQuery, locals())
queryResultString = queryResult.to_string()
print("----------------------------------")
print("----------------------------------")
print(queryResultString)
print("----------------------------------")
print("----------------------------------")

query = input(f"Enter in your query below for database called 'df' (default: {defaultQuery} ) \n\tOR \nEnter '1' for default 4XX error query [{default4xxQuery}] \nEnter '2' for default 5XX query [{default5xxQuery}]:\n")

if not query:
    print(f"No query entered! Using the default query: {defaultQuery}\n")
    finalQuery = defaultQuery
elif query in ('1', '2'):
    if query == '1':
        print(f"Option '1' selected! Using the default" + bcolors.FAIL + " 4XX" + bcolors.ENDC + f" query: {default4xxQuery}\n")
        finalQuery = default4xxQuery
    if query == '2':
        print(f"Option '2' selected! Using the default" + bcolors.FAIL + " 5XX" + bcolors.ENDC + f" query: {default5xxQuery}\n")
        finalQuery = default5xxQuery
else:
    print(f"Manual query entered! Using a custom query: {query}\n")
    finalQuery = query

queryResult = ps.sqldf(finalQuery, locals())
queryResultString = queryResult.to_string()
############################################### print(queryResultString)

##########################################
############ Post Query Info ############
##########################################
# Remind user how many log files they looked through and tell them how many total lines were processed
print("Total log lines parsed through in desired section consisting of '" + str(len(finalListOfLogObjectsToCheck)) + "' log files: ", bcolors.HEADER, len(bigLogList), bcolors.ENDC)
# Use elements in bigLogList to get the date and time of first line of processed log and the last line
firstDateElement = bigLogList[0][0]
firstTimeElement = bigLogList[0][1]
lastDateElement = bigLogList[-1][0]
lastTimeElement = bigLogList[-1][1]
print("Showing logs from", bcolors.BOLD, firstDateElement, bcolors.ENDC, firstTimeElement, "to", bcolors.BOLD, lastDateElement, bcolors.ENDC, lastTimeElement)


#######################################
############ Export to CSV ############
#######################################
# Make query result into a CSV
# Cleaning up query result
queryResultList = list(queryResultString.split("\n"))
queryResultListCounter = 0
bigQueryResultList = []
for queryResultListElement in queryResultList:
  if queryResultListCounter == 0:
    queryResultHeder = queryResultListElement
    queryResultHederList = queryResultHeder.split("\t")
    finalQueryResultHederList = []
    for element in queryResultHederList[0].split(" "):
        if element:
            finalQueryResultHederList.append(element)
  else:
    processedQueryResultListElement = queryResultListElement.split("\t")
    nestedQueryResultList = []
    for element in processedQueryResultListElement[0].split(" "):
        if element:
          nestedQueryResultList.append(element)
    nestedQueryResultList.pop(0)
    bigQueryResultList.append(nestedQueryResultList)
  queryResultListCounter += 1

userHome = os.path.expanduser('~')
currentDateTime = datetime.today().strftime('-%Y-%m-%d_%H:%M')
csvFileName = f"{input_arg.s3_bucket}{currentDateTime}.csv"
csvFilePath = userHome + "/Downloads/" + csvFileName

# Finally export query to CSV file
with open(csvFilePath, 'w') as f:
    write = csv.writer(f)
    write.writerow(finalQueryResultHederList)
    write.writerows(bigQueryResultList)

print("Your CSV file has been exported to " + bcolors.OKGREEN + bcolors.BOLD + csvFilePath + bcolors.ENDC + "!")
print("Opening file now...")
sleep(1)
os.system(f"chmod +x {csvFilePath} && open {csvFilePath}")