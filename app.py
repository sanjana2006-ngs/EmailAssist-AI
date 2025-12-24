Restart terminal after setting.
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

# ---------------- INPUT CARD ----------------
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

# ---------------- GENERATE REPLY ----------------
if st.button("✨ Generate Smart Reply"):
    if not email_input.strip():
        st.warning("Please paste an email.")
    else:
        with st.spinner("AI is reading the email and generating a reply..."):
            time.sleep(1)
            reply = generate_reply(email_input, tone)

        st.session_state.generated_reply = reply

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.success("✅ AI-Generated Reply")
        st.text_area("📤 Generated Reply", reply, height=220)
        st.markdown('</div>', unsafe_allow_html=True)

        if sender_email:
            st.info(f"📤 Reply prepared for: {sender_email}")

# ---------------- COPY & SEND ----------------
if "generated_reply" in st.session_state:

    st.download_button(
        label="📋 Copy Reply",
        data=st.session_state.generated_reply,
        file_name="email_reply.txt"
    )

    if sender_email:
        if st.button("📧 Send Reply"):
            st.success(f"✅ Reply successfully prepared and ready to be sent to {sender_email}")

st.toast("🚀 Saves time • Improves communication", icon="📧")
