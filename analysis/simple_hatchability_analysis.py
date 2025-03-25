import csv
import os
import datetime

# Settings
INCUBATION_PERIOD_WEEKS = 3  # Standard incubation period (21 days ≈ 3 weeks)
EGGS_DATA_PATH = 'datasets/egg_set_weekly_data.csv'
PLACEMENTS_DATA_PATH = 'datasets/chicken_placements_weekly_data.csv'
OUTPUT_DATA_PATH = 'datasets/hatchability_analysis.csv'

def load_data():
    """
    Load the egg set and chicken placement data
    """
    print("Loading datasets...")
    
    # Load eggs set data
    eggs_data = []
    with open(EGGS_DATA_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Check for correct columns and adapt as needed
            if 'Year' not in row and 'year' in row:
                year = row['year']
            else:
                year = row.get('Year', '')
                
            # Extract week from reference_period_desc if Week column doesn't exist
            if 'Week' not in row and 'reference_period_desc' in row:
                # Try to extract week number from format like "WEEK #01"
                week_str = row['reference_period_desc']
                if week_str.startswith('WEEK #'):
                    week = week_str[6:].strip()
                else:
                    week = '0' # default week if not found
            else:
                week = row.get('Week', '0')
                
            # Get the value (eggs set)
            if 'Eggs Set' in row:
                eggs_set = row['Eggs Set']
            elif 'Value' in row:
                eggs_set = row['Value']
            else:
                # Skip if we don't have a value
                continue
                
            try:
                # Clean and convert
                eggs_set = eggs_set.replace(',', '')
                eggs_data.append({
                    'Year': int(year),
                    'Week': int(week),
                    'Eggs Set': int(eggs_set)
                })
            except (ValueError, AttributeError):
                # Skip rows with invalid data
                continue
    
    # Load placements data
    placements_data = []
    with open(PLACEMENTS_DATA_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Check for correct columns and adapt as needed
            if 'Year' not in row and 'year' in row:
                year = row['year']
            else:
                year = row.get('Year', '')
                
            # Extract week from reference_period_desc if Week column doesn't exist
            if 'Week' not in row and 'reference_period_desc' in row:
                # Try to extract week number from format like "WEEK #01"
                week_str = row['reference_period_desc']
                if week_str.startswith('WEEK #'):
                    week = week_str[6:].strip()
                else:
                    week = '0' # default week if not found
            else:
                week = row.get('Week', '0')
                
            # Get the value (placements)
            if 'Placements' in row:
                placements = row['Placements']
            elif 'Value' in row:
                placements = row['Value']
            else:
                # Skip if we don't have a value
                continue
                
            try:
                # Clean and convert
                placements = placements.replace(',', '')
                placements_data.append({
                    'Year': int(year),
                    'Week': int(week),
                    'Placements': int(placements)
                })
            except (ValueError, AttributeError):
                # Skip rows with invalid data
                continue
    
    print(f"Loaded {len(eggs_data)} egg set records and {len(placements_data)} chicken placement records")
    
    return eggs_data, placements_data

def get_week_offset(year, week, offset_weeks):
    """
    Calculate a new year and week by adding/subtracting offset_weeks
    """
    # Calculate approximate date
    jan1 = datetime.date(year, 1, 1)
    days_to_monday = (7 - jan1.weekday()) % 7
    first_monday = jan1 + datetime.timedelta(days=days_to_monday)
    week_date = first_monday + datetime.timedelta(weeks=week-1)
    
    # Apply offset
    new_date = week_date - datetime.timedelta(weeks=offset_weeks)
    
    # Calculate new year and week
    new_year = new_date.year
    # Very approximate week calculation
    new_week = int((new_date - datetime.date(new_year, 1, 1)).days / 7) + 1
    
    # Edge case handling for week numbers
    if new_week < 1:
        new_year -= 1
        new_week = 52 + new_week
    elif new_week > 52:
        new_year += 1
        new_week = new_week - 52
        
    return new_year, new_week

def calculate_hatchability(eggs_data, placements_data):
    """
    Calculate hatchability by aligning eggs set with subsequent chick placements
    accounting for the incubation period
    """
    print(f"Calculating hatchability with {INCUBATION_PERIOD_WEEKS} weeks incubation period...")
    
    # Create a lookup dictionary for faster access to egg data
    eggs_lookup = {}
    for item in eggs_data:
        key = (item['Year'], item['Week'])
        eggs_lookup[key] = item['Eggs Set']
    
    # Calculate hatchability for each placement record
    hatchability_data = []
    
    for placement in placements_data:
        placement_year = placement['Year']
        placement_week = placement['Week']
        placements = placement['Placements']
        
        # Calculate the year and week when these eggs were set (3 weeks earlier)
        set_year, set_week = get_week_offset(placement_year, placement_week, INCUBATION_PERIOD_WEEKS)
        
        # Lookup the eggs set for this placement
        eggs_set = eggs_lookup.get((set_year, set_week))
        
        if eggs_set is not None:
            # Calculate hatchability
            hatchability = (placements / eggs_set) * 100  # in percentage
            
            hatchability_data.append({
                'Year': placement_year,
                'Week': placement_week,
                'Eggs Set Year': set_year,
                'Eggs Set Week': set_week,
                'Eggs Set': eggs_set,
                'Placements': placements,
                'Hatchability (%)': hatchability
            })
    
    # Sort by year and week
    hatchability_data.sort(key=lambda x: (x['Year'], x['Week']))
    
    print(f"Calculated hatchability for {len(hatchability_data)} weeks")
    
    return hatchability_data

def calculate_ltm_hatchability(hatchability_data, window=52):
    """
    Calculate Long-Term Mean (LTM) hatchability using a rolling window
    """
    for i in range(len(hatchability_data)):
        # Calculate start point for the window
        start = max(0, i - window + 1)
        
        # Get values in the window
        window_values = [item['Hatchability (%)'] for item in hatchability_data[start:i+1]]
        
        # Calculate mean
        ltm = sum(window_values) / len(window_values)
        
        # Add to data
        hatchability_data[i]['Hatchability LTM (%)'] = ltm
    
    return hatchability_data

def save_hatchability_data(hatchability_data, output_path):
    """
    Save hatchability data to CSV
    """
    # Get all fields
    if not hatchability_data:
        print("No hatchability data to save")
        return
        
    fieldnames = list(hatchability_data[0].keys())
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(hatchability_data)
    
    print(f"Hatchability analysis data saved to {output_path}")

def print_summary(hatchability_data):
    """
    Print a summary of the hatchability analysis
    """
    if not hatchability_data:
        print("No hatchability data available")
        return
    
    # Calculate statistics
    hatchability_values = [item['Hatchability (%)'] for item in hatchability_data]
    ltm_values = [item['Hatchability LTM (%)'] for item in hatchability_data]
    
    avg_hatchability = sum(hatchability_values) / len(hatchability_values)
    latest_ltm = ltm_values[-1] if ltm_values else 0
    
    # Find min and max years/weeks
    min_year = min(item['Year'] for item in hatchability_data)
    min_week = min(item['Week'] for item in hatchability_data if item['Year'] == min_year)
    max_year = max(item['Year'] for item in hatchability_data)
    max_week = max(item['Week'] for item in hatchability_data if item['Year'] == max_year)
    
    print("\nResults Summary:")
    print(f"Average Hatchability: {avg_hatchability:.2f}%")
    print(f"Latest LTM Hatchability: {latest_ltm:.2f}%")
    print(f"Data period: Year {min_year} Week {min_week} to Year {max_year} Week {max_week}")
    
    # Print recent data (last 5 weeks)
    print("\nRecent Hatchability Data (last 5 weeks):")
    print(f"{'Year':<6} {'Week':<6} {'Hatchability (%)':<20} {'LTM Hatchability (%)':<20}")
    print("-" * 70)
    
    for item in hatchability_data[-5:]:
        print(f"{item['Year']:<6} {item['Week']:<6} {item['Hatchability (%)']:.2f}%{' ':<13} {item['Hatchability LTM (%)']:.2f}%")

def main():
    print("Starting simple hatchability analysis...")
    
    # Create output directories if they don't exist
    os.makedirs(os.path.dirname(OUTPUT_DATA_PATH), exist_ok=True)
    
    # Load data
    eggs_data, placements_data = load_data()
    
    # Calculate hatchability
    hatchability_data = calculate_hatchability(eggs_data, placements_data)
    
    # Calculate Long-Term Mean (LTM)
    hatchability_data = calculate_ltm_hatchability(hatchability_data)
    
    # Save the hatchability data
    save_hatchability_data(hatchability_data, OUTPUT_DATA_PATH)
    
    # Print results summary
    print_summary(hatchability_data)
    
    print("\nAnalysis complete! To visualize the results, you can import the dataset into a spreadsheet program.")
    print(f"Data saved to: {OUTPUT_DATA_PATH}")

if __name__ == "__main__":
    main() 