import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def generate_fallback_summary(row):
    """Deterministic fallback if AI API fails or key is missing."""
    date_str = row.name.date() if hasattr(row.name, 'date') else row.name
    return f"""
1. Executive Summary:
A {row['severity']} anomaly was detected on {date_str}.

2. Key Findings:
{row['business_impact_context']}

3. Potential Business Impact:
KPIs affected: Revenue (${row['revenue']}), Traffic ({row['website_traffic']}), Conversion ({row['conversion_rate']*100:.2f}%).
This deviation requires immediate attention to prevent further metric degradation.

4. Recommended Investigation Areas:
Please review traffic sources, recent website deployments, product quality reports, and ad spend allocations.
"""

def generate_ai_insight(row, client=None):
    if not client:
        return generate_fallback_summary(row).strip()
        
    date_str = row.name.date() if hasattr(row.name, 'date') else row.name
    prompt = f"""
    You are an expert Business Data Analyst. Review the following daily KPI anomaly and provide a concise, professional explanation.
    DO NOT invent any numbers. Use ONLY the metrics provided.

    Metrics for {date_str}:
    - Severity: {row['severity']}
    - System Context: {row['business_impact_context']}
    - Revenue: ${row['revenue']} (DoD Growth: {row['revenue_growth_dod']*100:.1f}%)
    - Orders: {row['orders']}
    - Website Traffic: {row['website_traffic']}
    - Conversion Rate: {row['conversion_rate']*100:.2f}%
    - Ad Spend: ${row['ad_spend']}
    - Refund Rate: {row['refund_rate']*100:.2f}%

    Output exactly in this format:
    1. Executive Summary:
    2. Key Findings:
    3. Potential Business Impact:
    4. Recommended Investigation Areas:
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a highly analytical and concise business data assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.2 # Low temperature to prevent hallucination
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ AI API Failed: {e}. Switching to fallback.")
        return generate_fallback_summary(row).strip()

if __name__ == "__main__":
    INPUT_FILE = "data/processed/scored_anomalies.csv"
    OUTPUT_FILE = "data/processed/ai_insights.csv"
    
    api_key = os.getenv("OPENAI_API_KEY")
    # Initialize OpenAI client only if a real key is provided
    client = OpenAI(api_key=api_key) if api_key and api_key != "your_api_key_here_if_you_have_one" else None
    
    if not client:
        print("⚠️ No valid OPENAI_API_KEY found in .env file.")
        print("🔄 Using robust deterministic fallback generator instead (Perfect for local testing!).\n")
    
    if os.path.exists(INPUT_FILE):
        df = pd.read_csv(INPUT_FILE)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
        
        # To save API costs/time, we will only generate deep insights for CRITICAL anomalies
        criticals = df[df['severity'] == 'CRITICAL'].copy()
        print(f"Generating insights for {len(criticals)} CRITICAL anomalies...")
        
        # Apply the AI/Fallback function to each critical row
        criticals['ai_summary'] = criticals.apply(lambda row: generate_ai_insight(row, client), axis=1)
        
        criticals.to_csv(OUTPUT_FILE)
        print(f"✅ Interpretation complete! Saved to {OUTPUT_FILE}")
        
        # Print the very first insight as a sample
        if not criticals.empty:
            print("\n" + "="*50)
            print("SAMPLE INSIGHT GENERATED")
            print("="*50)
            print(criticals.iloc[0]['ai_summary'])
            print("="*50)
    else:
        print(f"❌ Error: Could not find {INPUT_FILE}. Run severity_scoring.py first.")