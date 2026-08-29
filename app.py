import streamlit as st
from PIL import Image

from ocr_engine import extract_text
from ai_engine import ask_ai, analyze_image
from tts_engine import text_to_speech
from stt_engine import record_voice, speech_to_text
from chat_engine import visiona_chat
from document_engine import extract_document_text

from quiz_engine import (
    generate_quiz,
    score_quiz,
    get_weak_topics
)

from adaptive_engine import generate_weak_topic_lesson


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="NIKA AI",
    page_icon="🧠",
    layout="wide"
)

# ============================================================
# NIKA ANIMATED VIDEO BACKGROUND
# ============================================================

from pathlib import Path
import base64

video_path = Path(__file__).parent / "assets" / "nika_background.mp4"

if video_path.exists():

    video_bytes = video_path.read_bytes()
    video_base64 = base64.b64encode(video_bytes).decode("utf-8")

    html = f"""
<style>
.stApp {{
    background: transparent !important;
}}

[data-testid="stAppViewContainer"] {{
    background: transparent !important;
}}

[data-testid="stHeader"] {{
    background: transparent !important;
}}

#nika-video {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    object-fit: cover;
    z-index: -100;
    pointer-events: none;
}}

#nika-overlay {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;

    background:
        linear-gradient(
            rgba(5, 5, 10, 0.05),
            rgba(5, 5, 10, 0.12)
        );

    z-index: -99;
    pointer-events: none;
}}
</style>

<video id="nika-video" autoplay muted loop playsinline>
<source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
</video>

<div id="nika-overlay"></div>
"""

    st.markdown(
        html,
        unsafe_allow_html=True
    )

else:

    st.error(
        f"NIKA background video not found: {video_path}"
    )

# ============================================================
# SESSION STATE
# ============================================================

if "selected_feature" not in st.session_state:
    st.session_state["selected_feature"] = "🏠 Dashboard"



# ============================================================
# SESSION STATE
# ============================================================


if "image" not in st.session_state:
    st.session_state.image = None

if "ocr_text" not in st.session_state:
    st.session_state.ocr_text = ""

if "vision_analysis" not in st.session_state:
    st.session_state.vision_analysis = ""

if "ai_result" not in st.session_state:
    st.session_state.ai_result = ""

if "audio_file" not in st.session_state:
    st.session_state.audio_file = None

if "audio_data" not in st.session_state: 
    st.session_state.audio_data = None 

if "voice_question" not in st.session_state:
    st.session_state.voice_question = ""

if "voice_audio" not in st.session_state:
    st.session_state.voice_audio = None    

if "tts_text" not in st.session_state: 
    st.session_state.tts_text = ""    

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "quiz" not in st.session_state:
    st.session_state.quiz = []

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

if "quiz_result" not in st.session_state:
    st.session_state.quiz_result = None

if "adaptive_lesson" not in st.session_state:
    st.session_state.adaptive_lesson = ""

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False   

# ============================================================
# NIKA DASHBOARD
# ============================================================

# ============================================================
# NIKA PREMIUM DASHBOARD
# ============================================================

st.markdown("""
<style>

/* =========================================================
   NIKA FEATURE CARDS
   ========================================================= */

.nika-card {

    min-height: 95px;

    padding: 14px 12px;

    margin-bottom: 5px;

    border-radius: 16px;

    text-align: center;

    background: rgba(15, 15, 25, 0.68);

    border: 1px solid rgba(255,255,255,0.10);

    backdrop-filter: blur(14px);

    box-shadow:
        0 6px 22px rgba(0,0,0,0.25);

    transition:
        transform 0.2s ease,
        border-color 0.2s ease;
}

.nika-card:hover {

    transform: translateY(-3px);

    border-color:
        rgba(255,80,30,0.55);

}

.nika-card-icon {

    font-size: 27px;

    margin-bottom: 3px;

}

.nika-card-title {

    font-size: 16px;

    font-weight: 800;

    margin-bottom: 2px;

}

.nika-card-text {

    font-size: 11px;

    opacity: 0.62;

}

/* =========================================================
   NIKA MAIN UI
   ========================================================= */

.nika-hero {

    text-align: center;

    padding: 25px 20px 20px 20px;

    position: relative;
}

.nika-logo {

    font-size: 64px;

    line-height: 1;

    margin-bottom: 8px;

    animation:
        nika-pulse 3s ease-in-out infinite;

    filter:
        drop-shadow(
            0 0 12px rgba(255,140,0,0.65)
        );
}

.nika-title {

    font-size: 52px;

    font-weight: 950;

    letter-spacing: 8px;

    margin: 0;

    background:
        linear-gradient(
            90deg,
            #ffb347,
            #ff5a36,
            #ffb347
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    background-size: 200% auto;

    animation:
        nika-title-shine 4s linear infinite;

    filter:
        drop-shadow(
            0 0 10px rgba(255,70,20,0.35)
        );
}

.nika-subtitle {
    font-size: 18px;
    opacity: 0.75;
    margin-top: 12px;
    letter-spacing: 2px;
}

.nika-status {

    display: inline-block;

    margin-top: 18px;

    padding: 8px 18px;

    border-radius: 30px;

    background: rgba(255, 70, 70, 0.12);

    border: 1px solid rgba(255, 90, 90, 0.35);

    font-size: 14px;

    letter-spacing: 1px;

    animation:
        nika-online-pulse 2.5s ease-in-out infinite;
}


/* =========================================================
   NIKA ONLINE GLOW
   ========================================================= */

@keyframes nika-online-pulse {

    0%, 100% {

        box-shadow:
            0 0 5px rgba(255,60,20,0.10);

        border-color:
            rgba(255,90,50,0.30);
    }

    50% {

        box-shadow:
            0 0 25px rgba(255,60,20,0.35),
            0 0 50px rgba(255,60,20,0.10);

        border-color:
            rgba(255,100,50,0.70);
    }

}

.nika-section {
    text-align: center;
    margin: 30px 0 20px 0;
}

.nika-section h2 {

    font-size: 27px;

    font-weight: 850;

    margin: 0;

    text-shadow:
        0 0 15px rgba(255,70,30,0.20);
}

/* =========================================================
   NIKA PREMIUM FEATURE BUTTONS
   ========================================================= */

div.stButton > button {

    min-height: 88px;

    padding: 8px 10px;

    border-radius: 16px;

    font-size: 14px;

    font-weight: 750;

    line-height: 1.35;

    color: white;

    background:
        linear-gradient(
            145deg,
            rgba(35, 25, 35, 0.72),
            rgba(10, 10, 18, 0.78)
        );

    border:
        1px solid rgba(255,255,255,0.10);

    backdrop-filter: blur(14px);

    box-shadow:
        0 6px 20px rgba(0,0,0,0.28);

    transition:
        transform 0.20s ease,
        box-shadow 0.20s ease,
        border-color 0.20s ease,
        background 0.20s ease;
}


/* Hover */

div.stButton > button:hover {

    transform:
        translateY(-3px);

    border-color:
        rgba(255,85,35,0.65);

    background:
        linear-gradient(
            145deg,
            rgba(65, 25, 30, 0.78),
            rgba(18, 10, 18, 0.82)
        );

    box-shadow:
        0 0 18px rgba(255,70,20,0.18),
        0 10px 28px rgba(0,0,0,0.40);
}


/* Click */

div.stButton > button:active {

    transform:
        scale(0.97);

}


/* =========================================================
   NIKA PULSE
   ========================================================= */

@keyframes nika-pulse {

    0%, 100% {

        transform: scale(1);

        filter:
            drop-shadow(
                0 0 8px
                rgba(255,150,0,0.5)
            );
    }

    50% {

        transform: scale(1.12);

        filter:
            drop-shadow(
                0 0 30px
                rgba(255,70,0,0.9)
            );
    }

}

/* =========================================================
   NIKA CINEMATIC OVERLAY
   ========================================================= */

.nika-cinematic-overlay {

    position: fixed;

    top: 0;
    left: 0;

    width: 100vw;
    height: 100vh;

    pointer-events: none;

    z-index: -1;

    background:
        radial-gradient(
            circle at 50% 35%,
            rgba(255, 70, 20, 0.08),
            transparent 45%
        ),

        linear-gradient(
            rgba(5, 5, 10, 0.15),
            rgba(5, 5, 10, 0.55)
        );
}
/* =========================================================
   NIKA SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {

    background:
        rgba(8, 8, 15, 0.72);

    backdrop-filter:
        blur(18px);

    border-right:
        1px solid rgba(255,255,255,0.08);
}


.nika-sidebar-title {

    text-align: center;

    font-size: 32px;

    font-weight: 900;

    letter-spacing: 4px;

    margin-top: 5px;

    text-shadow:
        0 0 12px rgba(255,100,20,0.7),
        0 0 25px rgba(255,50,0,0.35);
}


.nika-sidebar-status {

    text-align: center;

    margin-top: 5px;

    margin-bottom: 15px;

    font-size: 12px;

    letter-spacing: 2px;

    color: #ff7650;

    animation:
        nika-sidebar-glow 2.5s ease-in-out infinite;
}


@keyframes nika-sidebar-glow {

    0%, 100% {
        opacity: 0.65;
        text-shadow: 0 0 5px rgba(255,70,20,0.2);
    }

    50% {
        opacity: 1;
        text-shadow:
            0 0 10px rgba(255,70,20,0.8),
            0 0 20px rgba(255,70,20,0.4);
    }

}


.nika-sidebar-heading {

    font-size: 17px;

    font-weight: 800;

    margin-bottom: 12px;

    letter-spacing: 0.5px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# NIKA HERO
# ============================================================

st.markdown("""
<div class="nika-hero">
<div class="nika-logo">☀️</div>
<h1 class="nika-title">NIKA</h1>
<div class="nika-subtitle">LEARN · UNDERSTAND · LISTEN · EXPLORE</div>
<div class="nika-status">● NIKA AI ONLINE</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# NIKA ACTIONS
# ============================================================

st.markdown("""
<div class="nika-section">
    <h2>What do you want to do?</h2>
</div>
""", unsafe_allow_html=True)


# ============================================================
# NIKA FEATURE CARDS
# ============================================================

col1, col2, col3 = st.columns(3, gap="small")


with col1:

    if st.button(
        "🔊\nRead My Notes\nListen to your study material",
        key="nika_read_notes",
        use_container_width=True
    ):
        st.session_state["selected_feature"] = "🔊 Text-to-Speech"
        st.rerun()


with col2:

    if st.button(
        "🎙️\nTalk to NIKA\nAsk questions using your voice",
        key="nika_talk",
        use_container_width=True
    ):
        st.session_state["selected_feature"] = "🎙️ Voice Assistant"
        st.rerun()


with col3:

    if st.button(
        "📷\nScan Notes\nExtract information from notes",
        key="nika_scan",
        use_container_width=True
    ):
        st.session_state["selected_feature"] = "📷 Notes Scanner"
        st.rerun()


col4, col5, col6 = st.columns(3, gap="small")


with col4:

    if st.button(
        "🤖\nAI Learning\nUnderstand difficult concepts",
        key="nika_learning",
        use_container_width=True
    ):
        st.session_state["selected_feature"] = "🤖 AI Learning"
        st.rerun()


with col5:

    if st.button(
        "🎯\nTake Quiz\nTest what you have learned",
        key="nika_quiz",
        use_container_width=True
    ):
        st.session_state["selected_feature"] = "🎯 Adaptive Quiz"
        st.rerun()


with col6:

    if st.button(
        "💬\nChat with NIKA\nAsk NIKA about your notes",
        key="nika_chat",
        use_container_width=True
    ):
        st.session_state["selected_feature"] = "💬 Ask NIKA"
        st.rerun()

feature = st.session_state["selected_feature"]

st.write(
    f"### Current feature: {feature}"
)

# ============================================================
# NIKA SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="nika-sidebar-title">
            ☀️ NIKA
        </div>

        <div class="nika-sidebar-status">
            ● AI ONLINE
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        """
        <div class="nika-sidebar-heading">
            ⚙️ Learning Controls
        </div>
        """,
        unsafe_allow_html=True
    )

    mode = st.selectbox(
        "AI Learning Mode",
        [
            "Explain",
            "Summarize",
            "Quiz",
            "Flashcards",
            "Study Notes"
        ],
        key="sidebar_mode"
    )

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ],
        key="sidebar_difficulty"
    )

    language = st.selectbox(
        "Language",
        [
            "English",
            "Hindi"
        ],
        key="sidebar_language"
    )

# ============================================================
# NIKA FEATURES
# ============================================================

st.divider()

st.header("🧠 NIKA Features")

# ============================================================
# CURRENT FEATURE
# ============================================================

feature = st.session_state["selected_feature"]

# ============================================================
# FEATURE SELECTION
# ============================================================

if feature == "📷 Notes Scanner":
    st.info("Upload notes below to scan and extract text.")

elif feature == "👁️ Vision Analysis":
    st.info("Upload notes below to understand diagrams, formulas and visual content.")

elif feature == "🤖 AI Learning":
    st.info("Upload notes below and generate AI-powered learning material.")

elif feature == "🎯 Adaptive Quiz":
    st.info("Generate an adaptive quiz from your study material.")

elif feature == "💬 Ask NIKA":
    st.info("Ask NIKA questions about your uploaded material.")

elif feature == "🔊 Text-to-Speech":
    st.info("Convert your study material into spoken audio.")

elif feature == "🎙️ Voice Assistant":
    st.info("Speak to NIKA using your microphone.")

# ============================================================
# VOICE AI ASSISTANT
# ============================================================

if feature == "🎙️ Voice Assistant":

    st.divider()

    st.header("🎙️ Voice AI Assistant")

    st.write(
        "Speak your question and NIKA will answer with voice."
    )

    audio = record_voice()

    if audio:

        st.success("🎙️ Recording captured!")

        try:

            voice_text = speech_to_text(
                audio["bytes"]
            )

            if voice_text:

                st.write("📝 **You said:**")
                st.info(voice_text)

                with st.spinner(
                    "🤖 NIKA is thinking..."
                ):

                    answer = visiona_chat(
                        voice_text,
                        st.session_state.ocr_text,
                        st.session_state.vision_analysis
                    )

                st.subheader("🤖 NIKA")

                st.markdown(answer)

                with st.spinner(
                    "🔊 Creating voice response..."
                ):

                    audio_file = text_to_speech(
                        answer,
                        "English"
                    )

                st.audio(
                    audio_file,
                    format="audio/mp3"
                )

        except Exception as e:

            st.error(
                f"Voice AI failed: {e}"
            )

# ============================================================
# UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "📷 Upload your notes",
    type=[
        "png",
        "jpg",
        "jpeg",
        "pdf",
        "txt",
        "docx"
    ],
    key="main_notes_uploader"
)

# ============================================================
# FILE PROCESSING
# ============================================================

if uploaded_file:

    file_type = uploaded_file.type

    # --------------------------------------------------------
    # IMAGE FILES
    # --------------------------------------------------------

    if file_type in [
        "image/png",
        "image/jpeg",
        "image/jpg"
    ]:

        image = Image.open(uploaded_file)

        st.session_state.image = image

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("📷 Original Notes")

            st.image(
                image,
                width="stretch"
            )

        with col2:

            st.subheader("🔍 Vision + OCR")

            if st.button(
                "🚀 Analyze Complete Page",
                type="primary",
                use_container_width=True
            ):

                # Reset old learning data
                st.session_state.chat_history = []
                st.session_state.quiz = []
                st.session_state.quiz_answers = {}
                st.session_state.quiz_result = None
                st.session_state.quiz_submitted = False
                st.session_state.ai_result = ""

                # ------------------------------------------------
                # OCR
                # ------------------------------------------------

                with st.spinner(
                    "Step 1/2 — Extracting text..."
                ):

                    try:

                        ocr_text = extract_text(image)

                        st.session_state.ocr_text = ocr_text

                    except Exception as e:

                        st.error(
                            f"OCR failed: {e}"
                        )

                # ------------------------------------------------
                # VISION
                # ------------------------------------------------

                if st.session_state.ocr_text:

                    with st.spinner(
                        "Step 2/2 — Understanding diagrams, "
                        "formulas and concepts..."
                    ):

                        try:

                            analysis = analyze_image(
                                image,
                                st.session_state.ocr_text
                            )

                            st.session_state.vision_analysis = analysis

                            st.success(
                                "Complete multimodal analysis finished!"
                            )

                        except Exception as e:

                            st.error(
                                f"Vision analysis failed: {e}"
                            )


    # --------------------------------------------------------
    # PDF / DOCX / TXT FILES
    # --------------------------------------------------------

    elif file_type in [
        "application/pdf",
        "text/plain",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]:

        if st.button(
            "📄 Extract Document",
            type="primary",
            use_container_width=True
        ):

            with st.spinner(
                "📄 Extracting document text..."
            ):

                try:

                    document_text = extract_document_text(
                        uploaded_file
                    )

                    st.session_state.ocr_text = document_text

                    st.session_state.vision_analysis = ""

                    st.success(
                        "Document text extracted successfully!"
                    )

                except Exception as e:

                    st.error(
                        f"Document extraction failed: {e}"
                    )

# ============================================================
# OCR RESULT
# ============================================================

if feature == "📷 Notes Scanner" and st.session_state.ocr_text:

    st.divider()

    st.header("📝 Extracted Text")

    st.text_area(
        "OCR",
        st.session_state.ocr_text,
        height=200
    )


# ============================================================
# VISION RESULT
# ============================================================

if feature == "👁️ Vision Analysis" and st.session_state.vision_analysis:

    st.divider()

    st.header("👁️ Multimodal Understanding")

    st.markdown(
        st.session_state.vision_analysis
    )


# ============================================================
# AI LEARNING ENGINE
# ============================================================

if feature == "🤖 AI Learning" and st.session_state.ocr_text:

    st.divider()

    st.header("🤖 AI Learning Engine")

    st.write(
        f"**Mode:** {mode}  |  "
        f"**Difficulty:** {difficulty}  |  "
        f"**Language:** {language}"
    )


    if st.button(
        f"✨ Generate {mode}",
        type="primary",
        use_container_width=True
    ):

        text = st.session_state.ocr_text

        prompt = f"""
You are NIKA, an intelligent engineering education assistant.

Student notes:

{text}

Additional multimodal analysis:

{st.session_state.vision_analysis}

Create a {mode.lower()} for a
{difficulty.lower()} level student.

Language:
{language}

Use the visual analysis when relevant.

Important requirements:

- Preserve formulas accurately.
- Explain diagrams when relevant.
- Use clear engineering terminology.
- Give useful examples.
- Highlight important exam concepts.
- Do not invent unsupported information.
"""

        with st.spinner(
            "NIKA is generating your learning material..."
        ):

            try:

                result = ask_ai(prompt)

                st.session_state.ai_result = result

            except Exception as e:

                st.error(
                    f"AI generation failed: {e}"
                )


# ============================================================
# FINAL RESULT
# ============================================================

if st.session_state.ai_result:

    st.divider()

    st.header("🧠 NIKA Result")

    st.markdown(
        st.session_state.ai_result
    )


# ============================================================
# ADAPTIVE QUIZ
# ============================================================

if feature == "🎯 Adaptive Quiz":

    st.divider()

    st.header("🎯 Adaptive Knowledge Quiz")

    st.write(
        "NIKA generates questions from your uploaded "
        "material and measures your understanding by topic."
    )


    # --------------------------------------------------------
    # GENERATE QUIZ
    # --------------------------------------------------------

    if not st.session_state.quiz:

        if st.button(
            "🧠 Generate Adaptive Quiz",
            type="primary",
            use_container_width=True
        ):

            with st.spinner(
                "NIKA is designing your personalized quiz..."
            ):

                try:

                    quiz = generate_quiz(
                        st.session_state.ocr_text,
                        st.session_state.vision_analysis,
                        difficulty,
                        5
                    )

                    st.session_state.quiz = quiz

                    st.session_state.quiz_answers = {}

                    st.session_state.quiz_result = None

                    st.session_state.quiz_submitted = False

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Quiz generation failed: {e}"
                    )


    # --------------------------------------------------------
    # DISPLAY QUIZ
    # --------------------------------------------------------

    if st.session_state.quiz:

        quiz = st.session_state.quiz

        st.subheader(
            f"📝 {len(quiz)} Questions"
        )

        for index, question in enumerate(quiz):

            st.markdown(
                f"### Question {index + 1}"
            )

            st.write(
                question["question"]
            )

            selected = st.radio(
                "Choose your answer:",
                question["options"],
                key=f"quiz_question_{index}",
                disabled=st.session_state.quiz_submitted
            )

            st.session_state.quiz_answers[index] = selected

            st.caption(
                f"Topic: {question['topic']}"
            )


        # ----------------------------------------------------
        # SUBMIT
        # ----------------------------------------------------

        if not st.session_state.quiz_submitted:

            if st.button(
                "📊 Submit Quiz",
                type="primary",
                use_container_width=True
            ):

                result = score_quiz(
                    st.session_state.quiz,
                    st.session_state.quiz_answers
                )

                st.session_state.quiz_result = result

                st.session_state.quiz_submitted = True

                st.rerun()


        # ----------------------------------------------------
        # RESULTS
        # ----------------------------------------------------

        if st.session_state.quiz_result:

            result = st.session_state.quiz_result

            st.divider()

            st.header("📊 Your Learning Report")


            # Overall score
            percentage = result["percentage"]

            if percentage >= 80:

                st.success(
                    f"🏆 Excellent! Your score is {percentage}%"
                )

            elif percentage >= 60:

                st.info(
                    f"👍 Good progress! Your score is {percentage}%"
                )

            else:

                st.warning(
                    f"📚 More practice recommended. "
                    f"Your score is {percentage}%"
                )


            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Score",
                    f"{percentage}%"
                )

            with col2:

                st.metric(
                    "Correct",
                    result["correct"]
                )

            with col3:

                st.metric(
                    "Incorrect",
                    result["incorrect"]
                )


            # ------------------------------------------------
            # TOPIC PERFORMANCE
            # ------------------------------------------------

            st.subheader(
                "🧠 Topic Performance"
            )

            topic_stats = result["topic_stats"]

            for topic, stats in topic_stats.items():

                score = stats["percentage"]

                if score >= 80:

                    icon = "🟢"

                elif score >= 60:

                    icon = "🟡"

                else:

                    icon = "🔴"

                st.write(
                    f"{icon} **{topic}** — "
                    f"{score}% "
                    f"({stats['correct']}/{stats['total']})"
                )


            # ------------------------------------------------
            # WEAK TOPICS
            # ------------------------------------------------

            weak_topics = get_weak_topics(
                topic_stats
            )

            st.subheader(
                "🎯 Recommended Practice"
            )

            if weak_topics:

                st.warning(
                    "NIKA detected concepts that need more practice."
                )

                for weak in weak_topics:

                    st.write(
                        f"🔴 **{weak['topic']}** — "
                        f"{weak['percentage']}%"
                    )

                st.info(
                    "Next upgrade: NIKA will automatically "
                    "generate targeted questions for these weak topics."
                )

            else:

                st.success(
                    "🎉 No major weak areas detected!"
                )


            # ------------------------------------------------
            # QUESTION REVIEW
            # ------------------------------------------------

            st.subheader(
                "🔎 Answer Review"
            )

            for index, review in enumerate(
                result["results"]
            ):

                if review["correct"]:

                    st.success(
                        f"Question {index + 1}: Correct ✅"
                    )

                else:

                    st.error(
                        f"Question {index + 1}: Incorrect ❌"
                    )

                    st.write(
                        f"**Your answer:** "
                        f"{review['user_answer']}"
                    )

                    st.write(
                        f"**Correct answer:** "
                        f"{review['correct_answer']}"
                    )

                st.caption(
                    f"Topic: {review['topic']}"
                )

                st.write(
                    review["explanation"]
                )


            # ------------------------------------------------
            # RETAKE
            # ------------------------------------------------

            if st.button(
                "🔄 Generate Another Quiz",
                use_container_width=True
            ):

                st.session_state.quiz = []

                st.session_state.quiz_answers = {}

                st.session_state.quiz_result = None

                st.session_state.quiz_submitted = False

                st.rerun()





# ============================================================
# RESET
# ============================================================

st.sidebar.divider()

if st.sidebar.button(
    "🔄 Reset NIKA",
    use_container_width=True
):

    st.session_state.image = None
    st.session_state.ocr_text = ""
    st.session_state.vision_analysis = ""
    st.session_state.ai_result = ""
    st.session_state.chat_history = []

    st.session_state.quiz = []
    st.session_state.quiz_answers = {}
    st.session_state.quiz_result = None
    st.session_state.quiz_submitted = False

    st.rerun()
# ============================================================
# AI CHAT
# ============================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


if feature == "💬 Ask NIKA":

    st.divider()

    st.header("💬 Ask NIKA")

    st.write(
        "Ask questions about your uploaded notes."
    )

    # Display previous messages

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])


    # Chat input

    user_message = st.chat_input(
    "Ask something about your notes...",
    key="NIKA_chat_input"
)


    if user_message:

        # Show user message

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": user_message
            }
        )


        with st.chat_message("user"):

            st.markdown(user_message)


        # Build context

        context = f"""
OCR TEXT:

{st.session_state.ocr_text}


VISION ANALYSIS:

{st.session_state.vision_analysis}
"""


        # Generate AI response

        with st.chat_message("assistant"):

            with st.spinner("NIKA is thinking..."):

                try:

                    response = visiona_chat(
                        user_message,
                        context
                    )

                    st.markdown(response)

                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": response
                        }
                    )

                except Exception as e:

                    st.error(
                        f"Chat error: {e}"
                    )
# ============================================================
# ADAPTIVE QUIZ ENGINE
# ============================================================

if feature == "🎯 Adaptive Quiz" and st.session_state.ocr_text:

    st.divider()

    st.header("🎯 Adaptive Quiz")

    st.write(
        "NIKA generates questions from your uploaded material "
        "and identifies your weak topics."
    )

    quiz_difficulty = st.select_slider(
        "Quiz Difficulty",
        options=[
            "Beginner",
            "Intermediate",
            "Advanced"
        ],
        value=difficulty,
        key="quiz_difficulty"
    )

    number_of_questions = st.slider(
        "Number of Questions",
        min_value=3,
        max_value=10,
        value=5,
        key="number_of_questions"
    )

    # --------------------------------------------------------
    # GENERATE QUIZ
    # --------------------------------------------------------

    if st.button(
        "🧠 Generate Adaptive Quiz",
        type="primary",
        use_container_width=True,
        key="generate_quiz_button"
    ):

        with st.spinner(
            "NIKA is generating your adaptive quiz..."
        ):

            try:

                questions = generate_quiz(
                    st.session_state.ocr_text,
                    st.session_state.vision_analysis,
                    quiz_difficulty,
                    number_of_questions
                )

                st.session_state.quiz = questions
                st.session_state.quiz_result = None

                st.success(
                    f"Generated {len(questions)} questions!"
                )

            except Exception as e:

                st.error(
                    f"Quiz generation failed: {e}"
                )


    # --------------------------------------------------------
    # DISPLAY QUIZ
    # --------------------------------------------------------

    if st.session_state.quiz:

        questions = st.session_state.quiz

        st.subheader(
            f"📝 Quiz — {len(questions)} Questions"
        )

        with st.form("NIKA_quiz_form"):

            answers = {}

            for index, question in enumerate(questions):

                st.markdown(
                    f"### Question {index + 1}"
                )

                st.write(
                    question["question"]
                )

                selected_answer = st.radio(
                    "Select your answer:",
                    question["options"],
                    key=f"quiz_answer_{index}"
                )

                answers[index] = selected_answer

                st.caption(
                    f"Topic: {question['topic']}"
                )

            submitted = st.form_submit_button(
                "✅ Submit Quiz",
                use_container_width=True
            )

        # ----------------------------------------------------
        # SCORE
        # ----------------------------------------------------

        if submitted:

            try:

                result = score_quiz(
                    questions,
                    answers
                )

                st.session_state.quiz_result = result

            except Exception as e:

                st.error(
                    f"Could not score quiz: {e}"
                )


    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    if st.session_state.quiz_result:

        result = st.session_state.quiz_result

        st.divider()

        st.subheader("📊 Quiz Results")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Score",
                f"{result['correct']}/{result['total']}"
            )

        with col2:

            st.metric(
                "Accuracy",
                f"{result['percentage']}%"
            )

        with col3:

            st.metric(
                "Incorrect",
                result["incorrect"]
            )

        st.progress(
            result["percentage"] / 100
        )

        # ----------------------------------------------------
        # WEAK TOPICS
        # ----------------------------------------------------

        weak_topics = get_weak_topics(
            result["topic_stats"]
        )

        if weak_topics:

            st.subheader(
                "⚠️ Topics You Need to Practice"
            )

            for weak in weak_topics:

                st.warning(
                    f"{weak['topic']} — "
                    f"{weak['percentage']}%"
                )

        else:

            st.success(
                "🎉 No major weak topics detected!"
            )

        # ----------------------------------------------------
        # QUESTION REVIEW
        # ----------------------------------------------------

        st.subheader(
            "🔎 Question Review"
        )

        for index, item in enumerate(
            result["results"]
        ):

            if item["correct"]:

                st.success(
                    f"Question {index + 1} — Correct ✅"
                )

            else:

                st.error(
                    f"Question {index + 1} — Incorrect ❌"
                )

            st.write(
                f"**Your answer:** "
                f"{item['user_answer']}"
            )

            st.write(
                f"**Correct answer:** "
                f"{item['correct_answer']}"
            )

            st.info(
                item["explanation"]
            )

            st.caption(
                f"Topic: {item['topic']}"
            )
    # ============================================================
# ADAPTIVE WEAK-TOPIC TUTOR
# ============================================================

if st.session_state.quiz_result:

    st.divider()

    st.header("🎓 NIKA Adaptive Tutor")

    st.write(
        "NIKA identified your weaker areas and can now create "
        "a focused lesson to help you improve."
    )

    result = st.session_state.quiz_result

    weak_topics = get_weak_topics(
        result["topic_stats"]
    )

    if weak_topics:

        topic_names = [
            weak["topic"]
            for weak in weak_topics
        ]

        selected_topic = st.selectbox(
            "Choose a topic to practice",
            topic_names,
            key="adaptive_topic"
        )

        selected_percentage = next(
            weak["percentage"]
            for weak in weak_topics
            if weak["topic"] == selected_topic
        )

        st.info(
            f"Current performance: {selected_percentage}%"
        )

        if st.button(
            "🎓 Teach Me This Topic",
            type="primary",
            use_container_width=True,
            key="teach_weak_topic"
        ):

            with st.spinner(
                "NIKA is creating a personalized lesson..."
            ):

                try:

                    lesson = generate_weak_topic_lesson(
                        st.session_state.ocr_text,
                        selected_topic,
                        selected_percentage,
                        st.session_state.vision_analysis
                    )

                    st.session_state.adaptive_lesson = lesson

                except Exception as e:

                    st.error(
                        f"Adaptive lesson failed: {e}"
                    )

    else:

        st.success(
            "🎉 You currently have no major weak topics!"
        )


# ============================================================
# ADAPTIVE LESSON RESULT
# ============================================================

if "adaptive_lesson" in st.session_state:

    if st.session_state.adaptive_lesson:

        st.divider()

        st.subheader(
            "📚 Personalized Remedial Lesson"
        )

        st.markdown(
            st.session_state.adaptive_lesson
        )

# ============================================================
# TEXT TO SPEECH — MAIN ACCESSIBILITY FEATURE
# ============================================================

if feature == "🔊 Text-to-Speech" and st.session_state.ocr_text:

    st.divider()

    st.header("🔊 NIKA Text-to-Speech")

    st.write(
        "Listen to your study material instead of reading it."
    )

    col1, col2 = st.columns(2)

    with col1:

        speech_source = st.selectbox(
            "📖 What should NIKA read?",
            [
                "Extracted Notes",
                "AI Explanation",
                "Vision Analysis"
            ],
            key="speech_source"
        )

    with col2:

        speech_language = st.selectbox(
            "🌐 Speech Language",
            [
                "English",
                "Hindi"
            ],
            key="speech_language"
        )

    # Select text
    if speech_source == "Extracted Notes":

        speech_text = st.session_state.ocr_text

    elif speech_source == "AI Explanation":

        speech_text = st.session_state.ai_result

    else:

        speech_text = st.session_state.vision_analysis

    # Preview
    st.subheader("📄 Text to Read")

    if speech_text.strip():

        st.text_area(
            "Preview",
            speech_text,
            height=180,
            key="tts_preview"
        )

    else:

        st.warning(
            "No text is available for this option yet."
        )

    # Generate audio
    if st.button(
        "🔊 Generate & Read Aloud",
        type="primary",
        use_container_width=True,
        key="generate_tts"
    ):

        if not speech_text.strip():

            st.warning(
                "There is no text available to read."
            )

        else:

            with st.spinner(
                "🎙️ Preparing your audio..."
            ):

                try:

                    audio_file = text_to_speech(
                        speech_text,
                        speech_language
                    )

                    st.session_state.audio_file = audio_file
                    st.session_state.tts_text = speech_text

                    st.success(
                        "✅ Audio ready!"
                    )

                except Exception as e:

                    st.error(
                        f"Text-to-speech failed: {e}"
                    )

    # Audio player
    if st.session_state.audio_file:

        st.subheader("🎧 Your Audio")

        st.audio(
            st.session_state.audio_file,
            format="audio/mp3"
        )