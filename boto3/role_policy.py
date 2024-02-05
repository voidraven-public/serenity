import boto3

# Create an IAM client
iam = boto3.client('iam')

# List all roles
paginator = iam.get_paginator('list_roles')

for page in paginator.paginate():
    for role in page['Roles']:
        role_name = role['RoleName']

        # List inline policies for the role
        inline_policies = iam.list_role_policies(RoleName=role_name)

        # Print role name and attached inline policies
        print(f"Role: {role_name}")
        for policy in inline_policies['PolicyNames']:
            print(f"  - Inline Policy: {policy}")

        # (Optional) Get full inline policy document
        for policy in inline_policies['PolicyNames']:
            policy_document = iam.get_role_policy(RoleName=role_name, PolicyName=policy)
            print(f"    Policy document: {policy_document['PolicyDocument']}")
            print("----")

        print("")
