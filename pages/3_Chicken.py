import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Chicken - Industry Dashboard",
    page_icon="🍗",
    layout="wide"
)

# Title and description
st.title("🍗 Chicken")
st.markdown("""
This page shows chicken prices across different countries.
""")

# Load the data
@st.cache_data
def load_data():
    chicken_price_path = Path("datasets/BR_CHICKEN_PRICE.csv")
    broiler_costs_path = Path("datasets/BR_BROILER_COSTS_STATE.csv")
    broiler_costs_breakdown_path = Path("datasets/BR_BROILER_COSTS_BREAKDOWN.csv")
    
    chicken_df = pd.read_csv(chicken_price_path)
    broiler_costs_df = pd.read_csv(broiler_costs_path)
    broiler_costs_breakdown_df = pd.read_csv(broiler_costs_breakdown_path)
    
    # Convert date columns to datetime
    chicken_df['DATE'] = pd.to_datetime(chicken_df['DATE'])
    broiler_costs_df['Date'] = pd.to_datetime(broiler_costs_df['Date'])
    broiler_costs_breakdown_df['Date'] = pd.to_datetime(broiler_costs_breakdown_df['Date'])
    
    return chicken_df, broiler_costs_df, broiler_costs_breakdown_df

chicken_df, broiler_costs_df, broiler_costs_breakdown_df = load_data()

# Create tabs for different countries
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Brazil", "U.S.", "China", "EU", "Saudi Arabia"])

# Brazil Tab
with tab1:
    # Create two columns for side-by-side graphs
    col1, col2 = st.columns(2)

    # Chicken price graph
    with col1:
        fig_chicken = px.line(chicken_df, x='DATE', y='BR_CHICKEN_PRICE', 
                             title='Chicken Prices in Brazil',
                             labels={'BR_CHICKEN_PRICE': 'Price (BRL/kg)', 'DATE': 'Date'})
        st.plotly_chart(fig_chicken, use_container_width=True)
        
        # Ração costs in PR state
        racao_df = broiler_costs_breakdown_df[
            (broiler_costs_breakdown_df['State'] == 'PR') & 
            (broiler_costs_breakdown_df['CostName'] == 'Ração')
        ].sort_values('Date')
        
        fig_racao = px.line(racao_df, x='Date', y='R$_kg',
                           title='Feed Costs in Paraná',
                           labels={'R$_kg': 'Cost (BRL/kg)', 'Date': 'Date'})
        st.plotly_chart(fig_racao, use_container_width=True)

    # Broiler costs by state graph
    with col2:
        # Filter for only RS, SC, and PR states
        filtered_broiler_df = broiler_costs_df[broiler_costs_df['State'].isin(['RS', 'SC', 'PR'])]
        
        # Sort by date from oldest to newest
        filtered_broiler_df = filtered_broiler_df.sort_values('Date')
        
        fig_broiler = px.line(filtered_broiler_df, x='Date', y='R$_kg', 
                             color='State',
                             title='Broiler Costs by State in Brazil',
                             labels={'R$_kg': 'Cost (BRL/kg)', 'Date': 'Date', 'State': 'State'})
        st.plotly_chart(fig_broiler, use_container_width=True)
        
        # Genética costs in PR state
        genetica_df = broiler_costs_breakdown_df[
            (broiler_costs_breakdown_df['State'] == 'PR') & 
            (broiler_costs_breakdown_df['CostName'] == 'Genética')
        ].sort_values('Date')
        
        fig_genetica = px.line(genetica_df, x='Date', y='R$_kg',
                              title='Genetics Costs in Paraná',
                              labels={'R$_kg': 'Cost (BRL/kg)', 'Date': 'Date'})
        st.plotly_chart(fig_genetica, use_container_width=True)

# U.S. Tab
with tab2:
    st.info("U.S. chicken price data will be added soon.")

# China Tab
with tab3:
    st.info("China chicken price data will be added soon.")

# EU Tab
with tab4:
    st.info("EU chicken price data will be added soon.")

# Saudi Arabia Tab
with tab5:
    st.info("Saudi Arabia chicken price data will be added soon.") 