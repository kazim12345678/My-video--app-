import streamlit as st
from groq import Groq
import json
import os
import tempfile
import re
import io
from datetime import datetime
import shutil

# File parsing libraries - ensure these are installed:
# pip install PyPDF2 python-docx
try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None

try:
    from docx import Document
except Exception:
    Document = None

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="KAZIM AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# MEMORY AND FILE STORAGE
# =========================================================

MEMORY_FILE = "memory.json"
MEMORY_FOLDER = "memories"  # stores original uploaded files per machine

os.makedirs(MEMORY_FOLDER, exist_ok=True)

# LOAD MEMORY
if os.path.exists(MEMORY_FILE):
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            knowledge_data = json.load(f)
    except Exception:
        knowledge_data = {}
else:
    knowledge_data = {}

# ATOMIC SAVE MEMORY FUNCTION
def save_memory():
    tmp_fd, tmp_path = tempfile.mkstemp()
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
            json.dump(st.session_state.knowledge_base, f, indent=4, ensure_ascii=False)
        os.replace(tmp_path, MEMORY_FILE)
    except Exception:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
        raise

# =========================================================
# UTIL: parse uploaded files to extract text
# =========================================================

def extract_text_from_bytes(file_bytes: bytes, filename: str) -> str:
    name = filename.lower()
    if name.endswith(".txt"):
        try:
            return file_bytes.decode("utf-8-sig")
        except Exception:
            return file_bytes.decode("latin-1", errors="ignore")
    elif name.endswith(".pdf"):
        if PdfReader is None:
            raise RuntimeError("PyPDF2 is not installed (required for PDF parsing).")
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            text_parts = []
            for page in reader.pages:
                try:
                    ptext = page.extract_text()
                except Exception:
                    ptext = None
                if ptext:
                    text_parts.append(ptext)
            return "\n\n".join(text_parts)
        except Exception as e:
            raise RuntimeError(f"PDF parsing failed: {str(e)}")
    elif name.endswith(".docx"):
        if Document is None:
            raise RuntimeError("python-docx is not installed (required for DOCX parsing).")
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmpf:
                tmpf.write(file_bytes)
                tmpf.flush()
                tmpname = tmpf.name
            doc = Document(tmpname)
            paragraphs = [p.text for p in doc.paragraphs if p.text and p.text.strip()]
            try:
                os.remove(tmpname)
            except Exception:
                pass
            return "\n\n".join(paragraphs)
        except Exception as e:
            raise RuntimeError(f"DOCX parsing failed: {str(e)}")
    else:
        raise RuntimeError("Unsupported file type. Use .txt, .pdf or .docx")

# =========================================================
# SIMPLE RETRIEVAL: relevant memories only
# =========================================================

def retrieve_relevant_memories(query: str, knowledge_base: dict, top_n: int = 5, max_chars: int = 3000):
    """
    Very simple keyword-based retrieval.
    Returns concatenated memory string and list of used keys.
    """
    q = (query or "").lower()
    keywords = [w for w in re.findall(r"\w+", q) if len(w) > 2]
    if not keywords:
        return "", []

    scores = []
    for key, text in knowledge_base.items():
        t = (text or "").lower()
        score = sum(t.count(k) for k in keywords)
        if score > 0:
            scores.append((score, key, text))

    scores.sort(reverse=True, key=lambda x: x[0])

    chosen = scores[:top_n]
    combined = ""
    used_keys = []
    for _, key, text in chosen:
        snippet = f"\n\n### MEMORY: {key}\n{text.strip()}"
        if len(combined) + len(snippet) > max_chars:
            break
        combined += snippet
        used_keys.append(key)

    return combined, used_keys

# =========================================================
# UTILS: machine detection from prompt
# =========================================================

def detect_machines_in_prompt(prompt: str, lines_range=range(1, 21), machines_range=range(1, 19)):
    """
    Detect machine references in the user prompt.
    Looks for patterns like 'M1', 'm1', 'machine 1', 'line 3 m2', 'Line 18 M3' etc.
    Returns list of memory_keys detected (e.g., 'Line 18_M3').
    If none found returns empty list.
    """
    found = set()
    p = (prompt or "").lower()

    # detect explicit machine tokens like m1..m18
    for m in machines_range:
        token = f"m{m}".lower()
        if re.search(rf"\b{re.escape(token)}\b", p):
            # find nearby line mention if present
            line_match = re.search(r"line\s*(\d{1,2})", p)
            if line_match:
                line = int(line_match.group(1))
            else:
                # if no line mentioned, try default line 1 or look for "line X_M# keys in knowledge base"
                line = None
            if line:
                key = f"Line {line}_M{m}"
                found.add(key)
            else:
                # if we don't have line, match any keys ending with _M{m}
                for k in st.session_state.knowledge_base.keys():
                    if re.search(rf"_m{m}$", k.lower()):
                        found.add(k)
    # detect direct keys like 'line 18' with a machine mention M# somewhere
    # (Already covered above)
    return list(found)

# =========================================================
# CSS (same as before)
# =========================================================

st.markdown("""
<style>

/* MAIN */
.stApp{
    background:#F3F4F6;
}

/* HIDE STREAMLIT */
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

/* PAGE */
.block-container{
    padding-top:1rem;
    padding-bottom:120px;
    max-width:1400px;
}

/* TITLE */
.kazim-title{
    text-align:center;
    font-size:72px;
    font-weight:900;
    margin-top:20px;
    margin-bottom:0px;
    background: linear-gradient(90deg,#1D4ED8,#3B82F6);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.kazim-sub{
    text-align:center;
    color:#6B7280;
    font-size:18px;
    margin-bottom:40px;
}

/* CHAT */
div[data-testid="stChatMessage"]{
    background:white;
    border-radius:18px;
    padding:14px;
    margin-bottom:10px;
    color:#111827 !important;
}

/* FORCE TEXT */
div[data-testid="stChatMessage"] *{
    color:#111827 !important;
    opacity:1 !important;
}

/* CHAT INPUT */
div[data-testid="stChatInput"]{
    position:fixed !important;
    bottom:18px !important;
    left:50% !important;
    transform:translateX(-50%) !important;
    width:70vw !important;
    max-width:1100px !important;
    z-index:999999 !important;
}

/* INPUT BOX */
div[data-testid="stChatInput"] > div{
    background:white !important;
    border-radius:35px !important;
    border:1px solid #D1D5DB !important;
    padding:12px 18px !important;
    box-shadow:0 4px 18px rgba(0,0,0,0.08);
}

/* INPUT TEXT */
div[data-testid="stChatInput"] textarea{
    color:#111827 !important;
    background:white !important;
    opacity:1 !important;
    font-size:18px !important;
}

/* MOBILE */
@media (max-width: 768px){

    .kazim-title{
        font-size:48px !important;
    }

    .kazim-sub{
        font-size:16px !important;
    }

    div[data-testid="stChatInput"]{
        width:95vw !important;
        bottom:10px !important;
    }

    div[data-testid="stChatInput"] textarea{
        font-size:16px !important;
    }

}

/* ADMIN BOX */
.admin-box{
    background:white;
    padding:20px;
    border-radius:18px;
    border:1px solid #E5E7EB;
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATES
# =========================================================

if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = knowledge_data

if "messages" not in st.session_state:
    st.session_state.messages = []

if "admin_open" not in st.session_state:
    st.session_state.admin_open = False

if "admin_ok" not in st.session_state:
    st.session_state.admin_ok = False

# =========================================================
# TOP ADMIN BUTTON
# =========================================================

top1, top2, top3 = st.columns([1,2,1])

with top1:
    if st.button("⚙ Admin Access"):
        st.session_state.admin_open = not st.session_state.admin_open

# =========================================================
# ADMIN PANEL (TRAIN / UPLOAD PER MACHINE)
# =========================================================

if st.session_state.admin_open:
    st.markdown('<div class="admin-box">', unsafe_allow_html=True)

    password = st.text_input(
        "Enter Password",
        type="password"
    )

    if st.button("Login"):
        if "ADMIN_PASSWORD" in st.secrets and password == st.secrets["ADMIN_PASSWORD"]:
            st.session_state.admin_ok = True
            st.success("Admin Access Granted")
        else:
            st.error("Wrong Password or ADMIN_PASSWORD missing in secrets")

    if st.session_state.admin_ok:
        st.markdown("### Machine Memory Manager (Upload / Train / Delete)")

        # Choose line and machine (18 machines)
        selected_line = st.selectbox(
            "Select Line (if not relevant choose Line 1)",
            [f"Line {i}" for i in range(1, 21)]
        )

        # 18 machine options
        machines = [f"M{i}" for i in range(1, 19)]
        selected_machine = st.selectbox("Select Machine", machines)

        memory_key = f"{selected_line}_{selected_machine}"

        st.markdown(f"Selected memory key: **{memory_key}**")

        # Show existing memory preview if present
        if memory_key in st.session_state.knowledge_base:
            st.markdown("**Current stored memory (preview):**")
            st.code(st.session_state.knowledge_base[memory_key][:1000] + ("..." if len(st.session_state.knowledge_base[memory_key]) > 1000 else ""))
        else:
            st.info("No memory stored yet for this machine.")

        # File uploader for txt/pdf/docx
        uploaded_file = st.file_uploader(
            "Upload TXT / PDF / DOCX file (technical manual, notes).",
            type=["txt", "pdf", "docx"],
            accept_multiple_files=False
        )

        action = st.radio(
            "Select Action",
            ["Add (append)", "Override", "Delete memory", "List files", "Download files"]
        )

        if action == "Delete memory":
            if st.button("Delete Memory for Selected Machine"):
                # delete memory key and folder
                if memory_key in st.session_state.knowledge_base:
                    del st.session_state.knowledge_base[memory_key]
                    save_memory()
                # delete files
                folder = os.path.join(MEMORY_FOLDER, memory_key.replace(" ", "_"))
                if os.path.exists(folder):
                    try:
                        shutil.rmtree(folder)
                    except Exception:
                        pass
                st.success(f"Memory and files deleted for {memory_key}")
                st.rerun()

        elif action == "List files":
            folder = os.path.join(MEMORY_FOLDER, memory_key.replace(" ", "_"))
            if os.path.exists(folder):
                st.markdown("Files stored for this machine:")
                for fn in os.listdir(folder):
                    st.write("-", fn)
            else:
                st.info("No files stored for this machine yet.")

        elif action == "Download files":
            folder = os.path.join(MEMORY_FOLDER, memory_key.replace(" ", "_"))
            if os.path.exists(folder):
                files = os.listdir(folder)
                sel = st.selectbox("Select file to download", ["-- choose --"] + files)
                if sel and sel != "-- choose --":
                    path = os.path.join(folder, sel)
                    with open(path, "rb") as f:
                        data = f.read()
                    st.download_button(label=f"Download {sel}", data=data, file_name=sel)
            else:
                st.info("No files stored for this machine yet.")

        else:
            # Add or Override (requires uploaded_file)
            if st.button("Process Upload"):

                if uploaded_file is None:
                    st.warning("Please choose a file to upload first.")
                else:
                    file_bytes = uploaded_file.read()
                    filename = uploaded_file.name
                    try:
                        extracted = extract_text_from_bytes(file_bytes, filename)
                    except Exception as e:
                        st.error(f"Failed to parse file: {str(e)}")
                        extracted = None

                    if extracted is not None:
                        extracted = extracted.strip()

                        # Save original file into memories/<memory_key>/
                        folder = os.path.join(MEMORY_FOLDER, memory_key.replace(" ", "_"))
                        os.makedirs(folder, exist_ok=True)
                        # make a timestamped filename to avoid overwriting
                        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
                        save_name = f"{ts}_{filename}"
                        save_path = os.path.join(folder, save_name)
                        with open(save_path, "wb") as f:
                            f.write(file_bytes)

                        old_data = st.session_state.knowledge_base.get(memory_key, "").strip()

                        if action == "Add (append)":
                            if old_data:
                                st.session_state.knowledge_base[memory_key] = old_data + "\n\n" + extracted
                            else:
                                st.session_state.knowledge_base[memory_key] = extracted
                            save_memory()
                            st.success(f"Appended data to {memory_key} and saved file {save_name}")

                        elif action == "Override":
                            st.session_state.knowledge_base[memory_key] = extracted
                            save_memory()
                            st.success(f"Overrode memory for {memory_key} and saved file {save_name}")

        st.markdown("---")
        st.markdown("### All stored memories (keys)")
        if st.session_state.knowledge_base:
            for k in st.session_state.knowledge_base.keys():
                st.write("✅", k)
        else:
            st.info("No memories saved yet.")

        # clear chat and logout options
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

        if st.button("Logout"):
            st.session_state.admin_ok = False
            st.session_state.admin_open = False
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================

st.markdown('<div class="kazim-title">KAZIM AI</div>', unsafe_allow_html=True)
st.markdown('<div class="kazim-sub">Industrial AI Diagnostic Assistant</div>', unsafe_allow_html=True)

# =========================================================
# API CHECK
# =========================================================

if "GROQ_API_KEY" not in st.secrets:
    st.error("Missing GROQ API KEY in Streamlit secrets")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# =========================================================
# SHOW CHAT
# =========================================================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================================================
# CHAT INPUT
# =========================================================

prompt = st.chat_input("Ask fault code, PLC issue, alarm, breakdown or technical query...")

# =========================================================
# AI RESPONSE WITH MACHINE ROUTING
# =========================================================

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Try to detect machine(s) in prompt
    detected_keys = detect_machines_in_prompt(prompt)
    all_memory = ""
    used_keys = []

    if detected_keys:
        # Use detected keys (exact)
        for key in detected_keys:
            if key in st.session_state.knowledge_base:
                all_memory += f"\n\n### MEMORY: {key}\n{st.session_state.knowledge_base[key].strip()}"
                used_keys.append(key)
        if not all_memory:
            # none of detected keys have stored memory
            st.info("Mentioned machine found but no memory stored for it yet.")
    else:
        # No explicit machine mention: fall back to simple retrieval across all memories
        all_memory, used_keys = retrieve_relevant_memories(prompt, st.session_state.knowledge_base)

    if not all_memory:
        st.info("No related technical memory matched your query. The assistant will only answer if memory exists as per rules.")

    system_prompt = f"""
You are KAZIM AI.

You are industrial technical AI.

IMPORTANT RULES:
- Use ONLY uploaded memory.
- NEVER create fake machine information.
- NEVER guess specifications.
- If memory not available say:
"No related technical data found."

Technical Memory:
{all_memory}
"""

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1200
            )

            ai_reply = ""
            try:
                ai_reply = response.choices[0].message.content
            except Exception:
                ai_reply = getattr(response, "text", "No response content")

        except Exception as e:
            ai_reply = f"Error: {str(e)}"

        # append citation of used keys so user knows which memory was consulted
        if used_keys:
            citation_text = "\n\nSources used:\n" + "\n".join(f"- {k}" for k in used_keys)
            ai_reply = ai_reply + citation_text

        st.markdown(ai_reply)

    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
