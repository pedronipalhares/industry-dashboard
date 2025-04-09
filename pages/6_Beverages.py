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
    consumer_conf_path = Path("datasets/AR_CONSUMER_CONFIDENCE.csv")
    inflation_path = Path("datasets/AR_INFLATION.csv")
    bev_inflation_path = Path("datasets/AR_CPI_ALCOHOLIC_BEV.csv")
    interest_rate_path = Path("datasets/AR_INTEREST_RATE.csv")
    mom_inflation_path = Path("datasets/AR_MOM_INFLATION.csv")
    retail_sales_path = Path("datasets/AR_RETAIL_SALES.csv")
    unemployment_path = Path("datasets/AR_UNEMPLOYMENT_RATE.csv")
    
    capacity_util_df = pd.read_csv(capacity_util_path)
    consumer_conf_df = pd.read_csv(consumer_conf_path)
    inflation_df = pd.read_csv(inflation_path)
    bev_inflation_df = pd.read_csv(bev_inflation_path)
    interest_rate_df = pd.read_csv(interest_rate_path)
    mom_inflation_df = pd.read_csv(mom_inflation_path)
    retail_sales_df = pd.read_csv(retail_sales_path)
    unemployment_df = pd.read_csv(unemployment_path)
    
    # Convert date columns to datetime
    capacity_util_df['DATE'] = pd.to_datetime(capacity_util_df['DATE'])
    consumer_conf_df['DATE'] = pd.to_datetime(consumer_conf_df['DATE'])
    inflation_df['DATE'] = pd.to_datetime(inflation_df['DATE'])
    bev_inflation_df['DATE'] = pd.to_datetime(bev_inflation_df['DATE'])
    interest_rate_df['DATE'] = pd.to_datetime(interest_rate_df['DATE'])
    mom_inflation_df['DATE'] = pd.to_datetime(mom_inflation_df['DATE'])
    retail_sales_df['DATE'] = pd.to_datetime(retail_sales_df['DATE'])
    unemployment_df['DATE'] = pd.to_datetime(unemployment_df['DATE'])
    
    # Extract month and year for filtering and coloring
    capacity_util_df['Month'] = capacity_util_df['DATE'].dt.strftime('%b')
    capacity_util_df['Year'] = capacity_util_df['DATE'].dt.year
    
    consumer_conf_df['Month'] = consumer_conf_df['DATE'].dt.strftime('%b')
    consumer_conf_df['Year'] = consumer_conf_df['DATE'].dt.year
    
    inflation_df['Month'] = inflation_df['DATE'].dt.strftime('%b')
    inflation_df['Year'] = inflation_df['DATE'].dt.year
    
    bev_inflation_df['Month'] = bev_inflation_df['DATE'].dt.strftime('%b')
    bev_inflation_df['Year'] = bev_inflation_df['DATE'].dt.year
    
    interest_rate_df['Month'] = interest_rate_df['DATE'].dt.strftime('%b')
    interest_rate_df['Year'] = interest_rate_df['DATE'].dt.year
    
    mom_inflation_df['Month'] = mom_inflation_df['DATE'].dt.strftime('%b')
    mom_inflation_df['Year'] = mom_inflation_df['DATE'].dt.year
    
    retail_sales_df['Month'] = retail_sales_df['DATE'].dt.strftime('%b')
    retail_sales_df['Year'] = retail_sales_df['DATE'].dt.year
    
    unemployment_df['Month'] = unemployment_df['DATE'].dt.strftime('%b')
    unemployment_df['Year'] = unemployment_df['DATE'].dt.year
    
    return capacity_util_df, consumer_conf_df, inflation_df, bev_inflation_df, interest_rate_df, mom_inflation_df, retail_sales_df, unemployment_df

capacity_util_df, consumer_conf_df, inflation_df, bev_inflation_df, interest_rate_df, mom_inflation_df, retail_sales_df, unemployment_df = load_data()

# Create tabs for different countries
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Brazil", "Argentina", "Dominic Republic", "Guatemala", "Chile", "Canada","Panama"])

# Brazil Tab
with tab1:
    st.info("Brazil beverage price data will be added soon.")

# Argentina Tab
with tab2:
    # Get the current year
    current_year = datetime.now().year
    
    # Filter for the last 3 years
    recent_capacity_data = capacity_util_df[capacity_util_df['Year'] > current_year - 3]
    recent_consumer_data = consumer_conf_df[consumer_conf_df['Year'] > current_year - 3]
    recent_inflation_data = inflation_df[inflation_df['Year'] > current_year - 3]
    recent_bev_inflation_data = bev_inflation_df[bev_inflation_df['Year'] > current_year - 3]
    recent_interest_data = interest_rate_df[interest_rate_df['Year'] > current_year - 5]
    recent_mom_inflation_data = mom_inflation_df[mom_inflation_df['Year'] > current_year - 3]
    recent_retail_data = retail_sales_df[retail_sales_df['Year'] > current_year - 3]
    recent_unemployment_data = unemployment_df[unemployment_df['Year'] > current_year - 5]
    
    # Create two columns for the first row
    col1, col2 = st.columns(2)
    
    # First column - Capacity Utilization
    with col1:
        # Create the capacity utilization graph
        fig_capacity = px.line(recent_capacity_data, 
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
    
    # Second column - Consumer Confidence
    with col2:
        # Create the consumer confidence graph
        fig_consumer = px.line(recent_consumer_data, 
                              x='Month', 
                              y='AR_CONSUMER_CONFIDENCE',
                              color='Year',
                              title='Argentina Consumer Confidence',
                              labels={'AR_CONSUMER_CONFIDENCE': 'Consumer Confidence Index', 
                                     'Month': 'Month',
                                     'Year': 'Year'},
                              markers=True)
        
        # Update layout to ensure proper display
        fig_consumer.update_layout(
            xaxis={'categoryorder': 'array', 
                   'categoryarray': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']}
        )
        
        st.plotly_chart(fig_consumer, use_container_width=True)
    
    # Create two columns for the second row
    col3, col4 = st.columns(2)
    
    # First column of second row - Inflation Comparison
    with col3:
        # Merge the inflation data
        inflation_comparison = pd.merge(recent_inflation_data, recent_bev_inflation_data, on='DATE', suffixes=('', '_bev'))
        
        # Rename columns for better legend labels
        inflation_comparison = inflation_comparison.rename(columns={
            'AR_INFLATION': 'YoY Inflation',
            'AR_CPI_ALCOHOLIC_BEV': 'YoY F&B Inflation'
        })
        
        # Create the inflation comparison graph
        fig_inflation = px.line(inflation_comparison, 
                              x='DATE', 
                              y=['YoY Inflation', 'YoY F&B Inflation'],
                              title='Argentina Inflation Comparison',
                              labels={'value': 'Inflation Rate (%)', 
                                     'variable': 'Type',
                                     'DATE': 'Date'},
                              color_discrete_map={'YoY F&B Inflation': 'blue', 
                                                'YoY Inflation': 'red'})
        
        # Update layout
        fig_inflation.update_layout(
            legend_title_text='',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig_inflation, use_container_width=True)
    
    # Second column of second row - Interest Rate
    with col4:
        # Create the interest rate graph
        fig_interest = px.line(recent_interest_data, 
                             x='DATE', 
                             y='AR_INTEREST_RATE',
                             title='Argentina Interest Rate',
                             labels={'AR_INTEREST_RATE': 'Interest Rate (%)', 
                                    'DATE': 'Date'})
        
        st.plotly_chart(fig_interest, use_container_width=True)
    
    # Create two columns for the third row
    col5, col6 = st.columns(2)
    
    # First column of third row - MoM Inflation
    with col5:
        # Create the MoM inflation graph
        fig_mom_inflation = px.bar(recent_mom_inflation_data, 
                                 x='DATE', 
                                 y='AR_MOM_INFLATION',
                                 title='Argentina Month-over-Month Inflation',
                                 labels={'AR_MOM_INFLATION': 'MoM Inflation Rate (%)', 
                                        'DATE': 'Date'})
        
        st.plotly_chart(fig_mom_inflation, use_container_width=True)
    
    # Second column of third row - Retail Sales
    with col6:
        # Create the retail sales graph
        fig_retail = px.bar(recent_retail_data, 
                           x='DATE', 
                           y='AR_RETAIL_SALES',
                           title='Argentina Retail Sales',
                           labels={'AR_RETAIL_SALES': 'Retail Sales Growth (%)', 
                                  'DATE': 'Date'},
                           color='AR_RETAIL_SALES',
                           color_discrete_sequence=['red', 'blue'],
                           color_discrete_map={True: 'red', False: 'blue'})
        
        # Update the color mapping based on positive/negative values
        fig_retail.update_traces(
            marker_color=['red' if x < 0 else 'blue' for x in recent_retail_data['AR_RETAIL_SALES']]
        )
        
        st.plotly_chart(fig_retail, use_container_width=True)
    
    # Create two columns for the fourth row
    col7, col8 = st.columns(2)
    
    # First column of fourth row - Unemployment Rate
    with col7:
        # Create the unemployment rate graph
        fig_unemployment = px.line(recent_unemployment_data, 
                                 x='DATE', 
                                 y='AR_UNEMPLOYMENT_RATE',
                                 title='Argentina Unemployment Rate',
                                 labels={'AR_UNEMPLOYMENT_RATE': 'Unemployment Rate (%)', 
                                        'DATE': 'Date'})
        
        st.plotly_chart(fig_unemployment, use_container_width=True)

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

# Panama Tab
with tab7:
    st.info("Panama beverage price data will be added soon.") 