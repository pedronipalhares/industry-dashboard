import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime

@st.cache_data
def load_layer_herd_data():
    df = pd.read_csv('datasets/broiler_breeder_layer_herd_monthly.csv')
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str), format='%Y-%b')
    df = df.sort_values('Date')
    return df

@st.cache_data
def load_eggs_data():
    df = pd.read_csv('datasets/broiler_hatching_eggs_monthly.csv')
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str), format='%Y-%b')
    df = df.sort_values('Date')
    return df

@st.cache_data
def load_mortality_data():
    df = pd.read_csv('datasets/layer_mortality_rates.csv')
    # Check if the file has 'Year' and 'Month' columns or a 'Projected_Date' column
    if 'Projected_Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Projected_Date'])
    else:
        df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str), format='%Y-%b')
    df = df.sort_values('Date')
    return df

@st.cache_data
def load_egg_break_data():
    df = pd.read_csv('datasets/egg_break_analysis.csv')
    
    # Handle different column naming conventions
    if 'Date_produced' in df.columns:
        # Use the producer's date as the main date
        df['Date'] = pd.to_datetime(df['Date_produced'])
    elif 'Date' in df.columns:
        # If the file already has a 'Date' column, use it
        df['Date'] = pd.to_datetime(df['Date'])
    else:
        # Try to construct the date from Year/Month columns if they exist
        month_col = None
        if 'Month' in df.columns:
            month_col = 'Month'
        elif 'Month_produced' in df.columns:
            month_col = 'Month_produced'
            
        if 'Year' in df.columns and month_col is not None:
            df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df[month_col].astype(str), format='%Y-%b')
        else:
            # If no useful date/time columns are found, create a dummy date
            print("WARNING: No date columns found in egg_break_analysis.csv")
            df['Date'] = pd.to_datetime('2020-01-01')  # Default date as fallback
    
    # Ensure expected columns exist
    required_columns = ['Break_Ratio', 'Rolling_15M_Break_Ratio']
    for col in required_columns:
        if col not in df.columns:
            print(f"WARNING: Missing expected column {col} in egg_break_analysis.csv")
            df[col] = 0  # Add a placeholder column
    
    df = df.sort_values('Date')
    return df

@st.cache_data
def load_egg_set_data():
    df = pd.read_csv('datasets/egg_set_weekly_data.csv')
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-W' + df['Week'].astype(str).str.zfill(2) + '-1', format='%Y-W%W-%w')
    return df

@st.cache_data
def load_placement_data():
    df = pd.read_csv('datasets/chicken_placements_weekly_data.csv')
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-W' + df['Week'].astype(str).str.zfill(2) + '-1', format='%Y-W%W-%w')
    return df

@st.cache_data
def load_hatchability_data():
    df = pd.read_csv('datasets/hatchability_analysis.csv')
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-W' + df['Week'].astype(str).str.zfill(2) + '-1', format='%Y-W%W-%w')
    return df

@st.cache_data
def load_slaughter_data():
    """Load chicken slaughter data from CSV"""
    # Load the main slaughter data which already contains Heads, Weight, and Volume
    df = pd.read_csv('datasets/chicken_slaughter_monthly_data.csv')
    
    # Convert Year and Month to datetime
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str), format='%Y-%b')
    
    # Ensure data is sorted by date
    df = df.sort_values('Date')
    
    return df

@st.cache_data
def load_pullet_cumulative_placements():
    """Load pullet cumulative potential placements data
    
    This data represents the sum of pullets placed between 7 and 15 weeks,
    projecting the potential flock size with no mortality.
    """
    df = pd.read_csv('datasets/pullet_cumulative_potential_placements.csv')
    
    # Convert date columns to datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    else:
        df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str), format='%Y-%b')
    
    if 'Projected_Date' in df.columns:
        df['Projected_Date'] = pd.to_datetime(df['Projected_Date'])
    
    # Rename 'Cumulative_Potential_Placements' to 'Cumulative_Placements' for consistency
    if 'Cumulative_Potential_Placements' in df.columns:
        df['Cumulative_Placements'] = df['Cumulative_Potential_Placements']
    
    # Sort by date
    df = df.sort_values('Date')
    
    return df

@st.cache_data
def load_pullet_cumulative_yoy():
    """Load pullet cumulative placements year-over-year growth data
    
    This data shows the YoY growth percentage of the potential pullet flock size.
    """
    df = pd.read_csv('datasets/pullet_placement_cumulative_yoy_growth.csv')
    
    # Convert date columns to datetime
    if 'Projected_Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Projected_Date'])
    else:
        df['Date'] = pd.to_datetime(df['Date'])
    
    # Sort by date
    df = df.sort_values('Date')
    
    return df

@st.cache_data
def load_pullet_monthly_yoy():
    """Load monthly pullet placements year-over-year growth data
    
    This data shows the YoY growth percentage of the monthly pullet placements.
    """
    df = pd.read_csv('datasets/pullet_placement_monthly_yoy_growth.csv')
    
    # Convert date columns to datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    else:
        df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str), format='%Y-%b')
    
    # Sort by date
    df = df.sort_values('Date')
    
    return df 