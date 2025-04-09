#!/usr/bin/env python3
"""
YoY Growth Data Processing

This script processes Year-over-Year growth data for:
1. Egg sets
2. Chicken placements

The processed data is saved to CSV files for visualization.
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime

# Create output directory if it doesn't exist
os.makedirs('processed_data', exist_ok=True)

def process_yoy_growth_data(data_df, value_column):
    """
    Process YoY growth data
    
    Args:
        data_df (pandas.DataFrame): Input data
        value_column (str): Name of the column containing values for YoY calculation
        
    Returns:
        pandas.DataFrame: Processed data with YoY growth calculations
    """
    print(f"Processing YoY growth for {value_column}")
    
    # Create a copy of the dataframe
    df = data_df.copy()
    
    # Ensure the value column is numeric
    if value_column in df.columns:
        # Check if it's a string and convert it
        if pd.api.types.is_string_dtype(df[value_column]):
            # Remove commas and convert to numeric
            df[value_column] = df[value_column].str.replace(',', '').astype(float)
    else:
        print(f"Warning: Column '{value_column}' not found. Available columns: {df.columns.tolist()}")
        # Create a placeholder column with zeros
        df[value_column] = 0.0
    
    # Make sure we have a datetime column
    if 'Date' not in df.columns:
        # If no Date column, try to create one from Year and Week
        if 'Year' in df.columns and 'Week' in df.columns:
            try:
                # Make sure Year and Week are strings
                df['Year'] = df['Year'].astype(str)
                df['Week'] = df['Week'].astype(str).str.zfill(2)
                df['Date'] = pd.to_datetime(df['Year'] + df['Week'] + '0', format='%Y%W%w', errors='coerce')
            except Exception as e:
                print(f"Error creating Date from Year and Week: {e}")
                # Create a placeholder date
                df['Date'] = pd.to_datetime('2020-01-01')
        else:
            print("Warning: No Year/Week columns found to create Date. Using placeholder.")
            df['Date'] = pd.to_datetime('2020-01-01')
    
    # Make sure Date is datetime type
    if not pd.api.types.is_datetime64_dtype(df['Date']):
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # Sort by date
    df = df.sort_values('Date')
    
    # Calculate YoY growth (compare to 52 weeks ago for weekly data)
    df['YoY_Growth'] = df[value_column].pct_change(52) * 100
    
    # Calculate 12-period rolling average
    df['YoY_Growth_12_Period_Avg'] = df['YoY_Growth'].rolling(window=12).mean()
    
    # Add month and year columns for easier analysis
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    
    return df

def load_and_process_egg_set_data():
    """
    Load and process egg set data
    
    Returns:
        pandas.DataFrame: Processed egg set data with YoY growth
    """
    input_file = 'datasets/US_BROILER_EGG_SET_WEEKLY.csv'
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found")
        return None
    
    print(f"Loading egg set data from {input_file}")
    df = pd.read_csv(input_file)
    
    # Process CSV format to ensure we have the needed columns
    if 'Eggs Set' not in df.columns and 'Value' in df.columns:
        df['Eggs Set'] = df['Value']
    
    # Print column names and types for debugging
    print(f"Columns in egg set data: {df.columns.tolist()}")
    print(f"Sample data types: {df.dtypes}")
    
    # Create Date column if missing
    if 'Date' not in df.columns:
        if 'week_ending' in df.columns:
            df['Date'] = pd.to_datetime(df['week_ending'], errors='coerce')
        elif 'year' in df.columns and 'reference_period_desc' in df.columns:
            # Extract week number from reference period (format: 'WEEK #XX')
            df['Week'] = df['reference_period_desc'].str.extract(r'WEEK #(\d+)').astype(str).str.zfill(2)
            df['Year'] = df['year'].astype(str)
            # Create date from year and week
            try:
                df['Date'] = pd.to_datetime(df['Year'] + df['Week'] + '0', format='%Y%W%w', errors='coerce')
            except Exception as e:
                print(f"Error creating date: {e}")
                df['Date'] = pd.to_datetime('2020-01-01')  # Fallback
    
    # Process the data
    result_df = process_yoy_growth_data(df, 'Eggs Set')
    
    # Save to CSV
    output_file = 'processed_data/US_EGG_SET_YOY_GROWTH.csv'
    result_df.to_csv(output_file, index=False)
    print(f"Saved egg set YoY growth data to {output_file}")
    
    return result_df

def load_and_process_placements_data():
    """
    Load and process chicken placements data
    
    Returns:
        pandas.DataFrame: Processed placements data with YoY growth
    """
    input_file = 'datasets/US_CHICKEN_PLACEMENTS_WEEKLY.csv'
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found")
        return None
    
    print(f"Loading chicken placements data from {input_file}")
    df = pd.read_csv(input_file)
    
    # Process CSV format to ensure we have the needed columns
    if 'Placements' not in df.columns and 'Value' in df.columns:
        df['Placements'] = df['Value']
    
    # Print column names and types for debugging
    print(f"Columns in placements data: {df.columns.tolist()}")
    print(f"Sample data types: {df.dtypes}")
    
    # Create Date column if missing
    if 'Date' not in df.columns:
        if 'week_ending' in df.columns:
            df['Date'] = pd.to_datetime(df['week_ending'], errors='coerce')
        elif 'year' in df.columns and 'reference_period_desc' in df.columns:
            # Extract week number from reference period (format: 'WEEK #XX')
            df['Week'] = df['reference_period_desc'].str.extract(r'WEEK #(\d+)').astype(str).str.zfill(2)
            df['Year'] = df['year'].astype(str)
            # Create date from year and week
            try:
                df['Date'] = pd.to_datetime(df['Year'] + df['Week'] + '0', format='%Y%W%w', errors='coerce')
            except Exception as e:
                print(f"Error creating date: {e}")
                df['Date'] = pd.to_datetime('2020-01-01')  # Fallback
    
    # Process the data
    result_df = process_yoy_growth_data(df, 'Placements')
    
    # Save to CSV
    output_file = 'processed_data/US_PLACEMENTS_YOY_GROWTH.csv'
    result_df.to_csv(output_file, index=False)
    print(f"Saved placements YoY growth data to {output_file}")
    
    return result_df

def main():
    """Main function to run YoY growth analysis"""
    print("Starting YoY Growth Data Processing...")
    
    # Create output directory
    os.makedirs('processed_data', exist_ok=True)
    
    # Process egg set data
    egg_set_df = load_and_process_egg_set_data()
    
    # Process placements data
    placements_df = load_and_process_placements_data()
    
    if egg_set_df is not None and placements_df is not None:
        print("\nAnalysis complete! Results saved to processed_data directory.")
    else:
        print("\nWarning: Some analyses couldn't be completed due to missing data.")

if __name__ == "__main__":
    main() 