import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime, timedelta

# Set page config
st.set_page_config(
    page_title="Cookies & Pasta - Industry Dashboard",
    page_icon="🍪",
    layout="wide"
)

# Title and description
st.title("🍪 Cookies & Pasta")
st.markdown("""
This page shows data related to cookies and pasta industry, including inflation and costs metrics.
""")

# Create tabs for different sections
tab1, tab2 = st.tabs(["Inflation", "Costs"])

# Inflation Tab
with tab1:
    st.info("Inflation data will be added soon.")

# Costs Tab
with tab2:
    st.info("Costs data will be added soon.") 
    