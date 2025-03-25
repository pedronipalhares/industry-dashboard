import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
        .stChart > div > div > div > svg {
            background-color: #ffffff;
        }
        .st-bx {
            background-color: #ffffff;
        }
        .st-emotion-cache-13ln4jz div {
            background-color: #ffffff;
        }
        div[data-testid="stMetricValue"] {
            color: #8B0000;
            font-size: 1.2rem;
        }
        h1, h2, h3, h4 {
            color: #8B0000;
        }
        .download-btn {
            display: inline-block;
            padding: 0.4rem 0.8rem;
            background-color: #8B0000;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            text-align: center;
        }
        /* Custom nav buttons styling */
        .stButton button {
            width: 100%;
            border-radius: 4px;
            margin-bottom: 5px;
        }
        .stButton button[data-testid="baseButton-secondary"] {
            background-color: transparent;
            color: #8B0000;
            border: 1px solid #8B0000;
        }
        .stButton button[data-testid="baseButton-primary"] {
            background-color: #8B0000;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

# Color constants
COLORS = {
    'primary': '#2E3192',  # New primary color for all line charts
    'dark_red': '#8B0000',
    'dark_green': '#006400',
    'positive': '#006400',  # For positive bars in bar charts
    'negative': '#8B0000',  # For negative bars in bar charts
} 