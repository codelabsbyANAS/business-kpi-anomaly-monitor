import pandas as pd
import os

def clean_data(input_path, output_path):
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    
    # 1. Check for missing values
    missing_count = df.isnull().sum().sum()
    print(f"Missing values found: {missing_count}")
    if missing_count > 0:
        # Forward fill to patch missing data without dropping the row
        df = df.ffill() 
        
    # 2. Ensure date is standard datetime type
    df['date'] = pd.to_datetime(df['date'])
    
    # 3. Data Quality Checks (Removing impossible values, NOT anomalies)
    # E.g., Revenue cannot logically be less than 0
    invalid_rows = df[(df['revenue'] < 0) | (df['orders'] < 0)]
    print(f"Invalid rows (negative revenue/orders) found: {len(invalid_rows)}")
    if len(invalid_rows) > 0:
        # In a real scenario, we might investigate these. Here, we'd filter them out.
        df = df[(df['revenue'] >= 0) & (df['orders'] >= 0)]
    
    # 4. Sort chronologically to ensure time-series calculations work later
    df = df.sort_values('date').reset_index(drop=True)
    
    # Save processed data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")
    return df

if __name__ == "__main__":
    INPUT_FILE = "data/raw/synthetic_business_data.csv"
    OUTPUT_FILE = "data/processed/cleaned_business_data.csv"
    
    clean_data(INPUT_FILE, OUTPUT_FILE)