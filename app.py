import streamlit as st
from google import genai

# Page configuration
st.set_page_config(
    page_title="StudySpark AI",
    page_icon="📚",
    layout="centered"
)

# App heading
st.title("📚 StudySpark AI")
st.subheader("Your AI-powered study assistant")
st.write("Make studying easier with AI!")

# Load Gemini API key
try:
    api_key = st.secrets["GEMINI_API_KEY"]

    if not api_key:
        st.error("Please add your Gemini API key.")
        st.stop()

    client = genai.Client(api_key=api_key)

except Exception as e:
    st.error(
        "API key not found. Check your "
        ".streamlit/secrets.toml file."
    )
    st.stop()

# Notes input
notes = st.text_area(
    "Enter your study notes here:",
    placeholder="Paste your notes here...",
    height=200
)

# Summarize notes
if st.button("✨ Summarize Notes"):

    if not notes.strip():
        st.warning("Please enter your notes first.")

    else:
        try:
            with st.spinner(
                "AI is summarizing your notes..."
            ):
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=(
                        "You are a helpful study assistant. "
                        "Summarize the following study notes "
                        "in simple language. Use a heading "
                        "and clear bullet points. Include "
                        "the most important concepts.\n\n"
                        + notes
                    )
                )

            if response.text:
                st.subheader("📝 AI-Generated Summary")
                st.write(response.text)

            else:
                st.warning(
                    "The AI returned an empty response. "
                    "Please try again."
                )

        except Exception as e:
            st.error(f"Gemini API error: {e}")