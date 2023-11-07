## Install Argo WF

export VERSION=v3.5.0

kubectl create namespace argo
kubectl apply -n argo -f https://github.com/argoproj/argo-workflows/releases/download/$VERSION/install.yaml

kubectl patch deployment \
  argo-server \
  --namespace argo \
  --type='json' \
  -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/args", "value": [
  "server",
  "--auth-mode=server"
]}]'

kubectl -n argo port-forward deployment/argo-server 2746:2746

## Create Argo WF

kubectl apply -f role.yaml
kubectl create -n argo sa hera
kubectl create -n argo rolebinding hera --role=hera --serviceaccount=argo:hera

kubectl apply -f secret.yaml

kubectl -n argo port-forward deployment/argo-server 2746:2746


ARGO_TOKEN="$(kubectl get secret -n argo hera.service-account-token -o=jsonpath='{.data.token}' | base64 --decode)"
echo $ARGO_TOKEN

export ARGO_SERVER='localhost:2746'
export ARGO_HTTP1=true
export ARGO_SECURE=true
export ARGO_BASE_HREF=
export ARGO_TOKEN=""
export ARGO_NAMESPACE=argo ;# or whatever your namespace is
export KUBECONFIG=/dev/null ;# recommended
export ARGOcd .._INSECURE_SKIP_VERIFY=true

## Delete Argo WF

kubectl delete -n argo -f https://github.com/argoproj/argo-workflows/releases/download/v3.4.10/install.yaml

