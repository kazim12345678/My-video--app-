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
# MOBILE + DESKTOP CSS
# =========================================================

st.markdown("""
<style>

/* MAIN */
.stApp {
    background-color: #F3F4F6;
}

/* HIDE STREAMLIT */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* PAGE */
.block-container {
    padding-top: 1rem;
    padding-bottom: 140px;
    max-width: 1500px;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #E5E7EB;
}

/* SIDEBAR SHOW ALWAYS */
section[data-testid="stSidebar"] {
    min-width: 320px !important;
}

/* TITLE */
.kazim-title {
    text-align: center;
    font-size: 72px;
    font-weight: 900;
    margin-top: 10px;

    background: linear-gradient(
        90deg,
        #1D4ED8,
        #2563EB,
        #0EA5E9
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* SUBTITLE */
.kazim-sub {
    text-align: center;
    color: #6B7280;
    font-size: 18px;
    margin-bottom: 30px;
}

/* CHAT MESSAGE */
div[data-testid="stChatMessage"] {
    background: white !important;
    border-radius: 18px !important;
    padding: 14px !important;
    margin-bottom: 14px !important;
    color: black !important;
}

/* CHAT TEXT FIX */
div[data-testid="stChatMessage"] p {
    color: black !important;
    opacity: 1 !important;
}

/* INPUT BOX */
div[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 20px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 72vw !important;
    max-width: 1100px !important;
    z-index: 999999 !important;
}

/* INPUT INNER */
div[data-testid="stChatInput"] > div {
    background: white !important;
    border-radius: 35px !important;
    border: 1px solid #D1D5DB !important;
    padding: 12px 22px !important;

    box-shadow:
        0 4px 20px rgba(0,0,0,0.08) !important;
}

/* TEXTAREA */
div[data-testid="stChatInput"] textarea {
    background: white !important;
    color: black !important;
    font-size: 18px !important;
    opacity: 1 !important;
}

/* PLACEHOLDER */
textarea::placeholder {
    color: #6B7280 !important;
    opacity: 1 !important;
}

/* SEND BUTTON */
div[data-testid="stChatInput"] button {
    border-radius: 50% !important;
    height: 45px !important;
    width: 45px !important;
}

/* BUTTON */
.stButton>button {
    border-radius: 12px !important;
}

/* MOBILE FIX */
@media (max-width: 768px) {

    .kazim-title {
        font-size: 52px !important;
    }

    .kazim-sub {
        font-size: 15px !important;
    }

    div[data-testid="stChatInput"] {

        width: 95vw !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        bottom: 12px !important;
    }

    div[data-testid="stChatInput"] > div {

        border-radius: 30px !important;
        padding: 10px 16px !important;
    }

    div[data-testid="stChatInput"] textarea {

        font-size: 16px !important;
    }

    .block-container {

        padding-bottom: 160px !important;
    }

    section[data-testid="stSidebar"] {

        min-width: 270px !important;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = {}

if "admin_unlocked" not in st.session_state:
    st.session_state.admin_unlocked = False

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("KAZIM AI")

    st.markdown("---")

    # =====================================================
    # ADMIN ACCESS
    # =====================================================

    st.subheader("🔐 Admin Access")

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

        st.subheader("Machine Memory")

        line = st.selectbox(
            "Select Line",
            [f"Line {i}" for i in range(1, 21)]
        )

        machine = st.selectbox(
            "Select Machine",
            [
                "M1","M2","M3","M4","M5","M6",
                "M7","M8","M9","M10","M11","M12",
                "M13","M14","M15","M16","M17","M18",
                "Filler",
                "Packer",
                "Palletizer",
                "Conveyor",
                "Lanfranchi",
                "Stacker",
                "Stretch Machine"
            ]
        )

        memory_key = f"{line}_{machine}"

        st.info(f"Memory Loaded: {memory_key}")

        uploaded_file = st.file_uploader(
            "Upload Technical TXT File",
            type=["txt"],
            key=memory_key
        )

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

                file_text = uploaded_file.read().decode(
                    "utf-8",
                    errors="ignore"
                )

                # ADD
                if action == "Add Data":

                    existing_data = st.session_state.knowledge_base.get(
                        memory_key,
                        ""
                    )

                    st.session_state.knowledge_base[memory_key] = (
                        existing_data
                        + "\n\n"
                        + file_text
                    )

                    st.success(
                        f"Data Added To {memory_key}"
                    )

                # OVERRIDE
                else:

                    st.session_state.knowledge_base[memory_key] = file_text

                    st.success(
                        f"Data Overridden For {memory_key}"
                    )

        # =================================================
        # DELETE MEMORY
        # =================================================

        st.markdown("---")

        st.subheader("Delete Memory")

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

        # =================================================
        # LOGOUT
        # =================================================

        st.markdown("---")

        if st.button("Logout"):

            st.session_state.admin_unlocked = False

            st.success("Logged Out")

            st.rerun()

    st.markdown("---")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

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
# API CHECK
# =========================================================

if "GROQ_API_KEY" not in st.secrets:

    st.error("Missing GROQ API KEY")
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
# AI RESPONSE
# =========================================================

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):

        st.markdown(prompt)

    # =====================================================
    # ALL MEMORY
    # =====================================================

    combined_memory = ""

    for key, value in st.session_state.knowledge_base.items():

        combined_memory += f"""

========================
MACHINE MEMORY: {key}
========================

{value}

"""

    # =====================================================
    # SYSTEM PROMPT
    # =====================================================

    system_prompt = f"""
You are KAZIM AI.

You are an industrial maintenance AI assistant.

IMPORTANT RULES:

1. Use ONLY uploaded technical memory.
2. NEVER create fake machine information.
3. NEVER guess.
4. If data not available say:
"No related technical data found."
5. Search ALL uploaded machine memories.
6. Clearly mention which machine memory was used.
7. Do not invent PLC brands or machine specifications.

Technical Memory:
{combined_memory}
"""

    # =====================================================
    # GENERATE RESPONSE
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
        "role": "assistant",
        "content": ai_reply
    })
