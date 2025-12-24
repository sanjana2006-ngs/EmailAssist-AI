import streamlit as st
from openai import OpenAI
import time

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI Email Reply Generator",
    page_icon="📧",
    layout="centered"
)

# -------------------------------------------------
# UI DESIGN
# -------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #1e1b4b, #0f172a);
    color: #f9fafb;
}

.card {
    background: #111827;
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.45);
    margin-bottom: 20px;
}

.stButton > button {
    background: linear-gradient(90deg, #6366f1, #9333ea);
    color: white;
    border-radius: 14px;
    height: 3em;
    font-size: 16px;
    font-weight: 600;
}

textarea {
    background: #020617 !important;
    color: #f9fafb !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# TITLE
# -------------------------------------------------
st.title("📧 AI-Based Email Reply Generator")
st.subheader("Generate context-aware replies using Generative AI")

# -------------------------------------------------
# API KEY INPUT (TEMPORARY DEMO METHOD)
# -------------------------------------------------
st.markdown("### 🔑 Enter OpenAI API Key (for demo)")
api_key = st.text_input(
    "OpenAI API Key",
    type="password"
