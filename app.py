import streamlit as st
from openai import OpenAI
import time
import os

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI Email Reply Generator",
    page_icon="📧",
    layout="centered"
)

# -------------------------------------------------
# UI THEME & UX
# -------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #1e1b4b, #0f172a);
    color: #f9fafb;
    animation: fadeIn 0.6s ease-in;
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
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
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 8px 25px rgba(99,102,241,0.6);
}

textarea {
    background: #020617 !important;
    color: #f9fafb !important;
    border-radius: 12px !important;
    border: 1px solid #312e81 !important;
}

h1, h2 {
    color: #e0e7ff;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# OPENAI KEY DETECTION (CLOUD + LOCAL)
# -------------------------------------------------
api_key = None

# 1️⃣ Try Streamlit Cloud Secrets
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]

# 2️⃣ Try Environment Variable (Local)
elif os.getenv("OPENAI_API_KEY"):
    api_key = os.getenv("OPENAI_API_KEY")

# 3️⃣ If still not found → show clear message
if not api_key:
    st.error("❌ OpenAI API key not found.")
    st.info("""
### How to fix:
**Streamlit Cloud**
- Go to Manage App → Secrets
- Add:
