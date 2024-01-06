import requests
import json

# Replace with your Rancher API endpoint, access key, and secret key
RANCHER_URL = "https://your-rancher-server/v3"
ACCESS_KEY = "your-access-key"
SECRET_KEY = "your-secret-key"

# Authentication headers
headers = {
    "Authorization": f"Bearer {ACCESS_KEY}",
    "Accept": "application/json",
}

# API endpoint for listing node templates
url = f"{RANCHER_URL}/nodeTemplates"

try:
    # Send GET request to fetch node templates
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse JSON response
        data = json.loads(response.text)

        # Print node template details
        for template in data["data"]:
            print(f"ID: {template['id']}")
            print(f"Name: {template['name']}")
            print(f"Description: {template['description']}")
            print(f"Labels: {template['labels']}")
            print(f"Taints: {template['taints']}")
            print("------------------")
    else:
        print("Failed to fetch node templates. Response:", response.text)
except requests.exceptions.RequestException as err:
    print("Error making API request:", err)
