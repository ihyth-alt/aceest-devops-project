# ACEest Fitness & Gym — DevOps CI/CD Pipeline

> **Course:** Introduction to DevOps (CSIZG514 / SEZG514 / SEUSZG514) — S2-25
> **Assignment:** Implementing Automated CI/CD Pipelines for ACEest Fitness & Gym
> **Repository:** https://github.com/ihyth-alt/aceest-devops-project

---

## Project Overview

ACEest Fitness & Gym is a Flask-based REST API that manages fitness programs,
client profiles, and calorie calculations. This project demonstrates a complete
DevOps lifecycle — from local development through version control, unit testing,
containerisation, Jenkins BUILD integration, and a fully automated GitHub Actions
CI/CD pipeline.

---

## Version History (VCS Strategy)

This repository tracks the full evolution of the ACEest application using
descriptive Git commits. Each version was committed separately to demonstrate
industry-standard version control practices.

| Version | Description |
|---------|-------------|
| v1.0 | Basic program display with tkinter UI |
| v1.1 | Added client profile inputs and calorie calculator |
| v1.1.2 | Added CSV export and matplotlib progress chart |
| v2.0.1 | Added SQLite database for client storage |
| v2.1.2 | Added load client and save progress features |
| v2.2.1 | Added progress chart visualisation |
| v2.2.4 | Enhanced UI and additional features |
| v3.0.1 | Added login system and workout tracking |
| v3.1.2 | Added PDF report generation and membership billing |
| v3.2.4 | Full featured app with metrics and exercise tracking |
| v4.0 | **Migrated to Flask REST API for DevOps pipeline** |

---

## Project Structure

```
aceest-devops-project/
├── app.py                          # Flask application (core REST API)
├── requirements.txt                # Python dependencies
├── test_app.py                     # Pytest unit test suite (35 tests)
├── Dockerfile                      # Docker container definition
├── Jenkinsfile                     # Jenkins BUILD pipeline definition
├── README.md                       # This file
└── .github/
    └── workflows/
        └── main.yml                # GitHub Actions CI/CD pipeline
```

---

## Phase 1 — Flask Application

The application exposes the following REST API endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check — returns API status |
| GET | `/programs` | Lists all available fitness programs |
| GET | `/programs/<name>` | Returns workout and diet plan for a program |
| POST | `/calculate` | Calculates estimated daily calories |
| POST | `/clients` | Registers a new client |

### Available Programs
- **Fat Loss (FL)** — 22 kcal per kg body weight
- **Muscle Gain (MG)** — 35 kcal per kg body weight
- **Beginner (BG)** — 26 kcal per kg body weight

---

## Phase 2 — Local Setup and Execution

### Prerequisites
- Python 3.11+
- pip
- Docker (optional, for containerised run)
- Git

### Step 1 — Clone the repository
```bash
git clone https://github.com/ihyth-alt/aceest-devops-project.git
cd aceest-devops-project
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Run the Flask application
```bash
python app.py
```

The API will be available at: `http://localhost:5000`

### Example API calls

**Check API is running:**
```bash
curl http://localhost:5000/
```

**Calculate calories:**
```bash
curl -X POST http://localhost:5000/calculate \
  -H "Content-Type: application/json" \
  -d "{\"program\": \"Fat Loss (FL)\", \"weight\": 70}"
```

**Expected response:**
```json
{
  "program": "Fat Loss (FL)",
  "weight_kg": 70.0,
  "estimated_calories": 1540,
  "calorie_factor": 22
}
```

---

## Phase 3 — Running Tests Manually

```bash
pytest test_app.py -v
```

The test suite contains **35 unit tests** covering:
- All API route responses (GET and POST)
- Correct calorie calculations for all three programs
- Input validation — missing fields, invalid programs, zero and negative weight
- HTTP status code verification (200, 201, 400, 404, 415)
- Data integrity checks on the PROGRAMS dictionary

**Expected output:**
```
35 passed in 0.XX seconds
```

---

## Phase 4 — Docker Containerisation

The Dockerfile uses `python:3.11-slim` for a minimal, secure image.

### Build the Docker image
```bash
docker build -t aceest-fitness-app .
```

### Run the container
```bash
docker run -p 5000:5000 aceest-fitness-app
```

The app will be accessible at `http://localhost:5000`

### Why Docker?
Docker eliminates the "it works on my machine" problem by packaging the Flask
application, its dependencies, and runtime environment into a single portable
image. The same image runs identically on a developer's laptop, the Jenkins
BUILD server, and any production environment.

---

## Phase 5 — Jenkins BUILD Integration

Jenkins is configured as a secondary quality gate that pulls code from GitHub
and validates it in a clean, controlled build environment.

### Jenkins Pipeline Stages (Jenkinsfile)

| Stage | What it does |
|-------|-------------|
| Checkout | Pulls latest code from GitHub via `checkout scm` |
| Install Dependencies | Runs `pip install -r requirements.txt` |
| Lint | Checks code style with `flake8` |
| Test | Executes `pytest test_app.py -v` |
| Build Docker Image | Builds the Docker image as final validation |

### How to configure Jenkins to connect to this repository

1. Install Jenkins locally or use a Docker-based Jenkins server
2. Install the following Jenkins plugins: **Git Plugin**, **Pipeline Plugin**
3. Create a new **Pipeline** project in Jenkins
4. Under **Pipeline → Definition** select **Pipeline script from SCM**
5. Set SCM to **Git** and enter the repository URL:
   `https://github.com/ihyth-alt/aceest-devops-project.git`
6. Set the branch to `main`
7. Jenkins automatically detects and uses the `Jenkinsfile` in the repo root
8. Click **Build Now** to trigger a manual build

### Jenkins and GitHub Integration Logic

```
Developer pushes code to GitHub
        │
        ▼
GitHub notifies Jenkins via Webhook (or Jenkins polls GitHub)
        │
        ▼
Jenkins pulls latest code from GitHub
        │
        ▼
Jenkins runs Jenkinsfile pipeline stages:
  1. Checkout → 2. Install → 3. Lint → 4. Test → 5. Docker Build
        │
        ▼
BUILD SUCCESS / FAILURE reported in Jenkins dashboard
```

Jenkins acts as a controlled BUILD environment separate from the developer's
machine, ensuring code integrates correctly before it reaches production.

---

## Phase 6 — GitHub Actions CI/CD Pipeline

The pipeline is defined in `.github/workflows/main.yml` and triggers
automatically on every `push` or `pull_request` to the `main` branch.

### Pipeline Stages

| Stage | Tool | Description |
|-------|------|-------------|
| Checkout | `actions/checkout@v3` | Pulls the latest source code |
| Set up Python | `actions/setup-python@v4` | Installs Python 3.11 on the runner |
| Install Dependencies | pip | Installs all packages from `requirements.txt` |
| Lint | flake8 | Checks for syntax and style errors in `app.py` |
| Run Pytest | pytest | Executes all 35 unit tests |
| Build Docker Image | docker | Builds the container to confirm it assembles correctly |

### GitHub Actions Integration Logic

```
Every git push or pull_request to main branch
        │
        ▼
GitHub Actions runner (ubuntu-latest) spins up
        │
        ▼
Pipeline stages execute in sequence:
  Checkout → Setup Python → Install → Lint → Test → Docker Build
        │
        ├── All stages pass → Green checkmark ✅ on commit
        │
        └── Any stage fails → Red X ❌ — push is flagged, team is notified
```

### How to view pipeline results
1. Go to the repository on GitHub
2. Click the **Actions** tab
3. Every push shows a workflow run with green (pass) or red (fail) per stage
4. Click any run to see detailed logs for each stage

---

## Git Commit Convention

All commits in this project follow a structured format:

| Prefix | Meaning |
|--------|---------|
| `feat:` | New feature or version added |
| `fix:` | Bug fix |
| `test:` | Test added or updated |
| `docker:` | Dockerfile or container change |
| `ci:` | GitHub Actions or Jenkins update |
| `docs:` | README or documentation update |
