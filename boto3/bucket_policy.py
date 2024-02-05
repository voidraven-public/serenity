import boto3

# Create an S3 client
s3_client = boto3.client('s3')

# List all S3 buckets
buckets = s3_client.list_buckets()['Buckets']

# Iterate through each bucket
for bucket in buckets:
    bucket_name = bucket['Name']
    
    # Get the bucket policy
    try:
        bucket_policy = s3_client.get_bucket_policy(Bucket=bucket_name)
        policy_document = bucket_policy['Policy']
        print(f"Bucket: {bucket_name}\nBucket Policy:\n{policy_document}\n")
    except s3_client.exceptions.NoSuchBucketPolicy:
        print(f"Bucket: {bucket_name}\nBucket Policy: No bucket policy found.\n")

    # Get the KMS key associated with the bucket, if any
    try:
        bucket_location = s3_client.get_bucket_location(Bucket=bucket_name)
        region = bucket_location['LocationConstraint'] or 'us-east-1'  # Default to us-east-1 if no location constraint
        encryption_info = s3_client.get_bucket_encryption(Bucket=bucket_name)
        rules = encryption_info['ServerSideEncryptionConfiguration']['Rules']
        if rules:
            kms_key_id = rules[0]['ApplyServerSideEncryptionByDefault'].get('KMSMasterKeyID', 'None')
            print(f"KMS Key ID for Bucket {bucket_name} in Region {region}: {kms_key_id}\n")
        else:
            print(f"Bucket {bucket_name} in Region {region} is not encrypted with KMS.\n")
    except s3_client.exceptions.ClientError as e:
        print(f"Error getting KMS key info for bucket {bucket_name}: {e}\n")
