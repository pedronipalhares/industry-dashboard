import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime, timedelta

# Set page config
st.set_page_config(
    page_title="Table Eggs - Industry Dashboard",
    page_icon="🥚",
    layout="wide"
)

# Title and description
st.title("🥚 Table Eggs")
st.markdown("""
This page shows table egg prices and production across different countries.
""")

# Load the data
@st.cache_data
def load_data():
    eggs_path = Path("datasets/BR_EGGS.csv")
    eggs_df = pd.read_csv(eggs_path)
    
    # Convert date column to datetime
    eggs_df['Date'] = pd.to_datetime(eggs_df['Date'])
    
    # Filter for last 5 years
    five_years_ago = datetime.now() - timedelta(days=5*365)
    eggs_df = eggs_df[eggs_df['Date'] >= five_years_ago]
    
    return eggs_df

eggs_df = load_data()

# Create tabs for different countries
tab1, tab2, tab3 = st.tabs(["Brazil", "U.S.", "EU"])

# Brazil Tab
with tab1:
    # Create two columns for side-by-side graphs
    col1, col2 = st.columns(2)
    
    # Table Layers graph
    with col1:
        fig_table_layers = px.line(eggs_df, x='Date', y='TableLayers',
                                  title='Table Layers in Brazil (Last 5 Years)',
                                  labels={'TableLayers': 'Number of Layers', 'Date': 'Date'})
        st.plotly_chart(fig_table_layers, use_container_width=True)
    
    # Table Eggs Produced graph
    with col2:
        fig_table_eggs = px.line(eggs_df, x='Date', y='TableEggsProduced',
                                title='Table Eggs Produced in Brazil (Last 5 Years)',
                                labels={'TableEggsProduced': 'Eggs Produced', 'Date': 'Date'})
        st.plotly_chart(fig_table_eggs, use_container_width=True)

# U.S. Tab
with tab2:
    st.info("U.S. table egg price data will be added soon.")

# EU Tab
with tab3:
    st.info("EU table egg price data will be added soon.") 