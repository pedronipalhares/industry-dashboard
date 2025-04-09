import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Beef Analysis - Industry Dashboard",
    page_icon="🥩",
    layout="wide"
)

# Title and description
st.title("🥩 Beef Price Analysis")
st.markdown("""
This page shows the relationship between beef prices and cattle prices in Brazil over time.
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

# Create the visualization
st.write("### Beef vs Cattle Prices in Brazil")

# Create a figure with secondary y-axis
fig = px.line(beef_df, x='DATE', y='BR_BEEF_PRICES', 
              title='Beef and Cattle Prices in Brazil',
              labels={'BR_BEEF_PRICES': 'Beef Price (BRL/kg)', 'DATE': 'Date'},
              color_discrete_sequence=['#FF5733'])

# Add cattle price as a second line
fig.add_scatter(x=cattle_df['DATE'], y=cattle_df['BR_CATTLE_PRICE'], 
                name='Cattle Price', line=dict(color='#33A1FF'),
                yaxis='y2')

# Update layout for dual y-axis
fig.update_layout(
    yaxis2=dict(
        title='Cattle Price (BRL/kg)',
        overlaying='y',
        side='right'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    hovermode='x unified'
)

# Display the chart
st.plotly_chart(fig, use_container_width=True)

# Add some statistics
st.write("### Price Statistics")

col1, col2 = st.columns(2)

with col1:
    st.write("#### Beef Price Statistics")
    beef_stats = beef_df['BR_BEEF_PRICES'].describe()
    st.dataframe(beef_stats)

with col2:
    st.write("#### Cattle Price Statistics")
    cattle_stats = cattle_df['BR_CATTLE_PRICE'].describe()
    st.dataframe(cattle_stats)

# Add correlation analysis
st.write("### Price Correlation")
st.write("The correlation between beef and cattle prices indicates how closely these markets move together.")

# Calculate correlation
correlation = beef_df.set_index('DATE')['BR_BEEF_PRICES'].corr(cattle_df.set_index('DATE')['BR_CATTLE_PRICE'])
st.metric("Correlation Coefficient", f"{correlation:.2f}")

# Interpretation
if correlation > 0.7:
    st.success("Strong positive correlation: Beef and cattle prices tend to move together.")
elif correlation > 0.3:
    st.info("Moderate positive correlation: There is some relationship between beef and cattle prices.")
else:
    st.warning("Weak correlation: Beef and cattle prices show little relationship.") 