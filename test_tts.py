from tts_engine import text_to_speech


text = """
Newton's Second Law states that force is equal to mass multiplied by acceleration.
The formula is F equals m a.
"""


audio_file = text_to_speech(
    text,
    "English"
)

print("===== TTS SUCCESS =====")
print(audio_file)