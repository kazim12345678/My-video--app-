import streamlit as st
from groq import Groq

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="KAZIM AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# MOBILE + DESKTOP UI
# =========================================================

st.markdown("""
<style>

/* MAIN */
.stApp{
    background-color:#FFFFFF
