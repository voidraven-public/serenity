# Kind
`kind create cluster`

# Wordpress
```
helm install wordpress oci://registry-1.docker.io/bitnamicharts/wordpress --set service.type=ClusterIP
sleep 180
kubectl get pods
echo "Username: user"
echo "Password: $(kubectl get secret --namespace default wordpress -o jsonpath="{.data.wordpress-password}" | base64 -d)"
kubectl port-forward --namespace default svc/wordpress 8080:80 
```

WordPress URL: http://127.0.0.1:8080/

WordPress Admin URL: http://127.0.0.1:8080/admin (use username and password from above)

# Nextcloud 
```
helm repo add nextcloud https://nextcloud.github.io/helm/
helm repo update
helm install nextcloud nextcloud/nextcloud
export APP_HOST=127.0.0.1
export APP_PASSWORD=$(kubectl get secret --namespace default nextcloud -o jsonpath="{.data.nextcloud-password}" | base64 --decode)
echo "Login: admin / $APP_PASSWORD"
kubectl port-forward --namespace default svc/nextcloud 8081:8080
```

nextcloud url http://127.0.0.1:8081
user: admin
password: above from APP_PASSWORD

# Show pods
```
kubectl get pods

NAME                         READY   STATUS    RESTARTS   AGE
nextcloud-8965f848d-bs6fx    1/1     Running   0          40m
wordpress-56889c88d5-gngkx   1/1     Running   0          50m
wordpress-mariadb-0          1/1     Running   0          50m
```


# Delete kind cluster

`kind delete cluster`


# Set up K3s On VMS (3)

https://k3s.io/

Note: Install docker inside each VM.

## On VM1
1. Download K3s - latest release: x86_64, ARMv7, and ARM64 are supported. https://github.com/k3s-io/k3s/releases/latest
2. Run server
```
sudo k3s server &
# Kubeconfig is written to /etc/rancher/k3s/k3s.yaml
sudo k3s kubectl get node
```

## On VM2
1. Download K3s - latest release: x86_64, ARMv7, and ARM64 are supported. https://github.com/k3s-io/k3s/releases/latest
2. Run Agent
```
# NODE_TOKEN comes from /var/lib/rancher/k3s/server/node-token on your server
sudo k3s agent --server https://myserver:6443 --token ${NODE_TOKEN}
```

## On VM3
1. Download K3s - latest release: x86_64, ARMv7, and ARM64 are supported. https://github.com/k3s-io/k3s/releases/latest
2. Run Agent
```
# NODE_TOKEN comes from /var/lib/rancher/k3s/server/node-token on your server
sudo k3s agent --server https://myserver:6443 --token ${NODE_TOKEN}
```
