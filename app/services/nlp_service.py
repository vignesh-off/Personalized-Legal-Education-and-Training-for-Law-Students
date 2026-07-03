def evaluate_essay_mock(topic: str, essay_text: str):
    # Simulated NLP keyword extraction
    keywords = {
        "Contracts": ["offer", "acceptance", "consideration", "breach", "damages"],
        "Torts": ["duty", "breach", "causation", "damages", "negligence", "liability"],
        "Criminal Law": ["mens rea", "actus reus", "intent", "felony", "misdemeanor"],
        "Property Law": ["possession", "title", "easement", "tenant", "deed"]
    }
    
    topic_keywords = keywords.get(topic, ["law", "legal", "rule", "court"])
    found_keywords = [kw for kw in topic_keywords if kw.lower() in essay_text.lower()]
    
    score = min(100.0, (len(found_keywords) / max(1, len(topic_keywords))) * 100 + 40.0) # Base 40
    if len(essay_text) < 10:
        score = 0.0
    
    feedback = "Good effort. "
    if len(essay_text) < 10:
        feedback = "Response is too short to evaluate."
    elif len(found_keywords) == len(topic_keywords):
        feedback += "You covered all key concepts perfectly!"
    elif len(found_keywords) > 0:
        feedback += f"You mentioned some good points like {', '.join(found_keywords)}, but missed a few others."
    else:
        feedback += "You missed the core legal concepts for this topic. Please review the definitions."
        
    return {
        "score": round(score, 2),
        "feedback": feedback,
        "key_concepts_found": found_keywords
    }
