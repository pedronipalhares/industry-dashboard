import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Agribusiness - Industry Dashboard",
    page_icon="🌾",
    layout="wide"
)

# Title and description
st.title("🌾 Agribusiness")
st.markdown("""
This page shows agribusiness data including prices, funds, and supply & demand.
""")

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["Prices", "Funds", "S&D"])

# Prices Tab
with tab1:
    st.info("Agribusiness price data will be added soon.")

# Funds Tab
with tab2:
    st.info("Agribusiness funds data will be added soon.")

# S&D Tab
with tab3:
    st.info("Supply and demand data will be added soon.") 