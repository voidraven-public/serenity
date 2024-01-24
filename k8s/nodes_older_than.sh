kubectl get nodes -o json | jq -r '.items[] | select((.metadata.creationTimestamp | fromdateiso8601) < (now - 86400) | not) | .metadata.name'
