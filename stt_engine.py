import os
import shutil
import glob
import whisper
from streamlit_mic_recorder import mic_recorder
import tempfile

# Find FFmpeg
ffmpeg_path = shutil.which("ffmpeg")

if not ffmpeg_path:
    matches = glob.glob(
        os.path.expandvars(
            r"C:\Users\pansi\AppData\Local\Microsoft\WinGet\Packages\*\ffmpeg-*\bin\ffmpeg.exe"
        )
    )

    if matches:
        ffmpeg_path = matches[0]
        os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)




# ============================================================
# LOAD WHISPER ONCE
# ============================================================

model = whisper.load_model("base")


# ============================================================
# RECORD VOICE
# ============================================================

def record_voice():

    return mic_recorder(
        start_prompt="🎙️ Start Recording",
        stop_prompt="⏹️ Stop Recording",
        just_once=True,
        use_container_width=True,
        format="wav",
        key="visiona_microphone"
    )


# ============================================================
# SPEECH TO TEXT
# ============================================================

def speech_to_text(audio_bytes):

    # Prevent empty recordings from reaching Whisper
    if not audio_bytes:
        raise RuntimeError(
            "No audio was recorded. "
            "Please record for a few seconds and try again."
        )

    if len(audio_bytes) < 1000:
        raise RuntimeError(
            "The recording is too short or empty. "
            "Please speak for 2–5 seconds."
        )

    audio_path = None

    try:

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp:

            temp.write(audio_bytes)
            audio_path = temp.name

        # Check that the file actually contains data
        if not os.path.exists(audio_path):
            raise RuntimeError("Audio file could not be created.")

        if os.path.getsize(audio_path) < 1000:
            raise RuntimeError(
                "The recorded audio file is empty."
            )

        # Whisper transcription
        result = model.transcribe(
            audio_path,
            fp16=False
        )

        text = result.get("text", "").strip()

        if not text:
            raise RuntimeError(
                "Whisper could not detect any speech. "
                "Please speak clearly and try again."
            )

        return text

    finally:

        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)