import streamlit as st
import os
import time
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="KAZIM AI - Industrial Diagnostic", layout="centered")

# --- PREMIUM MODERN CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    /* Modern Big Search Box */
    .stChatInput textarea {
        font-size: 18px !important;
        padding: 20px !important;
        border-radius: 15px !important;
        border: 2px solid #3b82f6 !important;
        background-color: #ffffff !important;
    }
    /* Modern Chat Bubble Styling */
    .chat-bubble-ai { background-color: #f1f5f9; padding: 20px; border-radius: 15px; border-left: 5px solid #2563eb; margin: 15px 0; font-family: 'Segoe UI'; }
    .chat-bubble-user { background-color: #eff6ff; padding: 15px; border-radius: 15px; margin: 15px 0; text-align: right; border: 1px solid #bfdbfe; }
    .header-text { font-size: 28px; font-weight: bold; color: #1e293b; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- SIDEBAR: DIAGNOSTIC MATRIX ---
st.sidebar.markdown("### ⚙️ Diagnostic Console")
selected_line = st.sidebar.selectbox("Select Production Line:", [f"Line {i}" for i in range(1, 21)])
selected_machine = st.sidebar.selectbox("Select Filler Node:", [f"M{i} Unit" for i in range(1, 21)])
machine_id = f"database_{selected_line.replace(' ', '')}_{selected_machine.replace(' ', '')}.txt"

# Admin Access Panel
with st.sidebar.expander("🔐 Data Management Access"):
    if st.text_input("Admin Password:", type="password") == "Kazim@2026":
        st.success("Authorized")
        write_mode = st.radio("Access Mode:", ["Append", "Overwrite"])
        files = st.file_uploader("Upload reference files:", accept_multiple_files=True)
        if st.button("🚀 Commit to Matrix"):
            content = "".join([f.read().decode("utf-8", errors="ignore") for f in files])
            mode = "w" if write_mode == "Overwrite" else "a"
            with open(machine_id, mode, encoding="utf-8") as f: f.write(content)
            st.rerun()

# --- MAIN INTERFACE ---
st.markdown('<p class="header-text">KAZIM AI — Industrial Diagnostic Core</p>', unsafe_allow_html=True)
st.write(f"Diagnostic target: **{selected_machine}** | Status: **Online**")

if "messages" not in st.session_state: st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# --- BIG TECH SEARCH BOX ---
if prompt := st.chat_input("Enter fault code, error, or component symptom..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        # Diagnostic Logic
        context = open(machine_id, "r").read() if os.path.exists(machine_id) else "Manual pending."
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"Context: {context}\n\nFault/Query: {prompt}\n\nAct as a senior engineer.")
        
        full_res = ""
        for word in response.text.split():
            full_res += word + " "
            message_placeholder.markdown(full_res + "▌")
            time.sleep(0.01)
        message_placeholder.markdown(full_res)
        st.session_state.messages.append({"role": "assistant", "content": full_res})
