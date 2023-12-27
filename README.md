# k8s
# k8s

###
```
# memory percentage requested for each node in a Kubernetes cluster
kubectl describe nodes | grep -A 3 "Resource .*Requests .*Limits" | awk '/memory/ {if ($2 ~ /G$/) {print $2*1024} else {print $2}}' | awk '{if ($3 ~ /G$/) {print $1, $2/($3*1024)*100} else {print $1, $2/$3*100}}'
```