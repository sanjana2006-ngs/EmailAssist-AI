import streamlit as st
from openai import OpenAI
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Email Reply Generator", page_icon="📧")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1f2933, #111827);
    color: white;
}
.stButton > button {
    background: linear-gradient(90deg, #4f46e5, #9333ea);
    color: white;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
    font-weight: bold;
}
textarea {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- AI SETUP ----------------
USE_AI = False
client = None

if "OPENAI_API_KEY" in st.secrets:
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        USE_AI = True
    except Exception:
        USE_AI = False

# ---------------- FUNCTIONS ----------------
def generate_reply(email_text, tone):
    if USE_AI:
        try:
            prompt = f"""
            You are an AI email assistant.
            Generate a {tone.lower()} reply for the following email:

            Email:
            {email_text}
            """

            response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt
            )
            return response.output_text
        except Exception:
            pass

    # 🔁 OFFLINE FALLBACK (NEVER FAILS)
    return f"""
Subject: Re: Your Email

Dear Sender,

Thank you for your email. I appreciate you reaching out.

I will review the details you have shared and get back to you shortly.
Please feel free to let me know if you need any additional information.

Best regards,  
[Your Name]
"""

# ---------------- UI ----------------
st.title("📧 AI-Based Email Reply Generator")
st.subheader("Generate professional email replies using Generative AI")

if USE_AI:
    st.success("✅ AI Online Mode")
else:
    st.warning("⚠️ Offline Demo Mode (AI fallback)")

st.divider()

email_input = st.text_area(
    "📩 Paste the received email here",
    height=180,
    placeholder="Dear Sir/Madam,\nI am writing to inform you..."
)

tone = st.selectbox(
    "✍️ Select Reply Tone",
    ["Formal", "Professional", "Friendly"]
)

if st.button("Generate Reply"):
    if email_input.strip() == "":
        st.warning("Please paste an email first")
    else:
        with st.spinner("Generating reply..."):
            time.sleep(1)
            reply = generate_reply(email_input, tone)

        st.success("✅ Generated Email Reply")
        st.text_area("📤 Reply", reply, height=220)

st.toast("🚀 Saves time. Improves communication.", icon="📧")
