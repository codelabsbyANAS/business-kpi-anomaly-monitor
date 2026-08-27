import pandas as pd
import numpy as np
import os
from datetime import timedelta, date

def generate_ecommerce_data(start_date='2023-01-01', days=365):
    # Set seed for reproducibility
    np.random.seed(42)
    
    # 1. Generate Date Range
    dates = [pd.to_datetime(start_date) + timedelta(days=i) for i in range(days)]
    df = pd.DataFrame({'date': dates})
    
    # 2. Base Metrics Generation
    # E-commerce generally sees higher traffic but sometimes lower conversion on weekends.
    # Let's add a weekend effect.
    is_weekend = df['date'].dt.dayofweek.isin([5, 6]).astype(int)
    
    # Base traffic: ~5000 visits/day + trend + weekend drop + noise
    trend = np.linspace(0, 1500, days) # Gradual growth over the year
    base_traffic = 5000 + trend - (is_weekend * 800) + np.random.normal(0, 200, days)
    
    # Base Conversion Rate: ~2.5% + noise
    base_conv_rate = 0.025 + np.random.normal(0, 0.002, days)
    
    # Base AOV: ~$75 + noise
    base_aov = 75 + np.random.normal(0, 5, days)
    
    # Base Ad Spend: ~$1000 + noise (scales slightly with traffic)
    base_ad_spend = 1000 + (trend * 0.2) + np.random.normal(0, 50, days)
    
    # Base Refund Rate: ~3%
    base_refund_rate = 0.03 + np.random.normal(0, 0.005, days)
    
    # Apply to dataframe
    df['website_traffic'] = base_traffic
    df['conversion_rate'] = base_conv_rate
    df['average_order_value'] = base_aov
    df['ad_spend'] = base_ad_spend
    df['refund_rate'] = base_refund_rate

    # 3. INJECT ANOMALIES (Documented for later testing)
    
    # Anomaly 1: Mar 10-14 -> Bot Traffic Spikes (Traffic UP, Conv Rate DOWN)
    mask_a1 = (df['date'] >= '2023-03-10') & (df['date'] <= '2023-03-14')
    df.loc[mask_a1, 'website_traffic'] *= np.random.uniform(1.8, 2.2, mask_a1.sum())
    df.loc[mask_a1, 'conversion_rate'] *= np.random.uniform(0.3, 0.5, mask_a1.sum())

    # Anomaly 2: Jun 15-18 -> Checkout Bug (Traffic Normal, Conv Rate PLUMMETS -> Orders drop)
    mask_a2 = (df['date'] >= '2023-06-15') & (df['date'] <= '2023-06-18')
    df.loc[mask_a2, 'conversion_rate'] *= np.random.uniform(0.1, 0.2, mask_a2.sum())

    # Anomaly 3: Sep 05-09 -> Ad Platform Glitch (Ad Spend SPIKES, Traffic doesn't match)
    mask_a3 = (df['date'] >= '2023-09-05') & (df['date'] <= '2023-09-09')
    df.loc[mask_a3, 'ad_spend'] *= np.random.uniform(2.5, 3.0, mask_a3.sum())

    # Anomaly 4: Nov 20-25 -> Bad Product Batch (Refund Rate SPIKES)
    mask_a4 = (df['date'] >= '2023-11-20') & (df['date'] <= '2023-11-25')
    df.loc[mask_a4, 'refund_rate'] *= np.random.uniform(3.0, 4.0, mask_a4.sum())

    # 4. Calculate Dependent Variables (Business Logic)
    df['orders'] = (df['website_traffic'] * df['conversion_rate']).astype(int)
    df['revenue'] = df['orders'] * df['average_order_value']
    
    # Customer split (assuming ~70% new, 30% returning)
    new_cust_ratio = 0.7 + np.random.normal(0, 0.02, days)
    df['new_customers'] = (df['orders'] * new_cust_ratio).astype(int)
    df['returning_customers'] = df['orders'] - df['new_customers']
    
    # Customer Acquisition Cost = Ad Spend / New Customers
    df['customer_acquisition_cost'] = df['ad_spend'] / df['new_customers'].replace(0, 1) # Prevent div by 0
    
    # Gross Profit (Assuming fixed 40% COGS)
    cogs_percentage = 0.40
    cogs = df['revenue'] * cogs_percentage
    df['gross_profit'] = df['revenue'] - cogs
    df['profit_margin'] = df['gross_profit'] / df['revenue'].replace(0, 1)

    # 5. Clean up data types and rounding
    df['website_traffic'] = df['website_traffic'].astype(int)
    df['conversion_rate'] = df['conversion_rate'].round(4)
    df['average_order_value'] = df['average_order_value'].round(2)
    df['ad_spend'] = df['ad_spend'].round(2)
    df['refund_rate'] = df['refund_rate'].round(4)
    df['revenue'] = df['revenue'].round(2)
    df['customer_acquisition_cost'] = df['customer_acquisition_cost'].round(2)
    df['gross_profit'] = df['gross_profit'].round(2)
    df['profit_margin'] = df['profit_margin'].round(4)

    return df

if __name__ == "__main__":
    # Create output directories
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    print("Generating synthetic business dataset...")
    df = generate_ecommerce_data(start_date='2023-01-01', days=365)
    
    # Save to CSV
    output_path = 'data/raw/synthetic_business_data.csv'
    df.to_csv(output_path, index=False)
    
    print(f"Success! Dataset generated with {len(df)} rows and {len(df.columns)} columns.")
    print(f"Saved to: {output_path}")
    print("\nData Sample:")
    print(df[['date', 'website_traffic', 'orders', 'revenue', 'ad_spend']].head())