kubectl create serviceaccount <service-account-name>
kubectl create clusterrolebinding <binding-name> --clusterrole=cluster-admin --serviceaccount=<namespace>:<service-account-name>
kubectl get secret $(kubectl get serviceaccount <service-account-name> -n <namespace> -o jsonpath='{.secrets[0].name}') -n <namespace> -o jsonpath='{.data.token}' | base64 --decode
kubectl config set-credentials <your-context-name> --token=<your-token>
kubectl config set-context <your-context-name> --user=<your-context-name> --cluster=<your-cluster-name>
kubectl config use-context <your-context-name>
kubectl get pods
