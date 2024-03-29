import boto3

# Initialize a Boto3 CodeBuild client
codebuild_client = boto3.client('codebuild')

# List all CodeBuild projects
response = codebuild_client.list_projects()

# Iterate through the projects
for project_name in response['projects']:
    project_details = codebuild_client.batch_get_projects(names=[project_name])['projects'][0]
    
    # Get the role ARN associated with the CodeBuild project
    role_arn = project_details['serviceRole']

    print(f"CodeBuild Project Name: {project_name}")
    print(f"Role ARN: {role_arn}\n")

# with pagninator
# Create a Boto3 CodeBuild client
codebuild = boto3.client('codebuild')

# Initialize the CodeBuild paginator
paginator = codebuild.get_paginator('list_projects')

# Define any additional parameters or filters if needed
# For example:
# params = {'sortOrder': 'ASCENDING'}

# Use a generator to paginate through the results
for page in paginator.paginate():    
    projects = page.get('projects', [])
    
    # Process each project in the current page
    for project in projects:
        print(f"Project Name: {project}")
