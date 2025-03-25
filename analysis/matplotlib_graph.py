import csv
import os

# Settings
INPUT_DATA_PATH = 'datasets/hatchability_analysis.csv'

def load_hatchability_data():
    """
    Load hatchability data from CSV
    """
    print("Loading hatchability data...")
    
    data = []
    years = []
    weeks = []
    hatchability = []
    ltm = []
    
    with open(INPUT_DATA_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            years.append(int(row['Year']))
            weeks.append(int(row['Week']))
            hatchability.append(float(row['Hatchability (%)']))
            ltm.append(float(row['Hatchability LTM (%)']))
    
    print(f"Loaded {len(years)} hatchability records")
    
    return {
        'years': years,
        'weeks': weeks,
        'hatchability': hatchability,
        'ltm': ltm
    }

def main():
    print("Starting hatchability data processing...")
    
    try:
        # Load data
        data = load_hatchability_data()
        print("Data processing complete!")
    except Exception as e:
        print(f"Error processing data: {e}")

if __name__ == "__main__":
    main() 