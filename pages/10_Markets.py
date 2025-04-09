import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime, timedelta

# Set page config
st.set_page_config(
    page_title="Markets - Industry Dashboard",
    page_icon="📈",
    layout="wide"
)

# Title and description
st.title("📈 Markets")
st.markdown("""
This page shows market data including stock prices and short positions.
""")

# Load the data
@st.cache_data
def load_stock_data(stock_code):
    file_path = Path(f"datasets/BR_{stock_code}_PRICE.csv")
    df = pd.read_csv(file_path)
    df['DATE'] = pd.to_datetime(df['DATE'])
    
    # Filter last 2 years
    two_years_ago = datetime.now() - timedelta(days=2*365)
    df = df[df['DATE'] >= two_years_ago]
    
    return df

# Create tabs for different sections
tab1, tab2 = st.tabs(["Prices", "Short"])

# Prices Tab
with tab1:
    # Load data for each stock
    abev_df = load_stock_data("ABEV3")
    beef_df = load_stock_data("BEEF3")
    brfs_df = load_stock_data("BRFS3")
    caml_df = load_stock_data("CAML3")
    jbss_df = load_stock_data("JBSS3")
    mdia_df = load_stock_data("MDIA3")
    mfrg_df = load_stock_data("MRFG3")
    raiz_df = load_stock_data("RAIZ4")
    slce_df = load_stock_data("SLCE3")
    smto_df = load_stock_data("SMTO3")
    soja_df = load_stock_data("SOJA3")
    tten_df = load_stock_data("TTEN3")
    
    # Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        fig_abev = px.line(abev_df, 
                          x='DATE', 
                          y='BR_ABEV3_PRICE',
                          title='Ambev (ABEV3) Stock Price',
                          labels={'BR_ABEV3_PRICE': 'Price (BRL)', 
                                 'DATE': 'Date'})
        st.plotly_chart(fig_abev, use_container_width=True)
    
    with col2:
        fig_beef = px.line(beef_df, 
                          x='DATE', 
                          y='BR_BEEF3_PRICE',
                          title='Minerva (BEEF3) Stock Price',
                          labels={'BR_BEEF3_PRICE': 'Price (BRL)', 
                                 'DATE': 'Date'})
        st.plotly_chart(fig_beef, use_container_width=True)
    
    # Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        fig_brfs = px.line(brfs_df, 
                          x='DATE', 
                          y='BR_BRFS3_PRICE',
                          title='BRF (BRFS3) Stock Price',
                          labels={'BR_BRFS3_PRICE': 'Price (BRL)', 
                                 'DATE': 'Date'})
        st.plotly_chart(fig_brfs, use_container_width=True)
    
    with col2:
        fig_caml = px.line(caml_df, 
                          x='DATE', 
                          y='BR_CAML3_PRICE',
                          title='Camil (CAML3) Stock Price',
                          labels={'BR_CAML3_PRICE': 'Price (BRL)', 
                                 'DATE': 'Date'})
        st.plotly_chart(fig_caml, use_container_width=True)
    
    # Row 3
    col1, col2 = st.columns(2)
    
    with col1:
        fig_jbss = px.line(jbss_df, 
                          x='DATE', 
                          y='BR_JBSS3_PRICE',
                          title='JBS (JBSS3) Stock Price',
                          labels={'BR_JBSS3_PRICE': 'Price (BRL)', 
                                 'DATE': 'Date'})
        st.plotly_chart(fig_jbss, use_container_width=True)
    
    with col2:
        fig_mdia = px.line(mdia_df, 
                          x='DATE', 
                          y='BR_MDIA3_PRICE',
                          title='M. Dias Branco (MDIA3) Stock Price',
                          labels={'BR_MDIA3_PRICE': 'Price (BRL)', 
                                 'DATE': 'Date'})
        st.plotly_chart(fig_mdia, use_container_width=True)
    
    # Row 4
    col1, col2 = st.columns(2)
    
    with col1:
        fig_mfrg = px.line(mfrg_df, 
                          x='DATE', 
                          y='BR_MRFG3_PRICE',
                          title='Marfrig (MRFG3) Stock Price',
                          labels={'BR_MRFG3_PRICE': 'Price (BRL)', 
                                 'DATE': 'Date'})
        st.plotly_chart(fig_mfrg, use_container_width=True)
    
    with col2:
        fig_raiz = px.line(raiz_df, 
                          x='DATE', 
                          y='BR_RAIZ4_PRICE',
                          title='Raízen (RAIZ4) Stock Price',
                          labels={'BR_RAIZ4_PRICE': 'Price (BRL)', 
                                 'DATE': 'Date'})
        st.plotly_chart(fig_raiz, use_container_width=True)
    
    # Row 5
    col1, col2 = st.columns(2)
    
    with col1:
        fig_slce = px.line(slce_df, 
                          x='DATE', 
                          y='BR_SLCE3_PRICE',
                          title='SLC Agrícola (SLCE3) Stock Price',
                          labels={'BR_SLCE3_PRICE': 'Price (BRL)', 
                                 'DATE': 'Date'})
        st.plotly_chart(fig_slce, use_container_width=True)
    
    with col2:
        fig_smto = px.line(smto_df, 
                          x='DATE', 
                          y='BR_SMTO3_PRICE',
                          title='São Martinho (SMTO3) Stock Price',
                          labels={'BR_SMTO3_PRICE': 'Price (BRL)', 
                                 'DATE': 'Date'})
        st.plotly_chart(fig_smto, use_container_width=True)
    
    # Row 6
    col1, col2 = st.columns(2)
    
    with col1:
        fig_soja = px.line(soja_df, 
                          x='DATE', 
                          y='BR_SOJA3_PRICE',
                          title='Boa Safra (SOJA3) Stock Price',
                          labels={'BR_SOJA3_PRICE': 'Price (BRL)', 
                                 'DATE': 'Date'})
        st.plotly_chart(fig_soja, use_container_width=True)
    
    with col2:
        fig_tten = px.line(tten_df, 
                          x='DATE', 
                          y='BR_TTEN3_PRICE',
                          title='Tereos (TTEN3) Stock Price',
                          labels={'BR_TTEN3_PRICE': 'Price (BRL)', 
                                 'DATE': 'Date'})
        st.plotly_chart(fig_tten, use_container_width=True)

# Short Tab
with tab2:
    st.info("Short position data will be added soon.") 