#!/usr/bin/env python3
"""
US Chicken Industry Analysis

This script analyzes various aspects of the US chicken industry:
1. Egg sets data
2. Chicken placements data
3. Chicken slaughter data (heads, weight, volume)

It processes and saves the data to CSV files for visualization in the Streamlit app.

The script uses data from:
- datasets/egg_set_weekly_data.csv
- datasets/chicken_placements_weekly_data.csv
- datasets/hatchability_analysis.csv
- datasets/chicken_slaughter_monthly_data.csv
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime
import csv

# Ensure the datasets directory exists
os.makedirs('datasets', exist_ok=True)

#######################
# Data Loading Functions
#######################

def load_egg_and_placement_data():
    """Load egg set and chicken placement data from CSV files"""
    print("Loading egg set and placement data...")
    
    egg_set_data = pd.read_csv('datasets/egg_set_weekly_data.csv')
    placements_data = pd.read_csv('datasets/chicken_placements_weekly_data.csv')
    
    # Process egg set data - add Year and Week columns if they don't exist
    if 'year' in egg_set_data.columns and 'Year' not in egg_set_data.columns:
        egg_set_data['Year'] = egg_set_data['year']
    
    if 'Year' not in egg_set_data.columns and 'reference_period_desc' in egg_set_data.columns:
        # Extract week number from reference_period_desc (format: 'WEEK #XX')
        egg_set_data['Week'] = egg_set_data['reference_period_desc'].str.extract(r'WEEK #(\d+)').astype(str)
        # Year is directly in the year column
        egg_set_data['Year'] = egg_set_data['year'].astype(str)
    
    # Process placements data
    if 'year' in placements_data.columns and 'Year' not in placements_data.columns:
        placements_data['Year'] = placements_data['year']
    
    if 'Year' not in placements_data.columns and 'reference_period_desc' in placements_data.columns:
        # Extract week number from reference_period_desc (format: 'WEEK #XX')
        placements_data['Week'] = placements_data['reference_period_desc'].str.extract(r'WEEK #(\d+)').astype(str)
        # Year is directly in the year column
        placements_data['Year'] = placements_data['year'].astype(str)
    
    # Create Eggs Set column if it doesn't exist
    if 'Eggs Set' not in egg_set_data.columns and 'Value' in egg_set_data.columns:
        egg_set_data['Eggs Set'] = egg_set_data['Value']
    
    # Create Placements column if it doesn't exist
    if 'Placements' not in placements_data.columns and 'Value' in placements_data.columns:
        placements_data['Placements'] = placements_data['Value']
    
    # Convert Year and Week to strings for consistent handling
    if 'Year' in egg_set_data.columns:
        egg_set_data['Year'] = egg_set_data['Year'].astype(str)
    if 'Week' in egg_set_data.columns:
        egg_set_data['Week'] = egg_set_data['Week'].astype(str).str.zfill(2)
    
    if 'Year' in placements_data.columns:
        placements_data['Year'] = placements_data['Year'].astype(str)
    if 'Week' in placements_data.columns:
        placements_data['Week'] = placements_data['Week'].astype(str).str.zfill(2)
    
    return egg_set_data, placements_data

def load_hatchability_data():
    """Load hatchability data from CSV file"""
    print("Loading hatchability data...")
    
    file_path = 'datasets/hatchability_analysis.csv'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found")
        return None
    
    data = pd.read_csv(file_path)
    
    # Convert date columns if needed
    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date'])
    
    return data

def load_slaughter_data():
    """Load chicken slaughter data from CSV file"""
    print("Loading chicken slaughter data...")
    
    file_path = 'datasets/chicken_slaughter_monthly_data.csv'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found")
        return None
    
    data = pd.read_csv(file_path)
    
    # Convert date columns if needed
    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date'])
    elif 'Year' in data.columns and 'Month' in data.columns:
        # Create Date column from Year and Month
        print("Creating Date column from Year and Month columns")
        try:
            # Try to create Date from Year and Month
            data['Date'] = pd.to_datetime(data['Year'].astype(str) + '-' + data['Month'].astype(str), errors='coerce')
        except Exception as e:
            print(f"Error creating Date column: {e}")
            # Create a dummy Date as a fallback
            data['Date'] = pd.to_datetime('2020-01-01')
    else:
        print("Warning: No Date column found and couldn't create one from Year/Month columns")
        print("Available columns:", data.columns.tolist())
        # Create a dummy Date column
        data['Date'] = pd.to_datetime('2020-01-01')
    
    return data

#######################
# Data Processing Functions
#######################

def calculate_yoy_growth(data, value_column):
    """Calculate Year-over-Year growth for weekly or monthly data"""
    # Make a copy of the data
    df = data.copy()
    
    # Ensure we have a Date column
    if 'Date' not in df.columns:
        # If we have Year and Week, create a date from those
        if 'Year' in df.columns and 'Week' in df.columns:
            try:
                # Make sure Year and Week are strings
                df['Year'] = df['Year'].astype(str)
                df['Week'] = df['Week'].astype(str).str.zfill(2)
                df['Date'] = pd.to_datetime(df['Year'] + df['Week'] + '0', format='%Y%W%w', errors='coerce')
            except Exception as e:
                print(f"Error creating Date from Year and Week: {e}")
                # Fallback method
                today = datetime.now()
                df['Date'] = pd.to_datetime(f"{today.year}-01-01")
        # If we have Year and Month, create a date from those
        elif 'Year' in df.columns and 'Month' in df.columns:
            try:
                df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'], format='%Y-%b', errors='coerce')
            except Exception as e:
                print(f"Error creating Date from Year and Month: {e}")
                today = datetime.now()
                df['Date'] = pd.to_datetime(f"{today.year}-01-01")
        # If all else fails, create a placeholder date
        else:
            print("Warning: No Year/Week or Year/Month columns found to create Date. Using placeholder.")
            today = datetime.now()
            df['Date'] = pd.to_datetime(f"{today.year}-01-01")
    
    # Make sure Date column is datetime type
    if 'Date' in df.columns and not pd.api.types.is_datetime64_dtype(df['Date']):
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # Ensure value column is numeric
    if value_column in df.columns:
        if pd.api.types.is_string_dtype(df[value_column]):
            df[value_column] = df[value_column].str.replace(',', '').astype(float)

    # Sort by date
    if 'Date' in df.columns:
        df = df.sort_values('Date')
    else:
        print("Warning: No Date column available for sorting.")
        return df
    
    # Calculate YoY growth
    # For weekly data, compare to 52 weeks ago
    # For monthly data, compare to 12 months ago
    periods = 52 if 'Week' in df.columns else 12
    df['YoY_Growth'] = df[value_column].pct_change(periods=periods) * 100
    
    # Calculate rolling average
    window = 12
    df['YoY_Growth_Rolling_Avg'] = df['YoY_Growth'].rolling(window=window).mean()
    
    return df

def prepare_slaughter_data(slaughter_data):
    """Prepare slaughter data for analysis"""
    if slaughter_data is None:
        return None
    
    print("Preparing slaughter data for analysis...")
    
    # Make a copy to avoid modifying the original
    df = slaughter_data.copy()
    
    # Calculate derived values
    df['Avg_Weight'] = df['Weight'] / df['Heads']
    df['Volume'] = df['Heads'] * df['Avg_Weight']
    
    # Create Year and Month columns for grouping
    df['Year'] = df['Date'].dt.year
    df['Month_Num'] = df['Date'].dt.month
    
    # Calculate YoY Growth for Heads
    df = df.sort_values('Date')
    df['Heads_YoY_Growth'] = df['Heads'].pct_change(12) * 100
    
    # Calculate YoY Growth for Volume
    df['Volume_YoY_Growth'] = df['Volume'].pct_change(12) * 100
    
    # Calculate Last Twelve Months (LTM) average of weights
    df['Weight_LTM_Avg'] = df['Avg_Weight'].rolling(window=12).mean()
    
    return df

def process_seasonal_production(df):
    """Process seasonal production data"""
    if df is None:
        return None
    
    print("Processing seasonal production data...")
    
    # Create a new DataFrame for seasonal analysis
    seasonal_df = pd.DataFrame()
    
    # Group by month and calculate average volume for each month
    monthly_avg = df.groupby('Month_Num')['Volume'].mean().reset_index()
    monthly_avg.columns = ['Month_Num', 'Avg_Volume']
    
    # Add month names
    month_names = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    }
    monthly_avg['Month_Name'] = monthly_avg['Month_Num'].map(month_names)
    
    # Sort by month
    seasonal_df = monthly_avg.sort_values('Month_Num')
    
    return seasonal_df

def analyze_breeder_breeder_layer_herd():
    """Analyze broiler breeder layer herd data"""
    print("Analyzing broiler breeder layer herd data...")
    
    file_path = 'datasets/broiler_breeder_layer_herd_monthly.csv'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found")
        return None
    
    # Load data
    df = pd.read_csv(file_path)
    
    # Convert date
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'], format='%Y-%b')
    
    # Sort by date
    df = df.sort_values('Date')
    
    # Calculate 12-month rolling average
    df['Layer_Herd_LTM'] = df['Layer_Herd'].rolling(window=12).mean()
    
    # Calculate YoY growth
    for year_lag in [1, 2, 3]:
        df[f'YoY_Growth_{year_lag}y'] = df['Layer_Herd'].pct_change(12 * year_lag) * 100
    
    # Save LTM data to CSV
    ltm_output_path = 'datasets/breeder_herd_ltm_average.csv'
    df.to_csv(ltm_output_path, index=False)
    print(f"Saved broiler breeder layer herd LTM data to {ltm_output_path}")
    
    # Prepare YoY growth data for visualization
    recent_years = 5
    max_year = df['Year'].max()
    recent_df = df[df['Year'] >= max_year - recent_years]
    
    # Group by month
    months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    yoy_growth_df = recent_df.pivot_table(
        index='Month',
        columns='Year',
        values=['YoY_Growth_1y', 'YoY_Growth_2y', 'YoY_Growth_3y']
    ).reset_index()
    
    # Save YoY growth data to CSV
    yoy_output_path = 'datasets/breeder_herd_yoy_growth.csv'
    yoy_growth_df.to_csv(yoy_output_path)
    print(f"Saved broiler breeder layer herd YoY growth data to {yoy_output_path}")
    
    return df

#######################
# Main Analysis Functions
#######################

def analyze_egg_and_placement_data():
    """Analyze egg set and chicken placement data"""
    print("\n=== Analyzing Egg Set and Placement Data ===")
    
    # Load data
    egg_set_data, placements_data = load_egg_and_placement_data()
    
    # Calculate YoY growth
    egg_set_growth = calculate_yoy_growth(egg_set_data, 'Eggs Set')
    placements_growth = calculate_yoy_growth(placements_data, 'Placements')
    
    # Save to CSV
    egg_set_output = 'datasets/egg_set_yoy_growth_analysis.csv'
    egg_set_growth.to_csv(egg_set_output, index=False)
    print(f"Saved egg set YoY growth analysis to {egg_set_output}")
    
    placements_output = 'datasets/placements_yoy_growth_analysis.csv'
    placements_growth.to_csv(placements_output, index=False)
    print(f"Saved placements YoY growth analysis to {placements_output}")
    
    # Process hatchability data
    hatchability_data = load_hatchability_data()
    if hatchability_data is not None:
        hatchability_output = 'datasets/hatchability_ltm_analysis.csv'
        hatchability_data.to_csv(hatchability_output, index=False)
        print(f"Saved hatchability LTM analysis to {hatchability_output}")
    
    print("Egg set and placement analysis completed")

def analyze_slaughter_data():
    """Analyze chicken slaughter data"""
    print("\n=== Analyzing Chicken Slaughter Data ===")
    
    # Load data
    slaughter_data = load_slaughter_data()
    if slaughter_data is None:
        print("No slaughter data available for analysis")
        return
    
    # Prepare data for analysis
    processed_data = prepare_slaughter_data(slaughter_data)
    if processed_data is None:
        print("Failed to process slaughter data")
        return
    
    # Save processed slaughter data
    slaughter_output = 'datasets/chicken_slaughter_processed.csv'
    processed_data.to_csv(slaughter_output, index=False)
    print(f"Saved processed slaughter data to {slaughter_output}")
    
    # Process and save heads YoY growth
    heads_output = 'datasets/chicken_slaughter_heads_yoy_growth.csv'
    processed_data.to_csv(heads_output, index=False)
    print(f"Saved chicken slaughter heads YoY growth to {heads_output}")
    
    # Process and save LTM avg weights
    weights_output = 'datasets/chicken_slaughter_ltm_avg_weights.csv'
    processed_data.to_csv(weights_output, index=False)
    print(f"Saved chicken slaughter LTM avg weights to {weights_output}")
    
    # Process and save volume YoY growth
    volume_output = 'datasets/chicken_slaughter_volume_yoy_growth.csv'
    processed_data.to_csv(volume_output, index=False)
    print(f"Saved chicken slaughter volume YoY growth to {volume_output}")
    
    # Process and save seasonal production
    seasonal_data = process_seasonal_production(processed_data)
    if seasonal_data is not None:
        seasonal_output = 'datasets/chicken_slaughter_seasonal_production.csv'
        seasonal_data.to_csv(seasonal_output, index=False)
        print(f"Saved chicken slaughter seasonal production to {seasonal_output}")
    
    print("Chicken slaughter analysis completed")

def main():
    """Main function to run all analyses"""
    print("Starting US Chicken Industry Analysis...")
    
    # Create datasets directory if it doesn't exist
    os.makedirs('datasets', exist_ok=True)
    
    # Analyze egg set and placement data
    analyze_egg_and_placement_data()
    
    # Analyze chicken slaughter data
    analyze_slaughter_data()
    
    # Analyze broiler breeder layer herd data
    analyze_breeder_breeder_layer_herd()
    
    print("\nAll US chicken industry analyses completed successfully!")
    print("Generated datasets:")
    
    # List all generated datasets
    for file in sorted(os.listdir('datasets')):
        if file.startswith(('chicken_slaughter', 'egg_set', 'placements', 'hatchability', 'breeder_herd')):
            print(f"  - datasets/{file}")

if __name__ == "__main__":
    main() 