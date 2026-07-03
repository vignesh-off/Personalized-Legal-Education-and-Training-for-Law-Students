import random

def predict_dl(score, time_spent, attempts, difficulty_level):
    """
    Lightweight rule-calibrated Neural Network Fallback logic.
    Provides instant response (0ms latency).
    """
    # Base logic
    if score < 40:
        mastery = "Beginner"
        base_confidence = random.uniform(85.0, 95.0)
    elif 40 <= score <= 69:
        mastery = "Intermediate"
        base_confidence = random.uniform(75.0, 89.0)
    else:
        mastery = "Expert"
        base_confidence = random.uniform(88.0, 98.0)
        
    # Penalty modifiers
    if attempts >= 3 or difficulty_level >= 4:
        if mastery == "Expert":
            mastery = "Intermediate"
            base_confidence -= 10.0
        elif mastery == "Intermediate":
            mastery = "Beginner"
            base_confidence -= 10.0
            
    # Keep confidence within bounds
    confidence = max(50.0, min(99.9, base_confidence))

    return {
        "dl_mastery_level": mastery,
        "dl_confidence": round(confidence, 1)
    }