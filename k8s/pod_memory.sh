#!/bin/bash

# Node name as an argument
NODE_NAME=$1
 echo $NODE_NAME

# if [ -z "$NODE_NAME" ]; then
#     echo "Usage: $0 <node-name>"
#     exit 1
# fi

# # Get all pods running on the specified node and sum their memory requests
kubectl get pods --all-namespaces -o jsonpath='{.items[?(@.spec.nodeName=="'"$NODE_NAME"'")].spec.containers[*].resources.requests.memory}' | \
    tr -s '[:space:]' '\n' | \
    awk 'BEGIN{sum=0}{
        if(tolower($1) ~ /ki$/){sum += int($1)/1024} 
        else if(tolower($1) ~ /mi$/){sum += int($1)} 
        else if(tolower($1) ~ /gi$/){sum += int($1)*1024} 
        else if(tolower($1) ~ /ti$/){sum += int($1)*1048576} 
        else{sum += int($1)/1048576}
    }END{print sum "Mi"}'

