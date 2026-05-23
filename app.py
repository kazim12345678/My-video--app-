import streamlit as st
from groq import Groq

# --- Page Config ---
st.set_page_config(page_title="KAZIM AI - M18 Expert", layout="centered", page_icon="🤖")

# --- Groq Client ---
# Yeh line aapke Streamlit Secrets box se key utha rahi hai
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- Sidebar: M18 Matrix ---
st.sidebar.markdown("### ⚙️ M18 Diagnostic Console")
line = st.sidebar.selectbox("Select Line:", [f"Line {i}" for i in range(1, 21)])
machine = st.sidebar.selectbox("Select Node:", [f"M{i} Unit" for i in range(1, 21)])
machine_id = f"db_{line.replace(' ', '')}_{machine.replace(' ', '')}.txt"

# --- Data Management ---
with st.sidebar.expander("🔐 Data Management"):
    pwd = st.text_input("Admin Password:", type="password")
    if pwd == "Kazim@2026":
        uploaded_file = st.file_uploader("Upload logs:", accept_multiple_files=False)
        if st.button("🚀 Commit"):
            if uploaded_file:
                content = uploaded_file.read().decode("utf-8", errors="ignore")
                with open(machine_id, "w", encoding="utf-8") as f:
                    f.write(content)
                st.success("Data Saved Successfully!")
            else:
                st.warning("Please upload a file.")

# --- Main Interface ---
st.title("KAZIM AI - M18 Expert")
st.info(f"Targeting: **{line} | {machine}**")

# Session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Enter fault code or symptom..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Load context
    try:
        with open(machine_id, "r", encoding="utf-8") as f:
            context = f.read()
    except:
        context = "No manual data found for this node."

    # Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing M18 logs..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": f"You are a Senior Automation Engineer. Use this log context to diagnose issues: {context}"},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama3-8b-8192",
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                # Save assistant message
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Engine Error: {e}")
