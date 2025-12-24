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
# API KEY INPUT (DEMO SAFE METHOD)
# -------------------------------------------------
st.markdown("### 🔑 Enter OpenAI API Key (for demo)")
api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="sk-xxxxxxxxxxxxxxxxxxxx"
)

if not api_key:
    st.warning("Please enter your OpenAI API key to enable AI replies.")
    st.stop()

client = OpenAI(api_key=api_key)
st.success("✅ AI Online Mode Enabled")

# -------------------------------------------------
# AI FUNCTION
# -------------------------------------------------
def generate_reply(email_text, tone):
    prompt = f"""
You are an AI email assistant.

Rules:
- Read the email carefully
- Understand its intent
- Generate a clear and relevant reply
- Use a {tone.lower()} tone
- Reply strictly based on the given email

Email:
\"\"\"
{email_text}
\"\"\"

Write a complete professional email reply.
"""
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )
    return response.output_text

# -------------------------------------------------
# INPUT CARD
# -------------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

sender_email = st.text_input(
    "📨 Sender's Email Address",
    placeholder="example@gmail.com"
)

email_input = st.text_area(
    "📩 Paste the received email",
    height=180,
    placeholder="Paste the email you received here..."
)

tone = st.selectbox(
    "✍️ Select Reply Tone",
    ["Formal", "Professional", "Friendly"]
)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------
