from gtts import gTTS
import tempfile
import os


def text_to_speech(text, language="English"):

    if not text or not text.strip():
        raise ValueError("No text available for speech.")

    if language == "Hindi":
        lang_code = "hi"
    else:
        lang_code = "en"

    tts = gTTS(
        text=text,
        lang=lang_code,
        slow=False
    )

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )

    temp_file.close()

    tts.save(temp_file.name)

    return temp_file.name