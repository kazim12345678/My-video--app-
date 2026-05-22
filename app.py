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
    </style>
""", unsafe_allow_html=True)

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- SIDEBAR: MACHINE SELECTION (Always Visible) ---
st.sidebar.title("🏭 Production Matrix")
selected_line = st.sidebar.selectbox("Line:", [f"Line {i}" for i in range(1, 21)])
selected_machine = st.sidebar.selectbox("Machine Node:", [f"M{i}" for i in range(1, 21)])
machine_id = f"database_{selected_line.replace(' ', '')}_{selected_machine}.txt"

# --- SIDEBAR: ADMIN SECTION ---
st.sidebar.markdown("---")
with st.sidebar.expander("🔐 Admin Access (Data Management)"):
    admin_password = st.text_input("Password:", type="password")
    if admin_password == "Kazim@2026":
        st.success("Authorized")
        write_mode = st.radio("Mode:", ["Append", "Overwrite"])
        new_manuals = st.file_uploader("Upload logs:", type=["txt"], accept_multiple_files=True)
        
        if st.button("🚀 Process & Lock Data"):
            if new_manuals:
                content = "".join([f.read().decode("utf-8", errors="ignore") for f in new_manuals])
                mode = "w" if write_mode == "Overwrite" else "a"
                with open(machine_id, mode, encoding="utf-8") as f:
                    f.write(content)
                st.rerun()
        
        if st.button("🗑️ Wipe Database"):
            if os.path.exists(machine_id):
                os.remove(machine_id)
                st.rerun()
    elif admin_password:
        st.error("Wrong Password!")

# --- MAIN CHAT AREA ---
st.title("🤖 KAZIM AI")
st.write(f"Monitoring: **{selected_machine}** on **{selected_line}**")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Kazim AI se baat karein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        context = ""
        if os.path.exists(machine_id):
            with open(machine_id, "r", encoding="utf-8") as f:
                context = f.read()

        model = genai.GenerativeModel('gemini-1.5-flash')
        final_prompt = f"Context: {context}\n\nQuestion: {prompt}"
        response = model.generate_content(final_prompt)
        
        full_res = ""
        for word in response.text.split():
            full_res += word + " "
            message_placeholder.markdown(full_res + "▌")
            time.sleep(0.02)
        message_placeholder.markdown(full_res)
        st.session_state.messages.append({"role": "assistant", "content": full_res})
