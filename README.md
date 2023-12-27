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
label_key="beta.kubernetes.io/arch"
wildcard_pattern="arm"

# Time to summon the nodes with our mystical wildcard!
kubectl get nodes -o json | jq --arg key "$label_key" --arg pattern "$wildcard_pattern" '
    .items[] | select(.metadata.labels[$key] | test($pattern)) | .metadata.name + " | " + .status.allocatable.memory[:-2]'

echo "Node Name | Memory Allocatable (GB)"
echo "----------|---------------------"
kubectl get nodes -o json | jq --arg key "$label_key" --arg pattern "$wildcard_pattern" '
    .items[] | select(.metadata.labels[$key] | test($pattern)) | .metadata.name + " | " + ( .status.allocatable.memory[:-2] | tonumber / 1000 / 1000 |floor | tostring)'

```

```
#!/bin/bash

# The name of the node for which you want to calculate memory requests
node_name="kind-worker"

# Summoning the pod information from the specified node
kubectl get pods --all-namespaces -o json --field-selector spec.nodeName=$node_name | jq '[.items[] | .spec.containers[] | .resources.requests.memory // "0Mi"] | map(gsub("Mi"; " * 1024 * 1024") | gsub("Gi"; " * 1024 * 1024 * 1024") | gsub("Ki"; " * 1024")) | join(" + ") | "0 + " + .' | bc

```

```
label_key="beta.kubernetes.io/arch"
wildcard_pattern="arm"

NODES=(`kubectl get nodes -o json | jq --arg key "$label_key" --arg pattern "$wildcard_pattern" '
    .items[] | select(.metadata.labels[$key] | test($pattern)) | .metadata.name '`)

for NODE in ${NODES[@]}
do
NODE_NAME="${NODE//\"}"

POD_MEMORY_REQUESTED=`kubectl get pods --all-namespaces -o jsonpath='{.items[?(@.spec.nodeName=="'"$NODE_NAME"'")].spec.containers[*].resources.requests.memory}' | \
    tr -s '[:space:]' '\n' | \
    awk 'BEGIN{sum=0}{
        if(tolower($1) ~ /ki$/){sum += int($1)/1024} 
        else if(tolower($1) ~ /mi$/){sum += int($1)} 
        else if(tolower($1) ~ /gi$/){sum += int($1)*1024} 
        else if(tolower($1) ~ /ti$/){sum += int($1)*1048576} 
        else{sum += int($1)/1048576}
    }END{print sum "Mi"}'`

NODE_MEMORY_CAPACITY=`kubectl get node "$NODE_NAME" -o jsonpath='{.status.capacity.memory}' | \
    awk '{print int($1/1024) "Mi"}'`

echo "$NODE_NAME|$NODE_MEMORY_CAPACITY|$POD_MEMORY_REQUESTED"

done
```