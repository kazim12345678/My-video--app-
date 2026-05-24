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
# SESSION STATE
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
# CSS
# =========================================================

st.markdown("""
<style>

/* HIDE STREAMLIT */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* APP */
.stApp{
    background:#F3F4F6;
}

/* PAGE */
.block-container{
    max-width:1400px;
    padding-top:1rem;
    padding-bottom:140px;
}

/* TITLE */
.kazim-title{
    text-align:center;
    font-size:72px;
    font-weight:900;

    background: linear-gradient(
        90deg,
        #1D4ED8,
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
    font-size:18px;
    margin-bottom:35px;
}

/* CHAT */
div[data-testid="stChatMessage"]{
    background:white;
    border-radius:18px;
    padding:14px;
    margin-bottom:14px;
}

/* TEXT */
div[data-testid="stMarkdownContainer"] *{
    color:#111827 !important;
    opacity:1 !important;
}

/* CHAT INPUT */
div[data-testid="stChatInput"]{
    position:fixed !important;

    bottom:18px !important;

    left:50% !important;

    transform:translateX(-50%) !important;

    width:72vw !important;

    max-width:1100px !important;

    z-index:999999 !important;
}

/* INPUT BOX */
div[data-testid="stChatInput"] > div{

    background:white !important;

    border-radius:40px !important;

    border:1px solid #D1D5DB !important;

    padding:12px 18px !important;

    box-shadow:
    0 10px 30px rgba(0,0,0,0.08),
    0 2px 8px rgba(0,0,0,0.05) !important;
}

/* TEXTAREA */
div[data-testid="stChatInput"] textarea{

    background:white !important;

    color:#111827 !important;

    font-size:18px !important;

    border:none !important;

    box-shadow:none !important;

    opacity:1 !important;
}

/* PLACEHOLDER */
textarea::placeholder{
    color:#6B7280 !important;
    opacity:1 !important;
}

/* BUTTON */
div[data-testid="stChatInput"] button{
    border-radius:50% !important;
    width:42px !important;
    height:42px !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"]{
    background:white;
    border-right:1px solid #E5E7EB;
}

/* MOBILE */
@media (max-width:768px){

    .kazim-title{
        font-size:50px !important;
    }

    .kazim-sub{
        font-size:15px !important;
    }

    div[data-testid="stChatInput"]{

        width:95vw !important;

        bottom:10px !important;
    }

    div[data-testid="stChatInput"] > div{

        border-radius:28px !important;
    }

    div[data-testid="stChatInput"] textarea{

        font-size:16px !important;
    }

    .block-container{

        padding-bottom:160px !important;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## ⚙️ KAZIM AI")

    st.markdown("---")

    # =====================================================
    # ADMIN ACCESS
    # =====================================================

    if not st.session_state.admin_unlocked:

        st.subheader("Admin Access")

        password = st.text_input(
            "Enter Password",
            type="password"
        )

        if st.button("Login"):

            if password == "Kazim@2026":

                st.session_state.admin_unlocked = True

                st.success("Admin Access Granted")

                st.rerun()

            else:

                st.error("Wrong Password")

    # =====================================================
    # ADMIN PANEL
    # =====================================================

    if st.session_state.admin_unlocked:

        st.success("✅ Admin Mode Active")

        st.markdown("---")

        # LINE

        st.session_state.selected_line = st.selectbox(
            "Select Line",
            [f"Line {i}" for i in range(1,21)]
        )

        # MACHINE

        machine_options = [
            "M1",
            "M2",
            "M3",
            "M18",
            "Filler",
            "Packer",
            "Conveyor",
            "Palletizer",
            "Lanfranchi",
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

        st.info(f"Current Memory: {memory_key}")

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
        # PROCESS DATA
        # =================================================

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

                elif action == "Override Data":

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

        # =================================================
        # LOGOUT
        # =================================================

        st.markdown("---")

        if st.button("Logout"):

            st.session_state.admin_unlocked = False

            st.rerun()

# =========================================================
# TITLE
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
# MEMORY COMBINE
# =========================================================

all_memory = ""

for key, value in st.session_state.knowledge_base.items():

    all_memory += f"""

=========================
MEMORY NAME: {key}
=========================

{value}

"""

# =========================================================
# GROQ API
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
    "Ask fault code, PLC issue, alarm, breakdown or technical query..."
)

# =========================================================
# AI PROCESS
# =========================================================

if prompt:

    st.session_state.messages.append({
        "role":"user",
        "content":prompt
    })

    with st.chat_message("user"):

        st.markdown(prompt)

    # =====================================================
    # SYSTEM PROMPT
    # =====================================================

    system_prompt = f"""
You are KAZIM AI.

You are industrial maintenance AI.

IMPORTANT RULES:

1. Use ONLY uploaded memories.
2. NEVER generate fake machine details.
3. NEVER assume PLC types or specifications.
4. If information missing say:
"No related technical data found."
5. Mention exact memory source if possible.

Available Machine Memories:

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
                temperature=0.2,
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

    st.session_state.messages.append({
        "role":"assistant",
        "content":ai_reply
    })
