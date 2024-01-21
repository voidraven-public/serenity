import requests
import json

# Replace with your Rancher API URL and API token
rancher_url = "https://your-rancher-url/v3"
api_token = "your-api-token"

# Define headers with the API token
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json",
}

# Step 1: List existing node templates and find the one to copy
node_templates_url = f"{rancher_url}/nodetemplates"
response = requests.get(node_templates_url, headers=headers)

if response.status_code != 200:
    print("Failed to list node templates. Status code:", response.status_code)
    print("Response:", response.text)
    exit(1)

node_templates_data = response.json()

# Choose the node template to copy (you can specify criteria here)
template_to_copy = None
for node_template in node_templates_data["data"]:
    if node_template["name"] == "TemplateToCopy":  # Replace with the name of the template to copy
        template_to_copy = node_template
        break

if template_to_copy is None:
    print("Node template to copy not found.")
    exit(1)

# Step 2: Create a new node template by copying the existing one
copy_template_url = f"{rancher_url}/nodetemplates"
copy_template_data = {
    "name": "CopiedTemplate",  # Replace with the desired name for the copied template
    "driver": template_to_copy["driver"],
    "externalId": template_to_copy["externalId"],
    "labels": template_to_copy["labels"],
    "etcd": template_to_copy["etcd"],
    "controlPlane": template_to_copy["controlPlane"],
    "worker": template_to_copy["worker"],
}

response = requests.post(copy_template_url, headers=headers, json=copy_template_data)

if response.status_code != 201:
    print("Failed to create copied node template. Status code:", response.status_code)
    print("Response:", response.text)
    exit(1)

copied_template = response.json()

# Step 3: Update instance type and tags in the copied template
copied_template["etcd"]["instanceType"] = "t2.medium"  # Replace with the desired instance type
copied_template["labels"]["tag1"] = "value1"  # Replace with the desired tags

# Step 4: Save the copied and updated node template
update_template_url = f"{rancher_url}/nodetemplates/{copied_template['id']}"
response = requests.put(update_template_url, headers=headers, json=copied_template)

if response.status_code != 200:
    print("Failed to update copied node template. Status code:", response.status_code)
    print("Response:", response.text)
    exit(1)

print("Copied and updated node template successfully.")
