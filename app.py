import streamlit as st
import requests

st.set_page_config(
    page_title="Neravu",
    page_icon="💛",
    layout="centered"
)

st.title("💛 Neravu")
st.subheader("Your friendly AI companion")

st.write("Hello! I am Neravu. How can I help you today?")

# Language selection
language = st.selectbox(
    "Choose your preferred language:",
    [
        "English",
        "Kannada",
        "Hindi",
        "Tamil",
        "Telugu",
        "Marathi"
    ]
)

# User message
message = st.text_area(
    "What would you like to ask Neravu?",
    placeholder="Type your question here..."
)

if st.button("💬 Ask Neravu"):

    if message.strip() == "":
        st.warning("Please type something first.")

    else:
        with st.spinner("Neravu is thinking..."):

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={
                        "message": (
                            f"Respond to the user in {language}. "
                            f"User's message: {message}"
                        )
                    }
                )

                if response.status_code == 200:
                    data = response.json()

                    st.success("Neravu says:")
                    st.write(data["reply"])

                else:
                    st.error("Neravu could not respond.")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Neravu backend is not running. "
                    "Please start the FastAPI server first."
                )