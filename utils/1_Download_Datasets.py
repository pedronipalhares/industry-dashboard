import streamlit as st
import pandas as pd
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Download Datasets - Industry Dashboard",
    page_icon="📥",
    layout="wide"
)

# Title and description
st.title("📥 Download Datasets")
st.markdown("""
Download any dataset from the table below by clicking the download button next to it.
""")

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