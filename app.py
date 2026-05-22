import streamlit as st
import os
import time
import google.generativeai as genai
from PIL import Image

# --- MODERN INTERFACE CONFIG ---
st.set_page_config(page_title="KAZIM AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    /* Gemini-style Clean Interface */
    .stApp { background-color: #ffffff; }
    
    /* Styling chat input box to look like Gemini */
    .stChatInput { background-color: #f1f3f4; border-radius: 30px; }
    
    /* Elegant Chat Bubbles */
    .chat-bubble-ai { background-color: #f8f9fa; padding: 20px; border-radius: 15px; margin: 10px 0; border-left: 5px solid #4285f4; }
    .chat-bubble-user { background-color: #e8f0fe; padding: 15px; border-radius: 15px; margin: 10px 0; text-align: right; }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] { background-color: #f8f9fa; }
    </style>
""", unsafe_allow_html=True)

# API Setup
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🤖 KAZIM AI")
st.subheader("Serac Intelligence Matrix")

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- CHAT DISPLAY (The Gemini Way) ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INPUT AREA (The Expandable way) ---
if prompt := st.chat_input("Type hardware code or symptom (e.g., Profibus fault)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- IMAGE UPLOAD LOGIC ---
    uploaded_file = st.sidebar.file_uploader("Upload Diagnostic Image", type=["png", "jpg"])

    # Engine Logic
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Load context (Your M18 database)
        context = ""
        if os.path.exists("database_Line1_M1FillerUnit.txt"):
            with open("database_Line1_M1FillerUnit.txt", "r", encoding="utf-8") as f:
                context = f.read()

        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Combined Prompt
        final_prompt = f"Context: {context}\n\nUser Question: {prompt}\n\nRole: Act as a Sr. Engineer. If you don't know, ask for a photo."
        
        if uploaded_file:
            img = Image.open(uploaded_file)
            response = model.generate_content([final_prompt, img])
        else:
            response = model.generate_content(final_prompt)

        # Smooth Typing Effect
        for word in response.text.split():
            full_response += word + " "
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.02)
        message_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
