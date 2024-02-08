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

def get_node_pool_size(api_url, cluster_id, node_pool_id, token):
    url = f"{api_url}/clusters/{cluster_id}/nodepools/{node_pool_id}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        node_pool_info = response.json()
        return node_pool_info["workerCount"]
    else:
        print(f"Failed to get node pool size: {response.status_code} - {response.text}")
        return None


# Example usage
if __name__ == "__main__":
    api_url = "https://your-rancher-url.com/v3"
    cluster_id = "your_cluster_id"
    node_pool_id = "your_node_pool_id"
    token = "your_rancher_api_token"

    size = get_node_pool_size(api_url, cluster_id, node_pool_id, token)
    if size is not None:
        print(f"Node pool size: {size}")

    new_size = 5  # Set the new size of the node pool
    update_node_pool_size(api_url, cluster_id, node_pool_id, token, new_size)


