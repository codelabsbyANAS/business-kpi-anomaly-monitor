import pandas as pd
import os

def score_anomalies(df):
    print("Scoring anomaly severity and generating business context...")
    
    # Filter down to ONLY the days where an anomaly was flagged
    anomalies = df[df['is_anomaly'] == 1].copy()
    
    severities = []
    impacts = []
    
    for index, row in anomalies.iterrows():
        severity = "WARNING" # Default severity
        impact_text = []
        
        # RULE 1: Conversion Rate Drop Logic
        if row['anomaly_conv_rate'] == 1:
            drop_pct = ((row['conv_rate_14d_mean'] - row['conversion_rate']) / row['conv_rate_14d_mean']) * 100
            impact_text.append(f"Conversion rate dropped by {drop_pct:.1f}% compared to the 14-day baseline.")
            
            # Multi-metric check: Did revenue also drop significantly?
            if row['revenue_growth_dod'] < -0.10:
                severity = "CRITICAL"
                impact_text.append("This drop coincides with a >10% daily revenue decline. The traffic is not converting.")
        
        # RULE 2: Ad Spend Spike Logic
        if row['anomaly_ad_spend'] == 1:
            spike_pct = ((row['ad_spend'] - row['ad_spend_14d_mean']) / row['ad_spend_14d_mean']) * 100
            impact_text.append(f"Advertising spend spiked by {spike_pct:.1f}% above normal levels.")
            
            # Multi-metric check: Did traffic fail to increase despite the ad spend?
            if row['traffic_growth_dod'] < 0.05:
                severity = "CRITICAL"
                impact_text.append("Website traffic did not show a proportional increase, indicating potential ad spend waste or platform glitch.")
                
        # RULE 3: Refund Rate Logic
        if row['anomaly_refund'] == 1:
            impact_text.append(f"Refund rate spiked to {row['refund_rate']*100:.1f}%, which is {row['refund_rate_zscore']:.1f} standard deviations above the yearly average.")
            
            if row['refund_rate'] > 0.035:
                severity = "CRITICAL"
                impact_text.append("High risk of customer dissatisfaction. Potential product quality or shipping issue requires immediate investigation.")
        
        severities.append(severity)
        impacts.append(" ".join(impact_text))
        
    anomalies['severity'] = severities
    anomalies['business_impact_context'] = impacts
    
    # Keep only the essential columns for our final reports
    cols_to_keep = ['is_anomaly', 'severity', 'business_impact_context', 
                    'revenue', 'orders', 'website_traffic', 'conversion_rate', 
                    'ad_spend', 'refund_rate', 'revenue_growth_dod']
    
    return anomalies[cols_to_keep]

if __name__ == "__main__":
    INPUT_FILE = "data/processed/anomaly_data.csv"
    OUTPUT_FILE = "data/processed/scored_anomalies.csv"
    
    if os.path.exists(INPUT_FILE):
        df = pd.read_csv(INPUT_FILE)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            
        scored_df = score_anomalies(df)
        scored_df.to_csv(OUTPUT_FILE)
        
        print(f"✅ Severity scoring complete! Processed {len(scored_df)} anomalies.")
        print(f"Saved to {OUTPUT_FILE}")
        
        print("\n--- SAMPLE BUSINESS IMPACT STATEMENTS ---")
        # Print a couple of the critical anomalies to see our logic in action
        criticals = scored_df[scored_df['severity'] == 'CRITICAL'].head(3)
        for date, row in criticals.iterrows():
            print(f"\nDate: {date.date()} | SEVERITY: {row['severity']}")
            print(f"Context: {row['business_impact_context']}")
            
    else:
        print(f"❌ Error: Could not find {INPUT_FILE}. Run anomaly_detector.py first.")