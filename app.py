import streamlit as st
from openai import OpenAI
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI Email Reply Generator",
    page_icon="📧",
    layout="centered"
)

# -------------------------------------------------
# UI STYLE
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
st.subheader("Generate, copy, and send replies using Generative AI")

# -------------------------------------------------
# API KEY INPUT (DEMO FRIENDLY)
# -------------------------------------------------
st.markdown("### 🔑 OpenAI API Key")
openai_key = st.text_input(
    "Enter OpenAI API Key",
    type="password",
    placeholder="sk-xxxxxxxxxxxxxxxx"
)

if not openai_key:
    st.warning("Please enter OpenAI API key to continue.")
    st.stop()

client = OpenAI(api_key=openai_key)
st.success("✅ AI Connected")

# -------------------------------------------------
# EMAIL SENDER CONFIG (SMTP)
# -------------------------------------------------
st.markdown("### ✉️ Sender Email Configuration (Gmail SMTP)")
sender_email = st.text_input("Sender Gmail Address")
sender_password = st.text_input(
    "Gmail App Password",
    type="password",
    help="Use Gmail App Password, not normal password"
)

receiver_email = st.text_input("📨 Receiver Email Address")

# -------------------------------------------------
# AI FUNCTION
# -------------------------------------------------
def generate_reply(email_text, tone):
    prompt = f"""
You are an AI email assistant.

Instructions:
- Read the email carefully
- Understand the intent
- Generate a clear and relevant reply
- Use a {tone.lower()} tone
- Reply strictly based on the email content

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
# SEND EMAIL FUNCTION
# -------------------------------------------------
def send_email(sender, password, receiver, message):
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = "Re: Your Email"

    msg.attach(MIMEText(message, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)

# -------------------------------------------------
# INPUT CARD
# -------------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

email_input = st.text_area(
    "📩 Paste the received email",
    height=180,
    placeholder="Paste the received email here..."
)

tone = st.selectbox(
    "✍️ Select Reply Tone",
    ["Formal", "Professional", "Friendly"]
)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# GENERATE REPLY
# -------------------------------------------------
if st.button("✨ Generate Reply"):
    if not email_input.strip():
        st.warning("Please paste the email content.")
    else:
        with st.spinner("AI is generating reply..."):
            time.sleep(1)
            reply = generate_reply(email_input, tone)

        st.session_state.reply = reply

        st.success("✅ Reply Generated")
        st.text_area("📤 Generated Reply", reply, height=220)

# -------------------------------------------------
# COPY & SEND
# -------------------------------------------------
if "reply" in st.session_state:

    st.download_button(
        "📋 Copy Reply",
        st.session_state.reply,
        file_name="email_reply.txt"
    )

    if st.button("📧 Send Reply"):
        if not sender_email or not sender_password or not receiver_email:
            st.error("Please fill sender and receiver email details.")
        else:
            try:
                send_email(
                    sender_email,
                    sender_password,
                    receiver_email,
                    st.session_state.reply
                )
                st.success("✅ Email sent successfully!")
            except Exception as e:
                st.error("❌ Failed to send email. Check credentials.")
