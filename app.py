import streamlit as st
from groq import Groq

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="KAZIM AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# MODERN CHATGPT STYLE UI
# =========================================================

st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background-color: white;
}

/* HIDE STREAMLIT DEFAULT */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* PAGE WIDTH */
.block-container {
    max-width: 1400px !important;
    padding-top: 1rem !important;
    padding-bottom: 140px !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #FAFAFA;
    border-right: 1px solid #E5E7EB;
}

/* SIDEBAR TITLE */
.sidebar-title {
    font-size: 30px;
    font-weight: 800;
    color: #111827;
}

/* MAIN TITLE */
.kazim-title {
    text-align: center;
    font-size: 72px;
    font-weight: 900;
    margin-top: 10px;
    margin-bottom: 0px;

    background: linear-gradient(
        90deg,
        #111827,
        #2563EB,
        #06B6D4
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* SUBTITLE */
.kazim-sub {
    text-align: center;
    color: #6B7280;
    margin-bottom: 35px;
    font-size: 15px;
}

/* CHAT MESSAGE */
div[data-testid="stChatMessage"] {
    background: white;
    border-radius: 16px;
    padding: 12px;
}

/* BIG CHATGPT INPUT */
div[data-testid="stChatInput"] {

    position: fixed !important;

    bottom: 20px !important;

    left: 50% !important;

    transform: translateX(-50%) !important;

    width: 72vw !important;

    max-width: 1200px !important;

    min-width: 850px !important;

    z-index: 999999 !important;

    background: transparent !important;

    border: none !important;
}

/* WHITE BOX */
div[data-testid="stChatInput"] > div {

    background: white !important;

    border-radius: 34px !important;

    border: 1px solid #D1D5DB !important;

    padding: 14px 22px !important;

    box-shadow:
        0 4px 20px rgba(0,0,0,0.08),
        0 1px 3px rgba(0,0,0,0.05) !important;
}

/* TEXT AREA */
div[data-testid="stChatInput"] textarea {

    background: white !important;

    color: #111827 !important;

    font-size: 18px !important;

    min-height: 40px !important;

    border: none !important;

    box-shadow: none !important;

    padding-top: 8px !important;
}

/* REMOVE BORDER */
div[data-testid="stChatInput"] textarea:focus {

    border: none !important;

    outline: none !important;

    box-shadow: none !important;
}

/* SEND BUTTON */
div[data-testid="stChatInput"] button {

    background: #F9FAFB !important;

    border-radius: 50% !important;

    width: 42px !important;

    height: 42px !important;

    border: 1px solid #E5E7EB !important;
}

/* BUTTONS */
.stButton>button {

    border-radius: 12px !important;
}

/* SELECT BOX */
.stSelectbox div[data-baseweb="select"] {

    border-radius: 12px !important;
}

/* RADIO */
.stRadio {

    background: white;
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

if "show_admin" not in st.session_state:
    st.session_state.show_admin = False

if "selected_line" not in st.session_state:
    st.session_state.selected_line = "Line 18"

if "selected_machine" not in st.session_state:
    st.session_state.selected_machine = "Filler"

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">KAZIM AI</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # =====================================================
    # CLEAR CHAT
    # =====================================================

    if st.button("🗑 Clear Chat History"):

        st.session_state.messages = []

        st.rerun()

    st.markdown("---")

    # =====================================================
    # ADMIN ACCESS
    # =====================================================

    if st.button("🔐 Admin Access"):

        st.session_state.show_admin = True

    if st.session_state.show_admin:

        password = st.text_input(
            "Enter Password",
            type="password"
        )

        if st.button("Login"):

            if password == "Kazim@2026":

                st.session_state.admin_unlocked = True

                st.success("Admin Access Granted")

            else:

                st.error("Wrong Password")

    # =====================================================
    # ADMIN PANEL
    # =====================================================

    if st.session_state.admin_unlocked:

        st.markdown("---")

        st.subheader("Admin Panel")

        # =================================================
        # LINE SELECT
        # =================================================

        st.session_state.selected_line = st.selectbox(
            "Select Line",
            [f"Line {i}" for i in range(1, 21)]
        )

        # =================================================
        # MACHINE SELECT
        # =================================================

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

        # =================================================
        # MEMORY KEY
        # =================================================

        memory_key = (
            st.session_state.selected_line
            + "_"
            + st.session_state.selected_machine
        )

        # =================================================
        # FILE UPLOAD
        # =================================================

        uploaded_file = st.file_uploader(
            "Upload Technical TXT File",
            type=["txt"],
            key=memory_key
        )

        # =================================================
        # ACTION
        # =================================================

        action = st.radio(
            "Select Action",
            [
                "Add Data",
                "Override Data"
            ]
        )

        # =================================================
        # PROCESS BUTTON
        # =================================================

        if uploaded_file is not None:

            if st.button("Process Data"):

                file_text = uploaded_file.read().decode("utf-8")

                # ADD DATA

                if action == "Add Data":

                    old_data = st.session_state.knowledge_base.get(
                        memory_key,
                        ""
                    )

                    st.session_state.knowledge_base[memory_key] = (
                        old_data
                        + "\n\n"
                        + file_text
                    )

                    st.success(
                        f"Data Added To {memory_key}"
                    )

                # OVERRIDE DATA

                elif action == "Override Data":

                    st.session_state.knowledge_base[memory_key] = file_text

                    st.success(
                        f"Data Overridden For {memory_key}"
                    )

        # =================================================
        # DELETE MEMORY
        # =================================================

        st.markdown("---")

        st.subheader("Saved Machine Memory")

        if len(st.session_state.knowledge_base) > 0:

            saved_keys = list(
                st.session_state.knowledge_base.keys()
            )

            delete_key = st.selectbox(
                "Select Memory",
                saved_keys
            )

            if st.button("Delete Selected Memory"):

                del st.session_state.knowledge_base[delete_key]

                st.success(
                    f"{delete_key} Deleted"
                )

                st.rerun()

        else:

            st.info("No Saved Memory")

        # =================================================
        # LOGOUT
        # =================================================

        st.markdown("---")

        if st.button("Logout"):

            st.session_state.admin_unlocked = False

            st.session_state.show_admin = False

            st.success("Logged Out")

            st.rerun()

# =========================================================
# MAIN TITLE
# =========================================================

st.markdown(
    '<div class="kazim-title">KAZIM AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="kazim-sub">Industrial AI Diagnostic Assistant</div>',
    unsafe_allow_html=True
)

# =========================================================
# ACTIVE MEMORY
# =========================================================

active_memory_key = (
    st.session_state.selected_line
    + "_"
    + st.session_state.selected_machine
)

uploaded_data = st.session_state.knowledge_base.get(
    active_memory_key,
    ""
)

# =========================================================
# CHECK API
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
# DISPLAY CHAT
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

You are a senior industrial maintenance engineer.

Current Line:
{st.session_state.selected_line}

Current Machine:
{st.session_state.selected_machine}

Use ONLY uploaded technical memory.

Rules:
- Give industrial engineering answers.
- Mention root cause.
- Mention corrective action.
- Mention preventive action.
- Mention troubleshooting.
- Mention PLC logic if available.
- Mention sensor/interlock logic if available.
- Be practical and technical.
- No generic AI answers.
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

            ai_reply = (
                response
                .choices[0]
                .message
                .content
            )

        except Exception as e:

            ai_reply = f"Error: {str(e)}"

        st.markdown(ai_reply)

    # =====================================================
    # SAVE CHAT
    # =====================================================

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })
