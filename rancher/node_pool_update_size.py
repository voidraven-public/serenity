import requests

def update_node_pool_size(api_url, cluster_id, node_pool_id, token, new_size):
    url = f"{api_url}/clusters/{cluster_id}/nodepools/{node_pool_id}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        "workerCount": new_size
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Node pool size updated successfully.")
    else:
        print(f"Failed to update node pool size: {response.status_code} - {response.text}")

# Example usage
if __name__ == "__main__":
    api_url = "https://your-rancher-url.com/v3"
    cluster_id = "your_cluster_id"
    node_pool_id = "your_node_pool_id"
    token = "your_rancher_api_token"
    new_size = 5  # Set the new size of the node pool
    update_node_pool_size(api_url, cluster_id, node_pool_id, token, new_size)
