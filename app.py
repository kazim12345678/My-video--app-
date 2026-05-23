import streamlit as st
from groq import Groq

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="KAZIM AI",
    layout="wide"
)

# =========================================================
# SESSION STATES
# =========================================================

if "file_content" not in st.session_state:
    st.session_state.file_content = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "admin_unlocked" not in st.session_state:
    st.session_state.admin_unlocked = False

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("KAZIM AI")

line = st.sidebar.selectbox(
    "Select Line",
    [f"Line {i}" for i in range(1, 21)]
)

machine = st.sidebar.selectbox(
    "Select Machine",
    [f"M{i}" for i in range(1, 21)]
)

st.sidebar.markdown("---")

# =========================================================
# ADMIN PASSWORD
# =========================================================

password = st.sidebar.text_input(
    "Admin Password",
    type="password"
)

if st.sidebar.button("Unlock Admin"):
    if password == "Kazim@2026":
        st.session_state.admin_unlocked = True
        st.sidebar.success("Admin Unlocked")
    else:
        st.sidebar.error("Wrong Password")

# =========================================================
# MAIN TITLE
# =========================================================

st.title("KAZIM AI")
st.subheader("Industrial Diagnostic Assistant")

# =========================================================
# FILE UPLOADER
# =========================================================

uploaded_file = st.file_uploader(
    "Upload M18 Data File",
    type=["txt"]
)

if uploaded_file is not None:

    file_text = uploaded_file.read().decode("utf-8")

    if st.session_state.admin_unlocked:

        action = st.radio(
            "Select File Action",
            ["Override Existing Data", "Add New Data"]
        )

        if action == "Override Existing Data":
            st.session_state.file_content = file_text
            st.success("Data Overridden Successfully")

        elif action == "Add New Data":
            st.session_state.file_content += "\n\n" + file_text
            st.success("Data Added Successfully")

    else:

        if st.session_state.file_content == "":
            st.session_state.file_content = file_text
            st.success("Initial Data Loaded")
        else:
            st.warning("Admin Unlock Required To Modify Existing Data")

# =========================================================
# CURRENT SELECTION
# =========================================================

st.markdown("## Current Selection")

st.markdown(f"""
- **Line:** {line}
- **Machine:** {machine}
""")

# =========================================================
# CHECK API KEY
# =========================================================

if "GROQ_API_KEY" not in st.secrets:
    st.error("Groq API Key Not Found In Streamlit Secrets")
    st.stop()

# =========================================================
# GROQ CLIENT
# =========================================================

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================================================
# USER INPUT
# =========================================================

user_question = st.chat_input(
    "Ask Technical Question..."
)

if user_question:

    # USER MESSAGE
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.markdown(user_question)

    # =====================================================
    # SYSTEM PROMPT
    # =====================================================

    system_prompt = f"""
You are KAZIM AI.

You are a senior industrial maintenance engineer.

Current Line:
{line}

Current Machine:
{machine}

Use ONLY uploaded file data.

Focus only on:
- Module 5Y
- Module 19
- Module 25
- Module 29
- Module 30
- Module 32
- Module 87
- Module 88

Rules:
- Give engineering answers only.
- Mention root cause.
- Mention corrective action.
- Mention preventive action.
- Give practical troubleshooting.
- No generic AI answers.
- If data not found say:
"No related technical data found in uploaded file."

Uploaded Technical Data:
{st.session_state.file_content}
"""

    # =====================================================
    # AI RESPONSE
    # =====================================================

    with st.chat_message("assistant"):

        try:

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_question
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )

            ai_reply = response.choices[0].message.content

        except Exception as e:
            ai_reply = f"Error: {str(e)}"

        st.markdown(ai_reply)

    # SAVE AI RESPONSE

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })
