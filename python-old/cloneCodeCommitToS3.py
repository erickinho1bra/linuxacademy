import json
import boto3
import subprocess
#from git import Repo

#session = boto3.session.Session(profile_name='aws-dope-commerce')

def lambda_handler(event, context):
    
    print("----------------- EVENT -----------------------")
    print(event)
    print("----------------- EVENT -----------------------")

    #Log the updated references from the event
    references = { reference['ref'] for reference in event['Records'][0]['codecommit']['references'] }
    print("References: "  + str(references))
    codecommit = boto3.client('codecommit')

    #Get the repository from the event and show its git clone URL
    repository = event['Records'][0]['eventSourceARN'].split(':')[5]
    try:
        response = codecommit.get_repository(repositoryName=repository)
        cloneUrl = response['repositoryMetadata']['cloneUrlHttp']
        print("Clone URL: " + cloneUrl)
    except Exception as e:
        print(e)
        print('Error getting repository {}. Make sure it exists and that your repository is in the same region as this function.'.format(repository))
        raise e

    tag = ""
    print("References: ", references)
    for ref in references:
        if ref.startswith("refs/tags/"):
            tag = ref
            print(f"The reference '{ref}' is a tag. Moving on to next step")
            break
        else:
            print(f"Reference '{ref}' is not a tag. Moving on to next reference in event.")

    print(f"Checked all references. Made '{tag}' the 'tag' variable.")

    print(f"repository: {repository}")


    response = codecommit.get_folder(
        repositoryName=repository,
        commitSpecifier=str(tag),
        folderPath='/'
    )
    print(response)
    responseFolderPath = json.dumps(
        response['folderPath'],
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    )
    print(responseFolderPath)

    # Validate tag variable
    if tag.startswith('refs/tags/'):
        # Remove 'refs/tags/' from string
        tag = tag[10:]
        
        # Checking /tmp for a directory called by the name of the repository we are trying to clone
        try:
            subprocess.run([f"echo 'Checking /tmp for a directory callded: {repository} .... ' && ls -l /tmp/{repository}"], shell = True, check = True)
            # Deleting the folder
            print(f"Detected folder called /tmp/{repository} ... Deleting it now")
            subprocess.run([f"rm -rf /tmp/{repository}"], shell = True)
        except subprocess.CalledProcessError as e:
            print(f"Pass: No folder called /tmp/{repository} was found. Proceeding with 'git clone'")
        
        # Clone the repo
        try:
            subprocess.run([f"echo 'Checking /tmp BEFORE git clone.... ls -l /tmp' && ls -l /tmp/"], shell = True)
            subprocess.run(["HOME=/tmp git config --global credential.helper '!/opt/aws codecommit credential-helper $@'"], shell = True)
            subprocess.run(["HOME=/tmp git config --global credential.UseHttpPath true"], shell = True)
            # subprocess.run([f"HOME=/tmp git clone --depth 1 --branch {tag} {cloneUrl} /tmp/{repository} && cd /tmp/{repository} && git switch -c temp"], check = True, shell = True)
            subprocess.run([f"HOME=/tmp git clone {cloneUrl} /tmp/{repository} && cd /tmp/{repository} && git checkout {tag} && git status && rm -rf .git"], check = True, shell = True)
            subprocess.run([f"echo 'Checking /tmp AFTER git clone.... ls -lr /tmp/{repository}' && ls -l /tmp/{repository}"], shell = True)
        except Exception as e:
            print(f"Error: could not clone the repository: {repository}")
            print(e)
            raise e
        
        # Purge S3 bucket
        try:
            print("Starting purge of S3")
            cmd = f'/opt/aws s3 rm --recursive s3://{repository}'
            subprocess.run([cmd], check = True, shell = True)
            print("Finished purge of S3")
        except Exception as e:
            print("Error: could not purge S3")
            print(e)
            raise e

        # Copy code to S3
        try:
            print("Starting copy to S3")
            cmd = f'/opt/aws s3 cp /tmp/{repository}/ s3://{repository}/ --recursive'
            subprocess.run([cmd], check = True, shell = True)
            print("Finished copy to S3")
        except Exception as e:
            print("Error: could not copy to S3")
            print(e)
            raise e
            
        # Start build on AWS CodeBuild
        try:
            print(f"Triggering AWS CodeBuild build for project: {repository}-codebuild")
            client = boto3.client(service_name='codebuild', region_name='us-west-2')
            new_build = client.start_build(projectName=f"{repository}-codebuild")
        except Exception as e:
            print("Error: Could not trigger build on AWS CodeBuild")
            print(e)
            raise e
    else:
        print('No tag reference detected')




#event = {'Records': [{'awsRegion': 'us-west-2', 'codecommit': {'references': [{'commit': '80f1fbfc1b71f52446705343d5daa8b9ecc56a98', 'created': True, 'ref': 'refs/tags/v1.0.0-beta.7'}]}, 'customData': '', 'eventId': 'd28e0cd7-47cf-4115-9711-ef07fc6cacc2', 'eventName': 'ReferenceChanges', 'eventPartNumber': 1, 'eventSource': 'aws:codecommit', 'eventSourceARN': 'arn:aws:codecommit:us-west-2:205584903784:dc-shop-efs-staging-web', 'eventTime': '2022-01-04T23:33:19.191+0000', 'eventTotalParts': 1, 'eventTriggerConfigId': '9f3ea501-07e7-4ede-8ffa-c0d48cd261fc', 'eventTriggerName': 'Clone Tag to S3', 'eventVersion': '1.0', 'userIdentityARN': 'arn:aws:iam::205584903784:user/sa-dc-shop-efs-staging-web-codecommit'}]}
event = {
  "Records": [
    {
      "awsRegion": "us-west-2",
      "codecommit": {
        "references": [
          {
            "commit": "c3d763949c7c7615d846965340afcb1101d295f2",
            "created": "True", 
            "ref": "refs/heads/feature/COMM-1764_OrdersV2PaymentRequest"
          },
          {
            "commit": "f5bad23d1d745e12d42ca7d6d304589b4b4edda8",
            "created": "True", 
            "ref": "refs/tags/v1.0.1-beta.33"
          },
          {
            "commit": "0ab359a70d34b64e91186454b00b6e415f70fc1d",
            "created": "True", 
            "ref": "refs/heads/feature/COMM-1587_OpenProductCardInNewWindow"
          }
        ]
      },
      "customData": "this is custom data",
      "eventId": "fe772369-09ef-4562-93c1-064882cb6617",
      "eventName": "ReferenceChanges",
      "eventPartNumber": 1,
      "eventSource": "aws:codecommit",
      "eventSourceARN": "arn:aws:codecommit:us-west-2:205584903784:dc-shop-staging-web",
      "eventTime": "2022-01-10T18:55:09.100+0000",
      "eventTotalParts": 1,
      "eventTriggerConfigId": "c092af34-b7e0-4838-bedb-20cd1a43b36b",
      "eventTriggerName": "my-lambda-test-trigger",
      "eventVersion": "1.0",
      "userIdentityARN": "arn:aws:iam::205584903784:user/sa-dc-shop-staging-web-codecommit"
    }
  ]
}
context = 'LambdaContext([aws_request_id=bc5c6dfc-36a3-4d48-8cad-c544fd03a29d,log_group_name=/aws/lambda/dc-shop-efs-staging-web-tag-trigger,log_stream_name=2022/01/04/[$LATEST]2e24b47672474d99b7cf98e2b691e56a,function_name=dc-shop-efs-staging-web-tag-trigger,memory_limit_in_mb=128,function_version=$LATEST,invoked_function_arn=arn:aws:lambda:us-west-2:205584903784:function:dc-shop-efs-staging-web-tag-trigger,client_context=None,identity=CognitoIdentity([cognito_identity_id=None,cognito_identity_pool_id=None])])'

#references = event['Records'][0]['codecommit']['references'][0]['ref']
#print(references)


#s3 = session.resource('s3')
#for bucket in s3.buckets.all():
#    print(bucket.name)


lambda_handler(event, context)