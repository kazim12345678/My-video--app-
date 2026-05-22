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
    .main { background-color: #f9fabc; color: #1f2937; }
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
    machine_selection = st.selectbox("Select Machine Unit:", ["M2 Filler Unit", "M1 Filler", "Capper Unit", "Labeling Network"])
    
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
                        fname_lower = f.name.lower()
                        
                        if fname_lower.endswith(".txt"):
                            file_content = f.read().decode("utf-8", errors="ignore")
                            # File ka naam header mein save ho raha hai taake search strong ho
                            full_combined_text += f"\n[FILE NAME: {f.name}]\n{file_content}\n"
                        
                        elif fname_lower.endswith(".pdf"):
                            try:
                                reader = PyPDF2.PdfReader(f)
                                for p_idx, page in enumerate(reader.pages):
                                    t = page.extract_text()
                                    if t: 
                                        full_combined_text += f"\n[Manual: {f.name} | Page: {p_idx+1}]\n{t}\n"
                            except Exception as pdf_err:
                                st.warning(f"Could not read PDF {f.name}: {str(pdf_err)}")
                    
                    if full_combined_text.strip():
                        with open(TEXT_FILE, "w", encoding="utf-8") as f_out:
                            f_out.write(full_combined_text)
                        st.success("Knowledge vault locked successfully!")
                        st.rerun()
            else:
                st.error("Meharbani karke pehle koi file select ya drop karein!")

# --- MAIN CHAT INTERFACE PANEL ---
st.markdown(f"""
    <div class="copilot-header">
        <h1 style='margin:0; color:#111827; font-size: 26px;'>🤖 KAZIM Chat Assistant</h1>
        <p style='margin:5px 0 0 0; color:#6b7280; font-size:14px;'>Active Tracking on: <b>{line_selection} — {machine_selection}</b></p>
    </div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-bubble"><b>You:</b><br>{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-bubble"><b>KAZIM AI:</b><br>{message["content"]}</div>', unsafe_allow_html=True)

st.markdown("<div style='clear: both;'></div>", unsafe_allow_html=True)

st.write("---")
st.write("💬 Ask anything from KAZIM:")

attached_image = st.file_uploader("📸 Optional: Attach a picture:", type=["jpg", "jpeg", "png"])
user_query = st.chat_input("Type your hardware code or component symptom here...")

if user_query:
    st.markdown(f'<div class="user-bubble"><b>You:</b><br>{user_query}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # ADVANCED CONTEXT FILTER: Pure file scan matching mechanism
    filtered_manual_context = ""
    if os.path.exists(TEXT_FILE):
        matched_chunks = []
        # Chote keywords (jaise M2, CIP) ko filter se delete nahi karega
        keywords = [w.lower().strip() for w in user_query.split() if len(w.strip()) >= 2]
        
        with open(TEXT_FILE, "r", encoding="utf-8") as f_in:
            file_lines = f_in.readlines()
            
            # Smart logic: pura block scan karega agar M2 lafz milega
            for idx, line in enumerate(file_lines):
                if any(kw in line.lower() for kw in keywords):
                    # Us line ke aage peeche ki 5 lines bhi utha lega behtar context ke liye
                    start_idx = max(0, idx - 3)
                    end_idx = min(len(file_lines), idx + 7)
                    chunk_text = "".join(file_lines[start_idx:end_idx])
                    matched_chunks.append(chunk_text.strip())
        
        if matched_chunks:
            filtered_manual_context = "\n---\n".join(matched_chunks[:15])

    if not filtered_manual_context:
        filtered_manual_context = "General standard industrial automation specification database."

    prompt_instructions = (
        f"You are an Elite Industrial Automation Engineer analyzing a query on {machine_selection} at {line_selection}.\n"
        f"Strictly focus on the user's specific model keyword (e.g., M2 or M1) asked in the prompt.\n"
        f"Here is the Technical Reference Data extracted from your verified factory manuals:\n{filtered_manual_context}\n\n"
        f"Operator Question: {user_query}\n\n"
        "Provide a technical root-cause explanation or system operational breakdown. Use clear numbered bullet points for maintenance actions."
    )
    
    with st.spinner("Scanning Technical Manual Database..."):
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            if attached_image:
                img_data = Image.open(attached_image)
                response = model.generate_content([prompt_instructions, img_data])
            else:
                response = model.generate_content(prompt_instructions)
            
            st.markdown(f'<div class="ai-bubble"><b>KAZIM AI:</b><br>{response.text}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
            
        except Exception as e:
            st.error(f"System Trace Error: {str(e)}")
