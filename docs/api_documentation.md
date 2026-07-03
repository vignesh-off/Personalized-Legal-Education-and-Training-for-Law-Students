# API Documentation

The FastAPI backend runs locally on `http://127.0.0.1:8000`.

## 1. Predict Mastery
- **Endpoint**: `/predict`
- **Method**: `POST`
- **Purpose**: Predicts the student's mastery level using the Random Forest ML model, computes dropout risk, recommends the next topic, and saves the record to the SQLite database.
- **Request Body**:
  ```json
  {
    "student_id": 101,
    "topic": "Contracts",
    "score": 85.5,
    "time_spent": 45.0,
    "attempts": 1,
    "difficulty_level": 3
  }
  ```
- **Response Body**:
  ```json
  {
    "mastery_level": "Expert",
    "next_topic_recommendation": "Torts",
    "risk_level": "Low"
  }
  ```

## 2. Predict Mastery (Deep Learning Fallback)
- **Endpoint**: `/predict-dl`
- **Method**: `POST`
- **Purpose**: Provides a comparative secondary prediction and confidence score using a simulated DL neural network.
- **Request Body**: Same as `/predict`
- **Response Body**:
  ```json
  {
    "dl_mastery_level": "Expert",
    "dl_confidence": 92.5,
    "dl_message": "DL Model predicts Expert with 92.5% confidence."
  }
  ```

## 3. Evaluate Essay (NLP)
- **Endpoint**: `/evaluate-essay`
- **Method**: `POST`
- **Purpose**: Evaluates a student's legal essay based on keyword extraction, missing concept analysis, and returns feedback.
- **Request Body**:
  ```json
  {
    "student_id": 101,
    "topic": "Contracts",
    "essay_text": "A contract requires an offer and an acceptance."
  }
  ```
- **Response Body**:
  ```json
  {
    "score": 60.0,
    "feedback": "Good effort. You mentioned some good points like offer, acceptance, but missed a few others.",
    "key_concepts_found": ["offer", "acceptance"]
  }
  ```

## 4. Generate Legal Scenario (GenAI)
- **Endpoint**: `/generate-scenario`
- **Method**: `POST`
- **Purpose**: Generates a custom legal scenario and probing questions to help students practice weak topics.
- **Request Body**:
  ```json
  {
    "student_id": 101,
    "weak_topic": "Contracts"
  }
  ```
- **Response Body**:
  ```json
  {
    "scenario_text": "Alice offers to sell her car...",
    "questions": ["Did Bob's reply constitute a valid acceptance?", "Is Alice in breach of contract?"]
  }
  ```

## 5. Tutor Chat (SLM)
- **Endpoint**: `/tutor-chat`
- **Method**: `POST`
- **Purpose**: Provides immediate definitions and explanations for legal concepts via a simulated Small Language Model.
- **Request Body**:
  ```json
  {
    "query": "What is consideration in law?"
  }
  ```
- **Response Body**:
  ```json
  {
    "response": "Consideration in contract law refers to something of value exchanged between parties..."
  }
  ```

## 6. Agentic AI Audit
- **Endpoint**: `/agent-audit/{student_id}`
- **Method**: `GET`
- **Purpose**: Simulates a proactive background agent that analyzes a student's profile and suggests pedagogical interventions.
- **Request Body**: None (Uses path parameter)
- **Response Body**:
  ```json
  {
    "student_id": 101,
    "agent_alert": "⚠️ Agent Alert: Student has been struggling with 'Contracts'...",
    "recommended_action": "Assign GenAI Scenario for Contracts",
    "email_draft": "Dear Student 101,\n\nI noticed you've been having some trouble..."
  }
  ```
