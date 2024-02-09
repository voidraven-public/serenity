# kind
kind create cluster

# wordpress
helm install wordpress oci://registry-1.docker.io/bitnamicharts/wordpress --set service.type=ClusterIP
sleep 180
kubectl get pods
echo "Username: user"
echo "Password: $(kubectl get secret --namespace default wordpress -o jsonpath="{.data.wordpress-password}" | base64 -d)"
kubectl port-forward --namespace default svc/wordpress 8080:80 
# WordPress URL: http://127.0.0.1:8080/
# WordPress Admin URL: http://127.0.0.1:8080/admin (use username and password from above)

# nextcloud 
helm repo add nextcloud https://nextcloud.github.io/helm/
helm repo update
helm install nextcloud nextcloud/nextcloud
export APP_HOST=127.0.0.1
export APP_PASSWORD=$(kubectl get secret --namespace default nextcloud -o jsonpath="{.data.nextcloud-password}" | base64 --decode)
echo $APP_PASSWORD
kubectl port-forward --namespace default svc/nextcloud 8081:8080


# delete kind cluster
kind delete cluster

