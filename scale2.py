import time
from kubernetes import client, config

def scale_statefulset(namespace, statefulset_name, replicas, timeout=600):
    # Load the kubeconfig file
    config.load_kube_config()

    # Create an instance of the AppsV1Api class
    apps_v1_api = client.AppsV1Api()

    try:
        # Update the StatefulSet replicas
        patch_body = {'spec': {'replicas': replicas}}
        apps_v1_api.patch_namespaced_stateful_set(statefulset_name, namespace, patch_body)
        print(f"Scaling StatefulSet {statefulset_name} to {replicas} replicas.")

        # Wait for the StatefulSet to scale
        start_time = time.time()
        while time.time() - start_time < timeout:
            statefulset = apps_v1_api.read_namespaced_stateful_set(statefulset_name, namespace)
            if statefulset.status.replicas == replicas and statefulset.status.ready_replicas == replicas:
                print(f"All {replicas} replicas of StatefulSet {statefulset_name} are running.")
                return
            time.sleep(5)

        raise TimeoutError(f"Timeout while waiting for StatefulSet {statefulset_name} to scale.")

    except client.exceptions.ApiException as e:
        print(f"An exception occurred: {e}")

# Replace with your StatefulSet details
namespace = 'default'  # Namespace of the StatefulSet
statefulset_name = 'your-statefulset'  # Name of the StatefulSet
replicas = 3  # Number of replicas to scale to

scale_statefulset(namespace, statefulset_name, replicas)
