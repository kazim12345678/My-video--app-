import streamlit as st
from datetime import datetime
import random
import textwrap

st.set_page_config(
    page_title="Creator Studio Demo",
    page_icon="🎥",
    layout="wide"
)

# -----------------------------
# Helper functions (fake logic)
# -----------------------------
def generate_fake_script(topic, style):
    base = f"""
    Hey there, today we're talking about {topic}.
    You know, most people feel stuck not because they lack talent,
    but because they repeat the same habits every single day.
    In this session, we'll break down a simple, practical framework
    you can start using immediately to get unstuck and move forward
    with more clarity, confidence, and momentum.
    """
    if style == "Dr. Shadé Zahrai style":
        base += """
        We'll explore mindset shifts, micro-habits, and powerful questions
        you can ask yourself whenever you feel bored, deflated, or off-track.
        Remember: small, consistent changes compound into massive transformation.
        """
    return textwrap.dedent(base).strip()


def generate_fake_linkedin_caption(topic):
    caption = f"""
    🎯 Feeling stuck with your {topic}?  

    In my latest video, I break down:
    • 3 subtle habits that keep you stuck  
    • 3 simple shifts to get your momentum back  
    • A practical question you can ask yourself today  

    Watch the full video and tell me:
    👉 What’s ONE habit you’re ready to change?

    #growth #mindset #leadership #personaldevelopment
    """
    return textwrap.dedent(caption).strip()


def generate_fake_youtube_description(topic):
    desc = f"""
    In this video, we dive deep into how to get unstuck in your {topic} journey.

    You’ll learn:
    • Why feeling bored or deflated is actually a signal, not a failure  
    • How to reframe your self-talk when you feel stuck  
    • A simple, repeatable framework to rebuild momentum  

    This video is inspired by high-performance coaching and mindset work
    similar to what you might see from creators like Dr. Shadé Zahrai.

    If this helped you, like, comment, and subscribe for more content on
    mindset, leadership, and personal growth.
    """
    return textwrap.dedent(desc).strip()


def fake_processing(label, steps=5, delay=0.2):
    progress = st.progress(0, text=label)
    for i in range(steps):
        progress.progress(int((i + 1) / steps * 100), text=f"{label} ({i+1}/{steps})")
    progress.empty()


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🎬 Creator Studio Demo")
st.sidebar.markdown("This is a **demo app** with fake logic.\n\nLater we’ll plug in your **real voice + video**.")
mode = st.sidebar.radio(
    "Choose mode:",
    ["Idea → Script", "Upload → Process (Demo)", "Social Captions"]
)

st.sidebar.markdown("---")
st.sidebar.caption(f"Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# -----------------------------
# Main layout
# -----------------------------
st.title("🎥 Creator Studio Demo (Dr. Shadé style assumption)")
st.write("This is a **demo version** with placeholder logic. Later we’ll connect your **real voice, video, and automation.**")

# -----------------------------
# Mode 1: Idea → Script
# -----------------------------
if mode == "Idea → Script":
    st.subheader("🧠 From Topic to Script (Demo)")

    col1, col2 = st.columns(2)

    with col1:
        topic = st.text_input(
            "Your topic (demo):",
            value="5 Habits Keeping You Stuck & How to Get Unstuck"
        )
        style = st.selectbox(
            "Content style:",
            ["Dr. Shadé Zahrai style", "Motivational coach", "Corporate trainer"]
        )
        generate_btn = st.button("Generate demo script")

    with col2:
        st.markdown("### Notes")
        st.markdown(
            "- This script is **fake/demo**.\n"
            "- Later we’ll plug in **real LLM + your voice tone**.\n"
            "- You can copy this and tweak it for your video."
        )

    if generate_btn:
        fake_processing("Generating demo script...")
        script = generate_fake_script(topic, style)
        st.markdown("### 🎤 Demo Script")
        st.code(script, language="markdown")

# -----------------------------
# Mode 2: Upload → Process (Demo)
# -----------------------------
elif mode == "Upload → Process (Demo)":
    st.subheader("📂 Upload Video / Audio (Demo Only)")

    col1, col2 = st.columns(2)

    with col1:
        video_file = st.file_uploader(
            "Upload your video file (demo, not processed):",
            type=["mp4", "mov", "mkv", "avi"]
        )
        audio_file = st.file_uploader(
            "Upload your voice/audio file (demo, not processed):",
            type=["mp3", "wav", "m4a"]
        )

        process_type = st.multiselect(
            "Select demo processing steps:",
            [
                "Clean background noise (fake)",
                "Enhance voice clarity (fake)",
                "Auto-cut silences (fake)",
                "Generate subtitles (fake)",
                "Prepare LinkedIn clip (fake)"
            ],
            default=["Clean background noise (fake)", "Generate subtitles (fake)"]
        )

        process_btn = st.button("Run demo processing")

    with col2:
        st.markdown("### What this demo does")
        st.markdown(
            "- **Does NOT** actually modify your files.\n"
            "- Simulates a **real pipeline** with progress bars.\n"
            "- Later we’ll connect **FFmpeg, Whisper, etc.** for real processing."
        )

    if process_btn:
        if not video_file and not audio_file:
            st.error("Please upload at least a video or audio file (even for demo).")
        else:
            fake_processing("Analyzing file(s)...")
            for step in process_type:
                fake_processing(step + " ...")
            st.success("✅ Demo processing complete (no real changes made).")
            st.info("In the real version, you’ll be able to **download processed files** from here.")

# -----------------------------
# Mode 3: Social Captions
# -----------------------------
elif mode == "Social Captions":
    st.subheader("📣 Social Media Captions (Demo)")

    topic = st.text_input(
        "What is your video about?",
        value="5 Habits Keeping You Stuck & 5 Ways to Get Unstuck"
    )
    platform = st.radio(
        "Choose platform:",
        ["LinkedIn", "YouTube"],
        horizontal=True
    )

    generate_cap_btn = st.button("Generate demo caption")

    if generate_cap_btn:
        fake_processing("Generating caption...")
        if platform == "LinkedIn":
            caption = generate_fake_linkedin_caption(topic)
            st.markdown("### 💼 LinkedIn Caption (Demo)")
            st.code(caption, language="markdown")
        else:
            desc = generate_fake_youtube_description(topic)
            st.markdown("### ▶️ YouTube Description (Demo)")
            st.code(desc, language="markdown")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption(
    "Demo only • No real processing yet • Next step: plug in your **real voice, video, and automation.**"
)
