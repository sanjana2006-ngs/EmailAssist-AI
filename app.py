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
# OPENAI API KEY (CLOUD + LOCAL)
# -------------------------------------------------
api_key = None

if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
elif os.getenv("OPENAI_API_KEY"):
    api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ OpenAI API key not found.")
    st.info("""
Add API key in one of these ways:

Streamlit Cloud:
- Manage App → Secrets
- Add:
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxx"

Local System:
- Set environment variable:
setx OPENAI_API_KEY "sk-xxxxxxxxxxxxxxxx"
""")
    st.stop()

client = OpenAI(api_key=api_key)

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
# UI
# -------------------------------------------------
st.title("📧 AI-Based Email Reply Generator")
st.subheader("Generate context-aware replies using Generative AI")
st.success("✅ AI Online Mode Enabled")

st.markdown('<div class="card">', unsafe_allow_html=True)

sender_email = st.text_input("📨 Sender's Email Address")

email_input = st.text_area(
    "📩 Paste the received email",
    height=180
)

tone = st.selectbox(
    "✍️ Select Reply Tone",
    ["Formal", "Professional", "Friendly"]
)

st.markdown('</div>', unsafe_allow_html=True)

if st.button("✨ Generate Smart Reply"):
    if not email_input.strip():
        st.warning("Please paste an email.")
    else:
        with st.spinner("Generating reply..."):
            time.sleep(1)
            reply = generate_reply(email_input, tone)

        st.session_state.generated_reply = reply

        st.success("✅ AI-Generated Reply")
        st.text_area("📤 Generated Reply", reply, height=220)

        if sender_email:
            st.info(f"📤 Reply prepared for: {sender_email}")

if "generated_reply" in st.session_state:
    st.download_button(
        label="📋 Copy Reply",
        data=st.session_state.generated_reply,
        file_name="email_reply.txt"
    )

    if sender_email:
        if st.button("📧 Send Reply"):
            st.success(f"✅ Reply ready to be sent to {sender_email}")
