import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Business KPI Monitor", page_icon="📈", layout="wide")

# --- DATA LOADING ---
# We use @st.cache_data so the dashboard doesn't reload the CSVs every time you click a button
@st.cache_data
def load_data():
    # Load KPI Data
    kpi_df = pd.read_csv('data/processed/kpi_data.csv')
    kpi_df['date'] = pd.to_datetime(kpi_df['date'])
    kpi_df = kpi_df.sort_values('date')
    
    # Load Insights Data (Fallback/AI)
    try:
        insights_df = pd.read_csv('data/processed/ai_insights.csv')
        insights_df['date'] = pd.to_datetime(insights_df['date'])
    except FileNotFoundError:
        insights_df = pd.DataFrame() # Empty dataframe if file missing
        
    return kpi_df, insights_df

kpi_df, insights_df = load_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a Page:", 
                        ["Executive Overview", "Performance Trends", "Anomaly Monitor", "Business Insights"])

st.sidebar.markdown("---")
st.sidebar.info("This is a portfolio project demonstrating statistical anomaly detection and automated reporting.")

# --- PAGE 1: EXECUTIVE OVERVIEW ---
if page == "Executive Overview":
    st.title("📈 Executive Overview")
    st.markdown("Latest Daily Performance Metrics")
    
    # Get the most recent day's data
    latest_data = kpi_df.iloc[-1]
    
    # Create rows of metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Revenue", 
                  value=f"${latest_data['revenue']:,.2f}", 
                  delta=f"{latest_data['revenue_growth_dod']*100:.1f}%")
        st.metric(label="Profit Margin", 
                  value=f"{latest_data['profit_margin']*100:.1f}%")
        
    with col2:
        st.metric(label="Orders", 
                  value=f"{latest_data['orders']}", 
                  delta=f"{latest_data['orders_growth_dod']*100:.1f}%")
        st.metric(label="Gross Profit", 
                  value=f"${latest_data['gross_profit']:,.2f}")
        
    with col3:
        st.metric(label="Conversion Rate", 
                  value=f"{latest_data['conversion_rate']*100:.2f}%")
        st.metric(label="Ad Spend", 
                  value=f"${latest_data['ad_spend']:,.2f}")

# --- PAGE 2: PERFORMANCE TRENDS ---
elif page == "Performance Trends":
    st.title("📊 Performance Trends")
    
    st.subheader("Revenue Over Time")
    fig_rev = px.line(kpi_df, x='date', y=['revenue', 'revenue_7d_avg'], 
                      labels={'value': 'Revenue ($)', 'variable': 'Metric'},
                      title='Daily Revenue vs 7-Day Rolling Average')
    st.plotly_chart(fig_rev, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Website Traffic")
        fig_traffic = px.line(kpi_df, x='date', y='website_traffic')
        st.plotly_chart(fig_traffic, use_container_width=True)
        
    with col2:
        st.subheader("Conversion Rate")
        fig_conv = px.line(kpi_df, x='date', y='conversion_rate', color_discrete_sequence=['green'])
        st.plotly_chart(fig_conv, use_container_width=True)

# --- PAGE 3: ANOMALY MONITOR ---
elif page == "Anomaly Monitor":
    st.title("🚨 Anomaly Monitor")
    st.markdown("Monitoring system for statistically significant deviations in business KPIs.")
    
    if not insights_df.empty:
        # Display the anomalies in an interactive table
        display_df = insights_df[['date', 'severity', 'revenue', 'conversion_rate', 'refund_rate', 'business_impact_context']].copy()
        display_df['date'] = display_df['date'].dt.date
        
        # Style the severity column
        st.dataframe(display_df, use_container_width=True)
    else:
        st.warning("No anomalies found in the current dataset.")

# --- PAGE 4: BUSINESS INSIGHTS ---
elif page == "Business Insights":
    st.title("🧠 Business Insights")
    st.markdown("Automated analytical interpretation of critical business events.")
    
    if not insights_df.empty:
        # Filter for critical anomalies
        criticals = insights_df[insights_df['severity'] == 'CRITICAL']
        
        for index, row in criticals.iterrows():
            with st.expander(f"CRITICAL ANOMALY: {row['date'].date()}"):
                st.markdown(row['ai_summary'])
    else:
        st.info("No critical insights to display.")