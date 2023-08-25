# Pre-requisites

- [minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [helm](https://helm.sh/docs/intro/install/)
- [istioctl](https://istio.io/latest/docs/setup/getting-started/#download)

# Setup

Start minikube

```sh
minikube start
```

Install cert-manager

```sh
# Add the Jetstack Helm repository
helm repo add jetstack https://charts.jetstack.io

# Install cert-manager
helm install cert-manager jetstack/cert-manager --version v1.12.0 --namespace cert-manager --create-namespace --set installCRDs=true
```

Install Istio-Operator and Istio control plane

```sh
istioctl operator init
kubectl apply -f - <<EOF
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  namespace: istio-system
  name: istiocontrolplane
spec:
  profile: default
EOF
```

Optional: Enable Istio injection (deploys a sidecard but adds no functionality in the current state).

```sh
kubectl label namespace ztp istio-injection=enabled
```

Install ZTP Browser

```sh
helm install ztp-browser . -n ztp --create-namespace
```

## Uninstall

```sh
helm uninstall ztp-browser -n ztp
```

## Troubleshooting TLS Certificates

```
openssl s_client -connect ztp.dev:443 -servername ztp.dev
```

Resetting cert-manager

```bash
helm uninstall cert-manager -n cert-manager
kubectl delete crd --all -n cert-manager
kubectl delete ns cert-manager
```

You can also try checking your istio-ingressgateway logs for TLS errors

```bash
istioctl pc log <istio-ingressgateway-pod> -n istio-system --level debug
kubectl logs -f -n istio-system services/istio-ingressgateway
```

## Getting the TLS certs

```bash
mkdir -p certs
kubectl get secret -n istio-system ztp-tls -o jsonpath='{.data.tls\.crt}' | base64 --decode > certs/ztp.crt
kubectl get secret -n istio-system ztp-tls -o jsonpath='{.data.tls\.key}' | base64 --decode > certs/ztp.key
```

You can add the `ztp.crt` to your local keychain or browser to trust them!

## Installing Keycloak

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
```

## Build the ztp-browser image in for rancher-desktop

```bash
nerdctl -n k8s.io build -t base2/ztp-browser:latest .
```
