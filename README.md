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
label_key="beta.kubernetes.io/arch"
wildcard_pattern="arm"

echo "NICE_NODE_NAME|NODE_NAME|NODE_MEMORY_CAPACITY Mi|POD_MEMORY_REQUESTED Mi|Percentage"


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
    }END{print sum}'`

NODE_MEMORY_CAPACITY=`kubectl get node "$NODE_NAME" -o jsonpath='{.status.capacity.memory}' | \
    awk '{print int($1/1024)}'`

NICE_NODE_NAME=`kubectl get nodes $NODE_NAME -o jsonpath='{.metadata.labels.name}'`

result=$(echo "scale=2; $POD_MEMORY_REQUESTED / $NODE_MEMORY_CAPACITY" | bc)
percentage=$(echo "scale=2; $result * 100" | bc)
echo "$NICE_NODE_NAME|$NODE_NAME|$NODE_MEMORY_CAPACITY Mi|$POD_MEMORY_REQUESTED Mi|${percentage}%"

done
```