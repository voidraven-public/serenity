from kubernetes import client, config

def scale_deployment(namespace, deployment_name, replicas):
    # Load the kubeconfig file
    config.load_kube_config()

    # Create an instance of the AppsV1Api class
    apps_v1_api = client.AppsV1Api()

    try:
        # Fetch the deployment
        deployment = apps_v1_api.read_namespaced_deployment(deployment_name, namespace)

        # Update the replicas
        deployment.spec.replicas = replicas

        # Update the deployment
        apps_v1_api.replace_namespaced_deployment(deployment_name, namespace, deployment)

        print(f"Deployment {deployment_name} scaled to {replicas} replicas.")
        
    except client.exceptions.ApiException as e:
        print(f"An exception occurred: {e}")

# Replace with your deployment details
namespace = 'default'  # Namespace of the deployment
deployment_name = 'nginx'  # Name of the deployment
replicas = 3  # Number of replicas to scale to

scale_deployment(namespace, deployment_name, replicas)
