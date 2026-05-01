import streamlit as st

st.set_page_config(
    page_title="Creator Pipeline Demo",
    page_icon="🎥",
    layout="wide"
)

# -----------------------------
# Sidebar – pipeline overview
# -----------------------------
st.sidebar.title("🎬 Creator Pipeline (Demo)")
st.sidebar.markdown(
    """
    **Fake demo** of your future system:

    1. Record simple video on mobile  
    2. Upload to system  
    3. Code cleans voice, fixes background  
    4. Adds Shadé-style text & structure  
    5. Final video ready for YouTube / LinkedIn  
    """
)

st.sidebar.markdown("---")
st.sidebar.markdown("Later: we plug in your **real voice, video, and picture.**")

# -----------------------------
# Main title
# -----------------------------
st.title("🎥 Dr. Shadé-Style Video Demo (FAKE VERSION)")
st.write(
    "This is a **visual demo** of how your future system will look. "
    "Right now everything is **fake / placeholder**, but the layout and flow "
    "match what you described: real face + real voice, upgraded by code."
)

# -----------------------------
# Layout: left = media, right = script
# -----------------------------
col_media, col_script = st.columns([1.2, 1.8])

# -----------------------------
# LEFT: Fake picture, fake voice, fake video
# -----------------------------
with col_media:
    st.subheader("👤 Fake 'Your Picture'")

    # You can replace this URL later with your real hosted image
    st.image(
        "https://via.placeholder.com/600x800.png?text=Your+Photo+Here",
        caption="Placeholder for your real face",
        use_column_width=True
    )

    st.markdown("---")
    st.subheader("🎙 Fake 'Your Voice' (Demo)")

    st.info("Here we will later play your **real cleaned voice**. For now, imagine a demo audio here.")
    st.caption("(We avoid external audio files here to keep Streamlit Cloud simple and error-free.)")

    st.markdown("---")
    st.subheader("🎞 Fake Processed Video (Shadé-style placeholder)")

    st.write(
        "Below is a **sample video** acting as a placeholder for your future "
        "**processed, upgraded video**."
    )

    # Public sample MP4 – you can replace with your own hosted video later
    demo_video_url = "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4"
    st.video(demo_video_url)

    st.caption(
        "Later: this will be your real video after voice cleaning, background fix, and text overlays."
    )

# -----------------------------
# RIGHT: Script, key points, pipeline explanation
# -----------------------------
with col_script:
    st.subheader("🧠 Demo Script (Dr. Shadé-style tone)")

    demo_script = """
    You are not stuck because you lack talent.

    You are stuck because you repeat the same habits every single day.

    Today, I want to share three micro-shifts
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

    st.markdown("### 🔑 Key On-Screen Text (for future captions)")
    st.markdown(
        """
        - *“You are not stuck because you lack talent.”*  
        - *“You are stuck because you repeat the same habits.”*  
        - *“Change your self-talk.”*  
        - *“Momentum is built, not found.”*  
        - *“What is one thing my future self will thank me for?”*  
        """
    )

    st.markdown("### ⚙️ Future Automation (what code will do later)")
    st.markdown(
        """
        **Voice processing (future):**  
        - Reduce room noise (fan, hiss, echo)  
        - Balance volume and clarity  
        - Keep your natural tone, just cleaner  

        **Background handling (future):**  
        - Blur messy background  
        - Or replace with simple clean color  
        - Or use a professional office-style image  

        **On-screen text & motion (future):**  
        - Auto captions based on your speech  
        - Highlight key phrases (bold, color, zoom)  
        - Smooth entry/exit animations for text  

        **Final output (future):**  
        - MP4 ready for YouTube, LinkedIn, Facebook  
        - Same content, but more **professional and engaging**  
        """
    )

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption(
    "This is a FAKE demo on Streamlit. Next step: you send your real voice, video, and picture, "
    "and we connect this layout to real processing."
)
