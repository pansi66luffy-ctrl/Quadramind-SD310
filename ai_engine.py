import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("API key loaded:", bool(api_key))

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY was not found. Check your .env file."
    )


client = genai.Client(api_key=api_key)


def ask_ai(prompt):

    response = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return response.output_text


def analyze_image(image, ocr_text):

    prompt = f"""
You are VISIONA, an advanced multimodal AI learning assistant.

Analyze the uploaded educational image together with the OCR text.

OCR TEXT:
{ocr_text}

Analyze:

1. Main topic
2. Important text
3. Mathematical formulas
4. Diagrams
5. Graphs
6. Tables
7. Relationships between concepts
8. Important definitions
9. Engineering applications
10. Information OCR may have missed

Use the actual image as the primary visual source.

Do not invent information.

If something is unclear, say so.

Return:

# Main Topic

# Concepts

# Formulas

# Diagrams

# Tables / Graphs

# Important Definitions

# Key Points

# Engineering Applications

# OCR Corrections / Missing Information
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            image,
            prompt
        ]
    )

    return response.text


def tutor_ai(question, notes, vision_analysis, history):

    conversation = ""

    for message in history:
        conversation += (
            f"{message['role']}: {message['content']}\n"
        )

    prompt = f"""
You are VISIONA, an intelligent AI tutor.

You are tutoring a student using their uploaded study material.

ORIGINAL OCR NOTES:
{notes}

MULTIMODAL ANALYSIS:
{vision_analysis}

PREVIOUS CONVERSATION:
{conversation}

STUDENT'S NEW QUESTION:
{question}

Rules:

1. Answer using the uploaded material whenever possible.
2. Use the visual analysis when relevant.
3. If the material does not contain enough information, clearly say so.
4. Do not pretend unsupported information came from the notes.
5. Explain difficult concepts step-by-step.
6. Use engineering examples when useful.
7. Preserve formulas accurately.
8. Adapt the explanation to a first-year engineering student.
9. Do not unnecessarily repeat previous answers.
10. If the student asks a follow-up question, use the conversation context.

Give a clear, educational answer.
"""

    return ask_ai(prompt)