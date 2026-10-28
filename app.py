
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Email & Message Writer",
    page_icon="✉️",
    layout="wide"
)

st.title("✉️ AI Email & Message Writer")
st.write("Create professional emails and messages in seconds.")

# Secure API key
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = ""

if not api_key:
    st.warning("Please add GROQ_API_KEY in Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

st.sidebar.title("About")
st.sidebar.write(
    "This AI writing assistant helps you create "
    "emails, replies, and messages in different tones and languages."
)

category = st.selectbox(
    "Choose message type",
    [
        "Professional Email",
        "Formal Email",
        "Friendly Email",
        "WhatsApp Message",
        "Reply to an Email",
        "Follow-up Email",
        "Apology Message",
        "Thank-You Message",
        "Job Application Email",
        "Custom Message"
    ]
)

col1, col2 = st.columns(2)

with col1:
    recipient = st.text_input("Recipient Name (optional)")
    sender = st.text_input("Your Name (optional)")
    subject = st.text_input("Email Subject (optional)")

with col2:
    tone = st.selectbox(
        "Choose Tone",
        [
            "Professional",
            "Formal",
            "Friendly",
            "Polite",
            "Confident",
            "Persuasive",
            "Warm",
            "Casual"
        ]
    )

    language = st.selectbox(
        "Choose Language",
        ["English", "Urdu", "Roman Urdu"]
    )

    length = st.selectbox(
        "Message Length",
        ["Short", "Medium", "Detailed"]
    )

purpose = st.text_area(
    "What do you want to write?",
    placeholder="Explain the purpose of your email or message...",
    height=130
)

details = st.text_area(
    "Additional Details (optional)",
    placeholder="Add any important information here...",
    height=90
)

original_message = ""

if category == "Reply to an Email":
    original_message = st.text_area(
        "Paste the original email or message",
        height=150
    )

if st.button("✨ Generate Message", use_container_width=True):
    if not purpose.strip():
        st.error("Please enter the purpose of your message.")
    elif category == "Reply to an Email" and not original_message.strip():
        st.error("Please paste the original email or message.")
    else:
        prompt = f"""
        Write a {category}.

        Recipient: {recipient or "Not specified"}
        Sender: {sender or "Not specified"}
        Subject: {subject or "Create a suitable subject if needed"}
        Tone: {tone}
        Language: {language}
        Length: {length}

        Purpose:
        {purpose}

        Additional details:
        {details or "None provided"}

        Original message to reply to:
        {original_message or "Not applicable"}

        Instructions:
        - Write naturally and professionally.
        - Follow the requested tone, language, and length.
        - Do not invent facts or personal details.
        - Use placeholders when information is missing.
        - Include a suitable greeting and closing when appropriate.
        - For emails, provide a subject line when useful.
        - Return only the finished draft.
        """

        try:
            with st.spinner("Writing your message..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a professional AI writing "
                                "assistant. Create clear, natural, "
                                "context-aware emails and messages."
                            )
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )

                generated = response.choices[0].message.content

            if generated:
                st.session_state["generated_message"] = generated
            else:
                st.error("The AI returned an empty response.")

        except Exception as e:
            st.error(
                "Message generation failed. Check your Groq API key, "
                "model availability, and API settings."
            )
            st.caption(f"Technical details: {type(e).__name__}")

if "generated_message" in st.session_state:
    st.divider()
    st.subheader("Your Generated Message")

    edited_message = st.text_area(
        "Edit your message if needed",
        value=st.session_state["generated_message"],
        height=300,
        key="edited_message"
    )

    st.download_button(
        "⬇️ Download Message",
        data=edited_message,
        file_name="generated_message.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.button(
        "🔄 Generate Another Version",
        on_click=lambda: st.session_state.pop("generated_message", None),
        use_container_width=True
    )

st.divider()
st.caption("AI Email & Message Writer | Powered by Groq and Streamlit")
