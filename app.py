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
# MOBILE + DESKTOP UI
# =========================================================

st.markdown("""
<style>

/* =========================================================
MAIN APP
========================================================= */

.stApp{
    background-color:#F5F7FA;
}

/* Hide Streamlit */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* =========================================================
MAIN CONTAINER
========================================================= */

.block-container{
    padding-top:1rem !important;
    padding-bottom:140px !important;
    max-width:1400px !important;
}

/* =========================================================
SIDEBAR
========================================================= */

section[data-testid="stSidebar"]{
    background:#FFFFFF;
    border-right:1px solid #E5E7EB;
}

/* =========================================================
TITLE
========================================================= */

.kazim-title{
    text-align:center;
    font-size:72px;
    font-weight:900;
    line-height:1;
    margin-top:10px;

    background: linear-gradient(
        90deg,
        #1D4ED8,
        #2563EB,
        #38BDF8
    );

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.kazim-sub{
    text-align:center;
    color:#6B7280;
    font-size:16px;
    margin-bottom:30px;
}

/* =========================================================
CHAT MESSAGE
========================================================= */

div[data-testid="stChatMessage"]{
    background:white !important;
    border-radius:18px !important;
    padding:14px !important;
    margin-bottom:12px !important;
    box-shadow:0 1px 4px rgba(0,0,0,0.04);
}

/* TEXT FIX */
div[data-testid="stMarkdownContainer"] p{
    color:#111827 !important;
    opacity:1 !important;
    font-size:16px !important;
}

/* =========================================================
CHAT INPUT DESKTOP
========================================================= */

div[data-testid="stChatInput"]{
    position:fixed !important;
    bottom:20px !important;
    left:50% !important;
    transform:translateX(-50%) !important;

    width:72vw !important;
    max-width:1200px !important;
    min-width:850px !important;

    z-index:999999 !important;
    background:transparent !important;
}

/* INPUT BOX */

div[data-testid="stChatInput"] > div{
    background:white !important;

    border-radius:36px !important;

    border:1px solid #D1D5DB !important;

    padding:12px 20px !important;

    box-shadow:
        0 10px 30px rgba(0,0,0,0.08),
        0 2px 8px rgba(0,0,0,0.04) !important;
}

/* TEXT AREA */

div[data-testid="stChatInput"] textarea{
    background:white !important;
    color:#111827 !important;
    font-size:18px !important;
    border:none !important;
    box-shadow:none !important;
    min-height:40px !important;
}

/* REMOVE FOCUS */

div[data-testid="stChatInput"] textarea:focus{
    border:none !important;
    outline:none !important;
    box-shadow:none !important;
}

/* BUTTON */

div[data-testid="stChatInput"] button{
    background:#F3F4F6 !important;
    border-radius:50% !important;
    border:1px solid #E5E7EB !important;
    width:42px !important;
    height:42px !important;
}

/* =========================================================
BUTTONS
========================================================= */

.stButton>button{
    border-radius:12px !important;
}

/* =========================================================
MOBILE FIX
========================================================= */

@media (max-width: 768px){

    .kazim-title{
        font-size:52px !important;
    }

    .kazim-sub{
        font-size:14px !important;
    }

    .block-container{
        padding-left:12px !important;
        padding-right:12px !important;
        padding-bottom:170px !important;
    }

    /* MOBILE CHAT BOX */

    div[data-testid="stChatInput"]{

        left:0px !important;
        right:0px !important;
        bottom:12px !important;

        transform:none !important;

        width:100% !important;
        min-width:100% !important;
        max-width:100% !important;

        padding-left:10px !important;
        padding-right:10px !important;
    }

    div[data-testid="stChatInput"] > div{

        border-radius:30px !important;
        padding:10px 16px !important;
    }

    div[data-testid="stChatInput"] textarea{

        font-size:16px !important;
        min-height:38px !important;

        color:#111827 !important;
        opacity:1 !important;
    }

    /* FIX BLUR TEXT */

    textarea,
    input{
        color:#111827 !important;
        opacity:1 !important;
        -webkit-text-fill-color:#111827 !important;
    }

    /* SIDEBAR MOBILE */

    section[data-testid="stSidebar"]{
        width:85% !important;
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

    if st.button("🗑 Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    # ADMIN ACCESS

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

        # LINE

        st.session_state.selected_line = st.selectbox(
            "Select Line",
            [f"Line {i}" for i in range(1, 21)]
        )

        # MACHINE

        machine_options = [
            "M1","M2","M3","M4","M5",
            "M6","M7","M8","M9","M10",
            "M11","M12","M13","M14","M15",
            "M16","M17","M18",
            "Filler",
            "Packer",
            "Palletizer",
            "Conveyor",
            "Lanfranchi",
            "Stretch Machine",
            "Stacker",
            "Upstream",
            "Downstream"
        ]

        st.session_state.selected_machine = st.selectbox(
            "Select Machine",
            machine_options
        )

        # MEMORY KEY

        memory_key = (
            st.session_state.selected_line
            + "_"
            + st.session_state.selected_machine
        )

        # SHOW ACTIVE MEMORY

        if memory_key in st.session_state.knowledge_base:

            st.success(f"Memory Loaded: {memory_key}")

        # FILE

        uploaded_file = st.file_uploader(
            "Upload Technical TXT File",
            type=["txt"],
            key=f"uploader_{memory_key}"
        )

        # ACTION

        action = st.radio(
            "Select Action",
            ["Add Data", "Override Data"]
        )

        # PROCESS DATA

        if uploaded_file is not None:

            if st.button("Process Data"):

                file_text = uploaded_file.read().decode("utf-8")

                # ADD DATA

                if action == "Add Data":

                    existing_data = st.session_state.knowledge_base.get(
                        memory_key,
                        ""
                    )

                    combined_data = (
                        existing_data
                        + "\n\n"
                        + file_text
                    )

                    st.session_state.knowledge_base[memory_key] = combined_data

                    st.success(f"Data Added To {memory_key}")

                # OVERRIDE

                elif action == "Override Data":

                    st.session_state.knowledge_base[memory_key] = file_text

                    st.success(f"Data Overridden For {memory_key}")

        # =================================================
        # SAVED MEMORY
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

                st.success(f"{delete_key} Deleted")

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
# ALL MACHINE MEMORIES
# =========================================================

all_machine_memory = ""

for key, value in st.session_state.knowledge_base.items():

    all_machine_memory += f"""

==========================
MACHINE MEMORY: {key}
==========================

{value}

"""

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
# DISPLAY CHAT
# =========================================================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# =========================================================
# CHAT INPUT
# =========================================================

prompt = st.chat_input(
    "Ask fault code, PLC issue, alarm, breakdown or technical query..."
)

# =========================================================
# AI PROCESS
# =========================================================

if prompt:

    # SAVE USER MESSAGE

    st.session_state.messages.append({
        "role":"user",
        "content":prompt
    })

    with st.chat_message("user"):

        st.markdown(prompt)

    # SYSTEM PROMPT

    system_prompt = f"""
You are KAZIM AI.

You are a senior industrial maintenance engineer.

IMPORTANT RULES:

1. Use ONLY uploaded machine memory.
2. NEVER create fake information.
3. NEVER guess machine specifications.
4. If data not found say:
"No related technical data found."
5. Always search ALL uploaded machine memories.
6. Mention exact machine name from memory.
7. Do NOT mix M3 and M18 data.
8. If user asks comparison:
   Compare ONLY using uploaded memory.
9. Give practical engineering answers only.

ALL MACHINE MEMORIES:

{all_machine_memory}
"""

    # AI RESPONSE

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
                temperature=0.1,
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

    # SAVE RESPONSE

    st.session_state.messages.append({
        "role":"assistant",
        "content":ai_reply
    })
