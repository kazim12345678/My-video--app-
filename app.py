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
# MOBILE + DESKTOP FIXED UI
# =========================================================

st.markdown("""
<style>

/* =====================================================
MAIN
===================================================== */

html, body, [class*="css"]  {
    font-family: sans-serif;
}

.stApp{
    background: #F8FAFC;
}

/* HIDE STREAMLIT */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* =====================================================
CONTAINER
===================================================== */

.block-container{
    padding-top: 1rem;
    padding-bottom: 140px;
    max-width: 1500px;
}

/* =====================================================
SIDEBAR
===================================================== */

section[data-testid="stSidebar"]{
    background: #FFFFFF;
    border-right: 1px solid #E5E7EB;
}

/* =====================================================
TITLE
===================================================== */

.kazim-title{
    text-align:center;
    font-size:72px;
    font-weight:900;
    margin-top:20px;

    background: linear-gradient(
        90deg,
        #1D4ED8,
        #2563EB,
        #0EA5E9
    );

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.kazim-sub{
    text-align:center;
    color:#6B7280;
    margin-bottom:40px;
    font-size:18px;
}

/* =====================================================
CHAT MESSAGE
===================================================== */

div[data-testid="stChatMessage"]{
    background:white;
    border-radius:18px;
    padding:14px;
    margin-bottom:10px;
    border:1px solid #F1F5F9;
}

/* =====================================================
DESKTOP CHAT INPUT
===================================================== */

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
    background:#FFFFFF !important;

    border-radius:40px !important;

    border:1px solid #D1D5DB !important;

    padding:14px 24px !important;

    box-shadow:
        0 10px 25px rgba(0,0,0,0.06),
        0 2px 6px rgba(0,0,0,0.04) !important;
}

/* TEXT AREA */
div[data-testid="stChatInput"] textarea{
    background:#FFFFFF !important;
    color:#111827 !important;
    font-size:20px !important;
    min-height:42px !important;
    border:none !important;
    box-shadow:none !important;
}

/* REMOVE BLUR / FOCUS */
div[data-testid="stChatInput"] textarea:focus{
    outline:none !important;
    border:none !important;
    box-shadow:none !important;
}

/* SEND BUTTON */
div[data-testid="stChatInput"] button{
    border-radius:50% !important;
    height:48px !important;
    width:48px !important;
    background:#F3F4F6 !important;
    border:1px solid #E5E7EB !important;
}

/* =====================================================
BUTTONS
===================================================== */

.stButton>button{
    border-radius:12px !important;
}

/* =====================================================
MOBILE FIX
===================================================== */

@media (max-width: 768px){

    /* TITLE */
    .kazim-title{
        font-size:52px !important;
        margin-top:10px !important;
    }

    .kazim-sub{
        font-size:16px !important;
    }

    /* PAGE */
    .block-container{
        padding-left:10px !important;
        padding-right:10px !important;
        padding-bottom:160px !important;
    }

    /* MOBILE INPUT */
    div[data-testid="stChatInput"]{

        position:fixed !important;

        left:50% !important;

        transform:translateX(-50%) !important;

        bottom:70px !important;

        width:92vw !important;

        min-width:unset !important;

        max-width:unset !important;

        z-index:999999 !important;
    }

    /* INPUT BOX */
    div[data-testid="stChatInput"] > div{

        background:#FFFFFF !important;

        border-radius:34px !important;

        padding:16px 20px !important;

        border:1px solid #D1D5DB !important;

        box-shadow:
            0 8px 24px rgba(0,0,0,0.08) !important;
    }

    /* TEXT */
    div[data-testid="stChatInput"] textarea{

        font-size:18px !important;

        background:#FFFFFF !important;

        color:#111827 !important;
    }

    /* REMOVE BLUR TEXT ISSUE */
    div[data-testid="stChatInput"] textarea::placeholder{
        color:#9CA3AF !important;
        opacity:1 !important;
    }

    /* FIX STREAMLIT FLOATING ICON OVERLAP */
    button[kind="secondary"]{
        bottom:120px !important;
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

            st.warning("No Memory Loaded")

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

        # PROCESS DATA

        if uploaded_file is not None:

            if st.button("Process Data"):

                file_text = uploaded_file.read().decode(
                    "utf-8",
                    errors="ignore"
                )

                # ADD DATA

                if action == "Add Data":

                    if memory_key not in st.session_state.knowledge_base:

                        st.session_state.knowledge_base[memory_key] = ""

                    st.session_state.knowledge_base[memory_key] += (
                        "\n\n"
                        + file_text
                    )

                    st.success(
                        f"Data Added To {memory_key}"
                    )

                # OVERRIDE

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

            delete_key = st.selectbox(
                "Select Memory To Delete",
                list(st.session_state.knowledge_base.keys())
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
# LOAD ALL MEMORY
# =========================================================

all_memory = ""

for key, value in st.session_state.knowledge_base.items():

    all_memory += f"""

========================
MEMORY SOURCE: {key}
========================

{value}

"""

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
    "Ask fault code, alarm, PLC issue, breakdown or technical query..."
)

# =========================================================
# AI RESPONSE
# =========================================================

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):

        st.markdown(prompt)

    # SYSTEM PROMPT

    system_prompt = f"""
You are KAZIM AI.

You are an industrial maintenance engineer.

IMPORTANT RULES:

1. Use ONLY uploaded memory data.

2. NEVER create fake machine information.

3. NEVER guess machine specifications.

4. If information not found in memory say:
"No related technical data found."

5. If user asks difference between machines:
Compare ONLY uploaded memory.

6. Mention memory source names if possible.

7. Give industrial engineering answers only.

UPLOADED MACHINE MEMORIES:

{all_memory}
"""

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
                temperature=0.1,
                max_tokens=1200
            )

            ai_reply = response.choices[0].message.content

        except Exception as e:

            ai_reply = f"Error: {str(e)}"

        st.markdown(ai_reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })
