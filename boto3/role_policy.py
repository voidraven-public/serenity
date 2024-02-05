import boto3

iam_client = boto3.client('iam')

def list_roles_and_policies(exclude_aws=True):
    """Lists IAM roles and their attached inline policies, potentially excluding roles starting with 'AWS'.

    Args:
        exclude_aws (bool, optional): Whether to skip roles starting with 'AWS'. Defaults to True.

    Returns:
        list: A list of dictionaries, where each dictionary contains:
            - 'RoleName': The name of the IAM role.
            - 'InlinePolicies': A list of dictionaries, where each dictionary contains:
                - 'PolicyName': The name of the inline policy.
                - 'PolicyDocument': The JSON-formatted policy document.
    """

    paginator = iam_client.get_paginator('list_roles')
    roles = paginator.paginate().build_complete_result()['Roles']

    filtered_roles = []
    for role in roles:
        if exclude_aws and role['RoleName'].startswith('AWS'):
            continue

        inline_policies = []
        paginator = iam_client.get_paginator('list_role_policies')
        for page in paginator.paginate(RoleName=role['RoleName']):
            for policy_name in page['PolicyNames']:
                policy_document = iam_client.get_role_policy(RoleName=role['RoleName'], PolicyName=policy_name)['PolicyDocument']
                inline_policies.append({'PolicyName': policy_name, 'PolicyDocument': policy_document})

        filtered_roles.append({'RoleName': role['RoleName'], 'InlinePolicies': inline_policies})

    return filtered_roles

if __name__ == '__main__':
    roles_and_policies = list_roles_and_policies()

    # Print role names and policy details
    for role in roles_and_policies:
        print(f"Role Name: {role['RoleName']}")
        for policy in role['InlinePolicies']:
            print(f"- Policy Name: {policy['PolicyName']}")
            print(f"  Policy Document: {policy['PolicyDocument']}")
            print("")  # Add an empty line for readability

