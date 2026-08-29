from ai_engine import ask_ai


# ============================================================
# ADAPTIVE WEAK-TOPIC TUTOR
# ============================================================

def generate_weak_topic_lesson(
    notes,
    weak_topic,
    score_percentage,
    vision_analysis=""
):

    prompt = f"""
You are VISIONA, an adaptive engineering education tutor.

The student has completed a quiz based on their study material.

The student is struggling with this topic:

WEAK TOPIC:
{weak_topic}

STUDENT SCORE ON THIS TOPIC:
{score_percentage}%

ORIGINAL STUDY MATERIAL:
{notes}

MULTIMODAL ANALYSIS:
{vision_analysis}

Your job is to create a focused remediation lesson ONLY for
the weak topic.

The goal is to help the student understand the concept and
improve their performance.

Structure your response exactly like this:

# 1. Concept Explanation

Explain the weak topic clearly from first principles.

Use simple language but maintain correct engineering terminology.

# 2. Why Students Get This Wrong

Explain the most likely conceptual confusion.

# 3. Important Formula or Principle

If the topic contains formulas, show them accurately.

Explain every variable.

If there is no formula, explain the key principle instead.

# 4. Engineering Example

Give one practical engineering example related to the topic.

# 5. Worked Example

Give one numerical or logical example and solve it step by step
when appropriate.

# 6. Common Mistakes

List the important mistakes the student should avoid.

# 7. Quick Check

Create exactly 3 short questions about this weak topic.

Do NOT provide the answers immediately.

Keep the lesson focused on the supplied material.

Do not invent unsupported facts.
"""


    return ask_ai(prompt)