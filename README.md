# 📈 Business KPI Anomaly Monitor

An end-to-end data pipeline and interactive web dashboard designed to automatically ingest business metrics, detect statistically significant anomalies, and generate actionable business insights.

## 🏗️ System Architecture

This project simulates a production-grade automated analytics pipeline, processing raw data through several modular stages before serving it to a frontend application:

1. **Data Ingestion & Storage:** Raw CSV data is processed and loaded into a local `SQLite` database.
2. **KPI Engine:** Calculates rolling averages, day-over-day growth, and aggregate metrics using `Pandas`.
3. **Statistical Detection:** Identifies anomalies (e.g., revenue drops, ad spend spikes) using Z-scores and 14-day rolling standard deviation baselines.
4. **Severity Scoring & Interpretation:** Evaluates the business impact of detected anomalies and assigns severity levels (WARNING vs. CRITICAL).
5. **AI Insight Generation:** Integrates with the `OpenAI API` to generate executive summaries. **Features a deterministic local fallback generator** to ensure pipeline resilience during API outages or rate limits.
6. **Frontend UI:** A responsive, multi-page web application built with `Streamlit` and `Plotly` to visualize trends and flag critical events.

## 🚀 Key Features

*   **Transparent Statistical Modeling:** Uses explicit mathematical thresholds (not black-box ML) to ensure all flagged anomalies are highly interpretable to stakeholders.
*   **System Resilience:** Built-in fault tolerance handling external API failures gracefully without crashing the data pipeline.
*   **Full-Stack Implementation:** Bridges the gap between backend data modeling/database management and frontend interactive visualization.
*   **Secure Credential Management:** Utilizes `.env` configurations to protect sensitive API keys.

## 💻 Tech Stack

*   **Language:** Python 3.x
*   **Data Processing:** Pandas, NumPy
*   **Database:** SQLite
*   **Visualization & UI:** Streamlit, Plotly Express
*   **External Integration:** OpenAI API, python-dotenv

## 🛠️ Local Setup & Installation

**1. Clone the repository**
```bash
git clone [https://github.com/YourUsername/business-kpi-anomaly-monitor.git](https://github.com/YourUsername/business-kpi-anomaly-monitor.git)
cd business-kpi-anomaly-monitor