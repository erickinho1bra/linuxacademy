import getpass, subprocess, boto3
from botocore.exceptions import ClientError

def getCreds():
    user=getpass.getuser()
    file_path="/Users/" + user + "/.aws/credentials"
    file = open(file_path, "r")
    readFile = file.readlines()    
    lineNum = -1
    for line in readFile:
      lineNum += 1
      if 'aws-dope-commerce' in line:
        awsCreds = []
        lineNum += 1 # Add Access Key to Array
        accessKeyFull = readFile[lineNum] 
        accessKeyFullParts = accessKeyFull.split(' ')
        accessKeyFinal = accessKeyFullParts[2]
        awsCreds.append(accessKeyFinal)
        lineNum += 1 # Do the same but for Secret Key
        secretKeyFull = readFile[lineNum]
        secretKeyFullParts = secretKeyFull.split(' ')
        secretkeyFinal = secretKeyFullParts[2]
        awsCreds.append(secretkeyFinal)
        return awsCreds

def printSecret():
    secret_name='/dc-shop-strapi/staging/DC_SHOP_STRAPI_STAGING_DATABASE_PASSWORD'
    credsArray = getCreds()
    accessKey=credsArray[0].replace('\n', '')
    secretKey=credsArray[1].replace('\n', '')
    session = boto3.Session(
    aws_access_key_id=accessKey,
    aws_secret_access_key=secretKey
    )
    client = session.client(
    service_name='secretsmanager',
    region_name='us-west-2'
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
        elif e.response['Error']['Code'] == 'DecryptionFailure':
            print("The requested secret can't be decrypted using the provided KMS key:", e)
        elif e.response['Error']['Code'] == 'InternalServiceError':
            print("An error occurred on service side:", e)
    else:
        if 'SecretString' in get_secret_value_response:
            text_secret_data = get_secret_value_response['SecretString']
            return text_secret_data
            #print(text_secret_data)
        else:
            binary_secret_data = get_secret_value_response['SecretBinary']
            #print(binary_secret_data)

dbPassword = printSecret()
bashCommand = "DATABASE_PASSWORD=" + dbPassword + " " + "yarn start"
bashCommandArray = bashCommand.split()
bashCommandFinal = str(bashCommandArray)
subprocess.run([bashCommandFinal])