import pandas as pd
import os
import numpy as np

# Create output directory if it doesn't exist
os.makedirs('processed_data', exist_ok=True)

def main():
    print("Starting layer yield analysis...")
    
    # Load hatching eggs data
    eggs_df = pd.read_csv('datasets/US_BROILER_HATCHING_EGGS_MONTHLY.csv')
    print(f"Loaded eggs data with columns: {eggs_df.columns.tolist()}")
    
    # Load layer herd data
    herd_df = pd.read_csv('datasets/US_BROILER_BREEDER_HERD_MONTHLY.csv')
    print(f"Loaded herd data with columns: {herd_df.columns.tolist()}")
    
    # Ensure both datasets have the same date format
    eggs_df['Date'] = pd.to_datetime(eggs_df['Year'].astype(str) + '-' + eggs_df['Month'])
    herd_df['Date'] = pd.to_datetime(herd_df['Year'].astype(str) + '-' + herd_df['Month'])
    
    # Merge datasets
    merged_df = pd.merge(eggs_df, herd_df, on='Date', how='inner', suffixes=('_eggs', '_herd'))
    print(f"Merged data has columns: {merged_df.columns.tolist()}")
    
    # Identify the correct column name for hatching eggs
    hatching_eggs_col = None
    layer_herd_col = None
    
    # Find hatching eggs column
    for col in merged_df.columns:
        if 'hatching' in col.lower() or 'eggs' in col.lower():
            hatching_eggs_col = col
            print(f"Found hatching eggs column: {hatching_eggs_col}")
            break
    
    if not hatching_eggs_col and 'Hatching Eggs' in merged_df.columns:
        hatching_eggs_col = 'Hatching Eggs'
        print(f"Using column 'Hatching Eggs'")
    
    # Find layer herd column
    for col in merged_df.columns:
        if 'layer' in col.lower() or 'herd' in col.lower():
            layer_herd_col = col
            print(f"Found layer herd column: {layer_herd_col}")
            break
    
    if not layer_herd_col and 'Layer_Herd' in merged_df.columns:
        layer_herd_col = 'Layer_Herd'
    
    # Check if we found the needed columns
    if not hatching_eggs_col or not layer_herd_col:
        print("ERROR: Could not find hatching eggs or layer herd column")
        print(f"Available columns: {merged_df.columns.tolist()}")
        return None
    
    # Calculate yield (eggs per layer)
    merged_df['Yield'] = merged_df[hatching_eggs_col] / merged_df[layer_herd_col] * 1000  # Eggs per 1000 layers
    
    # Calculate YoY growth
    merged_df = merged_df.sort_values('Date')
    merged_df['Yield_YoY'] = merged_df['Yield'].pct_change(12) * 100  # 12 months year-over-year change
    
    # Calculate LTM average
    merged_df['Yield_LTM'] = merged_df['Yield'].rolling(window=12).mean()
    
    # Save data to CSV
    output_path = 'processed_data/US_LAYER_YIELD_ANALYSIS.csv'
    merged_df.to_csv(output_path, index=False)
    
    print(f"Analysis complete. Results saved to {output_path}")
    
    # Return the dataframe for further analysis if needed
    return merged_df

if __name__ == "__main__":
    main() 