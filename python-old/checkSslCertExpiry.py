import boto3
import time
import json
from json import JSONEncoder
import datetime 
from datetime import timedelta
import dateutil.parser

#session = boto3.session.Session(profile_name='aws-dope-commerce', region_name='us-west-2')


def lambda_handler(event):

    ### Preset variables
    awsRegionsList = ["us-west-2", "us-east-1"]

    ### Class of warning colors for text output
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

    ### Option to print out colors to see what they look like on your terminal
    #print(bcolors.OKBLUE + "OKBLUE" + bcolors.ENDC)
    #print(bcolors.OKCYAN + "OKCYAN" + bcolors.ENDC)
    #print(bcolors.OKGREEN + "OKGREEN" + bcolors.ENDC)
    #print(bcolors.WARNING + "WARNING" + bcolors.ENDC)
    #print(bcolors.FAIL + "FAIL" + bcolors.ENDC)
    #print(bcolors.BOLD + "BOLD" + bcolors.ENDC)
    #print(bcolors.UNDERLINE + "UNDERLINE" + bcolors.ENDC)

    ### Defining function that wil check cert expiry in different regions
    def checkLambdasInMultipleRegions(awsRegion):
        try:
            session = boto3.session.Session(profile_name='aws-dope-commerce', region_name=awsRegion)
            acmClient = boto3.client('acm')

            ### Query ACM for list of certs and then format the json info so it looks pretty
            certsRaw = acmClient.list_certificates()
            certsJson = json.dumps(certsRaw, indent=2)
            ### Option to print it out below
            #print("Certificates: ", certsJson)

            ### Load certs through json packages so we can parse through the dict
            certsLoaded = json.loads(certsJson)
            ### Iterate through the dict and tell us the Domain Name and the ARN of the cert
            for listCertsItem in certsLoaded['CertificateSummaryList']:
                domainName = listCertsItem['DomainName']
                print("\nDomain Name: \t\t", domainName)
                certificateArn = listCertsItem['CertificateArn']
                print("Certificate: \t\t", certificateArn)

                ### Descrivbe each certificate
                describeCertListRaw = acmClient.describe_certificate(CertificateArn=certificateArn)
                ### Create a class that encodes a 'datetime' object type so that it can be iterable
                class DateTimeEncoder(JSONEncoder):
                    def default(self, obj):
                        if isinstance(obj, (datetime.date, datetime.datetime)):
                            return obj.isoformat()
                ### Encode DateTime Object into JSON using custom JSONEncoder created above
                describeCertListJson = json.dumps(describeCertListRaw, indent=4, cls=DateTimeEncoder)

                #for x in describeCertListRaw['Certificate']:
                #    print(x)




                now = datetime.datetime.now() # current date and time

                describeCertListLoaded = json.loads(describeCertListJson)
                expirationDateRaw = describeCertListLoaded["Certificate"]["NotAfter"]
                expirationDate = expirationDateRaw[:10]
                print("Expiration Date: \t", expirationDate)
                todaysDate = now.strftime("%Y-%m-%d")
                print("Date now: \t\t", todaysDate)

                insertion_date = dateutil.parser.parse(expirationDate)

                time_between_insertion = datetime.datetime.now() - insertion_date
                if  time_between_insertion.days>-30 and time_between_insertion.days<-1:                    
                    print(bcolors.WARNING + f"Based on the insertion date '{time_between_insertion}' your cert for " + bcolors.UNDERLINE + f"'{domainName}'" + bcolors.ENDC + bcolors.WARNING + " is about to expire!" + bcolors.ENDC)

                    #print(f"The insertion date '{time_between_insertion}' is older than 30 days")
                elif time_between_insertion.days>=-1:
                    print(bcolors.FAIL + f"Based on the insertion date '{time_between_insertion}', your cert for " + bcolors.UNDERLINE + f"'{domainName}'" + bcolors.ENDC + bcolors.FAIL + " has already expired!" + bcolors.ENDC)

                else:
                    print(f"The insertion date '{time_between_insertion}' is not older than 30 days")

        except KeyboardInterrupt as e:
            print("\n\nExiting")
        except Exception as e:
            raise e

    ### Iterate through list of AWS regions (created at top of script)
    try:
        for region in awsRegionsList:
            print(bcolors.OKCYAN + f"--------------------------------" + bcolors.ENDC)
            print(bcolors.OKCYAN + f"Checking {region} region" + bcolors.ENDC)
            print(bcolors.OKCYAN + f"--------------------------------" + bcolors.ENDC)
            checkLambdasInMultipleRegions(region)
    except KeyboardInterrupt as e:
        print("\n\nExiting")
    except Exception as e:
        raise e

# Run the code
event = ""
lambda_handler(event)