import boto3
import pdb
import pprint

def get_instance_profiles(ec2_client):
  """
  This function retrieves information about EC2 instances and their attached IAM instance profiles.

  Args:
      ec2_client (boto3.client): A boto3 client for EC2 service.

  Returns:
      dict: A dictionary where keys are instance IDs and values are dictionaries containing instance details (InstanceId, InstanceType, InstanceProfile)
  """
  instances_data = {}

  # Get information about all running instances
  reservations = ec2_client.describe_instances(Filters=[])["Reservations"]
  for reservation in reservations:
    for instance in reservation["Instances"]:
      instance_id = instance["InstanceId"]
      instance_type = instance["InstanceType"]

      # Check if instance has an IAM instance profile attached
      if "IamInstanceProfile" in instance:
        instance_profile_arn = instance["IamInstanceProfile"]["Arn"]
        instance_profile_name = instance_profile_arn.split("/")[-1]  # Extract profile name from ARN
      else:
        instance_profile_name = "Not Attached"

      instances_data[instance_id] = {
          "InstanceId": instance_id,
          "InstanceType": instance_type,
          "InstanceProfile": instance_profile_name,
          "PrivateDnsName": instance["PrivateDnsName"]
      }

  return instances_data

def get_instance_iam_role(instance_id):
    # Describe the specified instance
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    iam_role_info = response['Reservations'][0]['Instances'][0].get('IamInstanceProfile', None)
    
    if iam_role_info:
        return iam_role_info['Arn']
    else:
        return "No IAM role attached to this instance."

def get_iam_role(instance_id):
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    iam_instance_profile = response['Reservations'][0]['Instances'][0].get('IamInstanceProfile', None)
    if iam_instance_profile:
        return iam_instance_profile['Arn']
    else:
        return 'No IAM role attached'

if __name__ == "__main__":
  # Create an EC2 client
  ec2_client = boto3.client('ec2')
  iam_client = boto3.client('iam')  

  # Get instance information and attached IAM profiles
  instance_data = get_instance_profiles(ec2_client)

  with open('ec2_profile.txt', 'w') as file:
    file.write('id,private_ip,type,profile,role-a,role-b')        

    # Print the results
    if instance_data:
        print("EC2 Instances and Attached IAM Instance Profiles:")
        for instance_id, data in instance_data.items():
            print(f"  - Instance ID: {data['InstanceId']}")
            print(f"    PrivateDnsName: {data['PrivateDnsName']}")
            print(f"    Instance Type: {data['InstanceType']}")
            print(f"    IAM Instance Profile: {data['InstanceProfile']}")
            iam_profile_role = get_instance_iam_role(instance_id)
            print(f"    IAM Instance Role for EC2 Instance {instance_id}: {iam_profile_role}")
            iam_role = get_iam_role(instance_id)
            print(f"    IAM Role for EC2 Instance {instance_id}: {iam_role}")
            file.write(f"{data['InstanceId']},{data['PrivateDnsName']},{data['InstanceType']},{data['InstanceProfile']},{iam_profile_role},{iam_role}\n")
    else:
        print("No EC2 instances found.")

    
