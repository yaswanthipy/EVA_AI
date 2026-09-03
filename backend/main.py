from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from interview import router as interview_router
from evaluator import evaluate_answer as evaluate_answer_logic

app = FastAPI(
    title="EVA API",
    description="Enhanced Voice-based AI Interviewer",
    version="1.0.0"
)
app.include_router(
    interview_router,
    prefix="/interview",
    tags=["Interview"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnswerRequest(BaseModel):
    question_id: int
    question: str
    answer: str

@app.post("/evaluate")
def evaluate_answer(data: AnswerRequest):

    result = evaluate_answer_logic(data.answer)

    return {
        "question_id": data.question_id,
        "question": data.question,
        "answer": data.answer,
        "score": result["score"],
        "feedback": result["feedback"]
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