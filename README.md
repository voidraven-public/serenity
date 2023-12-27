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

jq -r '.items[] | .metadata.name + " | " + .status.allocatable.memory'  <<< "$nodes"

```

```
#!/bin/bash

# Grabbing the details of each node, it's like Pokémon but for memory stats
kubectl get nodes -o json | jq '.items[] | {
    name: .metadata.name,
    memoryCapacity: .status.capacity.memory,
    memoryAllocatable: .status.allocatable.memory
}' | while read -r line; do
    # It's like a memory party, and we're keeping track of who brings what
    if echo $line | grep -q "name"; then
        nodeName=$(echo $line | awk '{print $2}' | sed 's/"//g;s/,//g')
    elif echo $line | grep -q "memoryCapacity"; then
        memoryCapacity=$(echo $line | awk '{print $2}' | sed 's/"//g;s/Gi//g')
    elif echo $line | grep -q "memoryAllocatable"; then
        memoryAllocatable=$(echo $line | awk '{print $2}' | sed 's/"//g;s/Gi//g')

        # The magical math part where we figure out the memory percentage
        memoryRequested=$(bc <<< "scale=2; 100 - ($memoryAllocatable/$memoryCapacity)*100")
        echo "Node: $nodeName, Memory % Requested: $memoryRequested%"
    fi
done
```

```
kubectl get nodes --show-labels -o json | jq '.items[] | select(.metadata.labels | to_entries[] | select(.value | contains("wrk")))' 
```