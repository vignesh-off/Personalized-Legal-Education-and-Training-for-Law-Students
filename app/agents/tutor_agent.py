def run_agentic_audit_mock(student_id: int):
    # Simulates a background agent auditing the student's risk profile
    # In a real app, this would query the DB. We'll return a mock alert for simulation purposes.
    return {
        "student_id": student_id,
        "agent_alert": "⚠️ Agent Alert: Student has been struggling with 'Contracts'. I recommend sending them the newly generated practice scenario.",
        "recommended_action": "Assign GenAI Scenario for Contracts",
        "email_draft": f"Dear Student {student_id},\n\nI noticed you've been having some trouble with Contracts recently. I've prepared a custom practice case for you to try out.\n\nBest,\nAI Tutor"
    }
