# ACEest Fitness — Live Cluster Endpoints

## 🌐 Public URL (GKE on GCP)

### **http://136.110.151.78**

| # | Strategy | Path | Full URL |
|---|---|---|---|
| 1 | Rolling Update (default) | `/` | http://136.110.151.78/ |
| 2 | UI (rolling) | `/ui` | http://136.110.151.78/ui |
| 3 | Blue-Green | `/blue-green` | http://136.110.151.78/blue-green |
| 4 | Canary Release | `/canary` | http://136.110.151.78/canary |
| 5 | A/B Testing | `/ab-test` | http://136.110.151.78/ab-test |
| 6 | Shadow Deployment | `/shadow` | http://136.110.151.78/shadow |

Each strategy URL serves the HTML UI with a "Served by:" badge identifying the deployment that handled the request.

---

## Cluster Details

| Attribute | Value |
|---|---|
| Cloud Provider | Google Cloud Platform |
| Region / Zone | asia-south1-b (Mumbai) |
| Cluster Name | aceest-cluster |
| Project ID | aceest-ihyth-2026 |
| Node Count | 4 |
| Machine Type | e2-small |
| Kubernetes Version | v1.33.8-gke.1026000 |
| Public IP | 136.110.151.78 |
| Routing | GCE HTTP(S) Load Balancer (Ingress) |

---

## Reproducing the Setup

```bash
# 1. Clone repository
git clone https://github.com/ihyth-alt/aceest-devops-project.git
cd aceest-devops-project

# 2. Authenticate with GCP
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 3. Create cluster
gcloud container clusters create aceest-cluster \
  --num-nodes=4 --machine-type=e2-small \
  --zone=asia-south1-b --release-channel=stable

# 4. Get credentials
gcloud container clusters get-credentials aceest-cluster --zone=asia-south1-b

# 5. Deploy all strategies + Ingress
kubectl apply -f k8s-cloud/

# 6. Wait for Ingress IP (5-10 min)
kubectl get ingress aceest-ingress -w

# 7. Test
curl http://INGRESS_IP/blue-green
```

---

## Local Minikube Endpoints

For local-only development. Minikube assigns random ports per session.

```bash
minikube start --driver=docker
kubectl apply -f k8s/
minikube service aceest-service
```

| Strategy | Service | NodePort |
|---|---|---|
| Rolling Update | `aceest-service` | 30080 |
| Blue-Green | `aceest-bg-service` | 30081 |
| Canary | `aceest-canary-service` | 30082 |
| A/B Testing | `aceest-version-a-svc` / `b-svc` | 30083, 30084 |
| Shadow | `aceest-prod-svc` / `shadow-svc` | 30085, 30086 |
