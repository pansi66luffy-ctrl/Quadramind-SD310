import json
import re

from ai_engine import ask_ai


# ============================================================
# EXTRACT JSON FROM AI RESPONSE
# ============================================================

def extract_json(text):

    # Try direct JSON first
    try:
        return json.loads(text)
    except:
        pass

    # Try ```json ... ```
    match = re.search(
        r"```json\s*(.*?)\s*```",
        text,
        re.DOTALL | re.IGNORECASE
    )

    if match:

        try:
            return json.loads(match.group(1))
        except:
            pass

    # Try finding the first JSON object
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:

        try:
            return json.loads(
                text[start:end + 1]
            )
        except:
            pass

    raise ValueError(
        "VISIONA received an invalid quiz format from the AI."
    )


# ============================================================
# GENERATE QUIZ
# ============================================================

def generate_quiz(
    notes,
    vision_analysis="",
    difficulty="Beginner",
    number_of_questions=5
):

    prompt = f"""
You are VISIONA, an advanced adaptive learning engine.

Create a high-quality educational quiz from the student's
uploaded study material.

STUDENT NOTES:
{notes}

MULTIMODAL ANALYSIS:
{vision_analysis}

DIFFICULTY:
{difficulty}

NUMBER OF QUESTIONS:
{number_of_questions}

IMPORTANT:

- Questions MUST be based primarily on the supplied material.
- Do not invent facts that are unsupported by the material.
- Test understanding, not just memorization.
- Include engineering reasoning when the material supports it.
- Each question must have exactly 4 options.
- Only one option can be correct.
- Include the correct answer.
- Include a short explanation.
- Assign each question a topic/concept.
- Topics should be specific enough to identify weak areas.
- Avoid duplicate questions.
- Keep questions appropriate for the requested difficulty.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "correct_answer": "Option A",
            "topic": "Topic name",
            "explanation": "Short explanation"
        }}
    ]
}}

Do not include Markdown.
Do not include ```json.
Do not include any text before or after the JSON.
"""

    raw_response = ask_ai(prompt)

    data = extract_json(raw_response)

    if "questions" not in data:
        raise ValueError(
            "Quiz response does not contain questions."
        )

    questions = data["questions"]

    if not questions:
        raise ValueError(
            "AI generated an empty quiz."
        )

    # Validate every question
    validated_questions = []

    for question in questions:

        if not isinstance(question, dict):
            continue

        required = [
            "question",
            "options",
            "correct_answer",
            "topic",
            "explanation"
        ]

        if not all(
            key in question
            for key in required
        ):
            continue

        if len(question["options"]) != 4:
            continue

        if question["correct_answer"] not in question["options"]:
            continue

        validated_questions.append(question)

    if not validated_questions:
        raise ValueError(
            "AI generated questions, but none passed validation."
        )

    return validated_questions


# ============================================================
# SCORE QUIZ
# ============================================================

def score_quiz(
    questions,
    answers
):

    total = len(questions)

    correct = 0

    topic_stats = {}

    results = []

    for index, question in enumerate(questions):

        user_answer = answers.get(index)

        correct_answer = question["correct_answer"]

        is_correct = (
            user_answer == correct_answer
        )

        if is_correct:
            correct += 1

        topic = question["topic"]

        if topic not in topic_stats:

            topic_stats[topic] = {
                "correct": 0,
                "total": 0
            }

        topic_stats[topic]["total"] += 1

        if is_correct:
            topic_stats[topic]["correct"] += 1

        results.append(
            {
                "question": question["question"],
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "correct": is_correct,
                "topic": topic,
                "explanation": question["explanation"]
            }
        )

    percentage = 0

    if total > 0:
        percentage = round(
            (correct / total) * 100
        )

    # Calculate topic percentages
    for topic in topic_stats:

        stats = topic_stats[topic]

        stats["percentage"] = round(
            (
                stats["correct"]
                /
                stats["total"]
            ) * 100
        )

    return {
        "total": total,
        "correct": correct,
        "incorrect": total - correct,
        "percentage": percentage,
        "topic_stats": topic_stats,
        "results": results
    }


# ============================================================
# FIND WEAK TOPICS
# ============================================================

def get_weak_topics(
    topic_stats,
    threshold=60
):

    weak_topics = []

    for topic, stats in topic_stats.items():

        if stats["percentage"] < threshold:

            weak_topics.append(
                {
                    "topic": topic,
                    "percentage": stats["percentage"]
                }
            )

    weak_topics.sort(
        key=lambda x: x["percentage"]
    )

    return weak_topics
