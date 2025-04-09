import streamlit as st
import os
import pandas as pd
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
Welcome to the Industry Dashboard! This application provides access to various industry-related datasets and analytics.

## Available Features

### 📥 Dataset Downloads
Access and download various industry datasets including:
- Agricultural commodity prices
- Currency exchange rates
- Economic indicators
- Production data
- Market prices
- And more...

### 📈 Analytics (Coming Soon)
- Data visualization
- Trend analysis
- Market insights
- Custom reports

## Getting Started
Use the sidebar to navigate between different sections of the dashboard.
""")

# Add some metrics or key information
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Available Datasets",
        value="100+",
        help="Total number of datasets available for download"
    )

with col2:
    st.metric(
        label="Data Categories",
        value="15+",
        help="Different categories of industry data"
    )

with col3:
    st.metric(
        label="Countries Covered",
        value="10+",
        help="Number of countries with data coverage"
    )

# Get all CSV files from the datasets directory
datasets_dir = Path("datasets")
csv_files = list(datasets_dir.glob("*.csv"))

# Create a table with dataset information
st.write("### Available Datasets")

# Create columns for the table header
col1, col2 = st.columns([3, 1])
with col1:
    st.write("**Dataset Name**")
with col2:
    st.write("**Download**")

# Create rows for each dataset
for csv_file in sorted(csv_files):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.write(csv_file.name)
    
    with col2:
        # Read the CSV file
        df = pd.read_csv(csv_file)
        csv = df.to_csv(index=False)
        
        # Create download button
        st.download_button(
            label="📥 Download",
            data=csv,
            file_name=csv_file.name,
            mime="text/csv",
            key=f"download_{csv_file.name}"
        ) 