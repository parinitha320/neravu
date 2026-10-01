import streamlit as st


def apply_styles():

    st.markdown("""
    <style>

    /* Main page */
    .stApp {
        background-color: #000000;
        color: white;
    }

    /* Main title */
    h1 {
        color: #FFD700;
        text-align: center;
        font-size: 48px !important;
        font-weight: 700;
    }

    h2 {
        color: #FFD700;
        font-size: 32px !important;
    }

    h3 {
        color: white;
        font-size: 26px !important;
    }

    /* Normal text */
    p {
        font-size: 20px !important;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        min-height: 70px;
        font-size: 22px;
        font-weight: 600;
        border-radius: 15px;
        border: 2px solid #FFD700;
        background-color: #FFD700;
        color: black;
    }

    .stButton > button:hover {
        background-color: #FFC107;
        color: black;
    }

    /* Select box */
    .stSelectbox label {
        font-size: 20px !important;
        color: white !important;
    }

    /* Chat input */
    .stChatInput input {
        font-size: 20px !important;
    }

    </style>
    """, unsafe_allow_html=True)