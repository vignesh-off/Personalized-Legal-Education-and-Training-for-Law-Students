# Legal Education Intelligence Platform

## Problem Statement
Personalized Legal Education and Training for Law Students. Traditional legal education often lacks real-time personalization, leaving students without timely feedback or tailored practice scenarios.

## Objective
Build an AI-powered legal education platform that adapts learning content, predicts mastery, detects risk, evaluates legal writing, generates practice cases, and supports tutoring/intervention.

## Tech Stack
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Database**: SQLite
- **Machine Learning**: Scikit-learn (Random Forest)
- **AI Modules**: Simulated DL, NLP, SLM, GenAI, and Agentic AI modules
- **Analytics**: Plotly
- **Execution**: Windows BAT launcher

## Architecture
Streamlit frontend → FastAPI API → ML/DL/NLP/GenAI/Agentic services → SQLite database → analytics dashboard

## Folder Structure
- `frontend.py`: Streamlit frontend application.
- `app/main.py`: FastAPI application entry point and endpoint definitions.
- `app/schemas.py`: Pydantic models for API request/response validation.
- `app/database.py`: SQLite database connection and query functions.
- `app/analytics.py`: Functions to load historical data for Plotly analytics.
- `app/services/nlp_service.py`: NLP logic for essay evaluation and keyword extraction.
- `app/services/llm_service.py`: GenAI and SLM simulation for scenario generation and tutor chat.
- `app/agents/tutor_agent.py`: Agentic AI logic for proactive student risk audits and interventions.
- `ml/train.py`: Script to generate synthetic data and train the Random Forest model.
- `ml/dl_model.py`: Neural-network-based comparative prediction and confidence scoring.
- `ml/models/`: Directory for saved trained model artifacts (e.g., `model.joblib`, `scaler.joblib`).
- `requirements.txt`: Python package dependencies.
- `run_project.bat`: Windows batch script to launch the application.
- `stop_project.bat`: Windows batch script to gracefully stop the application processes.

## Key Modules
- **Machine Learning (ML)**: Utilizes a Random Forest Classifier to predict student mastery based on scores, time spent, attempts, and difficulty level.
- **Deep Learning (DL)**: A neural-network-based comparative prediction module that acts as a fallback and provides a secondary confidence score to complement the ML model.
- **NLP**: Evaluates legal essays through keyword extraction, concept detection, missing concept analysis, and generates structured feedback.
- **Small Language Model (SLM)**: Simulates an offline tutor chat using dictionary/template responses for lightweight legal concept definitions.
- **Generative AI (GenAI)**: Template-based generation of personalized legal case scenarios for targeted student practice.
- **Agentic AI**: A proactive learning/intervention agent that audits student risk profiles, suggesting actions or drafting emails for early intervention.

## Role-Based Access Control (RBAC)
- **Student**: Access to live prediction, NLP essay grading, GenAI case generation, Tutor Chat, and strictly limited to their own personal analytics.
- **Teacher**: Access to student predictions, bulk file uploads, and full cohort analytics.
- **Admin**: Access to all features, full cohort analytics, and agentic intervention monitoring.

## Database Schema
The platform uses a local SQLite database (`students.db`) featuring a `predictions` table.
- **Fields**: `id` (PK), `student_id`, `topic`, `score`, `time_spent`, `attempts`, `difficulty_level`, `mastery_level`, `risk_level`, `next_topic`.

## How to Run
*(Note: Python 3.11 is strictly required and must be added to your system PATH)*

1. **First-time model training:**
   ```cmd
   .venv\Scripts\python.exe ml\train.py
   ```

2. **Start the Platform:**
   ```cmd
   run_project.bat
   ```
   *(One-click launcher that creates the virtual environment, installs dependencies, and starts the servers).*

3. **Open the Application:**
   Navigate to `http://localhost:8501` in your web browser.

4. **Stop the Platform:**
   ```cmd
   stop_project.bat
   ```

## Limitations & Deployment
- **Simulations**: GenAI, SLM, and Agentic modules are currently offline simulations (no external API required).
- **Deployment**: The included `Dockerfile` is optional deployment support if you intend to run this on a cloud container service.
- **Dataset**: The dataset and model are synthetic.

## Future Scope
- Integration with real transformer-based NLP models.
- Real SLM/LLM API integration for dynamic text generation.
- Adaptive learning path optimization based on continuous student profiling.
- Advanced student profile memory across multiple sessions.
- Cloud deployment and containerization via Docker.
