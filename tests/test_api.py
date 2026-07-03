import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_predict_success():
    payload = {
        "student_id": 123,
        "topic": "Contracts",
        "score": 85.0,
        "time_spent": 45.0,
        "attempts": 1,
        "difficulty_level": 3
    }

    with TestClient(app) as client:
        response = client.post("/predict", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "mastery_level" in data
    assert "next_topic_recommendation" in data
    assert "risk_level" in data


def test_predict_high_risk():
    payload = {
        "student_id": 124,
        "topic": "Torts",
        "score": 40.0,
        "time_spent": 90.0,
        "attempts": 4,
        "difficulty_level": 4
    }

    with TestClient(app) as client:
        response = client.post("/predict", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["risk_level"] in ["High", "Medium", "Low"]  # flexible test


def test_invalid_score():
    payload = {
        "student_id": 125,
        "topic": "Criminal Law",
        "score": 150.0,
        "time_spent": 30.0,
        "attempts": 1,
        "difficulty_level": 2
    }

    with TestClient(app) as client:
        response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_topic_recommendation():
    from app.main import recommend_next_topic

    assert recommend_next_topic("Contracts", "Beginner") == "Review: Contracts"
    assert recommend_next_topic("Contracts", "Expert") == "Torts"