# k8s
# k8s

###
```
# memory percentage requested for each node in a Kubernetes cluster
kubectl describe nodes | grep -A 3 "Resource .*Requests .*Limits"

kubectl describe nodes | grep -A 3 "Resource .*Requests .*Limits" | awk '/memory/ {if ($2 ~ /G$/) {print $2*1024} else {print $2}}' | awk '{if ($3 ~ /G$/) {print $1, $2/($3*1024)*100} else {print $1, $2/$3*100}}'

```


```
#!/bin/bash

# Fetch node information from the Kubernetes API
nodes=$(kubectl get nodes -o json)

# Use jq to extract and format the desired information
echo "Node Name | Memory Requested (%)"
echo "----------|---------------------"
jq -r '.items[] | .metadata.name + " | " + (.status.allocatable.memory | tonumber / .status.capacity.memory * 100 | floor | tostring) + "%"' <<< "$nodes"

```