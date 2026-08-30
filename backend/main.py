from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="EVA API",
    description="Enhanced Voice-based AI Interviewer",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnswerRequest(BaseModel):
    answer: str
    question: str


@app.post("/evaluate")
def evaluate_answer(data: AnswerRequest):

    answer_length = len(data.answer.strip())

    if answer_length < 20:
        feedback = "Your answer is a little short. Try adding more details or an example."
        score = 5

    elif answer_length < 80:
        feedback = "Good start. Your answer could be stronger with a specific example."
        score = 7

    else:
        feedback = "Good answer. You provided enough detail to demonstrate your thinking."
        score = 9

    return {
        "score": score,
        "feedback": feedback,
        "question": data.question
    }


@app.get("/")
def root():
    return {
        "message": "EVA API is running",
        "status": "success"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "EVA backend"
    }