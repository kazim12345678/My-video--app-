import streamlit as st
import pandas as pd
import PyPDF2
import google.generativeai as genai
import os
from PIL import Image

# --- COPILOT LIGHT THEME CONFIGURATION ---
st.set_page_config(
    page_title="KAZIM AI Assistant", 
    page_icon="⚙️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom CSS for a clean, modern white/light-grey Copilot interface
st.markdown("""
    <style>
    .main { background-color: #f9faExternalbc; color: #1f2937; }
    div[data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e5e7eb; }
    
    /* Copilot Header Styling */
    .copilot-header {
        padding: 15px 0px;
        border-bottom: 1px solid #e5e7eb;
        margin-bottom: 25px;
    }
    
    /* Chat Message Bubbles */
    .user-bubble {
        background-color: #f3f4f6;
        padding: 14px 18px;
        border-radius: 18px 18px 2px 18px;
        margin: 10px 0px;
        max-width: 80%;
        float: right;
        clear: both;
        color: #1f2937;
        font-family: sans-serif;
    }
    .ai-bubble {
        background-color: #edf5ff;
        border-left: 4px solid #0066cc;
        padding: 14px 18px;
        border-radius: 18px 18px 18px 2px;
        margin: 10px 0px;
        max-width: 85%;
        float: left;
        clear: both;
        color: #111827;
        font-family: sans-serif;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    /* System Status Alerts */
    .status-card {
        background-color: #ecfdf5;
        border: 1px solid #10b981;
        padding: 12px;
        border-radius: 8px;
        color: #065f46;
        font-weight: bold;
        font-size: 13px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Secure API Key Connection
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing GEMINI_API_KEY inside your Streamlit Advanced Secrets!")
    st.stop()

# Local database file paths
TEXT_FILE = "kazim_knowledge_text.txt"

# --- SIDEBAR CONTROL PANEL (TRAINING & CONFIGURATION) ---
with st.sidebar:
    st.markdown("<h2 style='color: #0066cc; margin-top: 0;'>⚙️ KAZIM Control Center</h2>", unsafe_allow_html=True)
    st.write("Configure your line matrix and upload reference manuals below.")
    st.write("---")
    
    # 1. Machine Selection Matrix
    line_selection = st.selectbox("Select Production Line:", [f"Line {i}" for i in range(1, 21)])
    machine_selection = st.selectbox("Select Machine Unit:", ["M1 Filler", "Capper Unit", "Labeling Network", "Palletizer Assembly"])
    
    st.write("---")
    st.markdown("### 📁 Training Knowledge Vault")
    
    is_trained = os.path.exists(TEXT_FILE)
    if is_trained:
        st.markdown('<div class="status-card">🟢 DATABASE ONLINE<br><span style="font-weight:normal; font-size:11px;">Manual data loaded into memory.</span></div>', unsafe_allow_html=True)
        force_rebuild = st.checkbox("🔄 Upload/Update Reference Materials?")
        if force_rebuild:
            is_trained = False

    if not is_trained:
        uploaded_docs = st.file_uploader(
            "Upload Cheat Sheets, Electrical TXT, or Machine Manual PDFs:", 
            type=["txt", "pdf", "xlsx", "csv"], 
            accept_multiple_files=True
        )
        
        if st.button("🚀 Process & Lock Data"):
            if uploaded_docs:
                full_combined_text = ""
                with st.spinner("Compiling technical blueprints..."):
                    for f in uploaded_docs:
                        if f.name.endswith(".txt"):
                            full_combined_text += f"\n[FILE: {f.name}]\n" + f.read().decode("utf-8")
                        elif f.name.endswith(".pdf"):
                            reader = PyPDF2.PdfReader(f)
                            for p_idx, page in enumerate(reader.pages):
                                t = page.extract_text()
                                if t: full_combined_text += f"\n[Manual: {f.name} | Page: {p_idx+1}]\n{t}\n"
                    
                    if full_combined_text.strip():
                        with open(TEXT_FILE, "w", encoding="utf-8") as f_out:
                            f_out.write(full_combined_text)
                        st.success("Knowledge vault updated!")
                        st.rerun()

# --- MAIN CHAT INTERFACE PANEL ---
st.markdown(f"""
    <div class="copilot-header">
        <h1 style='margin:0; color:#111827; font-size: 26px;'>🤖 KAZIM Chat Assistant</h1>
        <p style='margin:5px 0 0 0; color:#6b7280; font-size:14px;'>Active Tracking on: <b>{line_selection} — {machine_selection}</b></p>
    </div>
""", unsafe_allow_html=True)

# Initialize Chat History Memory arrays so it works like Copilot
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous messages on the screen automatically
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-bubble"><b>You:</b><br>{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-bubble"><b>KAZIM AI:</b><br>{message["content"]}</div>', unsafe_allow_html=True)

st.markdown("<div style='clear: both;'></div>", unsafe_allow_html=True)

# --- CHAT INPUT BAR & PICTURE ATTACHMENT BOX ---
st.write("---")
st.write("💬 Ask anything from KAZIM:")

# Image upload widget directly in the chat field area
attached_image = st.file_uploader("📸 Optional: Attach a picture of a fault code, screen error, or component:", type=["jpg", "jpeg", "png"])

# The continuous chat text box entry input
user_query = st.chat_input("Type your hardware code or component symptom here...")

if user_query:
    # 1. Print the user's question bubble instantly onto the screen
    st.markdown(f'<div class="user-bubble"><b>You:</b><br>{user_query}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # 2. Filter local text manuals for matching text snippets
    filtered_manual_context = "General operational engineering parameters."
    if os.path.exists(TEXT_FILE):
        matched_lines = []
        keywords = [w.lower().strip() for w in user_query.split() if len(w.strip()) > 2]
        with open(TEXT_FILE, "r", encoding="utf-8") as f_in:
            for line in f_in:
                if any(kw in line.lower() for kw in keywords) or "specification" in line.lower():
                    matched_lines.append(line.strip())
        if matched_lines:
            filtered_manual_context = "\n".join(matched_lines[:25])

    # 3. Handle prompt building whether it is a text-only prompt or an image analysis prompt
    prompt_instructions = (
        f"You are an Elite Industrial Automation Engineer analyzing a fault on {machine_selection} at {line_selection}.\n"
        f"Use these lines from the manual for technical reference:\n{filtered_manual_context}\n\n"
        f"Operator Question: {user_query}\n\n"
        "Provide a direct root-cause breakdown followed by a prioritized, numbered checklist for the technician."
    )
    
    with st.spinner("Analyzing parameters..."):
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            if attached_image:
                # Open and process the uploaded photo using PIL library
                img_data = Image.open(attached_image)
                # Send both the photo and the engineering instructions to Gemini
                response = model.generate_content([prompt_instructions, img_data])
            else:
                # Text-only call
                response = model.generate_content(prompt_instructions)
            
            # 4. Print the AI response bubble on the screen and save to chat history
            st.markdown(f'<div class="ai-bubble"><b>KAZIM AI:</b><br>{response.text}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
            
        except Exception as e:
            st.error(f"System communication trace anomaly: {str(e)}")
