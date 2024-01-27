import boto3

def list_codepipelines_and_roles():
    codepipeline_client = boto3.client('codepipeline')
    response = codepipeline_client.list_pipelines()

    for pipeline in response['pipelines']:
        pipeline_name = pipeline['name']

        # Get the role ARN from the pipeline structure
        role_arn = pipeline['roleArn']

        # Get role details using IAM client
        iam_client = boto3.client('iam')
        role_details = iam_client.get_role(RoleName=role_arn.split('/')[-1])

        print(f"Pipeline Name: {pipeline_name}")
        print(f"Role ARN: {role_arn}")
        print(f"Role Name: {role_details['Role']['RoleName']}")
        print(f"Role Description: {role_details['Role']['Description']}")
        print("-" * 50)

if __name__ == '__main__':
    list_codepipelines_and_roles()
