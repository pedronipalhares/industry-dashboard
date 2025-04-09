#!/usr/bin/env python3
"""
Layer Mortality Analysis

This script analyzes the difference between cumulative potential placements
and the actual broiler breeder layer herd to calculate mortality rates.

Methodology:
- Cumulative potential placements represent what the flock size would be with no mortality
- Actual layer herd represents the actual count of birds
- Mortality rate = (1 - Actual Herd / Potential Flock) * 100%
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar

def load_data():
    """
    Load both the cumulative potential placements and layer herd data
    
    Returns:
        tuple: (placements_df, herd_df)
    """
    potential_file = 'datasets/US_PULLET_CUMULATIVE_POTENTIAL_PLACEMENTS.csv'
    herd_file = 'datasets/US_BROILER_BREEDER_HERD_MONTHLY.csv'
    
    if not os.path.exists(potential_file) or not os.path.exists(herd_file):
        print(f"Error: Required files not found")
        return None, None
        
    print(f"Loading cumulative potential placements from {potential_file}")
    potential_df = pd.read_csv(potential_file)
    
    print(f"Loading broiler breeder layer herd data from {herd_file}")
    herd_df = pd.read_csv(herd_file)
    
    # Convert dates in the potential placements DataFrame
    potential_df['Projected_Date'] = pd.to_datetime(potential_df['Projected_Date'])
    
    # Convert Year and Month to date in the herd DataFrame
    herd_df['Date'] = pd.to_datetime(herd_df['Year'].astype(str) + '-' + herd_df['Month'], format='%Y-%b')
    
    print(f"Loaded {len(potential_df)} records of potential placements and {len(herd_df)} records of layer herd data")
    return potential_df, herd_df

def calculate_mortality_rates(potential_df, herd_df):
    """
    Calculate mortality rates based on potential placements and actual layer herd
    
    Args:
        potential_df (DataFrame): Cumulative potential placements data
        herd_df (DataFrame): Layer herd data
        
    Returns:
        DataFrame: Data with mortality rate calculations
    """
    print(f"Calculating mortality rates from {len(potential_df)} potential placement records " + 
          f"and {len(herd_df)} layer herd records")
    
    print(f"Potential placements columns: {potential_df.columns.tolist()}")
    print(f"Layer herd columns: {herd_df.columns.tolist()}")
    
    # Merge the datasets on matching dates
    result_df = pd.merge(
        potential_df[['Projected_Date', 'Cumulative_Potential_Placements']],
        herd_df[['Date', 'Layer_Herd']], 
        left_on='Projected_Date',
        right_on='Date',
        how='inner'
    )
    
    print(f"Merged dataframe columns: {result_df.columns.tolist()}")
    
    # Calculate mortality rate
    result_df['Mortality_Rate'] = (1 - result_df['Layer_Herd'] / result_df['Cumulative_Potential_Placements']) * 100
    
    # Calculate 12-month rolling average of mortality rate
    result_df = result_df.sort_values('Projected_Date')
    result_df['Mortality_Rate_LTM'] = result_df['Mortality_Rate'].rolling(window=12).mean()
    
    # Drop unnecessary columns (if they exist)
    if 'Date' in result_df.columns:
        result_df = result_df.drop(columns=['Date'])
    
    print(f"Calculated mortality rates for {len(result_df)} months")
    return result_df

def save_data_to_csv(df):
    """
    Save mortality rate data to CSV file
    
    Args:
        df (pandas.DataFrame): DataFrame with mortality rate calculations
        
    Returns:
        str: Path to the saved CSV file
    """
    # Ensure output directory exists
    os.makedirs('processed_data', exist_ok=True)
    
    # Save to CSV
    output_path = 'processed_data/LAYER_MORTALITY_RATES.csv'
    df.to_csv(output_path, index=False)
    
    print(f"Saved mortality rate data to {output_path}")
    return output_path

def create_comparative_view(df):
    """
    Create an integrated view comparing potential placements vs actual herd
    
    Args:
        df (pandas.DataFrame): DataFrame with mortality rate calculations
        
    Returns:
        pandas.DataFrame: DataFrame with comparative data prepared for visualization
    """
    # Make a copy to avoid modifying the original
    comparison_df = df.copy()
    
    # Use Projected_Date as the primary date
    comparison_df = comparison_df.rename(columns={'Projected_Date': 'Date'})
    
    # Add statistics and metadata for visualization
    comparison_df['Potential_vs_Actual_Diff'] = comparison_df['Cumulative_Potential_Placements'] - comparison_df['Layer_Herd']
    comparison_df['Potential_vs_Actual_Diff_Percent'] = comparison_df['Potential_vs_Actual_Diff'] / comparison_df['Cumulative_Potential_Placements'] * 100
    
    # Calculate 12-month moving averages
    comparison_df['Layer_Herd_LTM'] = comparison_df['Layer_Herd'].rolling(window=12).mean()
    comparison_df['Potential_Placements_LTM'] = comparison_df['Cumulative_Potential_Placements'].rolling(window=12).mean()
    
    # Format for output
    data_for_viz = comparison_df.sort_values('Date')
    
    print(f"Prepared comparative view with {len(data_for_viz)} records")
    return data_for_viz

def main():
    """
    Main function to run the layer mortality analysis
    """
    print("Starting Layer Mortality Analysis...")
    
    # Create output directory
    os.makedirs('processed_data', exist_ok=True)
    
    # Load data
    potential_df, herd_df = load_data()
    
    if potential_df is not None and herd_df is not None:
        # Calculate mortality rates
        mortality_df = calculate_mortality_rates(potential_df, herd_df)
        
        if not mortality_df.empty:
            # Save to CSV
            save_data_to_csv(mortality_df)
            
            # Create comparative view for visualization
            comparative_data = create_comparative_view(mortality_df)
            
            # Save comparative view to CSV
            comparative_output_path = 'processed_data/LAYER_FLOCK_COMPARISON_DATA.csv'
            comparative_data.to_csv(comparative_output_path, index=False)
            print(f"Saved comparative data to {comparative_output_path}")
            
            print("\nAnalysis complete! Results saved to processed_data directory.")
        else:
            print("Error: Failed to calculate mortality rates.")
    else:
        print("Error: Failed to load required data.")

if __name__ == "__main__":
    main() 