from kubernetes import client, config

def create_pod(namespace, pod_name, image):
    # Configure access to the cluster
    config.load_kube_config()

    # Define the pod specification
    pod = client.V1Pod(
        metadata=client.V1ObjectMeta(name=pod_name),
        spec=client.V1PodSpec(
            containers=[client.V1Container(name=pod_name, image=image)]
        )
    )

    # Create an API client for the CoreV1Api
    v1 = client.CoreV1Api()

    try:
        # Create the pod in the specified namespace
        v1.create_namespaced_pod(namespace=namespace, body=pod)
        print(f"Pod {pod_name} created in namespace {namespace}")
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")

# Example usage
namespace = 'default'  # Replace with the desired namespace
pod_name = 'mypod'    # Replace with your desired pod name
image = 'nginx'       # Replace with your desired container image

create_pod(namespace, pod_name, image)
