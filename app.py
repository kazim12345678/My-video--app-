import streamlit as st
import pandas as pd
import PyPDF2
import google.generativeai as genai
import numpy as np
import faiss
import pickle
import os

# --- ENTERPRISE THEME CONFIGURATION ---
st.set_page_config(
    page_title="KAZIM AI Assistant", 
    page_icon="⚙️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom Attractive CSS Injection for Dark Modern Industrial Look
st.markdown("""
    <style>
    .main { background-color: #0f1116; color: #e1e4ea; }
    .stButton>button {
        background-color: #1f2430 !important; color: #00ffcc !important;
        border: 1px solid #00ffcc !important; border-radius: 8px !important;
        padding: 0.5em 2em !important; font-weight: bold !important;
    }
    .stButton>button:hover { background-color: #00ffcc !important; color: #1f2430 !important; }
    .stTextInput>div>div>input { background-color: #1a1d24 !important; color: #ffffff !important; border: 1px solid #3a3f50 !important; }
    .stSelectbox>div>div>div { background-color: #1a1d24 !important; color: #ffffff !important; }
    div[data-testid="stExpander"] { background-color: #161920 !important; border: 1px solid #282c37 !important; border-radius: 8px !important; }
    .success-card { background-color: #1c2d27; border-left: 5px solid #00cc88; padding: 15px; border-radius: 6px; margin: 10px 0px; }
    .header-panel { background: linear-gradient(90deg, #1f2430 0%, #0d1117 100%); padding: 20px; border-radius: 10px; border-bottom: 2px solid #00ffcc; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

# Secure API Key Link
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing GEMINI_API_KEY inside your local '.streamlit/secrets.toml' file!")
    st.stop()

# Local Storage Database Paths
INDEX_FILE = "kazim_knowledge_index.bin"
TEXT_FILE = "kazim_knowledge_text.pkl"
FEEDBACK_FILE = "kazim_repair_ledger.csv"

# Build empty historical rating ledger locally if missing
if not os.path.exists(FEEDBACK_FILE):
    pd.DataFrame(columns=["Symptom", "AI_Solution", "Stars"]).to_csv(FEEDBACK_FILE, index=False)

# --- HEADER TITLE BANNER ---
st.markdown("""
    <div class="header-panel">
        <h1 style='margin:0; color:#00ffcc; font-family:sans-serif;'>🛠️ KAZIM AI Assistant Console</h1>
        <p style='margin:5px 0 0 0; color:#8b949e; font-size:14px;'>Self-Learning Dynamic Diagnostics • Local Workstation Secure Sandbox</p>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROL PANEL: KNOWLEDGE VAULT ---
with st.sidebar:
    st.markdown("<h2 style='color:#00ffcc; margin-bottom:0;'>📁 Knowledge Vault</h2>", unsafe_allow_html=True)
    st.write("Train or update your assistant's permanent memory files.")
    st.write("---")
    
    is_trained = os.path.exists(INDEX_FILE) and os.path.exists(TEXT_FILE)
    
    if is_trained:
        st.markdown('<div class="success-card"><b style="color:#00cc88;">🟢 SYSTEM ONLINE</b><br><span style="color:#a3b3a7; font-size:12px;">Local Knowledge Loaded</span></div>', unsafe_allow_html=True)
        force_rebuild = st.checkbox("🔄 Sync/Upload New Manuals?")
        if force_rebuild:
            is_trained = False
            
    if not is_trained:
        st.markdown("<b style='color:#ff5555;'>🔴 DATABASE STATUS: EMPTY</b>", unsafe_allow_html=True)
        uploaded_docs = st.file_uploader(
            "Drop the M1 Cheat Sheet Text or Machine Manual PDFs here:", 
            type=["txt", "pdf", "xlsx", "csv"], 
            accept_multiple_files=True
        )
        
        if st.button("🚀 Process & Lock Data Locally"):
            if uploaded_docs:
                chunks = []
                with st.spinner("Extracting engineering frameworks to local hard drive..."):
                    for f in uploaded_docs:
                        if f.name.endswith(".txt"):
                            raw_text = f.read().decode("utf-8")
                            # Cut the raw text file into clear paragraphs
                            paragraphs = raw_text.split("\n\n")
                            for p in paragraphs:
                                if p.strip():
                                    chunks.append(f"[Document Segment: {f.name}]\n{p.strip()}")
                        elif f.name.endswith(".pdf"):
                            reader = PyPDF2.PdfReader(f)
                            for page_num, page in enumerate(reader.pages):
                                t = page.extract_text()
                                if t: chunks.append(f"[Manual: {f.name} | Page: {page_num+1}]\n{t}")
                        elif f.name.endswith((".xlsx", ".xls", ".csv")):
                            df = pd.read_csv(f) if f.name.endswith(".csv") else pd.read_excel(f)
                            for idx, row in df.iterrows():
                                chunks.append(f"[Log: {f.name} | Row: {idx}]\n" + ", ".join([f"{c}: {v}" for c, v in row.items()]))
                    
                    # Convert texts to mathematical vector coordinates via Gemini
                    embed_payload = genai.embed_content(model="models/text-embedding-004", content=chunks, task_type="retrieval_document")
                    embeddings = np.array(embed_payload['embedding']).astype('float32')
                    
                    # Store indexed vectors and mappings locally
                    index = faiss.IndexFlatL2(embeddings.shape[1])
                    index.add(embeddings)
                    faiss.write_index(index, INDEX_FILE)
                    
                    with open(TEXT_FILE, "wb") as f_out:
                        pickle.dump(chunks, f_out)
                        
                st.success("Knowledge library locked to hard drive successfully!")
                st.rerun()

# --- MAIN FLOOR INTERFACE: RUNTIME CONTROL RADAR ---
st.markdown("<h3 style='color:#ffffff; margin-top:0;'>🔧 Live Field Diagnostic Configuration</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    line_selection = st.selectbox("Production Line Matrix:", [f"Line {i}" for i in range(1, 21)])
with col2:
    machine_selection = st.selectbox("Machine Identifier Classification:", ["M1 Filler", "Capper Unit", "Labeling Network", "Palletizer Assembly"])
with col3:
    user_query = st.text_input("Enter component error tag, fault code, or symptom profile:", placeholder="e.g., Pilz module red fault light / wire 84C2 lacks power")

# Cache states across asynchronous event loops for ratings
if "solution_cache" not in st.session_state:
    st.session_state.solution_cache = None
if "query_cache" not in st.session_state:
    st.session_state.query_cache = None

if st.button("⚡ Run KAZIM Diagnostic Engine") and user_query:
    if not (os.path.exists(INDEX_FILE) and os.path.exists(TEXT_FILE)):
        st.error("Your local knowledge vault is empty! Drop your files in the sidebar and process them first.")
    else:
        with st.spinner("Scanning internal blueprints and human feedback loops..."):
            # Load private documents 
            index = faiss.read_index(INDEX_FILE)
            with open(TEXT_FILE, "rb") as f_in:
                all_chunks = pickle.load(f_in)
            
            # Read star logs from local drive
            repair_history = ""
            if os.path.exists(FEEDBACK_FILE):
                ledger_df = pd.read_csv(FEEDBACK_FILE)
                if not ledger_df.empty:
                    repair_history = "\n[PAST TECHNICIAN STAR RATINGS LOG]:\n" + ledger_df.tail(15).to_string()

            # Execute context matrix search
            search_terms = f"{line_selection} {machine_selection} {user_query}"
            query_vector = np.array(genai.embed_content(
                model="models/text-embedding-004", 
                content=search_terms, 
                task_type="retrieval_query"
            )['embedding']).astype('float32').reshape(1, -1)
            
            _, indices = index.search(query_vector, 4)
            matched_context = ""
            
            st.markdown("<h5 style='color:#00ffcc;'>📑 Extracted Structural Layout Blueprints Found:</h5>", unsafe_allow_html=True)
            for idx in indices[0]:
                if idx < len(all_chunks):
                    matched_context += f"\n---\n{all_chunks[idx]}\n"
                    st.caption(f"📍 {all_chunks[idx].splitlines()[0]}")
            
            # Construct instruction prompt blending global AI with the local file
            engineered_prompt = (
                "You are an Elite Industrial Automation Engineer operating the KAZIM Factory Diagnostic System.\n"
                "Your objective is to solve a machinery problem using the provided manual clippings and real historical feedback data.\n\n"
                "CRITICAL LOGIC OVERRIDE:\n"
                "Examine the 'PAST TECHNICIAN STAR RATINGS LOG'. If a solution was awarded high ratings (4-5 stars), emphasize it prominently as the key path forward. "
                "If an approach was awarded 1 star, it was verified by a live field tech as completely wrong or counterproductive—do NOT suggest it. Change your technical path immediately.\n\n"
                f"--- PRIVATE BLUEPRINT MANUAL CLIPPINGS ---\n{matched_context}\n"
                f"--- FACTORY FIELD EXPERIENCE LEDGER ---\n{repair_history}\n\n"
                f"CURRENT BREAKDOWN SPECIFICATION: Machine {machine_selection} on {line_selection}\n"
                f"OPERATOR REPORTED SYMPTOM: {user_query}\n\n"
                "Provide a direct root-cause breakdown explaining the system context, followed immediately by a tactical, prioritized numbers-only field check list."
            )
            
            # Call Gemini
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(engineered_prompt)
            
            st.session_state.solution_cache = response.text
            st.session_state.query_cache = user_query

# Present solutions and activate human feedback recording loops
if st.session_state.solution_cache:
    st.markdown("<h3 style='color:#00ffcc; margin-top:20px;'>🤖 Actionable Field Repair Briefing:</h3>", unsafe_allow_html=True)
    st.info(st.session_state.solution_cache)
    
    st.write("---")
    st.markdown("<h4 style='color:#ffffff;'>📝 Rate this solution to train KAZIM Memory Log:</h4>", unsafe_allow_html=True)
    
    # Render Star Feedback widget
    rating = st.feedback("stars", key="kazim_feedback_stars")
    
    if rating is not None:
        actual_stars = rating + 1
        
        # Append rating straight down to your local hard drive file
        feedback_entry = pd.DataFrame([{
            "Symptom": st.session_state.query_cache,
            "AI_Solution": st.session_state.solution_cache.replace("\n", " "),
            "Stars": actual_stars
        }])
        feedback_entry.to_csv(FEEDBACK_FILE, mode='a', header=False, index=False)
        
        st.success(f"Log appended! System memory grew more mature with a {actual_stars}-star resolution record.")
        st.session_state.solution_cache = None
        st.session_state.query_cache = None
