import getpass, subprocess, boto3
from botocore.exceptions import ClientError

def printSecret():
    secret_name='/dc-fd/staging/DOT_ENV_FILE'
    session = boto3.Session(
    aws_access_key_id='',
    aws_secret_access_key=''
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

#fileContent = printSecret()
print(printSecret())
#bashCommandArray = bashCommand.split()
#bashCommandFinal = str(bashCommandArray)
#subprocess.run([bashCommandFinal])
