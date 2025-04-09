import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Macro - Industry Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 Macro")
st.markdown("""
This page shows macroeconomic indicators across different countries.
""")

# Create tabs for different countries
tab1, tab2, tab3, tab4 = st.tabs(["Currencies", "Brazil", "U.S.", "Argentina"])

# Currencies Tab
with tab1:
    st.info("Currencies data will be added soon.")

# Brazil Tab
with tab2:
    st.info("Brazil macroeconomic data will be added soon.")

# U.S. Tab
with tab2:
    st.info("U.S. macroeconomic data will be added soon.")

# Argentina Tab
with tab3:
    st.info("Argentina macroeconomic data will be added soon.") 