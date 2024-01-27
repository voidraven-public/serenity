import boto3

# Initialize a Boto3 CodeDeploy client
codedeploy_client = boto3.client('codedeploy')

# List all deployment groups
response = codedeploy_client.list_application_revisions(
    applicationName='Your-Application-Name'  # Replace with your application name
)

# Iterate through the deployment jobs and print their names and service roles
for deployment_job in response['revisions']:
    deployment_job_name = deployment_job['revisionLabel']
    service_role_arn = deployment_job['genericRevisionInfo']['serviceRoleArn']

    print(f"Deployment Job Name: {deployment_job_name}")
    print(f"Service Role ARN: {service_role_arn}\n")
