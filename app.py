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
# UI THEME & UX EFFECTS
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
# OPENAI ONLINE MODE (STRICT)
# -------------------------------------------------
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OPENAI_API_KEY not found. Please add it in Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -------------------------------------------------
# AI LOGIC (CONTEXT-AWARE REPLY)
# -------------------------------------------------
def generate_reply(email_text, tone):
    prompt = f"""
You are an AI email assistant.

Rules:
- Carefully read the given email
- Understand its intent
- Generate a relevant and complete reply
- Use a {tone.lower()} tone
- Reply strictly based on the email content

Email:
\"\"\"
{email_text}
\"\"\"

Write a professional email reply.
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

# ---------------- EMAIL INPUT ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

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

# ---------------- GENERATE REPLY ----------------
if st.button("✨ Generate Smart Reply"):
    if email_input.strip() == "":
        st.warning("Please paste an email first.")
    else:
        with st.spinner("AI is reading the email and generating a reply..."):
            time.sleep(1)
            reply = generate_reply(email_input, tone)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.success("✅ AI-Generated Reply")
        st.text_area("📤 Generated Reply", reply, height=220)
        st.markdown('</div>', unsafe_allow_html=True)

        # Copy button
        st.markdown("""
<button onclick="navigator.clipboard.writeText(
    document.querySelectorAll('textarea')[1].value
)"
style="
background:#22c55e;
color:white;
padding:10px 16px;
border:none;
border-radius:10px;
font-weight:600;
cursor:pointer;
margin-top:10px;
">
📋 Copy Reply
</button>
""", unsafe_allow_html=True)

st.toast("🚀 Saves time • Improves communication", icon="📧")
