import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Beef - Industry Dashboard",
    page_icon="🥩",
    layout="wide"
)

# Title and description
st.title("🥩 Beef")
st.markdown("""
This page shows beef prices and cattle prices across different countries.
""")

# Load the data
@st.cache_data
def load_data():
    beef_price_path = Path("datasets/BR_BEEF_PRICES.csv")
    cattle_price_path = Path("datasets/BR_CATTLE_PRICE.csv")
    
    beef_df = pd.read_csv(beef_price_path)
    cattle_df = pd.read_csv(cattle_price_path)
    
    # Convert date columns to datetime
    beef_df['DATE'] = pd.to_datetime(beef_df['DATE'])
    cattle_df['DATE'] = pd.to_datetime(cattle_df['DATE'])
    
    return beef_df, cattle_df

beef_df, cattle_df = load_data()

# Create tabs for different countries
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Brazil", "U.S.", "China", "Argentina", "Uruguay"])

# Brazil Tab
with tab1:
    # Create two columns for side-by-side graphs
    col1, col2 = st.columns(2)

    # Beef price graph
    with col1:
        fig_beef = px.line(beef_df, x='DATE', y='BR_BEEF_PRICES', 
                           title='Beef Prices in Brazil',
                           labels={'BR_BEEF_PRICES': 'Price (BRL/kg)', 'DATE': 'Date'})
        st.plotly_chart(fig_beef, use_container_width=True)

    # Cattle price graph
    with col2:
        fig_cattle = px.line(cattle_df, x='DATE', y='BR_CATTLE_PRICE', 
                             title='Cattle Prices in Brazil',
                             labels={'BR_CATTLE_PRICE': 'Price (BRL/kg)', 'DATE': 'Date'})
        st.plotly_chart(fig_cattle, use_container_width=True)

# U.S. Tab
with tab2:
    st.info("U.S. beef and cattle price data will be added soon.")

# China Tab
with tab3:
    st.info("China beef and cattle price data will be added soon.")

# Argentina Tab
with tab4:
    st.info("Argentina beef and cattle price data will be added soon.")

# Uruguay Tab
with tab5:
    st.info("Uruguay beef and cattle price data will be added soon.") 