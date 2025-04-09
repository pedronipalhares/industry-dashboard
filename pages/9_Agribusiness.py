import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime, timedelta

# Set page config
st.set_page_config(
    page_title="Agribusiness - Industry Dashboard",
    page_icon="🌾",
    layout="wide"
)

# Title and description
st.title("🌾 Agribusiness")
st.markdown("""
This page shows agribusiness data including commodity prices, funds, and supply & demand.
""")

# Load the data
@st.cache_data
def load_commodity_data(commodity_code):
    file_path = Path(f"datasets/US_{commodity_code}_PRICE.csv")
    df = pd.read_csv(file_path)
    df['DATE'] = pd.to_datetime(df['DATE'])
    
    # Filter last 2 years
    two_years_ago = datetime.now() - timedelta(days=2*365)
    df = df[df['DATE'] >= two_years_ago]
    
    return df

@st.cache_data
def load_net_long_data(commodity_code):
    file_path = Path(f"datasets/US_{commodity_code}_NET_LONG.csv")
    df = pd.read_csv(file_path)
    df['DATE'] = pd.to_datetime(df['DATE'])
    
    # Filter last 2 years
    two_years_ago = datetime.now() - timedelta(days=2*365)
    df = df[df['DATE'] >= two_years_ago]
    
    return df

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["Prices", "Funds", "S&D"])

# Prices Tab
with tab1:
    # Load data for each commodity
    corn_df = load_commodity_data("CORN")
    soy_df = load_commodity_data("SOY")
    cotton_df = load_commodity_data("COTTON")
    wheat_df = load_commodity_data("WHEAT")
    sugar_df = load_commodity_data("SUGAR")
    coffee_df = load_commodity_data("COFFEE")
    oil_df = load_commodity_data("OIL")
    
    # Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        fig_corn = px.line(corn_df, 
                          x='DATE', 
                          y='US_CORN_PRICE',
                          title='Corn Price',
                          labels={'US_CORN_PRICE': 'Price (US cents/bushel)', 
                                 'DATE': 'Date'})
        st.plotly_chart(fig_corn, use_container_width=True)
    
    with col2:
        fig_soy = px.line(soy_df, 
                         x='DATE', 
                         y='US_SOY_PRICE',
                         title='Soybean Price',
                         labels={'US_SOY_PRICE': 'Price (US cents/bushel)', 
                                'DATE': 'Date'})
        st.plotly_chart(fig_soy, use_container_width=True)
    
    # Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        fig_cotton = px.line(cotton_df, 
                            x='DATE', 
                            y='US_COTTON_PRICE',
                            title='Cotton Price',
                            labels={'US_COTTON_PRICE': 'Price (US cents/pound)', 
                                   'DATE': 'Date'})
        st.plotly_chart(fig_cotton, use_container_width=True)
    
    with col2:
        fig_wheat = px.line(wheat_df, 
                           x='DATE', 
                           y='US_WHEAT_PRICE',
                           title='Wheat Price',
                           labels={'US_WHEAT_PRICE': 'Price (US cents/bushel)', 
                                  'DATE': 'Date'})
        st.plotly_chart(fig_wheat, use_container_width=True)
    
    # Row 3
    col1, col2 = st.columns(2)
    
    with col1:
        fig_sugar = px.line(sugar_df, 
                           x='DATE', 
                           y='US_SUGAR_PRICE',
                           title='Sugar Price',
                           labels={'US_SUGAR_PRICE': 'Price (US cents/pound)', 
                                  'DATE': 'Date'})
        st.plotly_chart(fig_sugar, use_container_width=True)
    
    with col2:
        fig_coffee = px.line(coffee_df, 
                            x='DATE', 
                            y='US_COFFEE_PRICE',
                            title='Coffee Price',
                            labels={'US_COFFEE_PRICE': 'Price (US cents/pound)', 
                                   'DATE': 'Date'})
        st.plotly_chart(fig_coffee, use_container_width=True)
    
    # Row 4
    col1, col2 = st.columns(2)
    
    with col1:
        fig_oil = px.line(oil_df, 
                         x='DATE', 
                         y='US_OIL_PRICE',
                         title='Oil Price',
                         labels={'US_OIL_PRICE': 'Price (US dollars/barrel)', 
                                'DATE': 'Date'})
        st.plotly_chart(fig_oil, use_container_width=True)

# Funds Tab
with tab2:
    # Load data for each commodity's net long positions
    corn_long_df = load_net_long_data("CORN")
    soy_long_df = load_net_long_data("SOY")
    cotton_long_df = load_net_long_data("COTTON")
    sugar_long_df = load_net_long_data("SUGAR")
    wheat_long_df = load_net_long_data("WHEAT")
    
    # Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        # Create a color array based on whether values are positive or negative
        colors = ['red' if val < 0 else 'green' for val in corn_long_df['US_CORN_NET_LONG']]
        
        fig_corn_long = px.bar(corn_long_df, 
                              x='DATE', 
                              y='US_CORN_NET_LONG',
                              title='Corn Net Long Positions',
                              labels={'US_CORN_NET_LONG': 'Net Long (contracts)', 
                                     'DATE': 'Date'},
                              color_discrete_sequence=['green'])
        
        # Update the bar colors
        fig_corn_long.update_traces(marker_color=colors)
        
        st.plotly_chart(fig_corn_long, use_container_width=True)
    
    with col2:
        # Create a color array based on whether values are positive or negative
        colors = ['red' if val < 0 else 'green' for val in soy_long_df['US_SOY_NET_LONG']]
        
        fig_soy_long = px.bar(soy_long_df, 
                             x='DATE', 
                             y='US_SOY_NET_LONG',
                             title='Soybean Net Long Positions',
                             labels={'US_SOY_NET_LONG': 'Net Long (contracts)', 
                                    'DATE': 'Date'},
                             color_discrete_sequence=['green'])
        
        # Update the bar colors
        fig_soy_long.update_traces(marker_color=colors)
        
        st.plotly_chart(fig_soy_long, use_container_width=True)
    
    # Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        # Create a color array based on whether values are positive or negative
        colors = ['red' if val < 0 else 'green' for val in cotton_long_df['US_COTTON_NET_LONG']]
        
        fig_cotton_long = px.bar(cotton_long_df, 
                                x='DATE', 
                                y='US_COTTON_NET_LONG',
                                title='Cotton Net Long Positions',
                                labels={'US_COTTON_NET_LONG': 'Net Long (contracts)', 
                                       'DATE': 'Date'},
                                color_discrete_sequence=['green'])
        
        # Update the bar colors
        fig_cotton_long.update_traces(marker_color=colors)
        
        st.plotly_chart(fig_cotton_long, use_container_width=True)
    
    with col2:
        # Create a color array based on whether values are positive or negative
        colors = ['red' if val < 0 else 'green' for val in sugar_long_df['US_SUGAR_NET_LONG']]
        
        fig_sugar_long = px.bar(sugar_long_df, 
                               x='DATE', 
                               y='US_SUGAR_NET_LONG',
                               title='Sugar Net Long Positions',
                               labels={'US_SUGAR_NET_LONG': 'Net Long (contracts)', 
                                      'DATE': 'Date'},
                               color_discrete_sequence=['green'])
        
        # Update the bar colors
        fig_sugar_long.update_traces(marker_color=colors)
        
        st.plotly_chart(fig_sugar_long, use_container_width=True)
    
    # Row 3
    col1, col2 = st.columns(2)
    
    with col1:
        # Create a color array based on whether values are positive or negative
        colors = ['red' if val < 0 else 'green' for val in wheat_long_df['US_WHEAT_NET_LONG']]
        
        fig_wheat_long = px.bar(wheat_long_df, 
                               x='DATE', 
                               y='US_WHEAT_NET_LONG',
                               title='Wheat Net Long Positions',
                               labels={'US_WHEAT_NET_LONG': 'Net Long (contracts)', 
                                      'DATE': 'Date'},
                               color_discrete_sequence=['green'])
        
        # Update the bar colors
        fig_wheat_long.update_traces(marker_color=colors)
        
        st.plotly_chart(fig_wheat_long, use_container_width=True)

# S&D Tab
with tab3:
    st.info("Supply and demand data will be added soon.") 