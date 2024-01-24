import requests

# Replace with your Rancher server URL and API token
RANCHER_URL = "https://your-rancher-url.com/v3"
API_TOKEN = "your-api-token"

# ID of the cluster containing the node pool
CLUSTER_ID = "your-cluster-id"

# ID of the node pool you want to get details for
NODE_POOL_ID = "your-node-pool-id"

def get_node_pool_details():
    # Get the details of the specified node pool
    node_pool_details = requests.get(
        f"{RANCHER_URL}/clusters/{CLUSTER_ID}/nodePools/{NODE_POOL_ID}",
        headers={"Authorization": f"Bearer {API_TOKEN}"},
    ).json()

    return node_pool_details

if __name__ == "__main__":
    node_pool_details = get_node_pool_details()
    
    if node_pool_details:
        print("Node Pool Details:")
        print("Name:", node_pool_details['name'])
        print("ID:", node_pool_details['id'])
        # Add more fields as needed
    else:
        print("Node pool not found.")
