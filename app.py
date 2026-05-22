import streamlit as st
import os
import time
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="KAZIM AI - Industrial Diagnostic", layout="centered")

# --- PREMIUM MODERN CSS (FIXED) ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    /* Force Big Search Box */
    div[data-testid="stChatInput"] { 
        padding: 10px; 
        background: white; 
    }
    textarea {
        font-size: 18px !important;
        padding: 20px !important;
        border-radius: 20px !important;
        border: 2px solid #2563eb !important;
    }
    /* Modern Headers */
    .header-text { font-size: 28px; font-weight: 800; color: #1e293b; }
    </style>
""", unsafe_allow_html=True)

# API Configuration
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- SIDEBAR: CONSOLE ---
st.sidebar.markdown("### ⚙️ Diagnostic Console")
line = st.sidebar.selectbox("Select Line:", [f"Line {i}" for i in range(1, 21)])
machine = st.sidebar.selectbox("Select Node:", [f"M{i} Unit" for i in range(1, 21)])
machine_id = f"database_{line.replace(' ', '')}_{machine.replace(' ', '')}.txt"

# --- ADMIN PANEL ---
with st.sidebar.expander("🔐 Data Management"):
    if st.text_input("Admin Password:", type="password") == "Kazim@2026":
        mode = st.radio("Access:", ["Append", "Overwrite"])
        files = st.file_uploader("Upload logs:", accept_multiple_files=True)
        if st.button("🚀 Commit to Matrix"):
            content = "".join([f.read().decode("utf-8", errors="ignore") for f in files])
            with open(machine_id, "w" if mode == "Overwrite" else "a", encoding="utf-8") as f: f.write(content)
            st.rerun()

# --- MAIN INTERFACE ---
st.markdown('<p class="header-text">KAZIM AI — Industrial Diagnostic Core</p>', unsafe_allow_html=True)
st.info(f"Target: **{machine}** | Status: **{'Online' if os.path.exists(machine_id) else 'Awaiting Data'}**")

if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# --- BIG CHAT INPUT ---
if prompt := st.chat_input("Search filler faults, error codes, or symptoms..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Safe File Loading
        context = open(machine_id, "r").read() if os.path.exists(machine_id) else "Engineering manual not uploaded for this node."
        
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(f"Context: {context}\n\nFault: {prompt}\n\nRole: Senior Automation Engineer.")
            
            full_res = ""
            for word in response.text.split():
                full_res += word + " "
                message_placeholder.markdown(full_res + "▌")
                time.sleep(0.01)
            message_placeholder.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
        except Exception as e:
            st.error(f"System Error: {e}")
