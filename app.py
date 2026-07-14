import json
import streamlit as st

from transcriber import AudioTranscriber
from summarize import MeetingSummarizer


# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="🎙️",
    layout="wide"
)


# --------------------------------------------------
# Load Models Once
# --------------------------------------------------

@st.cache_resource
def load_transcriber():
    return AudioTranscriber()


@st.cache_resource
def load_summarizer():
    return MeetingSummarizer()


transcriber = load_transcriber()
summarizer = load_summarizer()


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "summary" not in st.session_state:
    st.session_state.summary = None

if "language" not in st.session_state:
    st.session_state.language = ""


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.title("⚙️ Settings")

    output_language = st.selectbox(
        "Summary Language",
        ["English", "Hindi"]
    )

    st.info(
        """
Supported Languages

✅ English

✅ Hindi

✅ Hinglish
"""
    )


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🎙️ AI Meeting Assistant")

st.write(
    "Upload your meeting audio and get an AI generated transcript and summary."
)


# --------------------------------------------------
# Upload
# --------------------------------------------------

uploaded_audio = st.file_uploader(
    "Upload Audio",
    type=["mp3", "wav", "m4a"]
)


# --------------------------------------------------
# Processing
# --------------------------------------------------

if uploaded_audio:

    progress = st.progress(0)

    try:

        progress.progress(20)

        with st.spinner("🎧 Transcribing audio..."):

            transcript, language = transcriber.transcribe(
                uploaded_audio
            )

        progress.progress(70)

        with st.spinner("🤖 Generating AI Summary..."):

            summary = summarizer.summarize(
                transcript
            )

        progress.progress(100)
        progress.empty()

        st.session_state.transcript = transcript
        st.session_state.summary = summary
        st.session_state.language = language

        st.success("Processing Completed!")

    except Exception as e:

        st.error(f"Error : {e}")


# --------------------------------------------------
# Display
# --------------------------------------------------

if st.session_state.transcript:

    transcript = st.session_state.transcript
    summary = st.session_state.summary

    word_count = len(transcript.split())
    character_count = len(transcript)
    reading_time = word_count / 150

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Words",
        word_count
    )

    col2.metric(
        "Characters",
        character_count
    )

    col3.metric(
        "Reading Time",
        f"{reading_time:.1f} min"
    )

    st.divider()

    tab1, tab2 = st.tabs(
        [
            "📝 Transcript",
            "🤖 Summary"
        ]
    )

    # --------------------------------------

    with tab1:

        st.subheader("Detected Language")

        st.success(
            st.session_state.language.upper()
        )

        st.write(transcript)

        st.download_button(
            "⬇️ Download Transcript",
            transcript,
            file_name="transcript.txt",
            mime="text/plain"
        )

    # --------------------------------------

    with tab2:

        if summary:

            st.header(
                summary.get(
                    "meeting_title",
                    "Meeting"
                )
            )

            st.subheader("Executive Summary")

            st.write(
                summary.get(
                    "executive_summary",
                    ""
                )
            )

            st.subheader("Key Discussion Points")

            for item in summary.get(
                "key_discussion_points",
                []
            ):
                st.write(f"• {item}")

            st.subheader("Decisions Taken")

            for item in summary.get(
                "decisions_taken",
                []
            ):
                st.success(item)

            st.subheader("Action Items")

            for item in summary.get(
                "action_items",
                []
            ):

                owner = item.get("owner", "Unknown")

                task = item.get("task", "")

                st.write(
                    f"👤 **{owner}** → {task}"
                )

            st.subheader("Open Questions")

            for item in summary.get(
                "open_questions",
                []
            ):
                st.write(f"❓ {item}")

            st.subheader("Next Steps")

            for item in summary.get(
                "next_steps",
                []
            ):
                st.write(f"➡️ {item}")

            st.download_button(
                "⬇️ Download Summary JSON",
                json.dumps(
                    summary,
                    indent=4,
                    ensure_ascii=False
                ),
                file_name="meeting_summary.json",
                mime="application/json"
            )