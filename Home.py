import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Industry Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for cards
st.markdown("""
<style>
.market-card {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-left: 5px solid #4CAF50;
}
.market-card h3 {
    color: #2E7D32;
    margin-top: 0;
}
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("📊 Industry Dashboard")
st.markdown("""
Welcome to the Industry Dashboard! This comprehensive platform provides real-time insights and analysis across multiple industries, helping you make informed decisions in today's dynamic markets.
""")

# Create columns for the market sections
col1, col2, col3 = st.columns(3)

# First column
with col1:
    # Beef Card
    st.markdown("""
    <div class="market-card">
        <h3>🥩 Beef</h3>
        <p><strong>Discover the complete beef supply chain from farm to table.</strong> Our dashboard tracks live cattle and beef prices across major global markets including Brazil, U.S., China, Argentina, and Uruguay. Analyze price trends, market dynamics, and identify opportunities in this essential protein market.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chicken Card
    st.markdown("""
    <div class="market-card">
        <h3>🍗 Chicken</h3>
        <p><strong>Stay ahead in the poultry industry with comprehensive market intelligence.</strong> Monitor live chicken and processed chicken prices across Brazil, U.S., China, EU, and Saudi Arabia. Track production trends, consumption patterns, and trade flows to optimize your poultry business strategy.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pork Card
    st.markdown("""
    <div class="market-card">
        <h3>🥓 Pork</h3>
        <p><strong>Navigate the complex pork market with confidence.</strong> Our dashboard provides detailed analysis of pork prices and market dynamics in Brazil, U.S., China, and EU. From live hog prices to processed pork products, gain insights into this versatile protein market.</p>
    </div>
    """, unsafe_allow_html=True)

# Second column
with col2:
    # Beverages Card
    st.markdown("""
    <div class="market-card">
        <h3>🥤 Beverages</h3>
        <p><strong>Quench your thirst for beverage market knowledge.</strong> Explore comprehensive data on beverage prices and consumption trends across Brazil, Argentina, Dominican Republic, Guatemala, Chile, and Canada. From soft drinks to alcoholic beverages, track market developments and consumer preferences.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Biodiesel Card
    st.markdown("""
    <div class="market-card">
        <h3>🛢️ Biodiesel</h3>
        <p><strong>Power your understanding of the renewable energy sector.</strong> Our dashboard tracks biodiesel production, prices, and market developments in Brazil, a global leader in biofuels. Monitor feedstock prices, production capacity, and policy impacts on this growing renewable energy market.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Ethanol Card
    st.markdown("""
    <div class="market-card">
        <h3>⛽ Ethanol</h3>
        <p><strong>Fuel your ethanol market analysis with real-time data.</strong> Monitor ethanol prices and market trends in Brazil and U.S., the world's largest ethanol producers. Track production, consumption, and trade flows to identify opportunities in this renewable fuel market.</p>
    </div>
    """, unsafe_allow_html=True)

# Third column
with col3:
    # Agribusiness Card
    st.markdown("""
    <div class="market-card">
        <h3>🌾 Agribusiness</h3>
        <p><strong>Cultivate success with comprehensive agribusiness insights.</strong> Access detailed data on agricultural commodity prices, investment funds performance, and supply & demand analysis. From grains to specialty crops, our dashboard helps you navigate the complex world of agribusiness.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Markets Card
    st.markdown("""
    <div class="market-card">
        <h3>📈 Markets</h3>
        <p><strong>Chart your course through financial markets with precision.</strong> View real-time market prices and short positions across various commodities and assets. Identify market trends, analyze trading volumes, and discover investment opportunities in global markets.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Macro Card
    st.markdown("""
    <div class="market-card">
        <h3>📊 Macro</h3>
        <p><strong>See the big picture with macroeconomic indicators.</strong> Explore comprehensive data on economic growth, inflation, interest rates, and currency exchange rates for Brazil, U.S., and Argentina. Understand how broader economic trends impact industry performance.</p>
    </div>
    """, unsafe_allow_html=True)

# Add a divider
st.divider()

# Add a footer with contact information
st.markdown("""
---
**Contact:** [Your Contact Information]
""") 