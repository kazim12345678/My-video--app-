import streamlit as st
import os
import time
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="KAZIM AI - M18 Diagnostic", layout="centered", page_icon="🤖")

# --- MODERN CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    textarea { font-size: 18px !important; padding: 20px !important; border-radius: 20px !important; border: 2px solid #2563eb !important; }
    .header-text { font-size: 28px; font-weight: 800; color: #1e293b; }
    </style>
""", unsafe_allow_html=True)

# API Configuration
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- SIDEBAR: 20-LINE MATRIX ---
st.sidebar.markdown("### ⚙️ M18 Diagnostic Console")
line = st.sidebar.selectbox("Select Line:", [f"Line {i}" for i in range(1, 21)])
machine = st.sidebar.selectbox("Select Node:", [f"M{i} Unit" for i in range(1, 21)])
# Machine specific database ID
machine_id = f"db_{line.replace(' ', '')}_{machine.replace(' ', '')}.txt"

# --- ADMIN PANEL ---
with st.sidebar.expander("🔐 Data Management"):
    if st.text_input("Admin Password:", type="password") == "Kazim@2026":
        mode = st.radio("Access:", ["Append", "Overwrite"])
        files = st.file_uploader("Upload logs:", accept_multiple_files=True)
        if st.button("🚀 Lock & Commit"):
            content = "".join([f.read().decode("utf-8", errors="ignore") for f in files])
            with open(machine_id, "w" if mode == "Overwrite" else "a", encoding="utf-8") as f: f.write(content)
            st.success("Data committed to memory.")
            st.rerun()

# --- MAIN INTERFACE ---
st.markdown('<p class="header-text">KAZIM AI — Industrial Core</p>', unsafe_allow_html=True)
st.info(f"Monitoring: **{line}** | **{machine}** | Status: **{'Active' if os.path.exists(machine_id) else 'Awaiting Manual'}**")

if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# --- DIAGNOSTIC ENGINE ---
if prompt := st.chat_input("Enter fault code or symptom..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        # Context loading
        context = open(machine_id, "r").read() if os.path.exists(machine_id) else "Manual not available."
        
        try:
            # Using 'gemini-1.5-flash' (Most compatible with Free Tier)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(f"Context: {context}\n\nFault: {prompt}\n\nAct as a Senior Automation Engineer.")
            
            full_res = ""
            for word in response.text.split():
                full_res += word + " "
                message_placeholder.markdown(full_res + "▌")
                time.sleep(0.01)
            message_placeholder.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
        except Exception as e:
            st.error(f"Engine Error: {e}. Check API connectivity.")
