kubectl apply -f role.yaml
kubectl create -n argo sa jenkins
kubectl create -n argo rolebinding jenkins --role=jenkins --serviceaccount=argo:jenkins

kubectl apply -f secret.yaml

ARGO_TOKEN="Bearer $(kubectl get secret -n argo jenkins.service-account-token -o=jsonpath='{.data.token}' | base64 --decode)"
echo $ARGO_TOKEN

export ARGO_SERVER='localhost:2746'
export ARGO_HTTP1=true
export ARGO_SECURE=true
export ARGO_BASE_HREF=
export ARGO_TOKEN=""
export ARGO_NAMESPACE=argo ;# or whatever your namespace is
export KUBECONFIG=/dev/null ;# recommended
export ARGOcd .._INSECURE_SKIP_VERIFY=true