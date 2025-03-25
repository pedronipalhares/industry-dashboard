import pandas as pd
import numpy as np
import streamlit as st
from .loaders import load_eggs_data, load_layer_herd_data, load_egg_set_data, load_placement_data, load_slaughter_data

@st.cache_data
def calculate_yield_data():
    """Calculate yield (eggs per layer) and LTM average"""
    layer_df = load_layer_herd_data()
    eggs_df = load_eggs_data()
    
    # Combine datasets on Year and Month
    combined_df = pd.merge(
        eggs_df, 
        layer_df[['Date', 'Layer_Herd']], 
        on='Date', 
        how='inner'
    )
    
    # Calculate yield per layer
    combined_df['Yield_Per_Layer'] = combined_df['Hatching Eggs'] / combined_df['Layer_Herd']
    
    # Calculate 12-month rolling average for LTM
    combined_df['LTM_Yield'] = combined_df['Yield_Per_Layer'].rolling(window=12).mean()
    
    return combined_df

def calculate_yoy_growth(df, value_column, date_column='Date', year_column='Year', week_column='Week'):
    df = df.sort_values(date_column)
    df['WeekNum'] = df[date_column].dt.isocalendar().week
    
    yoy_data = []
    
    for week_num in sorted(df['WeekNum'].unique()):
        week_data = df[df['WeekNum'] == week_num].sort_values(year_column)
        
        for i in range(1, len(week_data)):
            current_year = week_data.iloc[i][year_column]
            current_value = week_data.iloc[i][value_column]
            prev_year = week_data.iloc[i-1][year_column]
            prev_value = week_data.iloc[i-1][value_column]
            
            growth_pct = ((current_value - prev_value) / prev_value * 100) if prev_value > 0 else 0
            
            yoy_data.append({
                'Year': current_year,
                'Week': week_num,
                'Date': week_data.iloc[i][date_column],
                value_column: current_value,
                f'Previous Year {value_column}': prev_value,
                'YoY_Growth': growth_pct,
                'Previous Year': prev_year
            })
    
    yoy_df = pd.DataFrame(yoy_data)
    return yoy_df.sort_values('Date') if not yoy_df.empty else yoy_df

@st.cache_data
def calculate_egg_set_yoy():
    """Calculate year-over-year growth for egg sets"""
    egg_set_df = load_egg_set_data()
    
    # Sort by date for proper calculations
    egg_set_df = egg_set_df.sort_values('Date')
    
    # Get the same week from the previous year
    egg_set_df['Week_Number'] = egg_set_df['Date'].dt.isocalendar().week
    egg_set_df['Previous Year'] = egg_set_df['Year'] - 1
    
    # Create a key for merging (Year + Week)
    egg_set_df['Current_Key'] = egg_set_df['Year'].astype(str) + '-' + egg_set_df['Week'].astype(str)
    egg_set_df['Previous_Key'] = egg_set_df['Previous Year'].astype(str) + '-' + egg_set_df['Week'].astype(str)
    
    # Create a mapping of previous year's values
    prev_year_map = egg_set_df.set_index('Current_Key')['Eggs Set'].to_dict()
    
    # Get previous year's values
    egg_set_df['Previous Year Eggs Set'] = egg_set_df['Previous_Key'].map(prev_year_map)
    
    # Calculate YoY growth
    egg_set_df['YoY_Growth'] = ((egg_set_df['Eggs Set'] - egg_set_df['Previous Year Eggs Set']) / 
                               egg_set_df['Previous Year Eggs Set'] * 100)
    
    # Drop rows with NaN (first year of data)
    egg_set_df = egg_set_df.dropna(subset=['YoY_Growth'])
    
    return egg_set_df

@st.cache_data
def calculate_placement_yoy():
    """Calculate year-over-year growth for placements"""
    placement_df = load_placement_data()
    
    # Sort by date for proper calculations
    placement_df = placement_df.sort_values('Date')
    
    # Get the same week from the previous year
    placement_df['Week_Number'] = placement_df['Date'].dt.isocalendar().week
    placement_df['Previous Year'] = placement_df['Year'] - 1
    
    # Create a key for merging (Year + Week)
    placement_df['Current_Key'] = placement_df['Year'].astype(str) + '-' + placement_df['Week'].astype(str)
    placement_df['Previous_Key'] = placement_df['Previous Year'].astype(str) + '-' + placement_df['Week'].astype(str)
    
    # Create a mapping of previous year's values
    prev_year_map = placement_df.set_index('Current_Key')['Placements'].to_dict()
    
    # Get previous year's values
    placement_df['Previous Year Placements'] = placement_df['Previous_Key'].map(prev_year_map)
    
    # Calculate YoY growth
    placement_df['YoY_Growth'] = ((placement_df['Placements'] - placement_df['Previous Year Placements']) / 
                                 placement_df['Previous Year Placements'] * 100)
    
    # Drop rows with NaN (first year of data)
    placement_df = placement_df.dropna(subset=['YoY_Growth'])
    
    return placement_df

@st.cache_data
def calculate_ltm_chicken_weights():
    """Calculate LTM average chicken weights"""
    slaughter_df = load_slaughter_data()
    
    # Sort by date
    slaughter_df = slaughter_df.sort_values('Date')
    
    # Calculate 12-month moving average of weights
    slaughter_df['LTM_Weight'] = slaughter_df['Weight'].rolling(window=12).mean()
    
    return slaughter_df

@st.cache_data
def calculate_chicken_mortality_rate():
    """Calculate chicken mortality rate by comparing placements to slaughter for the same month
    
    Simplified approach:
    1. Sum placements and slaughter over 15 months for each date
    2. Calculate mortality as (sum of placements - sum of slaughter) / sum of placements
    """
    # Load placement data (weekly)
    placement_df = load_placement_data()
    
    # Load slaughter data (monthly)
    slaughter_df = load_slaughter_data()
    
    # Get the latest month with actual slaughter data (not filled zeros)
    max_slaughter_month = slaughter_df['Date'].max()
    
    # Convert placement data from weekly to monthly by summing
    placement_df['Year_Month'] = placement_df['Date'].dt.to_period('M')
    monthly_placements = placement_df.groupby('Year_Month')['Placements'].sum().reset_index()
    monthly_placements['Date'] = monthly_placements['Year_Month'].dt.to_timestamp()
    
    # Sort by date
    monthly_placements = monthly_placements.sort_values('Date')
    slaughter_df = slaughter_df.sort_values('Date')
    
    # Create a common date column for joining
    slaughter_df['Year_Month'] = slaughter_df['Date'].dt.to_period('M')
    
    # Create a complete range of dates to ensure we have continuous months
    # But only up to the last month with slaughter data
    min_date = min(monthly_placements['Date'].min(), slaughter_df['Date'].min())
    
    date_range = pd.date_range(
        start=min_date,
        end=max_slaughter_month,
        freq='MS'  # Month Start
    )
    date_df = pd.DataFrame({'Date': date_range})
    date_df['Year_Month'] = date_df['Date'].dt.to_period('M')
    
    # Merge placements with the date range
    placement_full = pd.merge(
        date_df,
        monthly_placements[['Year_Month', 'Placements']],
        on='Year_Month',
        how='left'
    ).fillna(0)
    
    # Merge slaughter with the date range - do not fill zeros for missing slaughter data
    # This ensures we only include months where actual slaughter data exists
    slaughter_full = pd.merge(
        date_df,
        slaughter_df[['Year_Month', 'Heads']],
        on='Year_Month',
        how='left'
    )
    
    # Calculate 15-month rolling sums for both placements and slaughter
    placement_full['Placements_15M_Sum'] = placement_full['Placements'].rolling(window=15).sum()
    slaughter_full['Heads_15M_Sum'] = slaughter_full['Heads'].rolling(window=15).sum()
    
    # Merge the placement and slaughter data on Year_Month
    mortality_df = pd.merge(
        placement_full[['Year_Month', 'Date', 'Placements_15M_Sum']],
        slaughter_full[['Year_Month', 'Heads_15M_Sum']],
        on='Year_Month',
        how='inner'
    )
    
    # Calculate mortality count and rate using the 15-month summed data
    mortality_df['Mortality_Count'] = mortality_df['Placements_15M_Sum'] - mortality_df['Heads_15M_Sum']
    mortality_df['Mortality_Rate'] = (mortality_df['Mortality_Count'] / mortality_df['Placements_15M_Sum']) * 100
    
    # Sort by date for display
    mortality_df = mortality_df.sort_values('Date')
    
    # Make sure we have both placement and slaughter data available - drop any rows with NaN values
    mortality_df = mortality_df.dropna(subset=['Placements_15M_Sum', 'Heads_15M_Sum'])
    
    # Add information about the last available month of data
    mortality_df['Latest_Data_Month'] = max_slaughter_month.strftime('%B %Y')
    
    return mortality_df 