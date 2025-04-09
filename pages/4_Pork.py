import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import datetime

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
    # Load the data
    try:
        df_br = pd.read_csv("datasets/BR_PORK_DOMESTIC_PRICE.csv")
        
        # Convert date column to datetime
        df_br['DATE'] = pd.to_datetime(df_br['DATE'])
        
        # Filter for last 5 years
        five_years_ago = datetime.datetime.now() - datetime.timedelta(days=5*365)
        df_br_filtered = df_br[df_br['DATE'] >= five_years_ago]
        
        # Create the line chart
        fig = px.line(
            df_br_filtered, 
            x='DATE', 
            y='BR_PORK_DOMESTIC_PRICE',
            title='Brazil Pork Domestic Price (Last 5 Years)',
            labels={'DATE': 'Date', 'BR_PORK_DOMESTIC_PRICE': 'Price (BRL/kg)'}
        )
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading Brazil pork data: {e}")

# U.S. Tab
with tab2:
    st.info("U.S. pork price data will be added soon.")

# China Tab
with tab3:
    st.info("China pork price data will be added soon.")

# EU Tab
with tab4:
    st.info("EU pork price data will be added soon.") 