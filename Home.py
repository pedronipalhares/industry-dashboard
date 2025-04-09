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

# Title and description
st.title("📊 Industry Dashboard")
st.markdown("""
Welcome to the Industry Dashboard! This dashboard provides insights into various industries including:
- 🥩 Beef
- 🍗 Chicken
- 🥓 Pork
- 🥤 Beverages
- 🛢️ Biodiesel
- ⛽ Ethanol
- 🌾 Agribusiness
- 📈 Markets
- 📊 Macro
""")

# Add a divider
st.divider()

# Add a footer with contact information
st.markdown("""
---
**Contact:** [Your Contact Information]
""") 