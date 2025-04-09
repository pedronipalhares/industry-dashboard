import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime

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
    cattle_herd_path = Path("datasets/BR_CATTLE_HERD.csv")
    ar_food_path = Path("datasets/AR_FOOD.csv")
    au_cattle_path = Path("datasets/AU_CATTLE_PRICE.csv")
    
    beef_df = pd.read_csv(beef_price_path)
    cattle_df = pd.read_csv(cattle_price_path)
    cattle_herd_df = pd.read_csv(cattle_herd_path)
    ar_food_df = pd.read_csv(ar_food_path)
    au_cattle_df = pd.read_csv(au_cattle_path)
    
    # Convert date columns to datetime
    beef_df['DATE'] = pd.to_datetime(beef_df['DATE'])
    cattle_df['DATE'] = pd.to_datetime(cattle_df['DATE'])
    cattle_herd_df['Date'] = pd.to_datetime(cattle_herd_df['Date'])
    ar_food_df['Date'] = pd.to_datetime(ar_food_df['Date'])
    au_cattle_df['DATE'] = pd.to_datetime(au_cattle_df['DATE'])
    
    # Extract month and year for filtering and coloring
    ar_food_df['Month'] = ar_food_df['Date'].dt.strftime('%b')
    ar_food_df['Year'] = ar_food_df['Date'].dt.year
    
    au_cattle_df['Month'] = au_cattle_df['DATE'].dt.strftime('%b')
    au_cattle_df['Year'] = au_cattle_df['DATE'].dt.year
    
    return beef_df, cattle_df, cattle_herd_df, ar_food_df, au_cattle_df

beef_df, cattle_df, cattle_herd_df, ar_food_df, au_cattle_df = load_data()

# Create tabs for different countries
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Brazil", "U.S.", "China", "Argentina", "Uruguay", "Australia"])

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
        
        # Cattle herd graph below beef price graph
        fig_herd = px.line(cattle_herd_df, x='Date', y='Cattle', 
                           title='Cattle Herd in Brazil',
                           labels={'Cattle': 'Number of Cattle', 'Date': 'Year'})
        st.plotly_chart(fig_herd, use_container_width=True)

    # Cattle price graph
    with col2:
        fig_cattle = px.line(cattle_df, x='DATE', y='BR_CATTLE_PRICE', 
                             title='Cattle Prices in Brazil',
                             labels={'BR_CATTLE_PRICE': 'Price (BRL/@)', 'DATE': 'Date'})
        st.plotly_chart(fig_cattle, use_container_width=True)

# U.S. Tab
with tab2:
    st.info("U.S. beef and cattle price data will be added soon.")

# China Tab
with tab3:
    st.info("China beef and cattle price data will be added soon.")

# Argentina Tab
with tab4:
    # Get the current year
    current_year = datetime.now().year
    
    # Filter for the last 3 years
    recent_food_data = ar_food_df[ar_food_df['Year'] > current_year - 3]
    
    # Create the slaughter heads graph
    fig_slaughter = px.line(recent_food_data, 
                           x='Month', 
                           y='Slaughter_heads',
                           color='Year',
                           title='Argentina Cattle Slaughter',
                           labels={'Slaughter_heads': 'Number of Heads', 
                                  'Month': 'Month',
                                  'Year': 'Year'},
                           markers=True)
    
    # Update layout to ensure proper display
    fig_slaughter.update_layout(
        xaxis={'categoryorder': 'array', 
               'categoryarray': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']}
    )
    
    st.plotly_chart(fig_slaughter, use_container_width=True)

# Uruguay Tab
with tab5:
    st.info("Uruguay beef and cattle price data will be added soon.") 

# Australia Tab
with tab6:
    # Get the current year
    current_year = datetime.now().year
    
    # Filter for the last 5 years
    recent_au_cattle_data = au_cattle_df[au_cattle_df['Year'] > current_year - 5]
    
    # Create the Australian cattle price graph
    fig_au_cattle = px.line(recent_au_cattle_data, 
                           x='DATE', 
                           y='AU_CATTLE_PRICE',
                           title='Australian Cattle Prices',
                           labels={'AU_CATTLE_PRICE': 'Price (AUD/kg)', 
                                  'DATE': 'Date'})
    
    st.plotly_chart(fig_au_cattle, use_container_width=True) 