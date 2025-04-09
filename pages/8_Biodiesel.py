import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import datetime
from auth import is_authenticated, require_auth

# Check authentication
if not is_authenticated():
    st.switch_page("pages/0_Login.py")

# Set page config
st.set_page_config(
    page_title="Biodiesel - Industry Dashboard",
    page_icon="🛢️",
    layout="wide"
)

# Title and description
st.title("🛢️ Biodiesel")
st.markdown("""
This page shows biodiesel prices and production in Brazil.
""")

# Load the data
@st.cache_data
def load_data():
    # Load price data
    biodiesel_price_path = Path("datasets/BR_BIODIESEL_PRICE.csv")
    biodiesel_df = pd.read_csv(biodiesel_price_path)
    biodiesel_df['DATE'] = pd.to_datetime(biodiesel_df['DATE'])
    
    # Load diesel price data
    diesel_price_path = Path("datasets/BR_DIESEL_PRICE.csv")
    diesel_df = pd.read_csv(diesel_price_path)
    diesel_df['DATE'] = pd.to_datetime(diesel_df['DATE'])
    
    # Filter for last three years
    current_year = datetime.datetime.now().year
    diesel_df = diesel_df[diesel_df['DATE'].dt.year >= current_year - 2]
    
    # Load production data
    production_path = Path("datasets/BR_BIODIESEL_PRODUCTION.csv")
    production_df = pd.read_csv(production_path)
    production_df['Date'] = pd.to_datetime(production_df['Date'])
    
    # Calculate total production by date
    total_production = production_df.groupby('Date')['Production'].sum().reset_index()
    
    return biodiesel_df, diesel_df, total_production

biodiesel_df, diesel_df, total_production = load_data()

# Create tabs
tab1, tab2, tab3 = st.tabs(["Economics", "Production", "Crushing"])

# Economics Tab
with tab1:
    # Create two columns for side-by-side graphs
    col1, col2 = st.columns(2)
    
    # Biodiesel price graph in first column
    with col1:
        fig_biodiesel = px.line(biodiesel_df, 
                               x='DATE', 
                               y='BR_BIODIESEL_PRICE',
                               title='Biodiesel Prices in Brazil',
                               labels={'BR_BIODIESEL_PRICE': 'Price (BRL/L)', 
                                      'DATE': 'Date'})
        st.plotly_chart(fig_biodiesel, use_container_width=True)
    
    # Diesel price graph in second column
    with col2:
        fig_diesel = px.line(diesel_df, 
                            x='DATE', 
                            y='BR_DIESEL_PRICE',
                            title='Diesel Prices in Brazil',
                            labels={'BR_DIESEL_PRICE': 'Price (BRL/L)', 
                                   'DATE': 'Date'})
        st.plotly_chart(fig_diesel, use_container_width=True)

# Production Tab
with tab2:
    # Create two columns for side-by-side graphs
    col1, col2 = st.columns(2)
    
    # Biodiesel production graph in first column
    with col1:
        fig_production = px.line(total_production,
                               x='Date',
                               y='Production',
                               title='Total Biodiesel Production in Brazil',
                               labels={'Production': 'Production (m³)',
                                      'Date': 'Date'})
        st.plotly_chart(fig_production, use_container_width=True)

# Crushing Tab
with tab3:
    st.info("Crushing data will be added soon.")
