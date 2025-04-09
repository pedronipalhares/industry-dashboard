import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime, timedelta

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

# Load the data
@st.cache_data
def load_data():
    capacity_util_path = Path("datasets/AR_CAPACITY_UTILIZATION_FB.csv")
    
    capacity_util_df = pd.read_csv(capacity_util_path)
    
    # Convert date column to datetime
    capacity_util_df['DATE'] = pd.to_datetime(capacity_util_df['DATE'])
    
    # Extract month and year for filtering and coloring
    capacity_util_df['Month'] = capacity_util_df['DATE'].dt.strftime('%b')
    capacity_util_df['Year'] = capacity_util_df['DATE'].dt.year
    
    return capacity_util_df

capacity_util_df = load_data()

# Create tabs for different countries
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Brazil", "Argentina", "Dominic Republic", "Guatemala", "Chile", "Canada"])

# Brazil Tab
with tab1:
    st.info("Brazil beverage price data will be added soon.")

# Argentina Tab
with tab2:
    # Get the current year
    current_year = datetime.now().year
    
    # Filter for the last 3 years
    recent_data = capacity_util_df[capacity_util_df['Year'] > current_year - 3]
    
    # Create the capacity utilization graph
    fig_capacity = px.line(recent_data, 
                          x='Month', 
                          y='AR_CAPACITY_UTILIZATION_FB',
                          color='Year',
                          title='Argentina Food & Beverage Capacity Utilization',
                          labels={'AR_CAPACITY_UTILIZATION_FB': 'Capacity Utilization (%)', 
                                 'Month': 'Month',
                                 'Year': 'Year'},
                          markers=True)
    
    # Update layout to ensure proper display
    fig_capacity.update_layout(
        xaxis={'categoryorder': 'array', 
               'categoryarray': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']}
    )
    
    st.plotly_chart(fig_capacity, use_container_width=True)

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