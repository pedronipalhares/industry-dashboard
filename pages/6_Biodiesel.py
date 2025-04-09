import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Biodiesel - Industry Dashboard",
    page_icon="🛢️",
    layout="wide"
)

# Title and description
st.title("🛢️ Biodiesel")
st.markdown("""
This page shows biodiesel prices in Brazil.
""")

# Create tab for Brazil
tab1 = st.tabs(["Brazil"])[0]

# Brazil Tab
with tab1:
    st.info("Brazil biodiesel price data will be added soon.") 