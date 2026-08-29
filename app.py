import streamlit as st
from PIL import Image

from ocr_engine import extract_text
from ai_engine import ask_ai, analyze_image
from tts_engine import text_to_speech
from stt_engine import record_voice, speech_to_text
from chat_engine import visiona_chat

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

st.title("☀️ NIKA")

st.caption(
    "Learn. Understand. Listen. Explore."
)

st.divider()

st.header("What do you want to do?")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔊 Read My Notes", use_container_width=True):
        st.session_state["selected_feature"] = "🔊 Text-to-Speech"
        st.rerun()

with col2:
    if st.button("🎙️ Talk to NIKA", use_container_width=True):
        st.session_state["selected_feature"] = "🎙️ Voice Assistant"
        st.rerun()

with col3:
    if st.button("📷 Scan Notes", use_container_width=True):
        st.session_state["selected_feature"] = "📷 Notes Scanner"
        st.rerun()

col4, col5, col6 = st.columns(3)

with col4:
    if st.button("🤖 AI Learning", use_container_width=True):
        st.session_state["selected_feature"] = "🤖 AI Learning"
        st.rerun()

with col5:
    if st.button("🎯 Take Quiz", use_container_width=True):
        st.session_state["selected_feature"] = "🎯 Adaptive Quiz"
        st.rerun()

with col6:
    if st.button("💬 Chat with NIKA", use_container_width=True):
        st.session_state["selected_feature"] = "💬 Ask NIKA"
        st.rerun()

feature = st.session_state["selected_feature"]

st.write(
    f"### Current feature: {feature}"
)



# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Learning Controls")

    mode = st.selectbox(
        "AI Learning Mode",
        [
            "Explain",
            "Summarize",
            "Quiz",
            "Flashcards",
            "Study Notes"
        ]
    )

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    language = st.selectbox(
        "Language",
        [
            "English",
            "Hindi"
        ]
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

st.divider()

st.header("🎙️ Voice AI Assistant")

st.write("Speak your question and NIKA will answer with voice.")

audio = st.session_state.get("voice_recording")

if audio:

    st.success("🎙️ Recording captured!")

    try:

        voice_text = speech_to_text(audio["bytes"])

        if voice_text:

            st.write("📝 **You said:**")
            st.info(voice_text)

            with st.spinner("🤖 NIKA is thinking..."):

                answer = visiona_chat(
                    voice_text,
                    st.session_state.ocr_text,
                    st.session_state.vision_analysis
                )

            st.subheader("🤖 NIKA")

            st.markdown(answer)

            with st.spinner("🔊 Creating voice response..."):

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

uploaded_file = None

if feature in [
    "📷 Notes Scanner",
    "👁️ Vision Analysis",
    "🤖 AI Learning"
]:

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
# IMAGE
# ============================================================

if uploaded_file:

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

            # --------------------------------------------
            # OCR
            # --------------------------------------------

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


            # --------------------------------------------
            # VISION
            # --------------------------------------------

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


# ============================================================
# OCR RESULT
# ============================================================

if st.session_state.ocr_text:

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

if st.session_state.vision_analysis:

    st.divider()

    st.header("👁️ Multimodal Understanding")

    st.markdown(
        st.session_state.vision_analysis
    )


# ============================================================
# AI LEARNING ENGINE
# ============================================================

if st.session_state.ocr_text:

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

if st.session_state.ocr_text:

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


if st.session_state.ocr_text:

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

                    response = NIKA_chat(
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

if st.session_state.ocr_text:

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
# 🎤 VOICE INPUT
# ============================================================

st.divider()

st.header("🎤 Talk to NIKA")

st.write(
    "Ask NIKA using your voice."
)

audio = record_voice()

if audio:

    st.session_state.voice_audio = audio

    st.success("🎙️ Recording captured!")

    st.audio(
        audio["bytes"],
        format="audio/wav"
    )

    with st.spinner("📝 Converting speech to text..."):

        try:

            voice_text = speech_to_text(
                audio["bytes"]
            )

            if voice_text:

                st.session_state.voice_question = voice_text

                st.success("✅ Speech converted!")

                st.write("📝 You said:")
                st.info(voice_text)

                with st.spinner("🤖 NIKA is thinking..."):

                    answer = visiona_chat(
                        voice_text,
                        st.session_state.ocr_text,
                    )

                st.subheader("🤖 NIKA")
                st.markdown(answer)

                with st.spinner("🔊 Creating voice response..."):
                    try:
                        audio_response = text_to_speech(
                            answer,
                            "English"
                        )

                        st.audio(
                            audio_response,
                            format="audio/mp3"
                        )

                    except Exception as e:
                        st.error(
                            f"Text-to-speech failed: {e}"
                        )
                

            else:

                st.warning(
                    "I couldn't understand the recording."
                )

        except Exception as e:

            st.error(
                f"Voice processing failed: {e}"
            )

# ============================================================
# TEXT TO SPEECH — MAIN ACCESSIBILITY FEATURE
# ============================================================

if st.session_state.ocr_text:

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