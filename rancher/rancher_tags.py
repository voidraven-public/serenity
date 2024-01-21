import requests

# Set your Rancher API details here
rancher_api_url = 'https://rancher.yourdomain.com/v3/nodetemplates/'
node_template_id = 'your-node-template-id'
api_key = 'your-api-key'
headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'}

# New tags to update
updated_tags = ['tag1', 'tag2', 'tag3']

# Make the API request to update the node template
response = requests.put(f"{rancher_api_url}{node_template_id}", json={'tags': updated_tags}, headers=headers)

# Check the response
if response.status_code == 200:
    print("Node template updated successfully.")
else:
    print(f"Failed to update node template: {response.content}")
