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
# CSS
# =========================================================

st.markdown("""
<style>

/* MAIN */
.stApp{
    background:#F3F4F6;
}

/* HIDE STREAMLIT */
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

/* PAGE */
.block-container{
    padding-top:1rem;
    padding-bottom:120px;
    max-width:1400px;
}

/* TITLE */
.kazim-title{
    text-align:center;
    font-size:72px;
    font-weight:900;
    margin-top:20px;
    margin-bottom:0px;
    background: linear-gradient(90deg,#1D4ED8,#3B82F6);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.kazim-sub{
    text-align:center;
    color:#6B7280;
    font-size:18px;
    margin-bottom:40px;
}

/* CHAT */
div[data-testid="stChatMessage"]{
    background:white;
    border-radius:18px;
    padding:14px;
    margin-bottom:10px;
    color:#111827 !important;
}

/* FORCE TEXT VISIBLE */
div[data-testid="stChatMessage"] *{
    color:#111827 !important;
    opacity:1 !important;
}

/* CHAT INPUT */
div[data-testid="stChatInput"]{
    position:fixed !important;
    bottom:18px !important;
    left:50% !important;
    transform:translateX(-50%) !important;
    width:70vw !important;
    max-width:1100px !important;
    z-index:999999 !important;
}

/* INPUT BOX */
div[data-testid="stChatInput"] > div{
    background:white !important;
    border-radius:35px !important;
    border:1px solid #D1D5DB !important;
    padding:12px 18px !important;
    box-shadow:0 4px 18px rgba(0,0,0,0.08);
}

/* INPUT TEXT */
div[data-testid="stChatInput"] textarea{
    color:#111827 !important;
    background:white !important;
    opacity:1 !important;
    font-size:18px !important;
}

/* MOBILE */
@media (max-width: 768px){

    .kazim-title{
        font-size:48px !important;
    }

    .kazim-sub{
        font-size:16px !important;
    }

    div[data-testid="stChatInput"]{
        width:95vw !important;
        bottom:10px !important;
    }

    div[data-testid="stChatInput"] textarea{
        font-size:16px !important;
    }

}

/* ADMIN BOX */
.admin-box{
    background:white;
    padding:20px;
    border-radius:18px;
    border:1px solid #E5E7EB;
    margin-bottom:20px;
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

if "admin_open" not in st.session_state:
    st.session_state.admin_open = False

if "admin_ok" not in st.session_state:
    st.session_state.admin_ok = False

# =========================================================
# TOP ADMIN BUTTON
# =========================================================

top1, top2, top3 = st.columns([1,2,1])

with top1:

    if st.button("⚙ Admin Access"):

        st.session_state.admin_open = not st.session_state.admin_open

# =========================================================
# ADMIN PANEL
# =========================================================

if st.session_state.admin_open:

    st.markdown('<div class="admin-box">', unsafe_allow_html=True)

    password = st.text_input(
        "Enter Password",
        type="password"
    )

    if st.button("Login"):

        if password == "Kazim@2026":

            st.session_state.admin_ok = True
            st.success("Admin Access Granted")

        else:

            st.error("Wrong Password")

    # =====================================================
    # FULL ADMIN SECTION
    # =====================================================

    if st.session_state.admin_ok:

        st.markdown("### Upload Machine Memory")

        selected_line = st.selectbox(
            "Select Line",
            [f"Line {i}" for i in range(1,21)]
        )

        machine_options = [
            "M1","M2","M3","M4","M5",
            "M6","M7","M8","M9","M10",
            "M11","M12","M13","M14",
            "M15","M16","M17","M18",
            "Filler","Packer","Conveyor"
        ]

        selected_machine = st.selectbox(
            "Select Machine",
            machine_options
        )

        memory_key = f"{selected_line}_{selected_machine}"

        uploaded_file = st.file_uploader(
            "Upload TXT Technical File",
            type=["txt"]
        )

        action = st.radio(
            "Select Action",
            ["Add Data", "Override Data"]
        )

        if st.button("Process Data"):

            if uploaded_file is not None:

                file_text = uploaded_file.read().decode("utf-8")

                # ADD DATA
                if action == "Add Data":

                    old_data = st.session_state.knowledge_base.get(
                        memory_key,
                        ""
                    )

                    st.session_state.knowledge_base[memory_key] = (
                        old_data + "\n\n" + file_text
                    )

                    st.success(f"Data Added: {memory_key}")

                # OVERRIDE
                else:

                    st.session_state.knowledge_base[memory_key] = file_text

                    st.success(f"Data Replaced: {memory_key}")

            else:

                st.warning("Upload TXT file first")

        # =================================================
        # SHOW SAVED MEMORIES
        # =================================================

        st.markdown("---")
        st.markdown("### Saved Memories")

        if len(st.session_state.knowledge_base) > 0:

            for key in st.session_state.knowledge_base.keys():

                st.write("✅", key)

            delete_key = st.selectbox(
                "Select Memory To Delete",
                list(st.session_state.knowledge_base.keys())
            )

            if st.button("Delete Selected Memory"):

                del st.session_state.knowledge_base[delete_key]

                st.success(f"{delete_key} Deleted")

                st.rerun()

        else:

            st.info("No Memory Saved")

        # =================================================
        # CLEAR CHAT
        # =================================================

        if st.button("Clear Chat History"):

            st.session_state.messages = []

            st.rerun()

        # =================================================
        # LOGOUT
        # =================================================

        if st.button("Logout"):

            st.session_state.admin_ok = False
            st.session_state.admin_open = False

            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

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

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# =========================================================
# SHOW CHAT
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
        "role":"user",
        "content":prompt
    })

    with st.chat_message("user"):

        st.markdown(prompt)

    # =====================================================
    # ALL MEMORY
    # =====================================================

    all_memory = ""

    for key, value in st.session_state.knowledge_base.items():

        all_memory += f"\n\n### MEMORY: {key}\n{value}"

    # =====================================================
    # SYSTEM PROMPT
    # =====================================================

    system_prompt = f"""
You are KAZIM AI.

You are industrial technical AI.

IMPORTANT RULES:
- Use ONLY uploaded memory.
- NEVER create fake machine information.
- NEVER guess specifications.
- If memory not available say:
"No related technical data found."

Technical Memory:
{all_memory}
"""

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

            ai_reply = response.choices[0].message.content

        except Exception as e:

            ai_reply = f"Error: {str(e)}"

        st.markdown(ai_reply)

    st.session_state.messages.append({
        "role":"assistant",
        "content":ai_reply
    })
