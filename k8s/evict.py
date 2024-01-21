from kubernetes import client, config
from kubernetes.client.rest import ApiException
config.load_kube_config()  # Or use load_incluster_config() if running inside a cluster
core_v1_api = client.CoreV1Api()
field_selector = 'spec.nodeName={node_name}'.format(node_name='kind-worker2')
pods = core_v1_api.list_pod_for_all_namespaces(field_selector=field_selector)
for pod in pods.items:
    try:
        eviction = client.V1beta1Eviction(metadata=client.V1ObjectMeta(name=pod.metadata.name, namespace=pod.metadata.namespace))
        core_v1_api.create_namespaced_pod_eviction(name=pod.metadata.name, namespace=pod.metadata.namespace, body=eviction)
    except ApiException as e:
        print("Exception when evicting pod: %s\n" % e)
