import boto3

# Initialize IAM client
iam = boto3.client('iam')

# Open file for writing role names
with open('roles.txt', 'w') as roles_file:

    # List all roles
    for role in iam.list_roles()['Roles']:
        role_name = role['RoleName']

        # Skip roles starting with 'AWS'
        if role_name.startswith('AWS'):
            continue

        # Open file for writing policy document
        with open(f"{role_name}.json", 'w') as policy_file:

            # List attached inline policies
            for policy in iam.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']:
                policy_arn = policy['PolicyArn']

                # Get inline policy document
                policy_document = iam.get_inline_policy(RoleName=role_name, PolicyName=policy['PolicyName'])['Policy']

                # Write policy document to file
                policy_file.write(policy_document)

                # Write role name to roles.txt
                roles_file.write(f"{role_name}\n")

print("Successfully wrote roles and policies to files.")
