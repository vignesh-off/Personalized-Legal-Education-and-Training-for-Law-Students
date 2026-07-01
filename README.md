# Personalized Legal Education and Training for Law Students

This project is an AI-powered tutor designed to provide personalized legal education for law students. It adapts content and exercises based on student understanding and progress, starting with a foundational Machine Learning pipeline and aiming to evolve into an Agentic AI system.

## Project Phases
This repository currently implements **Phase 1: ML Baseline**. The long-term roadmap includes:
1. **Level 1 (Current)**: Machine Learning Baseline (Predictive modeling & Knowledge Tracing).
2. **Level 2**: Deep Learning Enhancement.
3. **Level 3**: NLP & Small Language Model (SLM) Integration.
4. **Level 4**: Low-Level System Design (LLD).
5. **Level 5**: Generative AI Capabilities.
6. **Level 6**: Autonomous Agentic AI System.

## Project Structure
- `ml_baseline.py` : Core Machine Learning script that generates synthetic student data, preprocesses it, trains a Random Forest model, and evaluates its performance on predicting concept mastery.
- `app.js` / `index.html` / `styles.css` : Front-end files for the web application interface.
- `requirements.txt` : Python dependencies required to run the ML models.

## How to Run the ML Baseline

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vignesh-off/Personalized-Legal-Education-and-Training-for-Law-Students.git
   cd legal-ai-tutor-app
   ```

2. **Install dependencies:**
   Make sure you have Python installed. Then, install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the script:**
   ```bash
   python ml_baseline.py
   ```

Upon running, the script will:
- Generate a mock dataset (`student_data.csv`).
- Handle missing values and scale the data.
- Train a Random Forest model.
- Print out Evaluation Metrics (Accuracy, Precision, Recall, F1-Score, ROC-AUC) and Feature Importances.
