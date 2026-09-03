def evaluate_answer(answer: str):

    answer_length = len(answer.strip())

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
        "feedback": feedback
    }