import boto3

# Initialize the CodeBuild client
codebuild_client = boto3.client('codebuild')

# Parameters for the list_builds API call
page_size = 10  # Number of builds to fetch per request
next_token = None  # Initialize the pagination token

# Loop to fetch all CodeBuild jobs
while True:
    # Use the list_builds method to retrieve a page of builds
    response = codebuild_client.list_builds(
        sortOrder='DESCENDING',  # Sort order (DESCENDING or ASCENDING)
        pageSize=page_size,      # Number of builds to retrieve per request
        nextToken=next_token    # Pagination token
    )

    # Process the builds in the current page
    builds = response.get('ids', [])
    for build_id in builds:
        print(f"Build ID: {build_id}")

    # Check if there are more builds to fetch
    next_token = response.get('nextToken')
    if not next_token:
        break  # No more builds to fetch, exit the loop
