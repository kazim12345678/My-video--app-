import streamlit as st
import os
import time
from openai import OpenAI

# --- PAGE CONFIG ---
st.set_page_config(page_title="KAZIM AI - M18 Diagnostic", layout="centered", page_icon="🤖")

# --- MODERN CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    textarea { font-size: 18px !important; padding: 20px !important; border-radius: 20px !important; border: 2px solid #10b981 !important; background-color: #f8fafc !important; }
    .header-text { font-size: 28px; font-weight: 800; color: #064e3b; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- OPENAI SETUP ---
# Streamlit secrets mein OPENAI_API_KEY hona chahiye
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- SIDEBAR: 20-LINE MATRIX ---
st.sidebar.markdown("### ⚙️ M18 Diagnostic Console")
line = st.sidebar.selectbox("Select Production Line:", [f"Line {i}" for i in range(1, 21)])
machine = st.sidebar.selectbox("Select Filler Node:", [f"M{i} Unit" for i in range(1, 21)])
machine_id = f"db_{line.replace(' ', '')}_{machine.replace(' ', '')}.txt"

# --- ADMIN PANEL ---
with st.sidebar.expander("🔐 Data Management Access"):
    if st.text_input("Admin Password:", type="password") == "Kazim@2026":
        st.success("Authorized")
        mode = st.radio("Access Mode:", ["Append", "Overwrite"])
        files = st.file_uploader("Upload technical logs (.txt):", accept_multiple_files=True)
        if st.button("🚀 Commit to Matrix"):
            content = "".join([f.read().decode("utf-8", errors="ignore") for f in files])
            with open(machine_id, "w" if mode == "Overwrite" else "a", encoding="utf-8") as f: f.write(content)
            st.rerun()

# --- MAIN INTERFACE ---
st.markdown('<p class="header-text">KAZIM AI — Industrial Diagnostic Core</p>', unsafe_allow_html=True)
st.info(f"Monitoring: **{line}** | **{machine}** | Status: **{'Online' if os.path.exists(machine_id) else 'Awaiting Manual'}**")

# Session State for Chat
if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# --- CHAT INPUT (ChatGPT Engine) ---
if prompt := st.chat_input("Enter fault code or symptom..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Safe Context Loading
        context = open(machine_id, "r").read() if os.path.exists(machine_id) else "Technical manual not uploaded."
        
        try:
            # ChatGPT API Call
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are a Senior Automation Engineer. Use this technical context: {context}"},
                    {"role": "user", "content": prompt}
                ],
                stream=True,
            )
            
            full_res = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_res += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_res + "▌")
            
            message_placeholder.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
        except Exception as e:
            st.error(f"System Error: {e}")
