import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Sugar & Ethanol - Industry Dashboard",
    page_icon="⛽",
    layout="wide"
)

# Title and description
st.title("⛽ Ethanol")
st.markdown("""
This page shows ethanol prices across different countries.
""")

# Create tabs for different countries
tab1, tab2 = st.tabs(["Brazil", "U.S."])

# Brazil Tab
with tab1:
    st.info("Brazil ethanol price data will be added soon.")

# U.S. Tab
with tab2:
    st.info("U.S. ethanol price data will be added soon.") 