# Legal Education AI Platform

This project is a Legal Education AI Platform that predicts student mastery, risk level, and next-topic recommendations using a FastAPI backend, saved ML models, and a Streamlit dashboard.

## Features

- Student and teacher/admin login screens
- ML-based mastery prediction
- Deep-learning comparison endpoint
- Risk-level calculation
- Next legal topic recommendation
- Cohort analytics dashboard
- SQLite storage for prediction history

## Project Structure

```text
DA SC/
+-- app/
|   +-- main.py          # FastAPI backend
|   +-- database.py      # SQLite database setup and save logic
|   +-- analytics.py     # Dashboard data loading
|   +-- schemas.py       # API request/response models
+-- ml/
|   +-- train.py         # Model training script
|   +-- dl_model.py      # Deep-learning prediction logic
|   +-- models/          # Saved ML model files
+-- tests/
|   +-- test_api.py      # API tests
+-- frontend.py          # Streamlit frontend
+-- requirements.txt     # Python dependencies
+-- run_project.bat      # Windows one-click runner
+-- Dockerfile           # Docker backend runner
+-- students.db          # SQLite database
```

## Requirements

- Python 3.10 or newer
- pip
- Git, only if uploading to GitHub

## How to Run Locally

### 1. Open the project folder

```bash
cd "DA SC"
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the FastAPI backend

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend API will run at:

```text
http://127.0.0.1:8000
```

FastAPI docs:

```text
http://127.0.0.1:8000/docs
```

### 6. Run the Streamlit frontend

Open a second terminal in the same project folder, activate the virtual environment again, then run:

```bash
python -m streamlit run frontend.py
```

Frontend will run at:

```text
http://localhost:8501
```

## Windows Quick Run

On Windows, after installing dependencies, you can also run:

```bash
run_project.bat
```

This starts the backend, starts the Streamlit frontend, and opens the browser automatically.

## Login Details

Student login:

```text
Username: student
Password: student123
```

Teacher/Admin login:

```text
Username: teacher
Password: teacher123
```

## API Endpoints

### ML Prediction

```http
POST /predict
```

Example JSON:

```json
{
  "student_id": 101,
  "topic": "Contracts",
  "score": 75,
  "time_spent": 45,
  "attempts": 1,
  "difficulty_level": 3
}
```

### DL Prediction

```http
POST /predict-dl
```

Uses the same JSON body as `/predict`.

## Run Tests

```bash
pytest
```

## Docker Run

Build the Docker image:

```bash
docker build -t legal-education-ai .
```

Run the backend container:

```bash
docker run -p 8000:8000 legal-education-ai
```

The Dockerfile runs only the FastAPI backend. To use the Streamlit frontend, run it separately with:

```bash
python -m streamlit run frontend.py
```

## Uploading to GitHub

Before uploading, do not commit local environment or cache folders such as:

```text
.venv/
__pycache__/
.pytest_cache/
```

Recommended GitHub upload steps:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
git push -u origin main
```

If `students.db` contains demo or private student data, remove it from the commit and let the app create a fresh database when it runs.

## Notes

- Keep the backend running while using the Streamlit dashboard.
- The frontend calls the backend at `http://127.0.0.1:8000`.
- Saved ML model files must remain inside `ml/models/` for backend prediction to work.
