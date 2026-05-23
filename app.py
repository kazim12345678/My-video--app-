import streamlit as st
import os
from groq import Groq

# --- CONFIG ---
st.set_page_config(page_title="KAZIM AI - M18 Diagnostic", layout="centered", page_icon="🤖")

# --- GROQ CLIENT ---
# Streamlit secrets se key utha raha hai
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- SIDEBAR ---
st.sidebar.markdown("### ⚙️ M18 Diagnostic Console")
line = st.sidebar.selectbox("Select Line:", [f"Line {i}" for i in range(1, 21)])
machine = st.sidebar.selectbox("Select Node:", [f"M{i} Unit" for i in range(1, 21)])
machine_id = f"db_{line.replace(' ', '')}_{machine.replace(' ', '')}.txt"

# --- DATA MANAGEMENT ---
with st.sidebar.expander("🔐 Data Management"):
    if st.text_input("Admin Password:", type="password") == "Kazim@2026":
        files = st.file_uploader("Upload logs:", accept_multiple_files=True)
        if st.button("🚀 Commit"):
            content = "".join([f.read().decode("utf-8", errors="ignore") for f in files])
            with open(machine_id, "w", encoding="utf-8") as f: f.write(content)
            st.success("Data Saved!")

# --- CHAT ENGINE ---
st.title("KAZIM AI - M18 Expert")
if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Fault code ya symptom likhein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        context = open(machine_id, "r").read() if os.path.exists(machine_id) else "Manual load nahi hua."
        
        # Groq API call
        chat = client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"Aap Senior Automation Engineer hain. Context: {context}"},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
        )
        response = chat.choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
