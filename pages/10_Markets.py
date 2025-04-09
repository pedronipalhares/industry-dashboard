import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Markets - Industry Dashboard",
    page_icon="📈",
    layout="wide"
)

# Title and description
st.title("📈 Markets")
st.markdown("""
This page shows market data including prices and short positions.
""")

# Create tabs for different sections
tab1, tab2 = st.tabs(["Prices", "Short"])

# Prices Tab
with tab1:
    st.info("Market price data will be added soon.")

# Short Tab
with tab2:
    st.info("Short position data will be added soon.") 