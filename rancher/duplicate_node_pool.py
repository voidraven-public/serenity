import requests
import json

# Replace with your Rancher server URL and API token
RANCHER_URL = "https://your-rancher-url.com/v3"
API_TOKEN = "your-api-token"

# ID of the cluster containing the node pool you want to duplicate
CLUSTER_ID = "your-cluster-id"

# ID of the node pool you want to duplicate
SOURCE_NODE_POOL_ID = "your-source-node-pool-id"

def create_duplicate_node_pool():
    # Get the source node pool details
    source_node_pool = requests.get(
        f"{RANCHER_URL}/clusters/{CLUSTER_ID}/nodePools/{SOURCE_NODE_POOL_ID}",
        headers={"Authorization": f"Bearer {API_TOKEN}"},
    ).json()

    # Create a new node pool with the same configuration
    duplicate_node_pool = requests.post(
        f"{RANCHER_URL}/clusters/{CLUSTER_ID}/nodePools",
        headers={"Authorization": f"Bearer {API_TOKEN}"},
        json={
            "name": f"Duplicate of {source_node_pool['name']}",
            "dockerRootDir": source_node_pool["dockerRootDir"],
            "etcd": source_node_pool["etcd"],
            # Add more fields as needed
        },
    ).json()

    return duplicate_node_pool

if __name__ == "__main__":
    duplicate_node_pool = create_duplicate_node_pool()
    print("Duplicate Node Pool ID:", duplicate_node_pool["id"])
