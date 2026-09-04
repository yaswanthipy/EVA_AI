from fastapi import APIRouter
from pydantic import BaseModel

from evaluator import evaluate_answer


INTERVIEW_LEVELS = ["HR", "TECH", "PRODUCT"]

router = APIRouter()


# =====================================================
# QUESTIONS
# =====================================================

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


# =====================================================
# SHARED CANDIDATE CONTEXT
# =====================================================

candidate_context = {
    "answers": [],
    "scores": [],
    "roles": [],
    "weaknesses": [],
    "strengths": []
}


# =====================================================
# REQUEST MODEL
# =====================================================

class InterviewAnswer(BaseModel):
    question_id: int
    answer: str


# =====================================================
# FIND QUESTION
# =====================================================

def find_question(question_id: int):

    for level in INTERVIEW_LEVELS:

        for question in questions[level]:

            if question["id"] == question_id:

                return level, question

    return None, None


# =====================================================
# INTERVIEW CONTROLLER
# =====================================================

def interview_controller(
    current_level: str,
    score: int,
    evaluation: dict
):

    # ---------------------------------------------
    # HR → TECH
    # ---------------------------------------------

    if current_level == "HR":

        if evaluation["technical_detected"] or score >= 8:

            return {
                "next_level": "TECH",
                "reason": (
                    "Candidate response indicates sufficient "
                    "readiness for technical evaluation."
                )
            }

        return {
            "next_level": "HR",
            "reason": (
                "Candidate needs another HR question "
                "to provide more evidence."
            )
        }

    # ---------------------------------------------
    # TECH → PRODUCT
    # ---------------------------------------------

    if current_level == "TECH":

        if evaluation["missing_business_impact"]:

            return {
                "next_level": "PRODUCT",
                "reason": (
                    "Technical answer was detected, but "
                    "customer/business impact was not explained."
                )
            }

        if score >= 8:

            return {
                "next_level": "PRODUCT",
                "reason": (
                    "Technical performance is strong. "
                    "Panel is switching to product perspective."
                )
            }

        return {
            "next_level": "TECH",
            "reason": (
                "Technical depth needs further evaluation."
            )
        }

    # ---------------------------------------------
    # PRODUCT → FINISH
    # ---------------------------------------------

    if current_level == "PRODUCT":

        if score >= 8:

            return {
                "next_level": "COMPLETE",
                "reason": (
                    "All major interview perspectives "
                    "have been evaluated."
                )
            }

        return {
            "next_level": "PRODUCT",
            "reason": (
                "Product reasoning needs another "
                "follow-up question."
            )
        }

    return {
        "next_level": "COMPLETE",
        "reason": "Interview completed."
    }


# =====================================================
# DYNAMIC FOLLOW-UP QUESTIONS
# =====================================================

def generate_follow_up(
    current_level: str,
    evaluation: dict
):

    # Technical answer without business impact
    if evaluation["missing_business_impact"]:

        return {
            "question": (
                "You mentioned the technical solution. "
                "What measurable impact did it have on "
                "your users or customers?"
            ),
            "type": "business-impact-follow-up"
        }

    # Vague answer
    if evaluation["vague_detected"]:

        return {
            "question": (
                "Can you give me a specific example "
                "that demonstrates what you just described?"
            ),
            "type": "clarification-follow-up"
        }

    # Weak evidence
    if not evaluation["evidence_detected"]:

        return {
            "question": (
                "What measurable result or evidence "
                "supports your answer?"
            ),
            "type": "evidence-follow-up"
        }

    # Normal role-specific follow-up
    if current_level == "HR":

        return {
            "question": (
                "Can you give me a specific example "
                "from your experience?"
            ),
            "type": "experience-follow-up"
        }

    if current_level == "TECH":

        return {
            "question": (
                "What technical trade-offs did you "
                "consider when making that decision?"
            ),
            "type": "technical-follow-up"
        }

    return {
        "question": (
            "How would you measure whether your "
            "proposed solution was successful?"
        ),
        "type": "product-follow-up"
    }


# =====================================================
# START INTERVIEW
# =====================================================

@router.post("/start")
def start_interview():

    # Reset shared context
    candidate_context["answers"] = []
    candidate_context["scores"] = []
    candidate_context["roles"] = []
    candidate_context["weaknesses"] = []
    candidate_context["strengths"] = []

    level = "HR"

    return {
        "message": "EVA interview started successfully",

        "level": level,

        "interviewer": "HR Interviewer",

        "question": questions[level][0],

        "controller": {
            "status": "active",
            "current_role": level,
            "decision": "Starting with HR interviewer"
        }
    }


# =====================================================
# SUBMIT ANSWER
# =====================================================

@router.post("/answer")
def submit_answer(data: InterviewAnswer):

    # ---------------------------------------------
    # FIND CURRENT QUESTION
    # ---------------------------------------------

    current_level, current_question = find_question(
        data.question_id
    )

    if current_question is None:

        return {
            "error": "Question not found"
        }

    # ---------------------------------------------
    # EVALUATE ANSWER
    # ---------------------------------------------

    result = evaluate_answer(
        data.answer,
        candidate_context
    )

    # ---------------------------------------------
    # SAVE SHARED CONTEXT
    # ---------------------------------------------

    candidate_context["answers"].append({
        "question_id": data.question_id,
        "role": current_level,
        "question": current_question["question"],
        "answer": data.answer
    })

    candidate_context["scores"].append(result["score"])
    candidate_context["roles"].append(current_level)

    candidate_context["strengths"].extend(
        result["strengths"]
    )

    candidate_context["weaknesses"].extend(
        result["weaknesses"]
    )

    # ---------------------------------------------
    # CONTROLLER DECISION
    # ---------------------------------------------

    decision = interview_controller(
        current_level,
        result["score"],
        result
    )

    next_level = decision["next_level"]

    # ---------------------------------------------
    # INTERVIEW COMPLETE
    # ---------------------------------------------

    if next_level == "COMPLETE":

        average_score = round(
            sum(candidate_context["scores"])
            / len(candidate_context["scores"]),
            1
        )

        return {

            "message": "Interview completed",

            "question_id": data.question_id,

            "answer": data.answer,

            "score": result["score"],

            "feedback": result["feedback"],

            "current_level": current_level,

            "next_level": "COMPLETE",

            "next_question": None,

            "controller": {
                "status": "completed",
                "reason": decision["reason"]
            },

            "analysis": result,

            "shared_context": candidate_context,

            "average_score": average_score
        }

    # ---------------------------------------------
    # GENERATE FOLLOW-UP
    # ---------------------------------------------

    follow_up = generate_follow_up(
        current_level,
        result
    )

    # ---------------------------------------------
    # SELECT NEXT QUESTION
    # ---------------------------------------------

    next_question = None

    # If controller changes role,
    # start with that role's question.
    if next_level != current_level:

        next_question = questions[next_level][0]

    else:

        # Find another question in current role
        role_questions = questions[current_level]

        current_index = 0

        for index, question in enumerate(role_questions):

            if question["id"] == data.question_id:

                current_index = index
                break

        if current_index + 1 < len(role_questions):

            next_question = role_questions[
                current_index + 1
            ]

        else:

            next_question = {
                "id": data.question_id + 100,
                "question": follow_up["question"]
            }

    # ---------------------------------------------
    # FINAL RESPONSE
    # ---------------------------------------------

    return {

        "message": "Answer evaluated successfully",

        "question_id": data.question_id,

        "answer": data.answer,

        "score": result["score"],

        "feedback": result["feedback"],

        "current_level": current_level,

        "next_level": next_level,

        "next_question": next_question,

        "follow_up": follow_up,

        "controller": {

            "status": "active",

            "current_role": current_level,

            "next_role": next_level,

            "reason": decision["reason"],

            "action": (
                f"Switching from {current_level} "
                f"to {next_level}"
            )
        },

        "analysis": result,

        "shared_context": candidate_context
    }


# =====================================================
# GET QUESTION
# =====================================================

@router.get("/question/{question_id}")
def get_question(question_id: int):

    level, question = find_question(question_id)

    if question is None:

        return {
            "error": "Question not found"
        }

    return {
        "level": level,
        "question": question
    }