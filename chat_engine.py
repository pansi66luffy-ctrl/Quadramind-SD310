import streamlit as st
from ai_engine import ask_ai


def visiona_chat(user_message, context):

    history = ""

    for message in st.session_state.chat_history:
        history += (
            f"\n{message['role']}: "
            f"{message['content']}\n"
        )

    prompt = f"""
You are VISIONA, an advanced AI learning assistant.

You are helping a student understand their uploaded study material.

SOURCE MATERIAL:
{context}

PREVIOUS CONVERSATION:
{history}

STUDENT'S NEW QUESTION:
{user_message}

Rules:

1. Answer based primarily on the student's uploaded material.
2. If the material does not contain the answer, clearly say so.
3. Explain difficult concepts step-by-step.
4. Preserve formulas accurately.
5. Use engineering and robotics examples when useful.
6. Keep explanations understandable for a first-year engineering student.
7. If the student asks for a quiz, generate questions interactively.
8. If the student makes a mistake, explain why.
9. Do not invent information and claim it came from the notes.

Give a helpful educational answer.
"""

    return ask_ai(prompt)