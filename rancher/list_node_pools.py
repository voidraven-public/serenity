import requests

# Replace with your Rancher server URL and API token
RANCHER_URL = "https://your-rancher-url.com/v3"
API_TOKEN = "your-api-token"

# ID of the cluster for which you want to list node pools
CLUSTER_ID = "your-cluster-id"

def list_node_pools():
    # Get the list of node pools for the specified cluster
    node_pools = requests.get(
        f"{RANCHER_URL}/clusters/{CLUSTER_ID}/nodePools",
        headers={"Authorization": f"Bearer {API_TOKEN}"},
    ).json()

    return node_pools

if __name__ == "__main__":
    node_pools = list_node_pools()
    
    if node_pools:
        print("Node Pools:")
        for node_pool in node_pools:
            print(f"Name: {node_pool['name']}, ID: {node_pool['id']}")
    else:
        print("No node pools found.")
