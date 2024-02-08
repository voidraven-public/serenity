kubectl create serviceaccount <service-account-name>
kubectl create clusterrolebinding <binding-name> --clusterrole=cluster-admin --serviceaccount=<namespace>:<service-account-name>
kubectl get secret $(kubectl get serviceaccount <service-account-name> -n <namespace> -o jsonpath='{.secrets[0].name}') -n <namespace> -o jsonpath='{.data.token}' | base64 --decode
kubectl config set-credentials <your-context-name> --token=<your-token>
kubectl config set-context <your-context-name> --user=<your-context-name> --cluster=<your-cluster-name>
kubectl config use-context <your-context-name>
kubectl get pods



kubectl create namespace scaffold
kubectl create serviceaccount svcscaffold --namespace scaffold
kubectl create rolebinding svcscaffold-admin --namespace scaffold --clusterrole=cluster-admin --serviceaccount=scaffold:svcscaffold
kubectl create secret generic svc-account-token-scaffold --from-literal=token=$(kubectl create token --serviceaccount=scaffold/svcscaffold) -n scaffold
kubectl get secrets --namespace scaffold -o jsonpath='{.items[?(@.metadata.annotations["kubernetes.io/service-account.name"] == "svcscaffold")].metadata.name}'
kubectl get secret <secret-name> --namespace scaffold -o jsonpath='{.data.token}' | base64 -d

