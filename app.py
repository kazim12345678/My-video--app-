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
# MODERN UI
# =========================================================

st.markdown("""
<style>

/* MAIN */
.stApp{
    background-color:#FFFFFF;
}

/* HIDE */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* PAGE */
.block-container{
    max-width:1400px;
    padding-top:1rem;
    padding-bottom:140px;
}

/* SIDEBAR */
section[data-testid="stSidebar"]{
    background:#FAFAFA;
    border-right:1px solid #E5E7EB;
}

/* TITLE */
.kazim-title{
    text-align:center;
    font-size:72px;
    font-weight:900;
    margin-top:10px;
    margin-bottom:0px;

    background:linear-gradient(
        90deg,
        #111827,
        #2563EB,
        #06B6D4
    );

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

/* SUBTITLE */
.kazim-sub{
    text-align:center;
    color:#6B7280;
    margin-bottom:30px;
    font-size:15px;
}

/* CHAT */
div[data-testid="stChatMessage"]{
    background:white;
    border-radius:18px;
    padding:12px;
}

/* BIG INPUT */
div[data-testid="stChatInput"]{
    position:fixed !important;
    bottom:18px !important;
    left:50% !important;
    transform:translateX(-50%) !important;
    width:78vw !important;
    max-width:1200px !important;
    z-index:999999 !important;
}

/* INPUT BOX */
div[data-testid="stChatInput"] > div{
    background:white !important;
    border-radius:40px !important;
    border:1px solid #D1D5DB !important;
    padding:14px 22px !important;

    box-shadow:
    0 4px 25px rgba(0,0,0,0.08),
    0 1px 3px rgba(0,0,0,0.05) !important;
}

/* TEXTAREA */
div[data-testid="stChatInput"] textarea{
    font-size:18px !important;
    color:#111827 !important;
    background:white !important;
}

/* MOBILE */
@media (max-width:768px){

    .kazim-title{
        font-size:52px !important;
    }

    div[data-testid="stChatInput"]{
        width:95vw !important;
        bottom:10px !important;
    }

    div[data-testid="stChatInput"] textarea{
        font-size:16px !important;
    }

    .block-container{
        padding-left:10px !important;
        padding-right:10px !important;
    }
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

    st.markdown("## KAZIM AI")

    st.markdown("---")

    # CLEAR CHAT

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

    st.markdown("---")

    # ADMIN ACCESS

    if st.button("🔐 Admin Access"):

        st.session_state.show_admin = True

    if st.session_state.show_admin:

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            if password == "Kazim@2026":

                st.session_state.admin_unlocked = True

                st.success("Access Granted")

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

        machines = [
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
            machines
        )

        # MEMORY KEY

        memory_key = (
            st.session_state.selected_line
            + "_"
            + st.session_state.selected_machine
        )

        # SHOW MEMORY STATUS

        if memory_key in st.session_state.knowledge_base:

            st.success(f"Memory Loaded: {memory_key}")

        else:

            st.warning(f"No Memory For: {memory_key}")

        # FILE UPLOAD

        uploaded_file = st.file_uploader(
            "Upload Technical TXT File",
            type=["txt"],
            key=memory_key
        )

        # ACTION

        action = st.radio(
            "Select Action",
            [
                "Add Data",
                "Override Data"
            ]
        )

        # PROCESS

        if uploaded_file is not None:

            if st.button("Process Data"):

                file_text = uploaded_file.read().decode("utf-8")

                # ADD

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

                # OVERRIDE

                if action == "Override Data":

                    st.session_state.knowledge_base[memory_key] = file_text

                    st.success(
                        f"Data Overridden For {memory_key}"
                    )

        # =================================================
        # SAVED MEMORIES
        # =================================================

        st.markdown("---")

        st.subheader("Saved Machine Memory")

        if len(st.session_state.knowledge_base) > 0:

            saved_keys = list(
                st.session_state.knowledge_base.keys()
            )

            delete_key = st.selectbox(
                "Select Memory To Delete",
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

        # LOGOUT

        st.markdown("---")

        if st.button("Logout"):

            st.session_state.admin_unlocked = False

            st.session_state.show_admin = False

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
# API
# =========================================================

if "GROQ_API_KEY" not in st.secrets:

    st.error("Groq API Key Missing")

    st.stop()

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
# AI
# =========================================================

if prompt:

    st.session_state.messages.append({
        "role":"user",
        "content":prompt
    })

    with st.chat_message("user"):

        st.markdown(prompt)

    # =====================================================
    # ALL MEMORY DATA
    # =====================================================

    all_memory = ""

    for key, value in st.session_state.knowledge_base.items():

        all_memory += f"""

Machine Memory:
{key}

Technical Data:
{value}

====================================================

"""

    # =====================================================
    # SYSTEM PROMPT
    # =====================================================

    system_prompt = f"""
You are KAZIM AI.

You are a senior industrial maintenance engineer.

You have multiple machine memories.

Use ALL uploaded machine memories.

If user asks about:
- M3
- M18
- Line 3
- Line 18
- Any uploaded machine

Search all uploaded memories.

Rules:
- Give technical industrial answers
- Mention root cause
- Mention corrective action
- Mention preventive action
- Mention troubleshooting
- Mention PLC logic if available
- No generic answers

If no data found say:
"No related technical data found"

All Machine Memories:

{all_memory}
"""

    # =====================================================
    # RESPONSE
    # =====================================================

    with st.chat_message("assistant"):

        try:

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role":"system",
                        "content":system_prompt
                    },
                    {
                        "role":"user",
                        "content":prompt
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

    # SAVE CHAT

    st.session_state.messages.append({
        "role":"assistant",
        "content":ai_reply
    })
