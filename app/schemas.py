from pydantic import BaseModel, Field

class StudentDataInput(BaseModel):
    student_id: int = Field(..., description="Unique identifier for the student")
    topic: str = Field(..., description="The current legal topic being studied")
    score: float = Field(..., ge=0, le=100, description="Score achieved on the topic assessment (0-100)")
    time_spent: float = Field(..., ge=0, description="Time spent on the topic in minutes")
    attempts: int = Field(..., ge=1, description="Number of attempts to pass the topic")
    difficulty_level: int = Field(..., ge=1, le=5, description="Difficulty level of the topic (1-5)")

class PredictionOutput(BaseModel):
    mastery_level: str = Field(..., description="Predicted mastery level: Beginner, Intermediate, or Expert")
    next_topic_recommendation: str = Field(..., description="Recommended next legal topic")
    risk_level: str = Field(..., description="Risk level for failing or dropping out: Low, Medium, High")

class DLPredictionOutput(BaseModel):
    dl_mastery_level: str = Field(..., description="Predicted mastery level by Deep Learning model")
    dl_confidence: float = Field(..., description="Confidence score of the DL prediction (0-100)")
    dl_message: str = Field(..., description="Explanation message from DL model")

class EssayInput(BaseModel):
    student_id: int
    topic: str
    essay_text: str

class EssayOutput(BaseModel):
    score: float
    feedback: str
    key_concepts_found: list[str]

class ScenarioInput(BaseModel):
    student_id: int
    weak_topic: str

class ScenarioOutput(BaseModel):
    scenario_text: str
    questions: list[str]

class ChatInput(BaseModel):
    query: str

class ChatOutput(BaseModel):
    response: str
