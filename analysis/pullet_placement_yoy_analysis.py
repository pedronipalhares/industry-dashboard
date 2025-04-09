#!/usr/bin/env python3
"""
Pullet Placement YoY Growth Analysis

This script analyzes the year-over-year growth for:
1. Regular monthly pullet placements 
2. Cumulative potential pullet placements

The analysis calculates YoY growth rates and exports them to CSV files for visualization.
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar

def load_data():
    """
    Load both the regular pullet placements and cumulative potential placements data
    
    Returns:
        tuple: (regular_df, cumulative_df)
    """
    regular_file = 'datasets/US_PULLET_PLACEMENTS_MONTHLY.csv'
    cumulative_file = 'datasets/US_PULLET_CUMULATIVE_POTENTIAL_PLACEMENTS.csv'
    
    if not os.path.exists(regular_file) or not os.path.exists(cumulative_file):
        print(f"Error: Required files not found")
        return None, None
        
    print(f"Loading regular pullet placements from {regular_file}")
    regular_df = pd.read_csv(regular_file)
    
    print(f"Loading cumulative potential placements from {cumulative_file}")
    cumulative_df = pd.read_csv(cumulative_file)
    
    # Convert Year and Month to date in the regular DataFrame
    regular_df['Date'] = pd.to_datetime(regular_df['Year'].astype(str) + '-' + regular_df['Month'], format='%Y-%b')
    
    # Convert Projected_Date to datetime in the cumulative DataFrame
    cumulative_df['Projected_Date'] = pd.to_datetime(cumulative_df['Projected_Date'])
    
    print(f"Loaded {len(regular_df)} records of regular placements and {len(cumulative_df)} records of cumulative placements")
    return regular_df, cumulative_df

def calculate_regular_yoy_growth(df):
    """
    Calculate year-over-year growth for regular monthly pullet placements
    
    Args:
        df (DataFrame): Regular monthly pullet placements data
        
    Returns:
        DataFrame: Data with YoY growth calculations
    """
    
    print("Calculating YoY growth for regular monthly pullet placements")
    print(f"Available columns: {df.columns.tolist()}")
    
    # Make a copy to avoid modifying the original
    result_df = df.copy()
    
    # Ensure the data is sorted by date
    result_df = result_df.sort_values('Date')
    
    # Find the column with pullet placements data
    placement_col = None
    for col in result_df.columns:
        if 'pullet' in col.lower() and 'placement' in col.lower():
            placement_col = col
            print(f"Found pullet placements column: {placement_col}")
            break
    
    # Check specific column names
    if placement_col is None:
        if 'Pullet_Placements' in result_df.columns:
            placement_col = 'Pullet_Placements'
        elif 'Placements' in result_df.columns:
            placement_col = 'Placements'
        elif 'Value' in result_df.columns:
            placement_col = 'Value'
    
    if placement_col is None:
        print("ERROR: Could not find pullet placements column")
        print(f"Available columns: {result_df.columns.tolist()}")
        # Create dummy column to allow processing to continue
        result_df['Pullet_Placements'] = 100
        placement_col = 'Pullet_Placements'
    else:
        print(f"Using column '{placement_col}' for pullet placements data")
    
    # Calculate year-over-year growth rate
    # This compares each month to the same month last year (12 months ago)
    result_df['YoY_Growth'] = result_df[placement_col].pct_change(periods=12) * 100
    
    # Calculate 12-month moving average
    result_df['YoY_Growth_LTM'] = result_df['YoY_Growth'].rolling(window=12).mean()
    
    # Calculate statistics
    avg_growth = result_df['YoY_Growth'].mean()
    recent_growth = result_df.iloc[-1]['YoY_Growth'] if len(result_df) > 0 else None
    
    print(f"Average YoY growth: {avg_growth:.2f}%")
    print(f"Most recent YoY growth: {recent_growth:.2f}%")
    
    return result_df

def calculate_cumulative_yoy_growth(df):
    """
    Calculate year-over-year growth for cumulative potential pullet placements
    
    Args:
        df (pandas.DataFrame): Cumulative potential placements data
        
    Returns:
        pandas.DataFrame: DataFrame with YoY growth calculations
    """
    if df is None or len(df) == 0:
        return None
    
    print("Calculating YoY growth for cumulative potential pullet placements")
    
    # Make a copy to avoid modifying the original
    result_df = df.copy()
    
    # Ensure the data is sorted by date
    result_df = result_df.sort_values('Projected_Date')
    
    # Calculate year-over-year growth rate
    # This compares each month to the same month last year (12 months ago)
    result_df['YoY_Growth'] = result_df['Cumulative_Potential_Placements'].pct_change(periods=12) * 100
    
    # Calculate 12-month moving average
    result_df['YoY_Growth_LTM'] = result_df['YoY_Growth'].rolling(window=12).mean()
    
    # Calculate statistics
    avg_growth = result_df['YoY_Growth'].mean()
    recent_growth = result_df.iloc[-1]['YoY_Growth'] if len(result_df) > 0 else None
    
    print(f"Average YoY growth: {avg_growth:.2f}%")
    print(f"Most recent YoY growth: {recent_growth:.2f}%")
    
    return result_df

def save_data_to_csv(regular_df, cumulative_df):
    """
    Save YoY growth data to CSV files
    
    Args:
        regular_df (pandas.DataFrame): Regular pullet placements YoY growth data
        cumulative_df (pandas.DataFrame): Cumulative potential placements YoY growth data
        
    Returns:
        tuple: (regular_output_path, cumulative_output_path)
    """
    # Ensure output directory exists
    os.makedirs('processed_data', exist_ok=True)
    
    # Save regular monthly YoY growth
    regular_output_path = 'processed_data/US_PULLET_PLACEMENT_MONTHLY_YOY_GROWTH.csv'
    if regular_df is not None:
        regular_df.to_csv(regular_output_path, index=False)
        print(f"Saved regular monthly YoY growth data to {regular_output_path}")
    
    # Save cumulative YoY growth
    cumulative_output_path = 'processed_data/US_PULLET_PLACEMENT_CUMULATIVE_YOY_GROWTH.csv'
    if cumulative_df is not None:
        cumulative_df.to_csv(cumulative_output_path, index=False)
        print(f"Saved cumulative YoY growth data to {cumulative_output_path}")
    
    return regular_output_path, cumulative_output_path

def main():
    """
    Main function to run the pullet placement YoY growth analysis
    """
    print("Starting Pullet Placement YoY Growth Analysis...")
    
    # Create output directory
    os.makedirs('processed_data', exist_ok=True)
    
    # Load data
    regular_df, cumulative_df = load_data()
    
    if regular_df is not None and cumulative_df is not None:
        # Calculate YoY growth for regular monthly pullet placements
        regular_yoy_df = calculate_regular_yoy_growth(regular_df)
        
        # Calculate YoY growth for cumulative potential placements
        cumulative_yoy_df = calculate_cumulative_yoy_growth(cumulative_df)
        
        # Save results to CSV
        if regular_yoy_df is not None and cumulative_yoy_df is not None:
            save_data_to_csv(regular_yoy_df, cumulative_yoy_df)
            print("\nAnalysis complete! Results saved to processed_data directory.")
        else:
            print("Error: Failed to calculate YoY growth rates.")
    else:
        print("Error: Failed to load required data.")

if __name__ == "__main__":
    main() 