# Creating file that can be called from other scripts to pull AWS credentials
import getpass, boto3
#from appscript import *

def getCreds(awsProfileName):
    print("Getting your AWS profile credentials...")
    # Find out what user this is
    user=getpass.getuser()
    # Set path to aws credentials file
    file_path="/Users/" + user + "/.aws/credentials"
    # Open the file
    file = open(file_path, "r")
    readFile = file.readlines()
    # Need this to figure out what line we find the 'aws-dope-commerce' profile
    lineNum = -1
    # Go through ~/.aws/credentials file to get users Access Key and Secret Key securely
    for line in readFile:
      lineNum += 1
      # Looks for AWS profile called 'aws-dope-commerce'
      if awsProfileName in line:
        # Credentials will be loaded in an array, creating it here
        awsCreds = {}
        # Add Access Key to Array, cleaning it up since the credential is the third word in that line
        lineNum += 1
        accessKeyFull = readFile[lineNum]
        accessKeyFullParts = accessKeyFull.split('=')
        accessKey = accessKeyFullParts[0].strip()
        accessValue = accessKeyFullParts[1].strip()
        awsCreds[accessKey] = accessValue
        # Do the same but for Secret Key
        lineNum += 1
        secretKeyFull = readFile[lineNum]
        secretKeyFullParts = secretKeyFull.split('=')
        secretKey = secretKeyFullParts[0].strip()
        secretValue = secretKeyFullParts[1].strip()
        awsCreds[secretKey] = secretValue
        # Do the same but for session token
        lineNum += 1
        sessionTokenFull = readFile[lineNum]
        sessionTokenFullParts = sessionTokenFull.split('=')
        sessionTokenKey = sessionTokenFullParts[0].strip()
        sessionTokenValue = sessionTokenFullParts[1].strip()
        awsCreds[sessionTokenKey] = sessionTokenValue
        # Return the array with the Access Key and Secret Key
        return awsCreds
