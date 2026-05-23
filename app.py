import streamlit as st
from groq import Groq

# 1. Yahan apni API key seedhi paste karein
MY_API_KEY = "gsk_..." 

# 2. Page Setup
st.set_page_config(page_title="M18 Expert", layout="centered")

# 3. Client Setup
client = Groq(api_key=MY_API_KEY)

# 4. Data Management (File Upload)
machine_id = "m18_logs.txt"
with st.sidebar.expander("🔐 Admin Access"):
    if st.text_input("Password:", type="password") == "Kazim@2026":
        uploaded_file = st.file_uploader("Upload logs:")
        if st.button("Commit") and uploaded_file:
            with open(machine_id, "wb") as f: f.write(uploaded_file.getbuffer())
            st.success("Data Saved!")

# 5. Chat Logic
st.title("KAZIM AI - M18 Expert")

if "messages" not in st.session_state: st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Fault code ya symptom likhein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    # Read context
    try:
        context = open(machine_id, "r").read()
    except:
        context = "No manual uploaded."

    with st.chat_message("assistant"):
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
