import streamlit as st
import os
import time
import google.generativeai as genai
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(page_title="KAZIM AI", page_icon="🤖", layout="centered")

# --- MODERN CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .chat-bubble-ai { background-color: #f8f9fa; padding: 20px; border-radius: 15px; margin: 10px 0; border-left: 5px solid #4285f4; }
    .chat-bubble-user { background-color: #e8f0fe; padding: 15px; border-radius: 15px; margin: 10px 0; text-align: right; }
    section[data-testid="stSidebar"] { background-color: #f8f9fa; }
    </style>
""", unsafe_allow_html=True)

# API Configuration
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🤖 KAZIM AI")
st.subheader("Serac Intelligence Matrix - M18")

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR ADMIN PANEL (THE LOGIN GATEWAY) ---
with st.sidebar:
    st.markdown("### 🔒 Vault Control")
    admin_password = st.text_input("Enter Admin Password:", type="password")
    
    if admin_password == "Kazim@2026":
        st.success("🔓 Access Authorized")
        machine_id = "M18_Data.txt"
        
        write_mode = st.radio("Mode:", ["Append", "Overwrite"])
        new_manuals = st.file_uploader("Upload logs:", type=["txt"], accept_multiple_files=True)
        
        if st.button("🚀 Process & Lock Data"):
            if new_manuals:
                content = "".join([f.read().decode("utf-8") for f in new_manuals])
                mode = "w" if write_mode == "Overwrite" else "a"
                with open(machine_id, mode, encoding="utf-8") as f:
                    f.write(content)
                st.rerun()
        
        if st.button("🗑️ Wipe Database"):
            if os.path.exists(machine_id):
                os.remove(machine_id)
                st.rerun()
    elif admin_password:
        st.error("Invalid Credentials!")

# --- CHAT INTERFACE ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Kazim AI se baat karein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Load Data
        context = ""
        if os.path.exists("M18_Data.txt"):
            with open("M18_Data.txt", "r", encoding="utf-8") as f:
                context = f.read()

        model = genai.GenerativeModel('gemini-1.5-flash')
        final_prompt = f"Context: {context}\n\nQuestion: {prompt}\n\nAction: Diagnostic assistant."
        
        response = model.generate_content(final_prompt)
        
        # Typing Effect
        full_res = ""
        for word in response.text.split():
            full_res += word + " "
            message_placeholder.markdown(full_res + "▌")
            time.sleep(0.02)
        message_placeholder.markdown(full_res)
        st.session_state.messages.append({"role": "assistant", "content": full_res})
