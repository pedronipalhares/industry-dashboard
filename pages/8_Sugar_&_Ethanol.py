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
st.title("⛽ Sugar & Ethanol")
st.markdown("""
This page shows ethanol prices across different countries.
""")

# Create tabs for different countries
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(["Inventories", "Prices", "Production", "Demand", "Exports", "Imports","Corn","Costs","U.S."])

# Brazil Tab
with tab1:
    st.info("Brazil ethanol price data will be added soon.")

# Prices Tab
with tab2:
    st.info("Prices data will be added soon.") 

# Production Tab
with tab3:
    st.info("Production data will be added soon.") 

# Demand Tab
with tab4:
    st.info("Demand data will be added soon.") 

# Exports Tab
with tab5:
    st.info("Exports data will be added soon.") 

# Imports Tab
with tab6:
    st.info("Imports data will be added soon.") 

# Corn Tab
with tab7:
    st.info("Corn data will be added soon.") 

# Costs Tab
with tab8:
    st.info("Costs data will be added soon.")    

# U.S. Tab
with tab9:
    st.info("U.S. data will be added soon.")    