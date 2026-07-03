def generate_scenario_mock(topic: str):
    # Simulated Gen AI scenario generation
    scenarios = {
        "Contracts": {
            "text": "Alice offers to sell her car to Bob for $5,000. Bob replies, 'I accept, but only if you paint it red.' Alice ignores Bob and sells the car to Charlie.",
            "questions": ["Did Bob's reply constitute a valid acceptance?", "Is Alice in breach of contract?"]
        },
        "Torts": {
            "text": "David is driving 20 mph over the speed limit. He hits a patch of black ice, spins out, and damages a fence belonging to Eve.",
            "questions": ["Is David liable for negligence?", "What defenses might David raise regarding causation?"]
        },
        "Criminal Law": {
            "text": "Frank breaks into a house at night to stay warm. While inside, he sees a valuable watch and decides to take it.",
            "questions": ["Did Frank commit burglary when he first entered?", "What is the mens rea for his subsequent action?"]
        }
    }
    
    default = {
        "text": f"A complex legal dispute arises regarding {topic}. Two parties strongly disagree on the application of the relevant statute.",
        "questions": ["What is the primary legal issue?", "How should a court rule?"]
    }
    
    return scenarios.get(topic, default)

def tutor_chat_mock(query: str):
    # Simulated SLM tutor
    query = query.lower()
    if "consideration" in query:
        return "Consideration in contract law refers to something of value exchanged between parties. It can be money, goods, services, or a promise. It's what distinguishes a contract from a mere gift."
    elif "negligence" in query:
        return "Negligence requires proving four elements: 1) duty of care, 2) breach of that duty, 3) causation (both actual and proximate), and 4) actual damages."
    elif "mens rea" in query:
        return "Mens rea is the mental element of a person's intention to commit a crime; or knowledge that one's action or lack of action would cause a crime to be committed."
    elif "hi" in query or "hello" in query:
        return "Hello! I am your AI Legal Tutor. Feel free to ask me about any legal concepts like 'negligence', 'consideration', or 'mens rea'."
    else:
        return "That's an interesting legal question. Based on general principles, you should analyze the specific statutes and case law applicable to the jurisdiction. If you need a specific definition, please ask!"
