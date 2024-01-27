import boto3

# Initialize a Boto3 Lambda client
lambda_client = boto3.client('lambda')

# List all Lambda functions
response = lambda_client.list_functions()

# Iterate through the Lambda functions and print their names and associated role ARNs
for function in response['Functions']:
    function_name = function['FunctionName']
    role_arn = function['Role']

    print(f"Lambda Function Name: {function_name}")
    print(f"Role ARN: {role_arn}\n")
