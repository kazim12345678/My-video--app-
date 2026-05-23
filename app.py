import streamlit as st
import os
from openai import OpenAI

# --- PAGE CONFIG ---
st.set_page_config(page_title="KAZIM AI - Industrial Core", layout="centered", page_icon="🤖")

# --- OPENAI SETUP ---
try:
    # Secrets se key le rahe hain
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
except Exception as e:
    st.error("API Key missing or invalid. Please check Streamlit Secrets.")
    st.stop()

# --- SIDEBAR: M18 MATRIX ---
st.sidebar.markdown("### ⚙️ M18 Diagnostic Console")
line = st.sidebar.selectbox("Select Line:", [f"Line {i}" for i in range(1, 21)])
machine = st.sidebar.selectbox("Select Node:", [f"M{i} Unit" for i in range(1, 21)])
machine_id = f"db_{line.replace(' ', '')}_{machine.replace(' ', '')}.txt"

with st.sidebar.expander("🔐 Data Management"):
    pwd = st.text_input("Admin Password:", type="password")
    if pwd == "Kazim@2026":
        files = st.file_uploader("Upload logs:", accept_multiple_files=True)
        if st.button("🚀 Commit"):
            if files:
                content = "".join([f.read().decode("utf-8", errors="ignore") for f in files])
                with open(machine_id, "w", encoding="utf-8") as f: f.write(content)
                st.success("Data Saved!")
            else:
                st.warning("Upload a file first.")

# --- MAIN INTERFACE ---
st.title("KAZIM AI - Industrial Core")
st.info(f"Target: **{line} | {machine}**")

if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Enter fault code or symptom..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        # Context loading
        context = open(machine_id, "r").read() if os.path.exists(machine_id) else "No manual data found."
        
        try:
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are a Senior Automation Engineer. Use this manual: {context}"},
                    {"role": "user", "content": prompt}
                ],
                stream=True
            )
            full_res = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_res += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_res + "▌")
            message_placeholder.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
        except Exception as e:
            st.error(f"Engine Error: {e}")
