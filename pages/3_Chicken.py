import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Chicken - Industry Dashboard",
    page_icon="🍗",
    layout="wide"
)

# Title and description
st.title("🍗 Chicken")
st.markdown("""
This page shows chicken prices across different countries.
""")

# Create tabs for different countries
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Brazil", "U.S.", "China", "EU", "Saudi Arabia"])

# Brazil Tab
with tab1:
    st.info("Brazil chicken price data will be added soon.")

# U.S. Tab
with tab2:
    st.info("U.S. chicken price data will be added soon.")

# China Tab
with tab3:
    st.info("China chicken price data will be added soon.")

# EU Tab
with tab4:
    st.info("EU chicken price data will be added soon.")

# Saudi Arabia Tab
with tab5:
    st.info("Saudi Arabia chicken price data will be added soon.") 