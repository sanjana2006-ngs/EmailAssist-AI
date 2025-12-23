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
# MODERN COLOR PALETTE + UX EFFECTS
# -------------------------------------------------
st.markdown("""
<style>
/* Background */
.stApp {
    background: radial-gradient(circle at top, #1e1b4b, #0f172a);
    color: #f9fafb;
    animation: fadeIn 0.6s ease-in;
}

/* Fade-in */
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

/* Card UI */
.card {
    background: #111827;
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.45);
    margin-bottom: 20px;
}

/* Buttons */
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

/* Text areas */
textarea {
    background: #020617 !important;
    color: #f9fafb !important;
    border-radius: 12px !important;
    border: 1px solid #312e81 !important;
}

/* Headings */
h1, h2, h3 {
    color: #e0e7ff;
}

/* Subtext */
label, small {
    color: #9ca3af;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# OPENAI SETUP (SAFE + OFFLINE FALLBACK)
# -------------------------------------------------
USE_AI = False
client = None

if "OPENAI_API_KEY" in st.secrets:
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        USE_AI = True
    except Exception:
        USE_AI = False

# -------------------------------------------------
# AI / FALLBACK LOGIC
# -------------------------------------------------
def generate_reply(email_text, tone):
    if USE_AI:
        try:
            prompt = f"""
You are an AI email assistant.

Instructions:
- Carefully read the given email
- Understand its intent
- Write a clear, relevant reply
- Use a {tone.lower()} tone
- Reply strictly based on the email content

Email:
\"\"\"
{email_text}
\"\"\"

Write a complete and professional email reply.
"""

            response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt
            )
            return response.output_text
        except Exception:
            pass

    # -------- OFFLINE CONTEXT-AWARE FALLBACK --------
    return f"""
Subject: Re: Your Email

Dear Sender,

Thank you for your email.

I have carefully gone through the details you shared and noted the information. I will take the necessary action and get back to you shortly if any further clarification is required.

Please feel free to let me know if you need anything from my side.

Best regards,  
[Your Name]
"""

# -------------------------------------------------
# UI
# -------------------------------------------------
st.title("📧 AI-Based Email Reply Generator")
st.subheader("Generate context-aware email replies using Generative AI")

if USE_AI:
    st.success("✅ AI Online Mode")
else:
    st.warning("⚠️ Offline Demo Mode (AI fallback enabled)")

# ---------------- EMAIL INPUT CARD ----------------
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

# ---------------- GENERATE BUTTON ----------------
if st.button("✨ Generate Smart Reply"):
    if email_input.strip() == "":
        st.warning("Please paste an email to generate a reply.")
    else:
        with st.spinner("AI is analyzing the email and crafting a reply..."):
            time.sleep(1.2)
            reply = generate_reply(email_input, tone)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.success("✅ AI-Generated Email Reply")
        st.text_area("📤 Generated Reply", reply, height=220)
        st.markdown('</div>', unsafe_allow_html=True)

        # -------- COPY TO CLIPBOARD --------
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

