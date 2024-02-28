# install the CRDs first
linkerd install --crds | kubectl apply -f -

# install the Linkerd control plane once the CRDs have been installed
linkerd install | kubectl apply -f -

kubectl create namespace mesh1
kubectl create namespace mesh2
kubectl create namespace nomesh1

kubectl apply -f - <<EOF
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: mesh1
  namespace: mesh1
spec:
  rules:
  - http:
      paths:
      - backend:
          service:
            name: mesh1
            port:
              number: 80
        path: /
        pathType: Prefix
---
apiVersion: v1
kind: Service
metadata:
  name: mesh1
  namespace: mesh1
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: nginx
  sessionAffinity: None
  type: ClusterIP
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  namespace: mesh1
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      volumes:
      - name: nginx-content
        configMap:
          name: nginx-config
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
        livenessProbe:
          httpGet:
            path: /health.html
            port: 80
          initialDelaySeconds: 15
          periodSeconds: 20
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health.html
            port: 80
          initialDelaySeconds: 15
          periodSeconds: 20
          failureThreshold: 3
        volumeMounts:
          - name: nginx-content
            mountPath: /usr/share/nginx/html
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
  namespace: mesh1
data:
  default.html: |
    <!DOCTYPE html>
    <html>
    <body>
      <h1>Hello, World!</h1>
    </body>
    </html>
  health.html: |
    <html>
    <body>
      <h1>Health Check: OK</h1>
    </body>
    </html>

EOF

kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  namespace: mesh2
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 15
          periodSeconds: 20
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 15
          periodSeconds: 20
          failureThreshold: 3
EOF

kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  namespace: nomesh1
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 15
          periodSeconds: 20
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 15
          periodSeconds: 20
          failureThreshold: 3
EOF


kubectl apply -f - <<EOF

apiVersion: linkerd.io/v1alpha1
kind: Tap
metadata:
  name: tap-mesh1
spec:
  selector:
    matchLabels:
      app: nginx
  namespaces:
  - mesh1
---
apiVersion: linkerd.io/v1alpha1
kind: Tap
metadata:
  name: tap-mesh2
spec:
  selector:
    matchLabels:
      app: nginx
  namespaces:
  - mesh2

EOF


kubectl apply -f - <<EOF
---
apiVersion: policy.linkerd.io/v1beta1
kind: Server
metadata:
  namespace: mesh1
  name: nginx
spec:
  podSelector:
    matchLabels:
      app: nginx
  port: 80
---
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: nginx
  namespace: mesh1
spec:
  parentRefs:
    - name: nginx
      kind: Server
      group: policy.linkerd.io
  rules:
    - matches:
      - path:
          value: "/health.html"
        method: GET
---
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: nginx-all
  namespace: mesh1
spec:
  parentRefs:
    - name: nginx
      kind: Server
      group: policy.linkerd.io
  rules:
    - matches:
      - path:
          value: "/"
---
apiVersion: policy.linkerd.io/v1alpha1
kind: NetworkAuthentication
metadata:
  name: nginx
  namespace: mesh1
spec:
  networks:
  - cidr: 0.0.0.0/0

---
apiVersion: policy.linkerd.io/v1alpha1
kind: AuthorizationPolicy
metadata:
  name: nginx
  namespace: mesh1
spec:
  targetRef:
    group: policy.linkerd.io
    kind: HTTPRoute
    name: nginx
  requiredAuthenticationRefs:
    - name: nginx
      kind: NetworkAuthentication
      group: policy.linkerd.io

---
apiVersion: policy.linkerd.io/v1alpha1
kind: MeshTLSAuthentication
metadata:
  name: nginx
spec:
  identities: ["*"]

---
apiVersion: policy.linkerd.io/v1alpha1
kind: AuthorizationPolicy
metadata:
  name: meshnginx
spec:
  targetRef:
    group: policy.linkerd.io
    kind: Server
    name: nginx
  requiredAuthenticationRefs:
    - name: nginx
      kind: MeshTLSAuthentication
      group: policy.linkerd.io
EOF





kubectl get service nginx -n mesh1 -o jsonpath='{.spec.clusterIP}' | xargs -I {ip} sed "s/SERVICE_NAME/{ip}/" linkerd-policy.yaml -i > mesh1-policy.yaml
kubectl get service nginx -n mesh2 -o jsonpath='{.spec.clusterIP}' | xargs -I {ip} sed "s/SERVICE_NAME/{ip}/" linkerd-policy.yaml -i > mesh2-policy.yaml

kubectl annotate namespace mesh2 "linkerd.io/inject=enabled"
kubectl annotate namespace default "config.linkerd.io/default-inbound-policy=all-authenticated"
kubectl annotate namespace mesh1 "config.linkerd.io/default-inbound-policy=all-authenticated"
kubectl annotate namespace mesh1 "config.linkerd.io/default-inbound-policy=deny"

kubectl annotate deploy nginx -n mesh2 "linkerd.io/inject=enabled"
kubectl annotate deploy nginx -n mesh1 "config.linkerd.io/default-inbound-policy=all-authenticated"
kubectl annotate deploy nginx -n default "config.linkerd.io/default-inbound-policy=all-authenticated"
kubectl annotate deploy ingress-nginx-controller -n ingress-nginx "linkerd.io/inject=enabled"


linkerd.io/inject: enabled