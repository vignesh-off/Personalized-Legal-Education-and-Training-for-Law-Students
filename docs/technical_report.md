# Technical Report: Legal Education Intelligence Platform

## 1. Abstract
The Legal Education Intelligence Platform is an AI-powered ecosystem designed to provide personalized legal education and training for law students. It leverages Machine Learning, Natural Language Processing, and Generative AI paradigms to predict student mastery, detect dropout risks, evaluate legal writing, generate practice cases, and deploy proactive agentic interventions.

## 2. Problem Statement & Objective
**Problem:** Traditional legal education often lacks real-time personalization, leaving students without timely feedback or tailored practice scenarios.
**Objective:** Build an AI-powered legal education platform that adapts learning content, predicts mastery, detects risk, evaluates legal writing, generates practice cases, and supports tutoring/intervention.

## 3. Technology Stack
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Database**: SQLite
- **Machine Learning**: Scikit-learn (Random Forest)
- **AI Modules**: Simulated DL, NLP, SLM, GenAI, and Agentic AI modules
- **Analytics**: Plotly
- **Execution Environment**: Windows BAT scripts with Python 3.11 local `.venv`

## 4. System Architecture
The application architecture follows a decoupled microservices-inspired pattern:
**Streamlit frontend → FastAPI API → ML/DL/NLP/GenAI/Agentic services → SQLite database → Analytics dashboard**

## 5. Modules Implementation

### 5.1 Machine Learning (ML) Prediction
- **Algorithm**: Random Forest Classifier.
- **Input Features**: Assessment score, time spent, attempts, module difficulty level.
- **Target Output**: Mastery Level (Beginner, Intermediate, Expert).
- **Preprocessing**: Features are standardized using `StandardScaler` to ensure zero mean and unit variance.
- **Why Random Forest**: Random Forest was selected for its robust performance on tabular data, resistance to overfitting via bagging, and ability to handle non-linear relationships between inputs like attempts and score.

### 5.2 Deep Learning (DL) Fallback
- **Mechanism**: A simulated neural-network based comparative prediction module.
- **Function**: Acts as a cross-verification tool for the primary ML model. It outputs a mastery level accompanied by a confidence score. This complements the ML model by providing a secondary benchmark, demonstrating hybrid AI consensus logic.

### 5.3 NLP Essay Evaluation
- **Mechanism**: Keyword extraction and matching.
- **Function**: Scans student-submitted legal essays for crucial domain-specific concepts (e.g., "mens rea", "consideration"). It performs missing concept analysis and generates structured, constructive feedback along with a graded score.

### 5.4 Small Language Model (SLM) Tutor Chat
- **Mechanism**: Lightweight, offline, simulated SLM.
- **Function**: Provides instant conversational tutoring using dictionary-based and template-response mappings to explain fundamental legal concepts without requiring expensive cloud API calls.

### 5.5 Generative AI (GenAI) Cases
- **Mechanism**: Template-based legal scenario generation.
- **Function**: Dynamically creates personalized legal practice cases tailored to the student's current topic of study or weak areas, complete with probing analytical questions.

### 5.6 Agentic AI Intervention
- **Mechanism**: Proactive learning and intervention agent.
- **Function**: Audits the student's risk profile in the background. If a student is flagged as high risk (e.g., struggling with 'Contracts'), the agent recommends specific pedagogical actions and automatically drafts intervention emails for the instructor to send.

## 6. Database and Role-Based Access Control (RBAC)

### 6.1 Database Schema
The system uses SQLite. The primary table `predictions` logs all student evaluations.
- **Fields**: `id`, `student_id`, `topic`, `score`, `time_spent`, `attempts`, `difficulty_level`, `mastery_level`, `risk_level`, `next_topic`.

### 6.2 RBAC Policy
- **Student**: Restricted to live prediction, NLP essay grader, GenAI cases, Tutor Chat, and viewing only their own personal analytics.
- **Teacher**: Can run predictions for any student, perform bulk file uploads, and view the cohort analytics dashboard.
- **Admin**: Full access to all platform modules, including proactive agentic intervention monitoring and cohort analytics.

## 7. Limitations & Future Scope

### 7.1 Limitations
- GenAI, SLM, and Agentic modules are offline simulations to ensure the platform remains demo-ready without external API dependencies.
- No real external LLM (e.g., OpenAI, Gemini, Groq) is currently utilized.
- The ML dataset is synthetically generated.

### 7.2 Future Scope
- Integration with real transformer-based NLP models (e.g., BERT for legal text).
- Real SLM/LLM API integration for dynamic, non-templated text generation.
- Adaptive learning path optimization based on complex reinforcement learning.
- Persistent student profile memory using vector databases.
- Cloud deployment and Docker containerization.
