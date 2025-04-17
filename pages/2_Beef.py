import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
    cattle_cycle_path = Path("datasets/BR_CATTLE_CYCLE.csv")
    slaughter_path = Path("datasets/BR_SLAUGHTER_CATTLE_MONTHLY.csv")
    
    beef_df = pd.read_csv(beef_price_path)
    cattle_df = pd.read_csv(cattle_price_path)
    cattle_herd_df = pd.read_csv(cattle_herd_path)
    ar_food_df = pd.read_csv(ar_food_path)
    au_cattle_df = pd.read_csv(au_cattle_path)
    cattle_cycle_df = pd.read_csv(cattle_cycle_path)
    slaughter_df = pd.read_csv(slaughter_path)
    
    # Convert date columns to datetime
    beef_df['DATE'] = pd.to_datetime(beef_df['DATE'])
    cattle_df['DATE'] = pd.to_datetime(cattle_df['DATE'])
    cattle_herd_df['Date'] = pd.to_datetime(cattle_herd_df['Date'])
    ar_food_df['Date'] = pd.to_datetime(ar_food_df['Date'])
    au_cattle_df['DATE'] = pd.to_datetime(au_cattle_df['DATE'])
    slaughter_df['Date'] = pd.to_datetime(slaughter_df['Date'])
    
    # Extract month and year for filtering and coloring
    ar_food_df['Month'] = ar_food_df['Date'].dt.strftime('%b')
    ar_food_df['Year'] = ar_food_df['Date'].dt.year
    
    au_cattle_df['Month'] = au_cattle_df['DATE'].dt.strftime('%b')
    au_cattle_df['Year'] = au_cattle_df['DATE'].dt.year
    
    # Calculate the ratio between beef prices and cattle prices
    # Convert cattle price from R$/@ (15kg) to R$/kg
    beef_df = beef_df.merge(cattle_df, on='DATE', how='inner')
    beef_df['CATTLE_PRICE_PER_KG'] = beef_df['BR_CATTLE_PRICE'] / 15
    beef_df['PRICE_RATIO'] = beef_df['BR_BEEF_PRICES'] / beef_df['CATTLE_PRICE_PER_KG']
    
    # Process cattle cycle data
    # Create a date column from Year and Quarter
    cattle_cycle_df['Date'] = pd.to_datetime(cattle_cycle_df['Year'].astype(str) + '-' + 
                                            (cattle_cycle_df['Quarter'] * 3).astype(str) + '-01')
    
    # Calculate LTM (Last Twelve Months) averages
    cattle_cycle_df = cattle_cycle_df.sort_values('Date')
    cattle_cycle_df['LTM_Female_Slaughtered'] = cattle_cycle_df['Percentage_of_Females_Slaughtered'].rolling(window=4).mean()
    cattle_cycle_df['LTM_Calf_Cattle_Ratio'] = cattle_cycle_df['Calf_Cattle_Ratio'].rolling(window=4).mean()
    
    # Process slaughter data
    # Calculate YoY growth for Kilograms
    slaughter_df = slaughter_df.sort_values('Date')
    slaughter_df['Year'] = slaughter_df['Date'].dt.year
    slaughter_df['Month'] = slaughter_df['Date'].dt.month
    
    # Calculate YoY growth
    slaughter_df['Kilograms_LY'] = slaughter_df.groupby('Month')['Kilograms'].shift(1)
    slaughter_df['Kilograms_YoY_Growth'] = (slaughter_df['Kilograms'] - slaughter_df['Kilograms_LY']) / slaughter_df['Kilograms_LY'] * 100
    
    # Calculate quarterly beef to cattle ratio
    beef_df['Year'] = beef_df['DATE'].dt.year
    beef_df['Quarter'] = beef_df['DATE'].dt.quarter
    beef_df['YearQuarter'] = beef_df['Year'].astype(str) + 'Q' + beef_df['Quarter'].astype(str)
    
    # Calculate quarterly average ratio
    quarterly_ratio = beef_df.groupby('YearQuarter')['PRICE_RATIO'].mean().reset_index()
    quarterly_ratio['Year'] = quarterly_ratio['YearQuarter'].str[:4].astype(int)
    quarterly_ratio['Quarter'] = quarterly_ratio['YearQuarter'].str[5:].astype(int)
    
    return beef_df, cattle_df, cattle_herd_df, ar_food_df, au_cattle_df, cattle_cycle_df, slaughter_df, quarterly_ratio

beef_df, cattle_df, cattle_herd_df, ar_food_df, au_cattle_df, cattle_cycle_df, slaughter_df, quarterly_ratio = load_data()

# Create tabs for different countries
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Brazil", "U.S.", "China", "Argentina", "Uruguay", "Australia"])

# Brazil Tab
with tab1:
    # Create sections for different aspects of the Brazilian beef market
    # Domestic Market Section
    domestic_section = st.expander("Domestic Market", expanded=True)
    with domestic_section:
        # Create two columns for side-by-side graphs
        col1, col2 = st.columns(2)
        
        # Beef price graph
        with col1:
            # Filter for the last three years
            current_date = datetime.now()
            three_years_ago = current_date.replace(year=current_date.year - 3)
            recent_beef_data = beef_df[beef_df['DATE'] >= three_years_ago]
            
            fig_beef = px.line(recent_beef_data, x='DATE', y='BR_BEEF_PRICES', 
                               title='Beef Prices in Brazil - Last 3 Years',
                               labels={'BR_BEEF_PRICES': 'Price (BRL/kg)', 'DATE': 'Date'})
            st.plotly_chart(fig_beef, use_container_width=True)
            
            # Price ratio graph (Beef price / Cattle price)
            # Filter for the last twelve months
            current_date = datetime.now()
            twelve_months_ago = current_date.replace(year=current_date.year - 1)
            recent_ratio_data = beef_df[beef_df['DATE'] >= twelve_months_ago]
            
            fig_ratio = px.line(recent_ratio_data, x='DATE', y='PRICE_RATIO',
                               title='Beef to Cattle Price Ratio (R$/kg) - Last 12 Months',
                               labels={'PRICE_RATIO': 'Ratio (Beef/Cattle)', 'DATE': 'Date'})
            st.plotly_chart(fig_ratio, use_container_width=True)
        
        # Cattle price graph
        with col2:
            # Filter for the last three years
            recent_cattle_data = cattle_df[cattle_df['DATE'] >= three_years_ago]
            
            fig_cattle = px.line(recent_cattle_data, x='DATE', y='BR_CATTLE_PRICE', 
                                 title='Cattle Prices in Brazil - Last 3 Years',
                                 labels={'BR_CATTLE_PRICE': 'Price (BRL/@)', 'DATE': 'Date'})
            st.plotly_chart(fig_cattle, use_container_width=True)
            
            # Quarterly beef to cattle ratio
            # Filter for the last five years
            current_year = datetime.now().year
            five_years_ago = current_year - 5
            recent_quarterly_ratio = quarterly_ratio[quarterly_ratio['Year'] >= five_years_ago]
            
            # Calculate y-axis range with some padding
            y_min = recent_quarterly_ratio['PRICE_RATIO'].min() * 0.95  # 5% padding below min
            y_max = recent_quarterly_ratio['PRICE_RATIO'].max() * 1.05  # 5% padding above max
            
            # Create bar chart for quarterly ratio
            fig_quarterly_ratio = px.bar(recent_quarterly_ratio, 
                                        x='YearQuarter', 
                                        y='PRICE_RATIO',
                                        title='Quarterly Beef to Cattle Ratio (R$/kg)',
                                        labels={'PRICE_RATIO': 'Ratio (Beef/Cattle)', 'YearQuarter': 'Quarter'})
            
            # Update layout with trimmed y-axis
            fig_quarterly_ratio.update_layout(
                xaxis=dict(
                    title='',
                    showline=True,
                    linewidth=1,
                    linecolor='black',
                    showgrid=False
                ),
                yaxis=dict(
                    title='',
                    showline=True,
                    linewidth=1,
                    linecolor='black',
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='lightgray',
                    range=[y_min, y_max]  # Set trimmed y-axis range
                ),
                plot_bgcolor='white'
            )
            
            st.plotly_chart(fig_quarterly_ratio, use_container_width=True)
    
    # Export Market Section
    export_section = st.expander("Export Market", expanded=True)
    with export_section:
        st.info("Export market data will be added soon.")
    
    # Cycle Section
    cycle_section = st.expander("Cycle", expanded=True)
    with cycle_section:
        # Create two columns for side-by-side graphs
        col1, col2 = st.columns(2)
        
        # Cattle cycle indicators graph
        with col1:
            fig_cycle = go.Figure()
            
            # Add LTM Female Slaughtered line
            fig_cycle.add_trace(
                go.Scatter(
                    x=cattle_cycle_df['Date'],
                    y=cattle_cycle_df['LTM_Female_Slaughtered'] * 100,  # Convert to percentage
                    name='LTM Female Slaughtered % (LHS)',
                    line=dict(color='blue')
                )
            )
            
            # Add LTM Calf Cattle Ratio line on secondary y-axis
            fig_cycle.add_trace(
                go.Scatter(
                    x=cattle_cycle_df['Date'],
                    y=cattle_cycle_df['LTM_Calf_Cattle_Ratio'],
                    name='LTM Calf/Cattle Ratio (RHS)',
                    line=dict(color='red'),
                    yaxis='y2'
                )
            )
            
            # Update layout for dual y-axes with improved formatting
            fig_cycle.update_layout(
                title='Cattle Cycle Indicators - LTM Averages',
                xaxis=dict(
                    title='',
                    showline=True,
                    linewidth=1,
                    linecolor='black',
                    showgrid=False
                ),
                yaxis=dict(
                    title='',
                    titlefont=dict(color='blue'),
                    showline=True,
                    linewidth=1,
                    linecolor='black',
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='lightgray',
                    tickformat='.1f'  # Format as percentage with 1 decimal place
                ),
                yaxis2=dict(
                    title='',
                    titlefont=dict(color='red'),
                    overlaying='y',
                    side='right',
                    showline=True,
                    linewidth=1,
                    linecolor='black',
                    showgrid=False,
                    tickformat='.3f'  # Format with 3 decimal places
                ),
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                ),
                plot_bgcolor='white',
                margin=dict(b=80)  # Add bottom margin to accommodate the legend
            )
            
            st.plotly_chart(fig_cycle, use_container_width=True)
            
            # Cattle herd graph
            fig_herd = px.line(cattle_herd_df, x='Date', y='Cattle', 
                               title='Cattle Herd in Brazil',
                               labels={'Cattle': 'Number of Cattle', 'Date': 'Year'})
            st.plotly_chart(fig_herd, use_container_width=True)
        
        # Cattle price and calf ratio LTM graph
        with col2:
            # Calculate LTM average for Real_Cattle_Price
            cattle_cycle_df['LTM_Real_Cattle_Price'] = cattle_cycle_df['Real_Cattle_Price'].rolling(window=4).mean()
            
            # Create the dual y-axis chart
            fig_price_ratio = go.Figure()
            
            # Add LTM Real Cattle Price line
            fig_price_ratio.add_trace(
                go.Scatter(
                    x=cattle_cycle_df['Date'],
                    y=cattle_cycle_df['LTM_Real_Cattle_Price'],
                    name='LTM Real Cattle Price (LHS)',
                    line=dict(color='blue')
                )
            )
            
            # Add LTM Calf Cattle Ratio line on secondary y-axis
            fig_price_ratio.add_trace(
                go.Scatter(
                    x=cattle_cycle_df['Date'],
                    y=cattle_cycle_df['LTM_Calf_Cattle_Ratio'],
                    name='LTM Calf/Cattle Ratio (RHS)',
                    line=dict(color='red'),
                    yaxis='y2'
                )
            )
            
            # Update layout for dual y-axes with improved formatting
            fig_price_ratio.update_layout(
                title='Cattle Price and Calf Ratio - LTM Averages',
                xaxis=dict(
                    title='',
                    showline=True,
                    linewidth=1,
                    linecolor='black',
                    showgrid=False
                ),
                yaxis=dict(
                    title='',
                    titlefont=dict(color='blue'),
                    showline=True,
                    linewidth=1,
                    linecolor='black',
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='lightgray',
                    tickformat='.2f'  # Format with 2 decimal places
                ),
                yaxis2=dict(
                    title='',
                    titlefont=dict(color='red'),
                    overlaying='y',
                    side='right',
                    showline=True,
                    linewidth=1,
                    linecolor='black',
                    showgrid=False,
                    tickformat='.3f'  # Format with 3 decimal places
                ),
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                ),
                plot_bgcolor='white',
                margin=dict(b=80)  # Add bottom margin to accommodate the legend
            )
            
            st.plotly_chart(fig_price_ratio, use_container_width=True)
            
            # YoY growth of Kilograms
            # Filter for recent data
            recent_slaughter = slaughter_df[slaughter_df['Year'] >= current_year - 5]
            
            # Create bar chart with conditional coloring
            fig_yoy_growth = go.Figure()
            
            # Add bars with conditional coloring
            fig_yoy_growth.add_trace(
                go.Bar(
                    x=recent_slaughter['Date'],
                    y=recent_slaughter['Kilograms_YoY_Growth'],
                    name='Kilograms YoY Growth',
                    marker_color=recent_slaughter['Kilograms_YoY_Growth'].apply(
                        lambda x: 'red' if x < 0 else 'blue'
                    )
                )
            )
            
            # Update layout
            fig_yoy_growth.update_layout(
                title='Cattle Slaughter - Kilograms YoY Growth',
                xaxis=dict(
                    title='',
                    showline=True,
                    linewidth=1,
                    linecolor='black',
                    showgrid=False
                ),
                yaxis=dict(
                    title='',
                    showline=True,
                    linewidth=1,
                    linecolor='black',
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='lightgray',
                    tickformat='.1f'  # Format as percentage with 1 decimal place
                ),
                plot_bgcolor='white'
            )
            
            st.plotly_chart(fig_yoy_growth, use_container_width=True)

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