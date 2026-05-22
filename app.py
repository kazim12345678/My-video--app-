import streamlit as st
import os
import time
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="KAZIM AI - Industrial Diagnostic", layout="centered", page_icon="🤖")

# --- PREMIUM MODERN CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    /* Big Search Box */
    .stChatInput { padding: 10px; }
    textarea {
        font-size: 18px !important;
        padding: 20px !important;
        border-radius: 20px !important;
        border: 2px solid #2563eb !important;
        background-color: #f8fafc !important;
    }
    /* Modern Headers */
    .header-text { font-size: 28px; font-weight: 800; color: #1e293b; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# API Configuration
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- SIDEBAR: CONSOLE ---
st.sidebar.markdown("### ⚙️ Diagnostic Console")
line = st.sidebar.selectbox("Select Production Line:", [f"Line {i}" for i in range(1, 21)])
machine = st.sidebar.selectbox("Select Filler Node:", [f"M{i} Unit" for i in range(1, 21)])
machine_id = f"database_{line.replace(' ', '')}_{machine.replace(' ', '')}.txt"

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
st.info(f"Targeting: **{machine}** | Status: **{'Online' if os.path.exists(machine_id) else 'Awaiting Data'}**")

# Session State for Chat
if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# --- BIG CHAT INPUT ---
if prompt := st.chat_input("Enter fault code, error, or component symptom..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Load context safely
        context = open(machine_id, "r").read() if os.path.exists(machine_id) else "No manual loaded."
        
        try:
            # Using 'gemini-1.5-pro' for high stability (avoiding 404 error)
            model = genai.GenerativeModel('gemini-1.5-pro')
            response = model.generate_content(f"Context: {context}\n\nFault: {prompt}\n\nRole: Senior Automation Engineer. Provide expert breakdown.")
            
            full_res = ""
            for word in response.text.split():
                full_res += word + " "
                message_placeholder.markdown(full_res + "▌")
                time.sleep(0.01)
            message_placeholder.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
        except Exception as e:
            st.error(f"System Error: {e}. Please ensure your API Key has access to the selected model.")
