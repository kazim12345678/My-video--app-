import streamlit as st
import os
import time
import google.generativeai as genai
from PIL import Image

# --- WORLD-CLASS LAYOUT CONFIGURATION ---
st.set_page_config(
    page_title="KAZIM AI", 
    page_icon="🤖", 
    layout="wide", 
    initial_sidebar_state="collapsed"  # Hides boring controls from operators automatically
)

# --- MODERN ULTRA-CLEAN CSS (PREMIUM INTERFACE) ---
st.markdown("""
    <style>
    /* Absolute Body Clean Up */
    .stApp { background-color: #fcfcfd; color: #1e293b; }
    
    /* Header Container styling */
    .premium-header {
        text-align: center;
        padding: 40px 0px 20px 0px;
        margin-bottom: 20px;
        background: linear-gradient(to right, #ffffff, #f8fafc, #ffffff);
        border-bottom: 1px solid #e2e8f0;
    }
    .premium-title { font-size: 36px; font-weight: 800; color: #0f172a; font-family: -apple-system, sans-serif; letter-spacing: -0.5px; }
    .premium-subtitle { font-size: 14px; color: #64748b; margin-top: 6px; font-weight: 400; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Industrial Dropdown Panel Style */
    .selector-tray {
        background-color: #ffffff;
        padding: 15px 25px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 30px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    
    /* Elegant Chat Bubble Aesthetics */
    .chat-bubble-user {
        background-color: #0f172a; padding: 16px 24px; border-radius: 24px 24px 4px 24px;
        margin: 16px 0px; max-width: 70%; float: right; clear: both;
        color: #ffffff; font-family: -apple-system, sans-serif; font-size: 15px;
        box-shadow: 0 4px 12px rgba(15,23,42,0.08);
    }
    .chat-bubble-ai {
        background-color: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid #2563eb; 
        padding: 18px 24px; border-radius: 24px 24px 24px 4px; margin: 16px 0px; max-width: 82%; 
        float: left; clear: both; color: #0f172a; font-family: -apple-system, sans-serif; 
        font-size: 15px; line-height: 1.65; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.01);
    }
    
    /* Sidebar custom tuning */
    div[data-testid="stSidebar"] { background-color: #f8fafc !important; border-right: 1px solid #e2e8f0; }
    
    /* Space Equalizer */
    .space-breaker { clear: both; height: 10px; }
    </style>
""", unsafe_allow_html=True)

# Secure API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing GEMINI_API_KEY inside Streamlit Advanced Secrets!")
    st.stop()

# --- TOP HEADER PLATFORM ---
st.markdown("""
    <div class="premium-header">
        <div class="premium-title">🤖 KAZIM AI</div>
        <div class="premium-subtitle">Serac Intelligence Matrix — Digital Automation Hub</div>
    </div>
""", unsafe_allow_html=True)

# Memory Session Registers
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- HMI CONSOLE TRAYS (MINIMAL DROPDOWNS) ---
st.markdown('<div class="selector-tray">', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    selected_line = st.selectbox("🏭 Live Production Target Area:", [f"Line {i}" for i in range(1, 21)])
with c2:
    selected_machine = st.selectbox("⚙️ Active Machine Node:", [f"M{i} Filler Unit" for i in range(1, 21)])
st.markdown('</div>', unsafe_allow_html=True)

# Create unique binary identifiers for every separate machine file database
machine_id = f"database_{selected_line.replace(' ', '')}_{selected_machine.replace(' ', '')}.txt"

# --- RENDER MESSAGES WITH SMART DESIGN ---
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-bubble-user"><b>You:</b><br>{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble-ai"><b>KAZIM AI:</b><br>{message["content"]}</div>', unsafe_allow_html=True)

st.markdown("<div class=\"space-breaker\"></div>", unsafe_allow_html=True)

# --- MODERN CONSOLE CHAT INPUT & SCREENSHOT PORT ---
st.write("")
col_img, col_blank = st.columns([2, 2])
with col_img:
    attached_img = st.file_uploader("📸 Scan HMI Screen / Component Diagram (Optional):", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

user_prompt = st.chat_input("Type your hardware code or component symptom here...")

if user_prompt:
    # Print User Query immediately
    st.markdown(f'<div class="chat-bubble-user"><b>You:</b><br>{user_prompt}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    # Isolate and Load data strictly for the selected machine
    context_data = ""
    if os.path.exists(machine_id):
        with open(machine_id, "r", encoding="utf-8") as f_read:
            context_data = f_read.read()
    else:
        context_data = "No custom engineering manual loaded yet for this machine matrix."

    # Formulate Professional Prompt Environment
    final_system_prompt = (
        f"You are the world's leading Automation Engineer specialized in Serac Filling Systems.\n"
        f"You are directly diagnosing {selected_machine} operating on {selected_line}.\n"
        f"Base your analysis strictly on this locked technical context:\n{context_data}\n\n"
        f"Operator Query: {user_prompt}\n\n"
        "Provide an elite, professional breakdown using formatting toolkit principles. Use bold tags for steps."
    )
    
    with st.spinner("Decoding field signals..."):
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            if attached_img:
                img_open = Image.open(attached_img)
                response = model.generate_content([final_system_prompt, img_open])
            else:
                response = model.generate_content(final_system_prompt)
            
            # Simulated Premium Live Word-by-Word Typing Stream
            ai_response_text = response.text
            message_placeholder = st.empty()
            full_displayed_text = ""
            
            for word in ai_response_text.split(" "):
                full_displayed_text += word + " "
                message_placeholder.markdown(f'<div class="chat-bubble-ai"><b>KAZIM AI:</b><br>{full_displayed_text}▌</div>', unsafe_allow_html=True)
                time.sleep(0.03)  # Professional smooth text generation latency
                
            message_placeholder.markdown(f'<div class="chat-bubble-ai"><b>KAZIM AI:</b><br>{full_displayed_text}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": ai_response_text})
            st.rerun()
            
        except Exception as system_err:
            st.error(f"Execution Error: {str(system_err)}")


# --- HIDDEN SYSTEM DATA CENTER CONTROL PANEL (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h3 style='color: #1e293b; font-family:sans-serif;'>🔒 Vault Control</h3>", unsafe_allow_html=True)
    
    # Secret Password field
    admin_password = st.text_input("Enter Secret Admin Password:", type="password")
    
    if admin_password == "Kazim@2026":
        st.markdown("<div style='background-color:#d1fae5; padding:10px; border-radius:8px; color:#065f46; font-weight:bold; font-size:12px; margin-bottom:15px; border:1px solid #10b981;'>🔓 ACCESS AUTHORIZED</div>", unsafe_allow_html=True)
        st.markdown(f"**Target Allocation:** `{machine_id}`")
        
        db_exists = os.path.exists(machine_id)
        if db_exists:
            st.warning(f"Data balance found for {selected_machine}.")
            write_mode = st.radio("Choose Update Mode:", ["Add/Append Data (Don't Erase)", "Overwrite (Completely Erase Old Data)"])
        else:
            st.success("Database is clean. Ready to lock initial files.")
            write_mode = "Overwrite (Completely Erase Old Data)"
            
        # File Intake Stage
        new_manuals = st.file_uploader("Upload reference logs (.txt):", type=["txt"], accept_multiple_files=True)
        
        if st.button("🚀 Process & Lock Data Platform"):
            if new_manuals:
                combined_uploaded_text = ""
                for f in new_manuals:
                    combined_uploaded_text += f.read().decode("utf-8", errors="ignore") + "\n"
                
                # Dynamic Write/Append Execution
                file_open_flag = "w" if "Overwrite" in write_mode else "a"
                
                with open(machine_id, file_open_flag, encoding="utf-8") as f_target:
                    f_target.write(combined_uploaded_text)
                    
                st.success(f"Data locked successfully into matrix index: {machine_id}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Please insert a technical file first!")
                
        if db_exists:
            if st.button("🗑️ Wipe This Machine's Current Database"):
                os.remove(machine_id)
                st.success("Target database cleared from memory server.")
                time.sleep(1)
                st.rerun()
                
    elif admin_password != "":
        st.error("Invalid Security Credentials!")
