import streamlit as st
import pandas as pd

def render_download_section(datasets):
    st.header("Data Download Center")
    
    st.markdown("""
    This page provides access to all datasets used in the dashboard. Select the time period and download any dataset you need.
    """)
    
    # Offer different date ranges for download
    download_range = st.radio(
        "Select data range:",
        ["Last 5 years (default)", "All available data", "Last 12 months"]
    )
    
    # Create a table with all available datasets and download buttons in the same row
    st.subheader("Available Datasets")
    
    # Create columns for the dataset table with embedded download buttons
    col1, col2, col3, col4 = st.columns([2, 4, 1, 1.5])
    
    # Table Headers
    with col1:
        st.markdown("**Dataset**")
    with col2:
        st.markdown("**Description**")
    with col3:
        st.markdown("**Rows**")
    with col4:
        st.markdown("**Download**")
    
    # Separator
    st.markdown("---")
    
    # Render each dataset section
    for dataset_info in datasets:
        if dataset_info['df'] is not None and not dataset_info['df'].empty:
            st.markdown("---")
            col1, col2, col3, col4 = st.columns([2, 4, 1, 1.5])
            
            with col1:
                st.markdown(f"**{dataset_info['name']}**")
            with col2:
                st.markdown(f"{dataset_info['description']} ({dataset_info['df']['Date'].min().strftime('%b %Y')} to {dataset_info['df']['Date'].max().strftime('%b %Y')})")
            with col3:
                st.markdown(f"{len(dataset_info['df'])}")
            with col4:
                csv_data = dataset_info['df'][dataset_info['columns']].to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=dataset_info['filename'],
                    mime="text/csv",
                ) 