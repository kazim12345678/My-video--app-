import streamlit as st
from groq import Groq

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="KAZIM AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CHATGPT STYLE WHITE UI
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: white;
}

header {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.block-container {
    padding-top: 2rem;
    max-width: 900px;
}

h1, h2, h3 {
    color: black;
}

section[data-testid="stSidebar"] {
    background-color: #F7F7F8;
    border-right: 1px solid #E5E5E5;
}

.stChatMessage {
    background-color: white;
    border-radius: 10px;
    padding: 10px;
}

.stTextInput input {
    border-radius: 10px;
}

textarea {
    border-radius: 12px !important;
}

div[data-testid="stChatInput"] {
    background-color: white;
}

div[data-testid="stChatInput"] textarea {
    background-color: white !important;
    color: black !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 14px !important;
}

.stButton>button {
    border-radius: 10px;
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

if "selected_line" not in st.session_state:
    st.session_state.selected_line = "Line 1"

if "selected_machine" not in st.session_state:
    st.session_state.selected_machine = "Filler"

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("KAZIM AI")

    st.markdown("---")

    # CLEAR CHAT

    if st.button("🗑 Delete Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    # ADMIN ACCESS

    admin_toggle = st.button("🔐 Admin Access")

    if admin_toggle:
        st.session_state.show_admin = True

    if "show_admin" not in st.session_state:
        st.session_state.show_admin = False

    if st.session_state.show_admin:

        password = st.text_input(
            "Enter Password",
            type="password"
        )

        if st.button("Login"):

            if password == "Kazim@2026":

                st.session_state.admin_unlocked = True

                st.success("Admin Mode Enabled")

            else:
                st.error("Wrong Password")

    # =====================================================
    # ADMIN PANEL
    # =====================================================

    if st.session_state.admin_unlocked:

        st.markdown("---")

        st.subheader("Admin Panel")

        # LINE

        st.session_state.selected_line = st.selectbox(
            "Select Line",
            [f"Line {i}" for i in range(1, 21)]
        )

        # MACHINE

        machine_options = [
            "Upstream",
            "Downstream",
            "Filler",
            "Lanfranchi",
            "Crates Conveyor",
            "Packer",
            "Stacker",
            "Palletizer",
            "Stretch Machine",
            "Conveyor"
        ]

        st.session_state.selected_machine = st.selectbox(
            "Select Machine",
            machine_options
        )

        # FILE UPLOAD

        uploaded_file = st.file_uploader(
            "Upload Technical Data",
            type=["txt"]
        )

        if uploaded_file is not None:

            file_text = uploaded_file.read().decode("utf-8")

            action = st.radio(
                "Select Action",
                ["Add Data", "Override Data"]
            )

            memory_key = f"""
{st.session_state.selected_line}
_{st.session_state.selected_machine}
"""

            if st.button("Process Data"):

                # ADD DATA

                if action == "Add Data":

                    existing_data = st.session_state.knowledge_base.get(
                        memory_key,
                        ""
                    )

                    st.session_state.knowledge_base[memory_key] = (
                        existing_data + "\n\n" + file_text
                    )

                    st.success("Data Added Successfully")

                # OVERRIDE DATA

                elif action == "Override Data":

                    st.session_state.knowledge_base[memory_key] = file_text

                    st.success("Data Overridden Successfully")

        # =================================================
        # DELETE MEMORY
        # =================================================

        st.markdown("---")

        if len(st.session_state.knowledge_base) > 0:

            delete_key = st.selectbox(
                "Delete Saved Data",
                list(st.session_state.knowledge_base.keys())
            )

            if st.button("Delete Selected Data"):

                del st.session_state.knowledge_base[delete_key]

                st.success("Data Deleted")

                st.rerun()

        # =================================================
        # LOGOUT
        # =================================================

        st.markdown("---")

        if st.button("Logout"):

            st.session_state.admin_unlocked = False

            st.success("Logged Out")

            st.rerun()

# =========================================================
# MAIN SCREEN
# =========================================================

st.title("KAZIM AI")

st.caption("Industrial AI Diagnostic Assistant")

# =========================================================
# CURRENT ACTIVE MEMORY
# =========================================================

active_memory_key = f"""
{st.session_state.selected_line}
_{st.session_state.selected_machine}
"""

uploaded_data = st.session_state.knowledge_base.get(
    active_memory_key,
    ""
)

# =========================================================
# API CHECK
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

prompt = st.chat_input(
    "Ask fault code, alarm, PLC issue, breakdown or query..."
)

# =========================================================
# AI PROCESS
# =========================================================

if prompt:

    # USER MESSAGE

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):

        st.markdown(prompt)

    # =====================================================
    # SYSTEM PROMPT
    # =====================================================

    system_prompt = f"""
You are KAZIM AI.

You are an industrial maintenance engineer.

Current Line:
{st.session_state.selected_line}

Current Machine:
{st.session_state.selected_machine}

Use uploaded technical memory only.

Rules:
- Answer like professional engineer.
- Give root cause.
- Give corrective action.
- Give preventive action.
- Mention fault finding steps.
- Mention electrical and automation logic.
- Keep answers practical.
- If no data found say:
"No related technical data found."

Technical Memory:
{uploaded_data}
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
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1200
            )

            ai_reply = response.choices[0].message.content

        except Exception as e:

            ai_reply = f"Error: {str(e)}"

        st.markdown(ai_reply)

    # SAVE RESPONSE

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })
