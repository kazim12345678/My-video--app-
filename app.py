import streamlit as st

st.set_page_config(
    page_title="AI Video + Voice Demo",
    page_icon="🎥",
    layout="wide"
)

# -----------------------------
# Sidebar – topic & style
# -----------------------------
st.sidebar.title("🎬 AI Creator Demo")
topic = st.sidebar.text_input(
    "Topic (demo):",
    value="3 Micro-Shifts to Get Unstuck"
)
style = st.sidebar.selectbox(
    "Style:",
    ["Dr. Shadé Zahrai style", "Motivational coach", "Leadership", "Career growth"]
)

st.sidebar.markdown("---")
st.sidebar.write(
    "This is a **fake demo**. Later we plug in your **real voice, real video, and real picture** "
    "and connect AI processing."
)

# -----------------------------
# Main title
# -----------------------------
st.title("🎥 AI Video + Voice Demo (Shadé-style FAKE VERSION)")
st.write(
    "This page shows how your future system can look: "
    "**original video**, **AI-enhanced video**, **AI voice**, and "
    "**Shadé-style script & captions**. Everything here is **fake media**, "
    "but the structure is real."
)

# -----------------------------
# Layout
# -----------------------------
col_media, col_text = st.columns([1.3, 1.7])

# -----------------------------
# LEFT: Picture + videos + AI voice
# -----------------------------
with col_media:
    st.subheader("👤 Fake 'Your Picture'")
    st.image(
        "https://via.placeholder.com/600x800.png?text=Your+Photo+Here",
        caption="Placeholder for your real face",
        use_column_width=True
    )

    st.markdown("---")
    st.subheader("🎞 Original Demo Video (Fake)")

    original_video_url = "https://samplelib.com/lib/preview/mp4/sample-5s.mp4"
    st.video(original_video_url)
    st.caption("This represents your **raw mobile video** before AI processing.")

    st.markdown("---")
    st.subheader("🤖 AI-Enhanced Demo Video (Fake)")

    # For demo we use another sample; later this will be your processed output
    enhanced_video_url = "https://samplelib.com/lib/preview/mp4/sample-5s.mp4"
    st.video(enhanced_video_url)
    st.caption(
        "This represents your **AI-upgraded video** "
        "(cleaner voice, better background, on-screen text)."
    )

    st.markdown("---")
    st.subheader("🎙 AI Voice Demo (Fake)")

    st.write("Below is a **fake AI voice** placeholder (short sample audio).")

    demo_audio_url = "https://samplelib.com/lib/preview/mp3/sample-3s.mp3"
    st.audio(demo_audio_url)
    st.caption(
        "Later: this will be your **real voice**, cleaned and enhanced by AI "
        "(noise reduction, clarity, balanced volume)."
    )

# -----------------------------
# RIGHT: Script, captions, AI pipeline
# -----------------------------
with col_text:
    st.subheader("🧠 Demo Script (Shadé-style tone)")

    demo_script = f"""
    You are not stuck because you lack talent.

    You are stuck because you repeat the same habits every single day.

    Today, we’re talking about **{topic}**, in a **{style}** tone.

    I want to share three micro-shifts
    that can help you break the cycle
    and rebuild your momentum.

    **Number one – Change your self-talk.**  
    Your words shape your identity.

    **Number two – Take one small action.**  
    Momentum is built, not found.

    **Number three – Ask yourself:**  
    *What is one thing I can do today that my future self will thank me for?*

    Small changes create big transformation.  
    Start today.
    """

    st.markdown(demo_script)

    st.markdown("### 🔑 Key On-Screen Text (future AI captions)")
    st.markdown(
        """
        - “You are not stuck because you lack talent.”  
        - “You repeat the same habits every day.”  
        - “Change your self-talk.”  
        - “Momentum is built, not found.”  
        - “What will my future self thank me for?”  
        """
    )

    st.markdown("### ⚙️ Future AI Pipeline (what code will do later)")
    st.markdown(
        """
        **1️⃣ Voice AI (future):**  
        - Reduce fan / room noise  
        - Enhance clarity and warmth  
        - Keep your natural tone, just more professional  

        **2️⃣ Video AI (future):**  
        - Blur or replace messy background  
        - Adjust brightness / contrast  
        - Stabilize shaky footage (where possible)  

        **3️⃣ Text & Motion (future):**  
        - Auto-generate captions from your speech  
        - Highlight key phrases (bold, color, zoom)  
        - Time text with your voice for Shadé-style emphasis  

        **4️⃣ Final Output (future):**  
        - Export MP4 ready for YouTube / LinkedIn / Reels  
        - Same content, but more **engaging and polished**  
        """
    )

st.markdown("---")
st.caption(
    "This is a FAKE demo on Streamlit using sample media. "
    "Next step: you send your **real voice, real video, and real picture**, "
    "and we connect this layout to real AI processing."
)
