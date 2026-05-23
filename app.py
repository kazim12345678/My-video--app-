import streamlit as st
from groq import Groq
import pandas as pd
import PyPDF2
import io
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="KAZIM AI PRO",
    layout="wide"
)

# =========================================================
# DARK UI
# =========================================================

st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

h1, h2, h3 {
    color: #00FFAA;
}

.stButton>button {
    background-color: #00AA88;
    color: white;
    border-radius: 10px;
}

.stTextInput>div>div>input {
    background-color: #1F2937;
    color: white;
}

.stTextArea textarea {
    background-color: #1F2937;
    color: white;
}

div[data-testid="stChatMessage"] {
    background-color: #1F2937;
    border-radius: 10px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATES
# =========================================================

if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = {}

if "messages" not in st.session_state:
    st.session_state.messages = []

if "admin_unlocked" not in st.session_state:
    st.session_state.admin_unlocked = False

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("KAZIM AI PRO")

line = st.sidebar.selectbox(
    "Select Line",
    [f"Line {i}" for i in range(1, 21)]
)

machine = st.sidebar.selectbox(
    "Select Machine",
    [f"M{i}" for i in range(1, 21)]
)

# =========================================================
# ADMIN LOGIN
# =========================================================

st.sidebar.markdown("---")

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
# TITLE
# =========================================================

st.title("KAZIM AI PRO")
st.subheader("Industrial AI Diagnostic Platform")

# =========================================================
# FILE UPLOAD
# =========================================================

st.markdown("## Upload Industrial Data")

uploaded_files = st.file_uploader(
    "Upload TXT / PDF / Excel Files",
    type=["txt", "pdf", "xlsx", "csv"],
    accept_multiple_files=True
)

# =========================================================
# PROCESS FILES
# =========================================================

if uploaded_files:

    for uploaded_file in uploaded_files:

        file_name = uploaded_file.name

        file_content = ""

        # TXT
        if file_name.endswith(".txt"):
            file_content = uploaded_file.read().decode("utf-8")

        # PDF
        elif file_name.endswith(".pdf"):

            pdf_reader = PyPDF2.PdfReader(uploaded_file)

            for page in pdf_reader.pages:
                file_content += page.extract_text()

        # CSV
        elif file_name.endswith(".csv"):

            df = pd.read_csv(uploaded_file)

            file_content = df.to_string()

        # EXCEL
        elif file_name.endswith(".xlsx"):

            excel_data = pd.ExcelFile(uploaded_file)

            for sheet in excel_data.sheet_names:

                df = pd.read_excel(uploaded_file, sheet_name=sheet)

                file_content += f"\n\n--- SHEET: {sheet} ---\n\n"
                file_content += df.to_string()

        # SAVE DATA
        st.session_state.knowledge_base[file_name] = file_content

    st.success("Files Uploaded Successfully")

# =========================================================
# DELETE FILE OPTION
# =========================================================

st.markdown("## Uploaded Files")

if len(st.session_state.knowledge_base) > 0:

    for file in list(st.session_state.knowledge_base.keys()):

        col1, col2 = st.columns([8, 1])

        with col1:
            st.write(f"📁 {file}")

        with col2:

            if st.button("❌", key=file):

                del st.session_state.knowledge_base[file]

                st.rerun()

else:
    st.info("No files uploaded.")

# =========================================================
# KPI DASHBOARD
# =========================================================

st.markdown("## KPI Dashboard")

total_files = len(st.session_state.knowledge_base)

total_chars = sum(
    len(content)
    for content in st.session_state.knowledge_base.values()
)

col1, col2, col3 = st.columns(3)

col1.metric("Uploaded Files", total_files)

col2.metric("Data Size", f"{round(total_chars/1000,2)} K")

col3.metric("Chat History", len(st.session_state.messages))

# =========================================================
# SHOW CURRENT SELECTION
# =========================================================

st.markdown("## Current Selection")

st.markdown(f"""
- **Line:** {line}
- **Machine:** {machine}
- **Time:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
""")

# =========================================================
# CHECK API KEY
# =========================================================

if "GROQ_API_KEY" not in st.secrets:
    st.error("Groq API Key Missing")
    st.stop()

# =========================================================
# GROQ CLIENT
# =========================================================

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# =========================================================
# CHAT HISTORY
# =========================================================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# =========================================================
# CHAT INPUT
# =========================================================

user_question = st.chat_input(
    "Ask Technical Question..."
)

# =========================================================
# AI LOGIC
# =========================================================

if user_question:

    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.markdown(user_question)

    # =====================================================
    # MERGE KNOWLEDGE BASE
    # =====================================================

    combined_data = ""

    for file_name, content in st.session_state.knowledge_base.items():

        combined_data += f"""

FILE: {file_name}

{content}

====================================================
"""

    # =====================================================
    # SYSTEM PROMPT
    # =====================================================

    system_prompt = f"""
You are KAZIM AI PRO.

You are a senior beverage industry maintenance engineer.

Current Line:
{line}

Current Machine:
{machine}

Focus on:
- Root Cause Analysis
- Corrective Actions
- Preventive Actions
- MTTR
- MTBF
- OPL
- KPI Analysis
- Breakdown Analysis
- Technician Analysis
- Fault Code Analysis
- Machine History
- Beverage Industry Troubleshooting

Rules:
- Use uploaded data only.
- Give industrial engineering answers.
- Give practical troubleshooting.
- No generic AI answers.
- Mention important machine tags if found.
- If no data found say:
"No related technical data found."

Uploaded Data:
{combined_data}
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
                max_tokens=2000
            )

            ai_reply = response.choices[0].message.content

        except Exception as e:

            ai_reply = f"Error: {str(e)}"

        st.markdown(ai_reply)

    # =====================================================
    # SAVE RESPONSE
    # =====================================================

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })

# =========================================================
# EXTRA FEATURES
# =========================================================

st.markdown("---")

st.markdown("## AI Features Enabled")

st.markdown("""
✅ TXT Upload  
✅ PDF Upload  
✅ Excel Upload  
✅ CSV Upload  
✅ Delete Uploaded Files  
✅ Machine History Memory  
✅ KPI Dashboard  
✅ Breakdown Analysis  
✅ MTTR / MTBF Analysis  
✅ Fault Code Analysis  
✅ RCA Generation  
✅ OPL Suggestions  
✅ Technician Analysis  
✅ Dark Industrial UI  
✅ Multi File Knowledge Base  
✅ Industrial AI Assistant  
""")
