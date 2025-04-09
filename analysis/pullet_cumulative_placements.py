#!/usr/bin/env python3
"""
Pullet Cumulative Potential Placements Analysis

This script analyzes the pullet placement data and calculates the cumulative
potential placements, which is the sum of pullets placed between 7 and 15 weeks.
For monthly data, this is represented as a 9-month rolling sum (from month 7 to 15).

Example: January 2025 cumulative potential placements = sum of placements from
May 2024 to January 2025, projecting the potential flock size by August 2025
(with no mortality).
"""

import os
import sys
import pandas as pd
import numpy as np


from datetime import datetime, timedelta
import calendar

def load_pullet_data():
    """
    Load pullet placement data from CSV file
    
    Returns:
        pandas.DataFrame: The pullet placement data
    """
    file_path = 'datasets/US_PULLET_PLACEMENTS_MONTHLY.csv'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found")
        return None
        
    print(f"Loading pullet placement data from {file_path}")
    df = pd.read_csv(file_path)
    
    # Convert Year and Month to date
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'], format='%Y-%b')
    
    # Sort by date
    df = df.sort_values('Date')
    
    print(f"Loaded {len(df)} records of pullet placement data")
    return df

def calculate_cumulative_placements(df):
    """
    Calculate cumulative potential placements (9-month rolling sum of placements)
    
    Args:
        df (pandas.DataFrame): Pullet placement data
        
    Returns:
        pandas.DataFrame: DataFrame with cumulative placements
    """
    if df is None or len(df) == 0:
        return None
    
    print("Calculating cumulative potential placements (9-month rolling sum)")
    
    # Create a copy of the DataFrame to avoid modifying the original
    result_df = df.copy()
    
    # Calculate the 9-month rolling sum (representing months 7-15)
    result_df['9_Month_Rolling_Sum'] = result_df['Pullet Placements'].rolling(window=9).sum()
    
    # Calculate the projected date (7 months after the last month in the rolling sum)
    result_df['Projected_Date'] = result_df['Date'] + pd.DateOffset(months=7)
    
    # Drop rows with NaN values (first 8 months won't have a complete 9-month sum)
    result_df = result_df.dropna(subset=['9_Month_Rolling_Sum'])
    
    # Rename columns for clarity
    result_df = result_df.rename(columns={
        '9_Month_Rolling_Sum': 'Cumulative_Potential_Placements'
    })
    
    # Add a column for the start date of the 9-month period
    result_df['Start_Date'] = result_df['Date'] - pd.DateOffset(months=8)
    
    # Print summary statistics
    print("\nSummary Statistics for Cumulative Potential Placements:")
    print(result_df['Cumulative_Potential_Placements'].describe())
    
    # Print recent data
    print("\nRecent Cumulative Potential Placements:")
    recent_df = result_df.tail(5).copy()
    recent_df['Cumulative_Potential_Placements'] = recent_df['Cumulative_Potential_Placements'].map('{:,.0f}'.format)
    recent_df['Period'] = recent_df.apply(
        lambda row: f"{row['Start_Date'].strftime('%b %Y')} to {row['Date'].strftime('%b %Y')} → {row['Projected_Date'].strftime('%b %Y')}", 
        axis=1
    )
    print(recent_df[['Period', 'Cumulative_Potential_Placements']].to_string(index=False))
    
    return result_df

def save_data_to_csv(df):
    """
    Save the cumulative potential placements data to CSV
    
    Args:
        df (pandas.DataFrame): DataFrame with cumulative placements
        
    Returns:
        str: Path to the saved CSV file
    """
    if df is None or len(df) == 0:
        return None
    
    # Create processed_data directory if it doesn't exist
    processed_data_dir = 'processed_data'
    if not os.path.exists(processed_data_dir):
        os.makedirs(processed_data_dir)
    
    # Format dates as strings for CSV
    output_df = df.copy()
    output_df['Start_Date'] = output_df['Start_Date'].dt.strftime('%Y-%m-%d')
    output_df['Date'] = output_df['Date'].dt.strftime('%Y-%m-%d')
    output_df['Projected_Date'] = output_df['Projected_Date'].dt.strftime('%Y-%m-%d')
    
    # Select columns to save
    columns_to_save = [
        'Start_Date', 'Date', 'Projected_Date', 
        'Cumulative_Potential_Placements'
    ]
    
    # Create full file path
    output_path = os.path.join(processed_data_dir, 'US_PULLET_CUMULATIVE_POTENTIAL_PLACEMENTS.csv')
    
    # Save to CSV
    output_df[columns_to_save].to_csv(output_path, index=False)
    
    print(f"Cumulative potential placements data saved to {output_path}")
    return output_path

def main():
    """
    Main function to run the pullet cumulative potential placements analysis
    """
    print("Starting Pullet Cumulative Potential Placements Analysis...")
    
    # Load pullet placement data
    df = load_pullet_data()
    
    if df is not None and len(df) > 0:
        # Calculate cumulative potential placements
        result_df = calculate_cumulative_placements(df)
        
        if result_df is not None and len(result_df) > 0:
            # Create charts
            
            # Save data to CSV
            save_data_to_csv(result_df)
            
            print("\nAnalysis complete! Results saved to processed_data directory.")
        else:
            print("Error: Failed to calculate cumulative potential placements.")
    else:
        print("Error: Failed to load pullet placement data.")

if __name__ == "__main__":
    main() 