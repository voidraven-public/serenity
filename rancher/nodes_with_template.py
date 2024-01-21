import requests

# Replace with your Rancher API URL and access token
rancher_url = "https://your-rancher-server/v3"
access_token = "your-api-access-token"

headers = {"Authorization": f"Bearer {access_token}"}

# Fetch all node templates
templates_response = requests.get(f"{rancher_url}/nodeTemplates", headers=headers)
templates = templates_response.json()

# Iterate through templates and collect node information
for template in templates["data"]:
    template_id = template["id"]
    template_name = template["name"]

    # Fetch nodes using this template
    nodes_response = requests.get(f"{rancher_url}/nodes?nodeTemplateId={template_id}", headers=headers)
    nodes = nodes_response.json()

    print(f"Template: {template_name}")
    print("-" * len(template_name))
    for node in nodes["data"]:
        node_name = node["name"]
        node_id = node["id"]
        print(f"  Node: {node_name} (ID: {node_id})")
    print()
