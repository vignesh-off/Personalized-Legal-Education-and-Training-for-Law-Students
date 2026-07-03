# Low Level Design (LLD)

## 1. Application Structure
The application is structured into clearly separated layers:
- **Presentation Layer**: Streamlit (`frontend.py`)
- **API & Routing Layer**: FastAPI (`app/main.py`)
- **Service Layer**: ML Models, NLP, GenAI, SLM, Agentic AI
- **Data Access Layer**: SQLite Wrapper (`app/database.py`, `app/analytics.py`)

## 2. Folder Structure
```text
project_root/
├── frontend.py                     # Streamlit UI
├── requirements.txt                # Python dependencies
├── run_project.bat                 # Execution script
├── stop_project.bat                # Termination script
├── app/
│   ├── main.py                     # FastAPI routes
│   ├── schemas.py                  # Pydantic data models
│   ├── database.py                 # SQLite initialization & inserts
│   ├── analytics.py                # SQLite extraction for analytics
│   ├── services/
│   │   ├── nlp_service.py          # Essay evaluation logic
│   │   └── llm_service.py          # GenAI & SLM simulation
│   └── agents/
│       └── tutor_agent.py          # Agentic AI intervention logic
└── ml/
    ├── train.py                    # Dataset generation & RF Model training
    ├── dl_model.py                 # Neural-network fallback simulation
    └── models/
        ├── model.joblib            # Trained Random Forest model
        └── scaler.joblib           # Fitted StandardScaler
```

## 3. Database Schema
**Database Name**: `students.db`
**Table**: `predictions`
| Column | Data Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary Key, Auto-increment |
| `student_id` | INTEGER | Unique identifier for the student |
| `topic` | TEXT | The legal module being studied |
| `score` | REAL | Assessment score (0-100) |
| `time_spent` | REAL | Time taken to complete the module |
| `attempts` | INTEGER | Number of attempts taken |
| `difficulty_level`| INTEGER | Scale of 1 to 5 |
| `mastery_level` | TEXT | 'Beginner', 'Intermediate', or 'Expert' |
| `risk_level` | TEXT | 'Low', 'Medium', or 'High' |
| `next_topic` | TEXT | The recommended subsequent topic |

## 4. Component Interactions (Data Flow)
1. **User Input**: User interacts with the Streamlit UI, submitting assessment metrics or text.
2. **API Call**: Streamlit sends a POST request with a JSON payload to the FastAPI backend.
3. **Validation**: FastAPI validates the payload using Pydantic schemas (`app/schemas.py`).
4. **Processing**: 
   - For ML tasks, the input is standardized using `scaler.joblib` and inferred via `model.joblib`.
   - For text tasks, `nlp_service` or `llm_service` processes the request.
5. **Persistence**: In the case of predictions, `app/database.py` commits the transaction to SQLite.
6. **Response**: FastAPI returns a JSON response.
7. **Visualization**: Streamlit renders the JSON response as interactive Plotly charts or textual feedback.
