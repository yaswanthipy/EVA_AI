from fastapi import APIRouter
from pydantic import BaseModel
from evaluator import evaluate_answer
INTERVIEW_LEVELS = ["HR", "TECH", "PRODUCT"]
router = APIRouter()
class InterviewAnswer(BaseModel):
    question_id: int
    answer: str

questions = {
    "HR": [
        {
            "id": 1,
            "question": "Tell me about yourself."
        },
        {
            "id": 2,
            "question": "What are your strengths?"
        }
    ],

    "TECH": [
        {
            "id": 3,
            "question": "Explain a technical project you have worked on."
        },
        {
            "id": 4,
            "question": "What programming languages or technologies are you comfortable with?"
        }
    ],

    "PRODUCT": [
        {
            "id": 5,
            "question": "How would you improve a product that users are unhappy with?"
        },
        {
            "id": 6,
            "question": "How would you decide which feature should be built first?"
        }
    ]
}
@router.post("/start")
def start_interview():
    level = INTERVIEW_LEVELS[0]

    return {
        "message": "Interview started successfully",
        "level": level,
        "question": questions[level][0]
    }
@router.post("/answer")
def submit_answer(data: InterviewAnswer):

    result = evaluate_answer(data.answer)

    current_level = "HR"

    next_level = get_next_level(
        current_level,
        result["score"]
    )
    next_question = questions[next_level][0]  

    return {
        "message": "Answer evaluated successfully",
        "question_id": data.question_id,
        "answer": data.answer,
        "score": result["score"],
        "feedback": result["feedback"],
        "current_level": current_level,
        "next_level": next_level,
        "next_question": next_question
    }


@router.get("/question/{question_id}")
def get_question(question_id: int):

    for level in INTERVIEW_LEVELS:
        for question in questions[level]:
            if question["id"] == question_id:
                return {
                    "level": level,
                    "question": question
                }

    return {
        "error": "Question not found"
    }

def get_next_level(current_level: str, score: int):

    current_index = INTERVIEW_LEVELS.index(current_level)

    if score >= 8 and current_index < len(INTERVIEW_LEVELS) - 1:
        return INTERVIEW_LEVELS[current_index + 1]

    return current_level