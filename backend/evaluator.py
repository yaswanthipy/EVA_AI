def evaluate_answer(answer: str, context=None):

    answer = answer.strip()
    answer_lower = answer.lower()
    answer_length = len(answer)

    # -----------------------------------------
    # BASIC QUALITY SCORE
    # -----------------------------------------

    if answer_length < 20:
        score = 5
        feedback = (
            "Your answer is too short. "
            "Try explaining your reasoning and include an example."
        )

    elif answer_length < 80:
        score = 7
        feedback = (
            "Good start. Your answer would be stronger "
            "with a specific example or measurable result."
        )

    else:
        score = 9
        feedback = (
            "Good answer. You provided enough detail "
            "to demonstrate your thinking."
        )

    # -----------------------------------------
    # DETECT TECHNICAL CONTENT
    # -----------------------------------------

    technical_keywords = [
        "python",
        "java",
        "javascript",
        "react",
        "node",
        "api",
        "database",
        "sql",
        "mongodb",
        "firebase",
        "aws",
        "docker",
        "backend",
        "frontend",
        "algorithm",
        "machine learning",
        "ai",
        "model",
        "authentication",
        "jwt",
        "cache",
        "caching"
    ]

    technical_detected = any(
        keyword in answer_lower
        for keyword in technical_keywords
    )

    # -----------------------------------------
    # DETECT PRODUCT / BUSINESS CONTENT
    # -----------------------------------------

    product_keywords = [
        "customer",
        "user",
        "users",
        "business",
        "revenue",
        "cost",
        "impact",
        "customer satisfaction",
        "conversion",
        "retention",
        "market",
        "product",
        "requirement",
        "feedback",
        "experience"
    ]

    product_detected = any(
        keyword in answer_lower
        for keyword in product_keywords
    )

    # -----------------------------------------
    # DETECT VAGUE ANSWERS
    # -----------------------------------------

    vague_words = [
        "maybe",
        "something",
        "somehow",
        "things",
        "stuff",
        "etc",
        "good",
        "better",
        "improved"
    ]

    vague_detected = any(
        word in answer_lower
        for word in vague_words
    )

    # -----------------------------------------
    # DETECT MEASUREMENT / EVIDENCE
    # -----------------------------------------

    evidence_keywords = [
        "%",
        "percent",
        "seconds",
        "ms",
        "users",
        "increase",
        "decrease",
        "reduced",
        "improved",
        "faster",
        "slower",
        "times",
        "number"
    ]

    evidence_detected = any(
        keyword in answer_lower
        for keyword in evidence_keywords
    )

    # -----------------------------------------
    # STRENGTHS
    # -----------------------------------------

    strengths = []

    if answer_length >= 80:
        strengths.append("Detailed explanation")

    if technical_detected:
        strengths.append("Technical understanding")

    if product_detected:
        strengths.append("Business/customer awareness")

    if evidence_detected:
        strengths.append("Evidence or measurable impact")

    if not strengths:
        strengths.append("Attempted to answer the question")

    # -----------------------------------------
    # WEAKNESSES
    # -----------------------------------------

    weaknesses = []

    if answer_length < 80:
        weaknesses.append("Needs more detail")

    if vague_detected:
        weaknesses.append("Vague language")

    if not evidence_detected:
        weaknesses.append("No measurable evidence")

    # -----------------------------------------
    # SPECIAL DETECTION
    # -----------------------------------------

    missing_business_impact = (
        technical_detected and not product_detected
    )

    if missing_business_impact:
        weaknesses.append("Business/customer impact not explained")

    return {
        "score": score,
        "feedback": feedback,
        "technical_detected": technical_detected,
        "product_detected": product_detected,
        "vague_detected": vague_detected,
        "evidence_detected": evidence_detected,
        "missing_business_impact": missing_business_impact,
        "strengths": strengths,
        "weaknesses": weaknesses
    }