import requests

# Replace with your Rancher API URL and API token
rancher_url = "https://your-rancher-url/v3"
api_token = "your-api-token"

# Define headers with the API token
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json",
}

# Define the Rancher API endpoint for node templates
node_templates_url = f"{rancher_url}/nodetemplates"

# Make a GET request to list node templates
response = requests.get(node_templates_url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    node_templates_data = response.json()
    for node_template in node_templates_data["data"]:
        # Access and print information about each node template
        print("Node Template ID:", node_template["id"])
        print("Node Template Name:", node_template["name"])
        print("Node Template Description:", node_template["description"])
        print("-----")
else:
    print("Failed to retrieve node templates. Status code:", response.status_code)
    print("Response:", response.text)
