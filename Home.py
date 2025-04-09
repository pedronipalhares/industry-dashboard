import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from auth import is_authenticated, logout_user, require_auth

# Set page config
st.set_page_config(
    page_title="Industry Dashboard",
    page_icon="📊",
    layout="wide"
)

# Check authentication
if not is_authenticated():
    st.switch_page("pages/0_Login.py")

# Custom CSS for cards
st.markdown("""
<style>
.market-card {
    background-color: #ffffff;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border: 1px solid #000000;
}
.market-card h3 {
    color: #000000;
    margin-top: 0;
    margin-bottom: 15px;
    border-bottom: 2px solid #000000;
    padding-bottom: 5px;
}
.tab-list {
    list-style-type: none;
    padding-left: 0;
    margin: 0;
}
.tab-list li {
    padding: 5px 0;
    border-bottom: 1px solid #e0e0e0;
}
.tab-list li:last-child {
    border-bottom: none;
}
</style>
""", unsafe_allow_html=True)

# Add logout button in the top right
col1, col2, col3 = st.columns([1, 3, 1])
with col3:
    if st.button("Logout"):
        logout_user()

# Title and description
st.title("📊 Industry Dashboard")
st.markdown(f"""
Welcome to the Industry Dashboard, {st.session_state.get('username', 'User')}! This comprehensive platform provides real-time insights and analysis across multiple industries, helping you make informed decisions in today's dynamic markets.
""")

# Create columns for the market sections
col1, col2, col3 = st.columns(3)

# First column
with col1:
    # Beef Card
    st.markdown("""
    <div class="market-card">
        <h3>🥩 Beef</h3>
        <ul class="tab-list">
            <li>• Prices</li>
            <li>• Production</li>
            <li>• Trade Flow</li>
            <li>• Supply & Demand</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Chicken Card
    st.markdown("""
    <div class="market-card">
        <h3>🍗 Chicken</h3>
        <ul class="tab-list">
            <li>• Prices</li>
            <li>• Production</li>
            <li>• Trade Flow</li>
            <li>• Supply & Demand</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Pork Card
    st.markdown("""
    <div class="market-card">
        <h3>🥓 Pork</h3>
        <ul class="tab-list">
            <li>• Prices</li>
            <li>• Production</li>
            <li>• Trade Flow</li>
            <li>• Supply & Demand</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Table Eggs Card
    st.markdown("""
    <div class="market-card">
        <h3>🥚 Table Eggs</h3>
        <ul class="tab-list">
            <li>• Prices</li>
            <li>• Production</li>
            <li>• Trade Flow</li>
            <li>• Supply & Demand</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Second column
with col2:
    # Beverages Card
    st.markdown("""
    <div class="market-card">
        <h3>🥤 Beverages</h3>
        <ul class="tab-list">
            <li>• Prices</li>
            <li>• Production</li>
            <li>• Trade Flow</li>
            <li>• Market Share</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Cookies & Pasta Card
    st.markdown("""
    <div class="market-card">
        <h3>🍪 Cookies & Pasta</h3>
        <ul class="tab-list">
            <li>• Inflation</li>
            <li>• Costs</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Biodiesel Card
    st.markdown("""
    <div class="market-card">
        <h3>🛢️ Biodiesel</h3>
        <ul class="tab-list">
            <li>• Prices</li>
            <li>• Production</li>
            <li>• Trade Flow</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Sugar and Ethanol Card
    st.markdown("""
    <div class="market-card">
        <h3>⛽ Sugar and Ethanol</h3>
        <ul class="tab-list">
            <li>• Prices</li>
            <li>• Production</li>
            <li>• Trade Flow</li>
            <li>• Supply & Demand</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Third column
with col3:
    # Agribusiness Card
    st.markdown("""
    <div class="market-card">
        <h3>🌾 Agribusiness</h3>
        <ul class="tab-list">
            <li>• Prices</li>
            <li>• Funds</li>
            <li>• Supply & Demand</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Markets Card
    st.markdown("""
    <div class="market-card">
        <h3>📈 Markets</h3>
        <ul class="tab-list">
            <li>• Commodities</li>
            <li>• Currencies</li>
            <li>• Stocks</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Macro Card
    st.markdown("""
    <div class="market-card">
        <h3>📊 Macro</h3>
        <ul class="tab-list">
            <li>• GDP</li>
            <li>• Inflation</li>
            <li>• Interest Rates</li>
            <li>• Exchange Rates</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Add a divider
st.divider()

# Add a footer with contact information
st.markdown("""
---
**Contact:** [Your Contact Information]
""") 