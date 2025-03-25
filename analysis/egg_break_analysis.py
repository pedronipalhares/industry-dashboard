import pandas as pd
import numpy as np
import os
from datetime import datetime
import calendar

def load_data():
    """Load the required datasets"""
    # Load eggs produced (monthly data)
    eggs_produced_df = pd.read_csv('datasets/broiler_hatching_eggs_monthly.csv')
    
    # Load eggs set (weekly data)
    eggs_set_df = pd.read_csv('datasets/egg_set_weekly_data.csv')
    
    return eggs_produced_df, eggs_set_df

def aggregate_eggs_set_to_monthly(eggs_set_df):
    """Aggregate weekly eggs set data to monthly"""
    # Make a copy to avoid modifying the original
    df = eggs_set_df.copy()
    
    # Create Year and Week columns if they don't exist
    if 'Year' not in df.columns and 'year' in df.columns:
        df['Year'] = df['year']
    
    if 'Week' not in df.columns and 'reference_period_desc' in df.columns:
        # Extract week number from reference period (format: 'WEEK #XX')
        df['Week'] = df['reference_period_desc'].str.extract(r'WEEK #(\d+)').astype(str)
    
    # Create Eggs Set column if it doesn't exist
    if 'Eggs Set' not in df.columns and 'Value' in df.columns:
        df['Eggs Set'] = df['Value'].str.replace(',', '').astype(float)
    elif 'Eggs Set' in df.columns:
        # Make sure it's numeric
        if isinstance(df['Eggs Set'].iloc[0], str):
            df['Eggs Set'] = df['Eggs Set'].str.replace(',', '').astype(float)
    
    # Create Date column
    if 'Date' not in df.columns:
        if 'week_ending' in df.columns:
            df['Date'] = pd.to_datetime(df['week_ending'])
        else:
            try:
                df['Date'] = pd.to_datetime(df['Year'].astype(str) + 
                                           df['Week'].astype(str).str.zfill(2) + 
                                           '0', format='%Y%W%w', errors='coerce')
            except Exception as e:
                print(f"Error creating Date column: {e}")
                # Fallback - use just year as a last resort
                df['Date'] = pd.to_datetime(df['Year'].astype(str), format='%Y', errors='coerce')
    
    # Extract month and year
    df['Year_Month'] = df['Date'].dt.strftime('%Y-%m')
    
    # Aggregate to monthly
    monthly_eggs_set = df.groupby('Year_Month')['Eggs Set'].sum().reset_index()
    monthly_eggs_set['Date'] = pd.to_datetime(monthly_eggs_set['Year_Month'] + '-01')
    
    # Add month and year columns
    monthly_eggs_set['Year'] = monthly_eggs_set['Date'].dt.year
    # Use uppercase month abbreviation to match the egg production dataset
    monthly_eggs_set['Month'] = monthly_eggs_set['Date'].dt.strftime('%b').str.upper()
    
    print(f"Monthly egg set data has {len(monthly_eggs_set)} rows with months formatted as: {monthly_eggs_set['Month'].unique()[:5]}")
    
    return monthly_eggs_set

def calculate_egg_break_ratio(eggs_produced_df, monthly_eggs_set):
    """Calculate the egg break ratio - eggs not set as a percentage of eggs produced"""
    # Print month formats from both datasets for debugging
    print(f"Egg production months: {eggs_produced_df['Month'].unique()[:5]}")
    print(f"Egg set months: {monthly_eggs_set['Month'].unique()[:5]}")
    
    # Ensure date formats are compatible
    eggs_produced_df['Date'] = pd.to_datetime(
        eggs_produced_df['Year'].astype(str) + '-' + 
        pd.to_datetime(eggs_produced_df['Month'], format='%b').dt.month.astype(str),
        format='%Y-%m'
    )
    
    # Create numeric month for better merging
    eggs_produced_df['Month_Num'] = pd.to_datetime(eggs_produced_df['Month'], format='%b').dt.month
    monthly_eggs_set['Month_Num'] = pd.to_datetime(monthly_eggs_set['Month'], format='%b').dt.month
    
    # Merge datasets on Year and Month number for more reliable matching
    merged_df = pd.merge(
        eggs_produced_df, 
        monthly_eggs_set, 
        on=['Year', 'Month_Num'], 
        how='inner',
        suffixes=('_produced', '_set')
    )
    
    print(f"Successfully merged {len(merged_df)} rows between egg production and egg set data")
    
    # Calculate eggs not set (break)
    merged_df['Eggs_Break'] = merged_df['Hatching Eggs'] - merged_df['Eggs Set']
    
    # Calculate break ratio (percentage)
    merged_df['Break_Ratio'] = (merged_df['Eggs_Break'] / merged_df['Hatching Eggs']) * 100
    
    # Calculate 15-month rolling average
    merged_df = merged_df.sort_values('Date_set')
    merged_df['Rolling_15M_Break_Ratio'] = merged_df['Break_Ratio'].rolling(window=15).mean()
    
    # Clean up the dataframe for consistent column naming
    result_df = merged_df.copy()
    result_df['Date'] = result_df['Date_set']  # Use the set date as the main date
    result_df['Month'] = result_df['Month_set']  # Use the set month as the main month
    
    # Select the essential columns in a sensible order
    essential_columns = [
        'Date', 'Year', 'Month', 'Hatching Eggs', 'Eggs Set', 
        'Eggs_Break', 'Break_Ratio', 'Rolling_15M_Break_Ratio'
    ]
    
    # Ensure all essential columns exist
    for col in essential_columns:
        if col not in result_df.columns:
            print(f"WARNING: Missing column {col} in processed data")
    
    # Keep other columns that might be useful
    additional_columns = [col for col in result_df.columns if col not in essential_columns]
    output_columns = essential_columns + additional_columns
    
    # Filter to columns that actually exist
    existing_columns = [col for col in output_columns if col in result_df.columns]
    
    return result_df[existing_columns]

def main():
    """Main function to run egg break analysis"""
    print("Starting egg break analysis...")
    
    # Create output directory
    os.makedirs('datasets', exist_ok=True)
    
    # Load data
    eggs_produced_df, eggs_set_df = load_data()
    print(f"Loaded egg production data: {eggs_produced_df.shape} and egg set data: {eggs_set_df.shape}")
    
    # Aggregate eggs set data to monthly
    monthly_eggs_set = aggregate_eggs_set_to_monthly(eggs_set_df)
    
    # Calculate egg break ratio
    result_df = calculate_egg_break_ratio(eggs_produced_df, monthly_eggs_set)
    
    # Check if we got results
    if result_df.empty:
        print("ERROR: No data produced from the egg break analysis calculation")
        # Create a dummy dataframe with the expected columns for debugging
        result_df = pd.DataFrame(columns=['Date', 'Year', 'Month', 'Hatching Eggs', 'Eggs Set', 
                                         'Eggs_Break', 'Break_Ratio', 'Rolling_15M_Break_Ratio'])
    else:
        print(f"Successfully calculated egg break metrics for {len(result_df)} months")
    
    # Save results to CSV
    output_path = 'datasets/egg_break_analysis.csv'
    result_df.to_csv(output_path, index=False)
    
    print(f"Analysis complete. Results saved to {output_path}")
    
    # Return the dataframe for further analysis if needed
    return result_df

if __name__ == "__main__":
    main() 