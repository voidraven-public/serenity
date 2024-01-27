import boto3

# Initialize a Boto3 CodeDeploy client
codedeploy_client = boto3.client('codedeploy')

# List all CodeDeploy applications
response = codedeploy_client.list_applications()

# Iterate through the applications and print their names
for application_name in response['applications']:
    print(f"CodeDeploy Application Name: {application_name}")
