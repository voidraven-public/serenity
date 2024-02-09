#!/bin/bash

# Get the list of namespaces
namespaces=$(kubectl get namespaces -o jsonpath='{.items[*].metadata.name}')

# Iterate over each namespace
for namespace in $namespaces; do
    echo "Namespace: $namespace"
    # Get the pods in the current namespace with the name "violet"
    pods=$(kubectl get pods -n $namespace -l app=violet -o jsonpath='{.items[*].metadata.name}')
    # Iterate over each pod
    for pod in $pods; do
        echo "Pod: $pod"
        # Get the node name of the current pod
        node_name=$(kubectl get pod $pod -n $namespace -o jsonpath='{.spec.nodeName}')
        echo "Node Name: $node_name"
        # Get the labels of the node where the pod is deployed
        node_labels=$(kubectl get node $node_name -o jsonpath='{.metadata.labels}')
        echo "Node Labels: $node_labels"
    done
done
