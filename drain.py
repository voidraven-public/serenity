from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException
import time

def cordon_node(api_instance, node_name):
    body = {"spec": {"unschedulable": True}}
    api_instance.patch_node(node_name, body)
    print(f"Node {node_name} cordoned.")

def list_pods_on_node(api_instance, node_name):
    field_selector = f'spec.nodeName={node_name}'
    return api_instance.list_pod_for_all_namespaces(field_selector=field_selector)

def drain_node(node_name):
    config.load_kube_config()
    v1 = client.CoreV1Api()

    # Cordon the node
    cordon_node(v1, node_name)

    # List all pods on the node
    pods = list_pods_on_node(v1, node_name)
    for pod in pods.items:
        if pod.metadata.owner_references and pod.metadata.owner_references[0].kind != 'DaemonSet':
            try:
                print(f"Evicting pod {pod.metadata.name}")
                v1.create_namespaced_pod_eviction(
                    pod.metadata.name, 
                    pod.metadata.namespace, 
                    client.V1beta1Eviction(metadata=client.V1ObjectMeta(name=pod.metadata.name))
                )
            except ApiException as e:
                print(f"Exception when evicting pod: {e}")
            except Exception as e:
              
