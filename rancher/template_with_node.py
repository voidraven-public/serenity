import requests

# Replace with your Rancher API URL and API token
rancher_url = "https://your-rancher-url/v3"
api_token = "your-api-token"

# Define the name of the node template you want to check
node_template_name = "TemplateToCheck"  # Replace with the name of the template

# Define headers with the API token
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json",
}

# Step 1: List all nodes in your Rancher cluster
nodes_url = f"{rancher_url}/nodes"
response = requests.get(nodes_url, headers=headers)

if response.status_code != 200:
    print("Failed to list nodes. Status code:", response.status_code)
    print("Response:", response.text)
    exit(1)

nodes_data = response.json()

# Step 2: Retrieve information about the node template associated with each node
for node in nodes_data["data"]:
    if "nodeTemplateId" in node:
        node_template_id = node["nodeTemplateId"]
        node_name = node["name"]
        
        # Step 3: Check if the node template matches the one you want to check
        if node_template_id:
            node_template_url = f"{rancher_url}/nodetemplates/{node_template_id}"
            response = requests.get(node_template_url, headers=headers)
            
            if response.status_code == 200:
                node_template_data = response.json()
                if node_template_data["name"] == node_template_name:
                    print(f"Node '{node_name}' is using the template '{node_template_name}' (ID: {node_template_id}).")
                else:
                    print(f"Node '{node_name}' is using a different template.")
            else:
                print(f"Failed to retrieve template information for node '{node_name}'. Status code:", response.status_code)
        else:
            print(f"Node '{node_name}' does not have a template association.")
    else:
        print(f"Node '{node_name}' does not have a template association.")

print("Node template check completed.")
