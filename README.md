# ACEest Fitness & Gym — DevOps CI/CD Pipeline (Assignment 2)

> **Course:** Introduction to DevOps (CSIZG514 / SEZG514) — S2-25
> **Repository:** https://github.com/ihyth-alt/aceest-devops-project
> **Docker Hub:** https://hub.docker.com/r/ihyth32/aceest-fitness

---

## 🌐 Live Public Endpoint

### **http://136.110.151.78**

| Strategy | URL |
|---|---|
| Rolling Update (default) | http://136.110.151.78/ |
| UI (rolling) | http://136.110.151.78/ui |
| Blue-Green | http://136.110.151.78/blue-green |
| Canary Release | http://136.110.151.78/canary |
| A/B Testing | http://136.110.151.78/ab-test |
| Shadow Deployment | http://136.110.151.78/shadow |

Each path serves the HTML UI with a "Served by:" badge identifying which Kubernetes deployment handled the request. Routed via GCE Ingress on a 4-node GKE cluster in asia-south1 (Mumbai).

---

## Submission Index

| Deliverable | Location |
|---|---|
| Flask application + UI | `app.py`, `templates/`, `static/` |
| Pytest test suite (35 tests, 88% coverage) | `test_app.py`, `pytest.ini` |
| Jenkinsfile (8-stage pipeline) | `Jenkinsfile` |
| Dockerfile | `Dockerfile` |
| SonarQube configuration | `sonar-project.properties` |
| Kubernetes manifests — Minikube (local) | `k8s/` |
| Kubernetes manifests — GKE (cloud) | `k8s-cloud/` |
| Rollback + operational scripts | `scripts/` |
| Architecture, challenges, outcomes report | `docs/report.docx` |
| Live endpoint URLs | `docs/endpoints.md` |
| Pipeline + dashboard screenshots | `docs/screenshots/` |

---

## CI/CD Pipeline Stages (Jenkinsfile)

1. **Checkout** — Pulls main branch from GitHub via `github-creds`
2. **Install Dependencies** — `pip install -r requirements.txt`
3. **Lint** — `flake8 app.py --max-line-length=120`
4. **Run Tests with Coverage** — `pytest --cov=app --cov-report=xml` (35/35 passed, 88%)
5. **SonarQube Analysis** — `sonar-scanner` uploads to local server
6. **Quality Gate** — Webhook-driven, fails build if gate fails
7. **Build Docker Image** — Tags `v4.${BUILD_NUMBER}` and `latest`
8. **Push to Docker Hub** — Both tags published to public registry

---

## Deployment Strategies Implemented (GKE)

### 1. Rolling Update — `k8s-cloud/01-rolling-update.yaml`
Zero-downtime replacement with `maxSurge: 1`, `maxUnavailable: 0`.

### 2. Blue-Green — `k8s-cloud/02-blue-green.yaml`
Blue (`v4.0`) and Green (`latest`) run in parallel. Service selector switches color.

### 3. Canary Release — `k8s-cloud/03-canary.yaml`
Stable + canary pods with weighted traffic split via label-based service routing.

### 4. A/B Testing — `k8s-cloud/04-ab-testing.yaml`
Two versions behind one service for round-robin distribution.

### 5. Shadow Deployment — `k8s-cloud/05-shadow.yaml`
Production handles real traffic, shadow deployment runs latest image for parallel testing.

### Ingress — `k8s-cloud/06-ingress.yaml`
Single GCE HTTP(S) Load Balancer routes all 5 strategies through path-based rules on one public IP.

### Rollback — `scripts/rollback.ps1`
Wraps `kubectl rollout undo` with history display + status wait.

---

## Quality Metrics

| Metric | Result |
|---|---|
| Tests passing | 35 / 35 |
| Code coverage | 88.1% |
| SonarQube quality gate | ✅ Passed |
| Bugs / Vulnerabilities / Code Smells | 0 / 0 / 0 |
| Reliability / Security / Maintainability | A / A / A |
| Pipeline runtime | ~2.5 min |

---

## Architecture

```
GitHub (main branch)
        │
        ▼ (poll SCM / webhook)
Jenkins Pipeline
        │
        ├── pytest (35 tests, 88% cov)
        ├── flake8 (lint)
        ├── SonarQube (quality gate)
        └── docker build + push → Docker Hub (ihyth32/aceest-fitness:v4.X)
                │
                ▼
        GKE Cluster (asia-south1-b, 4 × e2-small)
                │
        9 Deployments × 5 strategies (rolling, blue/green, stable/canary, version-a/b, prod/shadow)
                │
                ▼
        GCE Ingress → Public IP 136.110.151.78
                │
        Path-based routing: /, /blue-green, /canary, /ab-test, /shadow
```

---

## Reproducing the Setup

### Prerequisites
- Windows 11 (Intel VT-x enabled in BIOS)
- Docker Desktop with WSL2
- Java 21 (Adoptium Temurin)
- Python 3.11+
- Jenkins 2.561 + suggested plugins
- SonarQube 9.9 LTS Community (Docker)
- Minikube + kubectl (local development)
- gcloud SDK + GKE auth plugin (cloud deployment)
- Sonar Scanner CLI

### Quick start (local)
```bash
git clone https://github.com/ihyth-alt/aceest-devops-project.git
cd aceest-devops-project
pip install -r requirements.txt
pytest test_app.py --cov=app
python app.py
# Open http://localhost:5000/ui
```

### Quick start (cloud)
```bash
gcloud container clusters create aceest-cluster \
  --num-nodes=4 --machine-type=e2-small \
  --zone=asia-south1-b --release-channel=stable

gcloud container clusters get-credentials aceest-cluster --zone=asia-south1-b

kubectl apply -f k8s-cloud/

kubectl get ingress aceest-ingress
# Wait 5–10 min for ADDRESS to populate
```

---

## Key Challenges

1. **WSL2 / VT-x disabled** — enabled Virtualisation in HP BIOS
2. **Jenkins PATH** — Python and Sonar Scanner added to *System* PATH
3. **PowerShell quoting** — wrapped sonar-scanner args in double quotes
4. **SonarQube webhook** — added `host.docker.internal:8080` for cross-container access
5. **GCP IP quota** — refactored from 5 LoadBalancers to 1 Ingress
6. **GCE stockout** — switched zone from asia-south1-a to asia-south1-b
7. **Image caching** — set `imagePullPolicy: Always` and force-deleted stale pods

Full details in `docs/report.docx`.

---

## Version History

| Version | Description |
|---|---|
| v1.0 – v3.2.4 | Tkinter desktop iterations (Assignment 1) |
| v4.0 | Migrated to Flask REST API for DevOps pipeline |
| v4.5+ | Jenkins build numbers (auto-tagged on each pipeline run) |
| v4.0-final | Final submission tag |

---

## Author

Ihyth A — `ihyth-alt` on GitHub, `ihyth32` on Docker Hub.
