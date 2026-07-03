import os
from app.database import init_db, save_prediction
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from ml.dl_model import predict_dl
from .schemas import StudentDataInput, PredictionOutput, DLPredictionOutput

# Global variables to hold the loaded models
ml_models = {}

# Basic legal topic progression
TOPIC_PROGRESSION = [
    "Introduction to Law",
    "Contracts",
    "Torts",
    "Criminal Law",
    "Property Law",
    "Constitutional Law",
    "Civil Procedure",
    "Evidence"
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    model_path = os.path.join("ml", "models", "model.joblib")
    scaler_path = os.path.join("ml", "models", "scaler.joblib")

    try:
        ml_models["model"] = joblib.load(model_path)
        ml_models["scaler"] = joblib.load(scaler_path)
    except FileNotFoundError:
        print("Model not found. Train first.")

    # ✅ FIX 1: INIT DB
    init_db()

    yield

    ml_models.clear()

app = FastAPI(
    title="Legal Education AI API",
    description="API for predicting student mastery and recommending next topics.",
    version="1.0.0",
    lifespan=lifespan
)

def determine_risk_level(score: float, attempts: int, difficulty_level: int, time_spent: float) -> str:
    """
    Calculate the risk level based on the newly defined weighted logic.
    """
    if score < 40:
        return "High"
    elif 40 <= score <= 59:
        # Base is Medium. Bump to High if struggling heavily.
        if attempts >= 3 or difficulty_level >= 4 or (time_spent > 60 and score < 60):
            return "High"
        return "Medium"
    elif 60 <= score <= 74:
        # Base is Low. Bump to Medium if attempts or difficulty are high.
        if attempts >= 2 or difficulty_level >= 4:
            return "Medium"
        return "Low"
    else:  # score >= 75
        # Base is Low. Bump to Medium if it took too many attempts.
        if attempts >= 3:
            return "Medium"
        return "Low"

def recommend_next_topic(current_topic: str, mastery: str) -> str:
    """
    Recommend the next topic based on the current topic and mastery level.
    If the student has not mastered the topic (Beginner), they might need review.
    Otherwise, move to the next topic in the progression.
    """
    if current_topic not in TOPIC_PROGRESSION:
        # Default fallback if the topic is unknown
        return TOPIC_PROGRESSION[0]
        
    current_index = TOPIC_PROGRESSION.index(current_topic)
    
    if mastery == "Beginner":
        # Recommend reviewing the same topic or prerequisite (simplified to same topic here)
        return f"Review: {current_topic}"
        
    # For Intermediate/Expert, move to next topic
    if current_index + 1 < len(TOPIC_PROGRESSION):
        return TOPIC_PROGRESSION[current_index + 1]
    else:
        return "Advanced Specialization Topics"

@app.post("/predict", response_model=PredictionOutput)
async def predict_mastery(data: StudentDataInput):
    if "model" not in ml_models or "scaler" not in ml_models:
        raise HTTPException(status_code=503, detail="ML model is not loaded. Please ensure the model is trained.")
        
    # Prepare the input for the model
    input_df = pd.DataFrame([{
        "score": data.score,
        "time_spent": data.time_spent,
        "attempts": data.attempts,
        "difficulty_level": data.difficulty_level
    }])
    
    # Scale the features
    try:
        scaled_features = ml_models["scaler"].transform(input_df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scaling features: {str(e)}")
        
    # Predict mastery level
    try:
        prediction = ml_models["model"].predict(scaled_features)
        mastery_level = prediction[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")
        
    # Determine risk level
    risk_level = determine_risk_level(data.score, data.attempts, data.difficulty_level, data.time_spent)
    
    # Recommend next topic
    next_topic = recommend_next_topic(data.topic, mastery_level)

    save_prediction({
    "student_id": data.student_id,
    "topic": data.topic,
    "score": data.score,
    "time_spent": data.time_spent,
    "attempts": data.attempts,
    "difficulty_level": data.difficulty_level,
    "mastery_level": mastery_level,
    "risk_level": risk_level,
    "next_topic_recommendation": next_topic
})
    
    return PredictionOutput(
        mastery_level=mastery_level,
        next_topic_recommendation=next_topic,
        risk_level=risk_level
    )

@app.post('/predict-dl', response_model=DLPredictionOutput)
async def predict_dl_endpoint(data: StudentDataInput):
    try:
        dl_result = predict_dl(
            data.score, 
            data.time_spent, 
            data.attempts, 
            data.difficulty_level
        )
        mastery = dl_result['dl_mastery_level']
        confidence = dl_result['dl_confidence']
        message = f"DL Model predicts {mastery} with {confidence}% confidence."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in DL prediction: {str(e)}")

    return DLPredictionOutput(
        dl_mastery_level=mastery,
        dl_confidence=confidence,
        dl_message=message
    )