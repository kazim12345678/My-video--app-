import streamlit as st

st.set_page_config(
    page_title="Dr. Shadé-Style Video Demo",
    page_icon="🎥",
    layout="wide"
)

st.title("🎥 Dr. Shadé-Style Video Demo (FAKE VERSION)")
st.write(
    "This is a **fake demo** showing how your future real video will look "
    "after voice cleaning, background fix, and Shadé-style text overlays."
)

col_media, col_script = st.columns([1.2, 1.8])

with col_media:
    st.subheader("👤 Fake 'Your Picture'")
    st.image(
        "https://via.placeholder.com/600x800.png?text=Your+Photo+Here",
        caption="Placeholder for your real face",
        use_column_width=True
    )

    st.markdown("---")
    st.subheader("🎞 Fake Processed Video (Working Demo)")

    st.write("Below is a **working demo video** (placeholder).")

    # 100% working MP4 link for Streamlit Cloud
    demo_video_url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
    st.video(demo_video_url)

    st.caption("Later: this will be your real processed video.")

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

    st.markdown("### 🔑 Key On-Screen Text (future captions)")
    st.markdown(
        """
        - “You are not stuck because you lack talent.”  
        - “You repeat the same habits every day.”  
        - “Change your self-talk.”  
        - “Momentum is built, not found.”  
        - “What will my future self thank me for?”  
        """
    )

st.markdown("---")
st.caption("Fake demo only. Later we plug in your real voice, video, and picture.")
