import streamlit as st
import os
from groq import Groq

# --- CONFIG ---
st.set_page_config(page_title="M18 Diagnostic", layout="centered")

# --- GROQ CLIENT FIX ---
# Agar key nahi mili toh clear error dega
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("Secrets mein GROQ_API_KEY nahi mil rahi. Settings -> Secrets check karein.")
    st.stop()

# --- SIDEBAR ---
machine_id = "m18_logs.txt"
with st.sidebar.expander("🔐 Data Management"):
    if st.text_input("Password:", type="password") == "Kazim@2026":
        uploaded_file = st.file_uploader("Upload logs:")
        if st.button("Commit") and uploaded_file:
            with open(machine_id, "wb") as f: f.write(uploaded_file.getbuffer())
            st.success("Saved!")

# --- CHAT ---
st.title("KAZIM AI - M18 Expert")

if prompt := st.chat_input("Symptom likhein..."):
    with st.chat_message("user"): st.markdown(prompt)
    
    # Read logs
    context = open(machine_id, "r").read() if os.path.exists(machine_id) else "No data."
    
    with st.chat_message("assistant"):
        try:
            chat = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"Automation Engineer. Context: {context}"},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192",
            )
            response = chat.choices[0].message.content
            st.markdown(response)
        except Exception as e:
            st.error(f"Error: {e}")
