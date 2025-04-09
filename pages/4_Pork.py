import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Pork - Industry Dashboard",
    page_icon="🥓",
    layout="wide"
)

# Title and description
st.title("🥓 Pork")
st.markdown("""
This page shows pork prices across different countries.
""")

# Create tabs for different countries
tab1, tab2, tab3, tab4 = st.tabs(["Brazil", "U.S.", "China", "EU"])

# Brazil Tab
with tab1:
    st.info("Brazil pork price data will be added soon.")

# U.S. Tab
with tab2:
    st.info("U.S. pork price data will be added soon.")

# China Tab
with tab3:
    st.info("China pork price data will be added soon.")

# EU Tab
with tab4:
    st.info("EU pork price data will be added soon.") 