import streamlit as st
import os
import time
import google.generativeai as genai
from PIL import Image

# --- WORLD-CLASS CONFIGURATION & THEME ---
st.set_page_config(
    page_title="KAZIM AI", 
    page_icon="🤖", 
    layout="wide", 
    initial_sidebar_state="collapsed" # Normal users ke liye sidebar band rahega
)

# Premium Minimalist ChatGPT/Copilot Style Theme
st.markdown("""
    <style>
    /* Main Background & Text Color */
    .stApp { background-color: #ffffff; color: #111827; }
    
    /* Elegant Clean Header */
    .header-container {
        text-align: center;
        padding: 30px 0px 10px 0px;
        border-bottom: 1px solid #f3f4f6;
        margin-bottom: 30px;
    }
    .header-title { font-size: 32px; font-weight: 700; color: #111827; font-family: sans-serif; }
    .header-subtitle { font-size: 15px; color: #6b7280; margin-top: 5px; }
    
    /* Chat Bubbles Layout */
    .chat-bubble-user {
        background-color: #f3f4f6; padding: 14px 20px; border-radius: 20px 20px 4px 20px;
        margin: 12px 0px; max-width: 75%; float: right; clear: both;
        color: #1f2937; font-family: sans-serif; font-size: 15px;
    }
    .chat-bubble-ai {
        background-color: #f8fafc; border-left: 4px solid #2563eb; padding: 14px 20px; 
        border-radius: 20px 20px 20px 4px; margin: 12px 0px; max-width: 85%; float: left; clear: both;
        color: #0f172a; font-family: sans-serif; font-size: 15px; line-height: 1.6;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    div[data-testid="stSidebar"] { background-color: #f9fafb !important; border-right: 1px solid #e5e7eb; }
    </style>
""", unsafe_allow_html=True)

# Secure API Key Link
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing GEMINI_API_KEY inside Streamlit Advanced Secrets!")
    st.stop()

# --- MAIN INTERFACE: CLEAN TOP BAR & CHAT ---
st.markdown("""
    <div class="header-container">
        <div class="header-title">🤖 KAZIM AI</div>
        <div class="header-subtitle">Enterprise Industrial Automation Assistant — Serac Intelligence Systems</div>
    </div>
""", unsafe_allow_html=True)

# Persistent Session Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Live Matrix Machine Selection (HMI Dashboard Style Top Selectors)
col1, col2 = st.columns(2)
with col1:
    selected_line = st.selectbox("🏭 Target Production Line:", [f"Line {i}" for i in range(1, 21)])
with col2:
    selected_machine = st.selectbox("⚙️ Selected Machine Unit:", [f"M{i} Filler Unit" for i in range(1, 21)])

# Create a clean machine file identity string (e.g., database_Line1_M2.txt)
machine_id = f"database_{selected_line.replace(' ', '')}_{selected_machine.replace(' ', '')}.txt"

# Display Chat History
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-bubble-user"><b>You:</b><br>{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble-ai"><b>KAZIM AI:</b><br>{message["content"]}</div>', unsafe_allow_html=True)

st.markdown("<div style='clear: both;'></div>", unsafe_allow_html=True)

# Chat Input & Image Upload Components
st.write("---")
attached_img = st.file_uploader("📸 Upload Component/HMI Screen Screenshot (Optional):", type=["jpg", "jpeg", "png"])
user_prompt = st.chat_input("Ask KAZIM AI about sequences, timers, calibration, or faults...")

if user_prompt:
    # Append User Input
    st.markdown(f'<div class="chat-bubble-user"><b>You:</b><br>{user_prompt}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    # Smart Data Loader: Load data ONLY for the selected machine matrix
    context_data = ""
    if os.path.exists(machine_id):
        with open(machine_id, "r", encoding="utf-8") as f_read:
            context_data = f_read.read()
    else:
        context_data = "No custom training manual loaded for this machine yet. Operating on standard industrial automation protocols."

    # Prompt Engineering Payload
    final_system_prompt = (
        f"You are the world's most advanced AI Automation Engineer specialized in Serac Filling Systems.\n"
        f"You are strictly troubleshooting {selected_machine} on {selected_line}.\n"
        f"Base your analysis strictly on this locked technical manual context:\n{context_data}\n\n"
        f"Operator Query: {user_prompt}\n\n"
        "Provide an elite, professional breakdown. Use clear bold numbers and steps for technician tasks."
    )
    
    # Execute Stream Generation (Typing Effect)
    with st.spinner("Analyzing signals..."):
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            if attached_img:
                img_open = Image.open(attached_img)
                response = model.generate_content([final_system_prompt, img_open])
            else:
                response = model.generate_content(final_system_prompt)
            
            # Simulated Streaming for World-Class UI Experience
            ai_response_text = response.text
            message_placeholder = st.empty()
            full_displayed_text = ""
            
            # Words chunk streaming
            for word in ai_response_text.split(" "):
                full_displayed_text += word + " "
                message_placeholder.markdown(f'<div class="chat-bubble-ai"><b>KAZIM AI:</b><br>{full_displayed_text}▌</div>', unsafe_allow_html=True)
                time.sleep(0.04) # Smooth typing delay
                
            message_placeholder.markdown(f'<div class="chat-bubble-ai"><b>KAZIM AI:</b><br>{full_displayed_text}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": ai_response_text})
            st.rerun()
            
        except Exception as system_err:
            st.error(f"Execution Error: {str(system_err)}")


# --- BEHIND THE SCENES: SECRET ADMIN PANEL ---
with st.sidebar:
    st.markdown("<h3 style='color: #4b5563;'>🔒 System Control</h3>", unsafe_allow_html=True)
    
    # Secret Password Gate
    admin_password = st.text_input("Enter Secret Admin Password:", type="password")
    
    # Kazim Bhai's Master Password Gate
    if admin_password == "Kazim@2026":
        st.markdown("<div style='background-color:#ecfdf5; padding:10px; border-radius:5px; color:#065f46; font-weight:bold; font-size:12px; margin-bottom:15px;'>🔓 ADMIN ACCESS GRANTED</div>", unsafe_allow_html=True)
        st.markdown(f"**Target System:** Key mapping to `{machine_id}`")
        
        # Check if current selected machine has data
        db_exists = os.path.exists(machine_id)
        if db_exists:
            st.warning(f"⚠️ Warning: Old data found for {selected_machine} ({selected_line}).")
            write_mode = st.radio("Choose Action Mode:", ["Add/Append Data (Don't Erase)", "Overwrite (Completely Erase Old Data)"])
        else:
            st.success("🆕 Database is empty. Ready for initial lock.")
            write_mode = "Overwrite (Completely Erase Old Data)"
            
        # File Uploader stage
        new_manuals = st.file_uploader("Upload New Reference Materials (.txt):", type=["txt"], accept_multiple_files=True)
        
        if st.button("🚀 Process & Lock Machine Data"):
            if new_manuals:
                combined_uploaded_text = ""
                for f in new_manuals:
                    combined_uploaded_text += f.read().decode("utf-8", errors="ignore") + "\n"
                
                # Apply Add vs Delete logic based on selection
                file_open_flag = "w" if "Overwrite" in write_mode else "a"
                
                with open(machine_id, file_open_flag, encoding="utf-8") as f_target:
                    f_target.write(combined_uploaded_text)
                    
                st.success(f"Successfully secured data into {machine_id} matrix!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Meharbani karke pehle training file select karein!")
                
        # Independent Manual Erase Button
        if db_exists:
            if st.button("🗑️ Permanently Delete This Unit's Database"):
                os.remove(machine_id)
                st.success("Database erased from server!")
                time.sleep(1)
                st.rerun()
                
    elif admin_password != "":
        st.error("Incorrect Password! Access Denied.")
