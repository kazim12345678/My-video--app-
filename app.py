import streamlit as st
import pandas as pd
import PyPDF2
import google.generativeai as genai
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
        width: 100% !important;
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
    st.error("Missing GEMINI_API_KEY inside your Streamlit Advanced Secrets!")
    st.stop()

# Database Paths on Streamlit Cloud Server
TEXT_FILE = "kazim_knowledge_text.txt"
FEEDBACK_FILE = "kazim_repair_ledger.csv"

# Build empty historical rating ledger locally if missing
if not os.path.exists(FEEDBACK_FILE):
    pd.DataFrame(columns=["Symptom", "AI_Solution", "Stars"]).to_csv(FEEDBACK_FILE, index=False)

# --- HEADER TITLE BANNER ---
st.markdown("""
    <div class="header-panel">
        <h1 style='margin:0; color:#00ffcc; font-family:sans-serif;'>🛠️ KAZIM AI Assistant Console</h1>
        <p style='margin:5px 0 0 0; color:#8b949e; font-size:14px;'>Self-Learning Dynamic Diagnostics • Production Floor Assistant</p>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROL PANEL: KNOWLEDGE VAULT ---
with st.sidebar:
    st.markdown("<h2 style='color:#00ffcc; margin-bottom:0;'>📁 Knowledge Vault</h2>", unsafe_allow_html=True)
    st.write("Train or update your assistant's permanent memory files.")
    st.write("---")
    
    is_trained = os.path.exists(TEXT_FILE)
    
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
                full_combined_text = ""
                with st.spinner("Processing technical text parameters..."):
                    for f in uploaded_docs:
                        if f.name.endswith(".txt"):
                            raw_text = f.read().decode("utf-8")
                            full_combined_text += f"\n[SOURCE FILE: {f.name}]\n" + raw_text
                        
                        elif f.name.endswith(".pdf"):
                            reader = PyPDF2.PdfReader(f)
                            for page_num, page in enumerate(reader.pages):
                                t = page.extract_text()
                                if t: 
                                    full_combined_text += f"\n[Manual: {f.name} | Page: {page_num+1}]\n{t}\n"
                        
                        elif f.name.endswith((".xlsx", ".xls", ".csv")):
                            df = pd.read_csv(f) if f.name.endswith(".csv") else pd.read_excel(f)
                            for idx, row in df.iterrows():
                                row_str = ", ".join([f"{c}: {v}" for c, v in row.items() if str(v).strip()])
                                if row_str.strip():
                                    full_combined_text += f"\n[Log: {f.name} | Row: {idx}] {row_str}\n"
                    
                    if not full_combined_text.strip():
                        st.error("No valid text found inside your files!")
                    else:
                        with open(TEXT_FILE, "w", encoding="utf-8") as f_out:
                            f_out.write(full_combined_text)
                            
                        st.success("Knowledge library built and locked in successfully!")
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
    if not os.path.exists(TEXT_FILE):
        st.error("Your knowledge vault is empty! Drop your files in the sidebar and process them first.")
    else:
        with st.spinner("Filtering layout lines and history logs..."):
            # Load stored documents line by line
            matched_lines = []
            keywords = user_query.lower().split()
            
            with open(TEXT_FILE, "r", encoding="utf-8") as f_in:
                for line in f_in:
                    # Smart Keyword Filtering: Find lines in your manual that match what the user typed
                    if any(word in line.lower() for word in keywords) or "specifications" in line.lower() or "directory" in line.lower():
                        matched_lines.append(line.strip())
            
            # Combine filtered lines (Max 100 lines to ensure it never crashes the API)
            filtered_manual_context = "\n".join(matched_lines[:100])
            
            if not filtered_manual_context.strip():
                filtered_manual_context = "No specific direct wiring lines found matching search terms. Use general system logic panels."

            # Read star logs from drive
            repair_history = ""
            if os.path.exists(FEEDBACK_FILE):
                ledger_df = pd.read_csv(FEEDBACK_FILE)
                if not ledger_df.empty:
                    repair_history = "\n[PAST TECHNICIAN STAR RATINGS LOG]:\n" + ledger_df.tail(15).to_string()

            # Construct structural instruction prompt for Gemini using FILTERED context
            engineered_prompt = (
                "You are an Elite Industrial Automation Engineer operating the KAZIM Factory Diagnostic System.\n"
                "Your objective is to solve a machinery problem using the provided manual blueprint context and historical field logs.\n\n"
                "CRITICAL LOGIC OVERRIDE:\n"
                "Examine the 'PAST TECHNICIAN STAR RATINGS LOG'. If a solution was awarded high ratings (4-5 stars), emphasize it prominently as the key path forward. "
                "If an approach was awarded 1 star, it was verified by a live field tech as completely wrong or counterproductive—do NOT suggest it. Change your technical path immediately.\n\n"
                f"--- TARGETED BLUEPRINT MANUAL SPECIFICATION LINES ---\n{filtered_manual_context}\n\n"
                f"--- FACTORY FIELD EXPERIENCE LEDGER ---\n{repair_history}\n\n"
                f"CURRENT BREAKDOWN SPECIFICATION: Machine {machine_selection} on {line_selection}\n"
                f"OPERATOR REPORTED SYMPTOM: {user_query}\n\n"
                "Provide a direct root-cause breakdown explaining the system context, followed immediately by a tactical, prioritized numbers-only field check list."
            )
            
            # Call Gemini safely
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
        
        # Append rating straight down to file
        feedback_entry = pd.DataFrame([{
            "Symptom": st.session_state.query_cache,
            "AI_Solution": st.session_state.solution_cache.replace("\n", " "),
            "Stars": actual_stars
        }])
        feedback_entry.to_csv(FEEDBACK_FILE, mode='a', header=False, index=False)
        
        st.success(f"Log appended! System memory grew more mature with a {actual_stars}-star resolution record.")
        st.session_state.solution_cache = None
        st.session_state.query_cache = None
