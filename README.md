<<<<<<< HEAD
# ACEest Fitness & Gym — DevOps CI/CD Pipeline

> **Course:** Introduction to DevOps (CSIZG514 / SEZG514 / SEUSZG514) — S2-25  
> **Assignment:** Implementing Automated CI/CD Pipelines for ACEest Fitness & Gym

---

## Project Overview

ACEest Fitness & Gym is a Flask-based REST API that manages fitness programs, client profiles, and calorie calculations. This project demonstrates a full DevOps lifecycle including version control, unit testing, containerisation, Jenkins BUILD integration, and a fully automated GitHub Actions CI/CD pipeline.

---

## Project Structure

```
aceest-devops/
├── app.py                          # Flask application (core API)
├── requirements.txt                # Python dependencies
├── test_app.py                     # Pytest unit tests
├── Dockerfile                      # Docker container definition
├── Jenkinsfile                     # Jenkins BUILD pipeline
├── README.md                       # This file
└── .github/
    └── workflows/
        └── main.yml                # GitHub Actions CI/CD pipeline
```

---

## Local Setup and Execution

### Prerequisites
- Python 3.11+
- pip
- Docker (optional, for containerised run)

### Step 1 — Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/aceest-devops.git
cd aceest-devops
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

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/programs` | List all fitness programs |
| GET | `/programs/<name>` | Get workout & diet for a program |
| POST | `/calculate` | Calculate daily calories |
| POST | `/clients` | Register a new client |

### Example — Calculate Calories
```bash
curl -X POST http://localhost:5000/calculate \
  -H "Content-Type: application/json" \
  -d '{"program": "Fat Loss (FL)", "weight": 70}'
```

Response:
```json
{
  "program": "Fat Loss (FL)",
  "weight_kg": 70,
  "estimated_calories": 1540,
  "calorie_factor": 22
}
```

---

## Running Tests Manually

```bash
pytest test_app.py -v
```

This runs all unit tests and shows a detailed pass/fail report. The test suite covers:
- All API routes (GET and POST)
- Correct calorie calculations for all three programs
- Validation — missing fields, invalid programs, zero/negative weight
- Data integrity checks on the PROGRAMS dictionary

---

## Docker — Build and Run

### Build the image
```bash
docker build -t aceest-fitness-app .
```

### Run the container
```bash
docker run -p 5000:5000 aceest-fitness-app
```

The app will be accessible at `http://localhost:5000` inside the container.

The Dockerfile uses `python:3.11-slim` to keep the image size minimal and copies only the required files into the container.

---

## Jenkins BUILD Integration

Jenkins is used as a secondary quality gate to ensure the code builds and tests correctly in a controlled CI environment.

### Jenkins Pipeline Stages (defined in `Jenkinsfile`)

| Stage | What it does |
|-------|-------------|
| Checkout | Pulls the latest code from GitHub |
| Install Dependencies | Runs `pip install -r requirements.txt` |
| Lint | Checks code style with `flake8` |
| Test | Executes `pytest test_app.py -v` |
| Build Docker Image | Builds the Docker image as a final validation |

### How Jenkins connects to GitHub
1. In Jenkins, create a new **Pipeline** project.
2. Under **Pipeline → Definition**, select **Pipeline script from SCM**.
3. Set SCM to **Git** and enter your GitHub repository URL.
4. Set the branch to `main`.
5. Jenkins will automatically detect and use the `Jenkinsfile` in the root of the repo.
6. Every time a build is triggered (manually or via webhook), Jenkins pulls the latest code and runs all stages defined in the Jenkinsfile.

---

## GitHub Actions — Automated CI/CD Pipeline

The pipeline is defined in `.github/workflows/main.yml` and triggers automatically on every `push` or `pull_request` to the `main` branch.

### Pipeline Stages

| Stage | Tool | Description |
|-------|------|-------------|
| Checkout | `actions/checkout@v3` | Pulls the latest source code |
| Set up Python | `actions/setup-python@v4` | Installs Python 3.11 |
| Install Dependencies | pip | Installs from `requirements.txt` |
| Lint | flake8 | Checks for syntax/style errors |
| Run Tests | pytest | Executes all unit tests |
| Build Docker Image | docker | Builds the container to confirm it works |

### How to view pipeline results
1. Go to your GitHub repository.
2. Click the **Actions** tab.
3. Every push will show a new workflow run with green (pass) or red (fail) status for each stage.

---

## Git Commit Strategy

Commits in this project follow a structured format for readability:

```
feat:    New feature added
fix:     Bug fix
test:    Test added or updated
docker:  Dockerfile or container change
ci:      GitHub Actions or Jenkins update
docs:    README or documentation update
```
=======
# aceest-devops-project
Devops assessment
>>>>>>> ddef4ff70c30fccad4f63714d3d6217d4d843c5d
