import os
from fastapi import APIRouter
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel
from evaluator import evaluate_answer

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

router = APIRouter()

INTERVIEW_LEVELS = ["HR", "TECH", "PRODUCT"]


def generate_ai_question(current_level, current_question, answer, score, feedback):
    prompt = f"""
You are EVA, an AI interviewer.

Current interview section: {current_level}
Current question: {current_question}
Candidate's answer: {answer}
Candidate score: {score}/10
Evaluation feedback: {feedback}

Generate ONE personalized follow-up interview question based specifically
on the candidate's answer.

Rules:
- Do not repeat the current question.
- If the answer is weak, ask a question that helps investigate or clarify it.
- If the answer is strong, ask a deeper question.
- Keep it relevant to the current interview section.
- Return ONLY the question.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text.strip()

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
    question: str
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

    current_question = None
    for level, level_questions in questions.items():
        if level != current_level:
            continue

        for question in level_questions:
            if question["id"] == data.question_id:
                current_question = question["question"]
                break

        if current_question is not None:
            break

    if current_question is None:
        current_question=data.question,

    ai_question = generate_ai_question(
        current_level=current_level,
        current_question=current_question,
        answer=data.answer,
        score=score,
        feedback=result["feedback"]
    )

    # Find current level index
    current_index = INTERVIEW_LEVELS.index(current_level)

    # Decide what happens next
    if score >= 8 and current_index < len(INTERVIEW_LEVELS) - 1:
        next_level = INTERVIEW_LEVELS[current_index + 1]
        action = "switch_interviewer"
    else:
        next_level = current_level
        action = "follow_up"

    interviewer_map = {
        "HR": "HR Interviewer",
        "TECH": "Technical Interviewer",
        "PRODUCT": "Product Manager"
    }

    next_question = {
        "id": data.question_id + 100,
        "question": ai_question,
        "interviewer": interviewer_map[next_level],
        "role": next_level
    }

    return {
        "message": "Answer evaluated successfully",

        "question_id": data.question_id,

        "answer": data.answer,

        "analysis": {
            "score": score,
            "feedback": result["feedback"],
            "ai_follow_up_question": ai_question
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