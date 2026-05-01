import streamlit as st

st.set_page_config(
    page_title="Maintenance KPIs – AI Demo",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Sidebar – topic & audience
# -----------------------------
st.sidebar.title("🎬 AI Trainer Demo")

audience = st.sidebar.selectbox(
    "Audience:",
    ["Operators", "Maintenance Technicians", "Supervisors", "Plant Manager"]
)

st.sidebar.markdown("---")
st.sidebar.write(
    "Fake demo: avatar + fake AI voice + sample video + real script "
    "on **OEE, MTTR, MTBF, KPIs**."
)

# -----------------------------
# Main title
# -----------------------------
st.title("📊 How to Improve OEE, MTTR, MTBF – AI Trainer (FAKE DEMO)")
st.write(
    "This page simulates a **training video** where a person explains how to work with KPIs "
    "like **OEE, MTTR, MTBF**. The media is fake/placeholder, but the **content and structure** "
    "are realistic for your maintenance world."
)

# -----------------------------
# Layout
# -----------------------------
col_media, col_text = st.columns([1.2, 1.8])

# -----------------------------
# LEFT: Avatar + video + voice
# -----------------------------
with col_media:
    st.subheader("👤 Trainer Avatar (Fake Person)")

    # Human-like illustration avatar (not a real person)
    st.image(
        "https://images.pexels.com/photos/1181519/pexels-photo-1181519.jpeg?auto=compress&cs=tinysrgb&w=600",
        caption="Placeholder trainer – later this can be your real photo or custom avatar.",
        use_column_width=True
    )

    st.markdown("---")
    st.subheader("🎞 Training Video Placeholder")

    # Sample video as stand-in for your future real training video
    video_url = "https://samplelib.com/lib/preview/mp4/sample-5s.mp4"
    st.video(video_url)
    st.caption(
        "This is a **sample video** acting as a placeholder for your real KPI/OEE training video."
    )

    st.markdown("---")
    st.subheader("🎙 Fake AI Voice Sample")

    audio_url = "https://samplelib.com/lib/preview/mp3/sample-3s.mp3"
    st.audio(audio_url)
    st.caption(
        "Later: this will be your **real voice**, cleaned and enhanced by AI "
        "(noise reduction, clarity, warmth)."
    )

# -----------------------------
# RIGHT: Script + KPI content + AI pipeline
# -----------------------------
with col_text:
    st.subheader("🧠 Trainer Script – How to Improve OEE, MTTR, MTBF")

    script = f"""
    Welcome. Today we’re talking about **maintenance KPIs** and how to use them to actually
    improve performance on the shop floor – not just in reports.

    We’ll focus on four key metrics:

    1. **OEE – Overall Equipment Effectiveness**  
       OEE tells you how effectively your line is running versus its full potential.
       It combines **Availability, Performance, and Quality**.

    2. **MTTR – Mean Time To Repair**  
       MTTR measures how long it takes, on average, to fix a breakdown.
       Lower MTTR means faster recovery and less downtime.

    3. **MTBF – Mean Time Between Failures**  
       MTBF tells you how long equipment runs, on average, before failing again.
       Higher MTBF means more reliability and fewer interruptions.

    4. **Planned vs Unplanned Downtime**  
       This shows how much of your stoppage is controlled (PM, changeovers)
       versus unexpected (breakdowns, minor stops).

    For **{audience}**, the goal is simple:

    - See these numbers every day  
    - Understand what is driving them  
    - Take small, consistent actions to improve them

    **How to improve OEE:**
    - Reduce small stops and minor jams  
    - Improve changeover discipline and SMED  
    - Attack chronic breakdowns with root cause analysis  
    - Stabilize speed and reduce micro-stops

    **How to improve MTTR:**
    - Standardize troubleshooting steps  
    - Keep critical spares available and organized  
    - Train technicians on common failure patterns  
    - Use clear escalation rules when repair is stuck

    **How to improve MTBF:**
    - Strengthen preventive maintenance (PM) and condition-based checks  
    - Fix root causes, not just symptoms  
    - Eliminate repeat failures with permanent countermeasures  
    - Involve operators in basic care (clean, inspect, tighten)

    Remember: KPIs are not just numbers for reports.
    They are **signals** that tell you where to focus your energy.

    Small, consistent improvements in OEE, MTTR, and MTBF
    compound into massive gains in uptime, output, and stability.
    """

    st.markdown(script)

    st.markdown("### 🔑 Key On-Screen Text (future captions)")
    st.markdown(
        """
        - “OEE = Availability × Performance × Quality”  
        - “Lower MTTR → faster recovery”  
        - “Higher MTBF → more reliability”  
        - “KPIs are signals, not just reports”  
        - “Small improvements compound into big results”  
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
        - Stabilize shaky footage  

        **3️⃣ Text & Motion (future):**  
        - Auto-generate captions from your speech  
        - Highlight key phrases (bold, color, zoom)  
        - Time text with your voice for emphasis  

        **4️⃣ Final Output (future):**  
        - Export MP4 ready for YouTube / LinkedIn / internal training  
        - Same content, but more engaging and polished  
        """
    )

st.markdown("---")
st.caption(
    "This is a FAKE demo using sample media. Next step: you send your real voice, real video, "
    "and real picture, and we connect this layout to real AI processing outside Streamlit."
)
