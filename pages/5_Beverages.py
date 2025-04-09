import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Beverages - Industry Dashboard",
    page_icon="🥤",
    layout="wide"
)

# Title and description
st.title("🥤 Beverages")
st.markdown("""
This page shows beverage prices across different countries.
""")

# Create tabs for different countries
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Brazil", "Argentina", "Dominic Republic", "Guatemala", "Chile", "Canada"])

# Brazil Tab
with tab1:
    st.info("Brazil beverage price data will be added soon.")

# Argentina Tab
with tab2:
    st.info("Argentina beverage price data will be added soon.")

# Dominic Republic Tab
with tab3:
    st.info("Dominic Republic beverage price data will be added soon.")

# Guatemala Tab
with tab4:
    st.info("Guatemala beverage price data will be added soon.")

# Chile Tab
with tab5:
    st.info("Chile beverage price data will be added soon.")

# Canada Tab
with tab6:
    st.info("Canada beverage price data will be added soon.") 