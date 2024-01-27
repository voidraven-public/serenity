import boto3

def get_stack_service_role(stack_name):
    cf_client = boto3.client('cloudformation')

    try:
        response = cf_client.describe_stacks(StackName=stack_name)
        stack = response['Stacks'][0]

        # Extract the service role ARN from the stack outputs
        service_role_arn = None
        for output in stack['Outputs']:
            if output['OutputKey'] == 'ServiceRoleArn':  # Common output key for service roles
                service_role_arn = output['OutputValue']
                break

        if service_role_arn:
            print(f"Service Role ARN: {service_role_arn}")
        else:
            print("Service role ARN not found in stack outputs.")

    except ClientError as e:
        print(f"Error retrieving stack information: {e}")

if __name__ == '__main__':
    stack_name = 'YourStackName'  # Replace with your stack name
    get_stack_service_role(stack_name)
