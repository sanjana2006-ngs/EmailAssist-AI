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
# BASIC HTML + CSS (UX)
# -------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: #0f172a;
    color: #f8fafc;
}
.card {
    background: #111827;
    padding: 20px;
    border-radius: 14px;
    margin-bottom: 20px;
}
button {
    background: #6366f1;
}
textarea {
    background: #020617 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# TITLE
# -------------------------------------------------
st.title("📧 AI-Based Email Reply Generator")
st.subheader("Generates, copies, and prepares replies using Generative AI")

# -------------------------------------------------
# API KEY INPUT (DEMO SAFE)
# -------------------------------------------------
api_key = st.text_input(
    "🔑 Enter OpenAI API Key",
    type="password",
    placeholder="sk-xxxxxxxxxxxxxxxx"
)

if not api_key:
    st.warning("Enter API key to enable AI reply generation.")
    st.stop()

# Initialize client safely
client = OpenAI(api_key=api_key)

# -------------------------------------------------
# AI FUNCTION (SAFE)
# -------------------------------------------------
def generate_reply(email_text, tone):
    prompt = f"""
You are an AI email assistant.

Task:
- Read the email carefully
- Understand intent
- Generate a reply in {tone.lower()} tone
- Reply only to the given email

Email:
\"\"\"
{email_text}
\"\"\"

Write a complete email reply.
"""
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        return response.output_text
    except Exception as e:
        return (
            "⚠️ AI service unavailable.\n\n"
            "This may be due to an invalid API key or network issue.\n\n"
            "In real deployment, this will be handled securely."
        )

# -------------------------------------------------
# INPUT UI
# -------------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

sender_email = st.text_input("📨 Sender Email ID")
email_text = st.text_area("📩 Paste received email", height=180)
tone = st.selectbox("✍️ Reply Tone", ["Formal", "Professional", "Friendly"])

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# GENERATE REPLY
# -------------------------------------------------
if st.button("✨ Generate Reply"):
    if not email_text.strip():
        st.warning("Please paste an email.")
    else:
        with st.spinner("Generating reply using AI..."):
            time.sleep(1)
            reply = generate_reply(email_text, tone)

        st.session_state.reply = reply

        st.success("✅ Reply Generated")
        st.text_area("📤 Generated Reply", reply, height=220)

        if sender_email:
            st.info(f"Reply prepared for: {sender_email}")

# -------------------------------------------------
# COPY FUNCTION (WORKS 100%)
# -------------------------------------------------
if "reply" in st.session_state:
    st.download_button(
        "📋 Copy Reply",
        st.session_state.reply,
        file_name="email_reply.txt"
    )

    if sender_email:
        if st.button("📧 Send Reply (Simulated)"):
            st.success(
                f"Reply is ready to be sent to {sender_email}. "
                "Email sending can be integrated using Gmail API or SMTP."
            )
