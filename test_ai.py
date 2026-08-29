from ai_engine import ask_ai


print("\n==============================")
print("       VISIONA AI TEST")
print("==============================\n")


prompt = """
You are helping a first-year engineering student.

Explain Newton's Second Law.

Include:
1. Simple explanation
2. Formula
3. Real-world example
4. One common mistake

Keep it understandable.
"""


print("Sending request to Gemini...\n")

try:

    answer = ask_ai(prompt)

    print("===== GEMINI RESPONSE =====\n")
    print(answer)

except Exception as e:

    print("\n===== GEMINI ERROR =====\n")
    print(type(e).__name__)
    print(e)