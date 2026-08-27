import pandas as pd
import numpy as np
import os

def detect_anomalies(df):
    print("Running statistical anomaly detection...")
    df_anom = df.copy()
    
    # METHOD 1: Global Z-Score (For Refund Rate)
    # Z-score = (Value - Mean) / Standard Deviation
    # A Z-score > 3 means it's extremely unusual compared to the whole year
    refund_mean = df_anom['refund_rate'].mean()
    refund_std = df_anom['refund_rate'].std()
    df_anom['refund_rate_zscore'] = (df_anom['refund_rate'] - refund_mean) / refund_std
    df_anom['anomaly_refund'] = df_anom['refund_rate_zscore'].apply(lambda x: 1 if x > 3 else 0)

    # METHOD 2: Rolling Baseline (For Conversion Rate & Ad Spend)
    # Compares today's value against the 14-day rolling average
    
    # 2a. Conversion Rate Anomalies (Looking for sudden drops)
    df_anom['conv_rate_14d_mean'] = df_anom['conversion_rate'].rolling(window=14, min_periods=1).mean()
    df_anom['conv_rate_14d_std'] = df_anom['conversion_rate'].rolling(window=14, min_periods=1).std().fillna(0)
    # Flag if conversion rate drops below: Mean - (2.5 * Standard Deviation)
    df_anom['conv_lower_bound'] = df_anom['conv_rate_14d_mean'] - (2.5 * df_anom['conv_rate_14d_std'])
    df_anom['anomaly_conv_rate'] = (df_anom['conversion_rate'] < df_anom['conv_lower_bound']).astype(int)

    # 2b. Ad Spend Anomalies (Looking for sudden spikes)
    df_anom['ad_spend_14d_mean'] = df_anom['ad_spend'].rolling(window=14, min_periods=1).mean()
    df_anom['ad_spend_14d_std'] = df_anom['ad_spend'].rolling(window=14, min_periods=1).std().fillna(0)
    # Flag if ad spend spikes above: Mean + (2.5 * Standard Deviation)
    df_anom['ad_upper_bound'] = df_anom['ad_spend_14d_mean'] + (2.5 * df_anom['ad_spend_14d_std'])
    df_anom['anomaly_ad_spend'] = (df_anom['ad_spend'] > df_anom['ad_upper_bound']).astype(int)

    # Combine flags to see if ANY anomaly occurred on a given day
    df_anom['is_anomaly'] = df_anom[['anomaly_refund', 'anomaly_conv_rate', 'anomaly_ad_spend']].max(axis=1)
    
    return df_anom

if __name__ == "__main__":
    INPUT_FILE = "data/processed/kpi_data.csv"
    OUTPUT_FILE = "data/processed/anomaly_data.csv"
    
    if os.path.exists(INPUT_FILE):
        df = pd.read_csv(INPUT_FILE)
        # Ensure date is the index
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            
        anom_df = detect_anomalies(df)
        anom_df.to_csv(OUTPUT_FILE)
        
        print(f"✅ Anomaly detection complete. Saved to {OUTPUT_FILE}")
        
        # --- THE MOMENT OF TRUTH: Did we catch the injected anomalies? ---
        total_anomalies = anom_df['is_anomaly'].sum()
        print(f"\nTotal days with detected anomalies: {total_anomalies}")
        
        print("\n--- CAUGHT: Conversion Rate Drops (Should show March & June dates) ---")
        print(anom_df[anom_df['anomaly_conv_rate'] == 1][['conversion_rate', 'conv_lower_bound']])
        
        print("\n--- CAUGHT: Ad Spend Spikes (Should show September dates) ---")
        print(anom_df[anom_df['anomaly_ad_spend'] == 1][['ad_spend', 'ad_upper_bound']])
        
        print("\n--- CAUGHT: Refund Rate Spikes (Should show November dates) ---")
        print(anom_df[anom_df['anomaly_refund'] == 1][['refund_rate', 'refund_rate_zscore']])
        
    else:
        print(f"❌ Error: Could not find {INPUT_FILE}. Run kpi_calculator.py first.")