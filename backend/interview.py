from fastapi import APIRouter
from pydantic import BaseModel
from evaluator import evaluate_answer

router = APIRouter()

INTERVIEW_LEVELS = ["HR", "TECH", "PRODUCT"]

questions = {
    "HR": [
        {
            "id": 1,
            "question": "Tell me about yourself and your background."
        },
        {
            "id": 2,
            "question": "What is one challenge you faced and how did you overcome it?"
        }
    ],

    "TECH": [
        {
            "id": 3,
            "question": "What is the difference between an array and a linked list?"
        },
        {
            "id": 4,
            "question": "Explain a technical project you have worked on."
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


class InterviewAnswer(BaseModel):
    question_id: int
    answer: str
    current_level: str


@router.post("/start")
def start_interview():

    return {
        "message": "Interview started successfully",
        "level": "HR",
        "question": questions["HR"][0],
        "interviewer": "HR Interviewer"
    }


@router.post("/answer")
def submit_answer(data: InterviewAnswer):

    # Evaluate candidate answer
    result = evaluate_answer(data.answer)

    score = result["score"]
    current_level = data.current_level

    # Find current level index
    current_index = INTERVIEW_LEVELS.index(current_level)

    # Decide what happens next
    if score >= 8 and current_index < len(INTERVIEW_LEVELS) - 1:

        next_level = INTERVIEW_LEVELS[current_index + 1]

        next_question = questions[next_level][0]

        action = "switch_interviewer"

    elif score < 8:

        next_level = current_level

        # Ask the second question of the same interviewer
        current_questions = questions[current_level]

        current_question_index = 0

        for index, question in enumerate(current_questions):

            if question["id"] == data.question_id:
                current_question_index = index
                break

        next_index = min(
            current_question_index + 1,
            len(current_questions) - 1
        )

        next_question = current_questions[next_index]

        action = "follow_up"

    else:

        next_level = current_level

        next_question = None

        action = "complete"


    interviewer_map = {
        "HR": "HR Interviewer",
        "TECH": "Technical Interviewer",
        "PRODUCT": "Product Manager"
    }

    return {
        "message": "Answer evaluated successfully",

        "question_id": data.question_id,

        "answer": data.answer,

        "analysis": {
            "score": score,
            "feedback": result["feedback"]
        },

        "controller": {
            "status": "active",
            "current_role": current_level,
            "next_role": next_level,
            "action": action
        },

        "next_question": next_question,

        "next_interviewer": interviewer_map[next_level]
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