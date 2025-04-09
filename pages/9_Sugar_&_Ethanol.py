import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import datetime

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
    st.header("Brazil CONSECANA Costs")
    
    # Function to load and process data
    def load_consecana_data(file_path):
        df = pd.read_csv(file_path)
        df['DATE'] = pd.to_datetime(df['DATE'])
        df['Year'] = df['DATE'].dt.year
        df['Month'] = df['DATE'].dt.month
        
        # Create a month name column for better display
        month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                       7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        df['Month_Name'] = df['Month'].map(month_names)
        
        # Create a custom month order starting from April
        df['Month_Order'] = df['Month'].apply(lambda x: x-3 if x >= 4 else x+9)
        
        # Create Harvest Year (starts in April)
        df['Harvest_Year'] = df.apply(lambda row: row['Year'] if row['Month'] >= 4 else row['Year'] - 1, axis=1)
        
        # Filter for last three harvest years
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        current_harvest_year = current_year if current_month >= 4 else current_year - 1
        df = df[df['Harvest_Year'] >= current_harvest_year - 2]
        
        return df
    
    # Load data
    acc_data = load_consecana_data("/Users/guilhermepalhares/Codes/industry-dashboard/datasets/BR_CONSECANA_ACC.csv")
    monthly_data = load_consecana_data("/Users/guilhermepalhares/Codes/industry-dashboard/datasets/BR_CONSECANA_MONTHLY.csv")
    
    # Create two columns for the plots
    col1, col2 = st.columns(2)
    
    # Plot 1: BR_CONSECANA_ACC
    with col1:
        fig1 = px.line(acc_data, 
                       x='Month_Name', 
                       y='BR_CONSECANA_ACC',
                       color='Harvest_Year',
                       title='Brazil CONSECANA Accumulated',
                       labels={'BR_CONSECANA_ACC': 'BR CONSECANA ACC', 'Month_Name': 'Month', 'Harvest_Year': 'Harvest Year'},
                       category_orders={'Month_Name': ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']})
        
        fig1.update_layout(
            xaxis_title="Month (April to March)",
            yaxis_title="BR CONSECANA ACC",
            legend_title="Harvest Year"
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    # Plot 2: BR_CONSECANA_MONTHLY
    with col2:
        fig2 = px.line(monthly_data, 
                       x='Month_Name', 
                       y='BR_CONSECANA_MONTHLY',
                       color='Harvest_Year',
                       title='Brazil CONSECANA Monthly',
                       labels={'BR_CONSECANA_MONTHLY': 'BR CONSECANA Monthly', 'Month_Name': 'Month', 'Harvest_Year': 'Harvest Year'},
                       category_orders={'Month_Name': ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']})
        
        fig2.update_layout(
            xaxis_title="Month (April to March)",
            yaxis_title="BR CONSECANA Monthly",
            legend_title="Harvest Year"
        )
        
        st.plotly_chart(fig2, use_container_width=True)

# U.S. Tab
with tab9:
    st.info("U.S. data will be added soon.")    