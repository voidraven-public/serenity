# pods on node
kubectl get pods --all-namespaces --field-selector spec.nodeName=<node-name> -o wide
