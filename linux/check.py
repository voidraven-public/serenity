from kubernetes import client, config

def is_node_cordoned(node_name):
    # Load the kubeconfig file
    config.load_kube_config()

    # Create an instance of the API class
    v1 = client.CoreV1Api()

    try:
        # Get the specified node
        node = v1.read_node(node_name)

        # Check if the node is cordoned (unschedulable)
        if node.spec.unschedulable:
            print(f"Node {node_name} is cordoned.")
        else:
            print(f"Node {node_name} is not cordoned.")
            
    except client.exceptions.ApiException as e:
        print(f"An exception occurred: {e}")

# Replace 'node_name_here' with the name of the node you want to check
is_node_cordoned('kind-control-plane')