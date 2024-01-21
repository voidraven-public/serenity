from kubernetes import client, config

def cordon_node(node_name):
    # Load the kubeconfig file
    config.load_kube_config()

    # Create an instance of the CoreV1Api class
    v1 = client.CoreV1Api()

    try:
        # Fetch the specified node
        node = v1.read_node(node_name)

        # Mark the node as unschedulable
        node.spec.unschedulable = True

        # Update the node
        v1.patch_node(node_name, node)
        print(f"Node {node_name} is successfully cordoned.")

    except client.exceptions.ApiException as e:
        print(f"An exception occurred: {e}")

# Replace 'node_name_here' with the name of the node you want to cordon
cordon_node('node_name_here')
