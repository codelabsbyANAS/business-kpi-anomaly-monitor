# 📈 Business KPI Anomaly Monitor

An end-to-end data pipeline and interactive web dashboard designed to automatically ingest business metrics, detect statistically significant anomalies, and generate actionable business insights.

## 🏗️ System Architecture

This project simulates a production-grade automated analytics pipeline, processing raw data through several modular stages before serving it to a frontend application:

1. **Data Ingestion & Storage:** Raw CSV data is processed and loaded into a local `SQLite` database.
2. **KPI Engine:** Calculates rolling averages, day-over-day growth, and aggregate metrics using `Pandas`.
3. **Statistical Detection:** Identifies anomalies (e.g., revenue drops, ad spend spikes) using Z-scores and 14-day rolling standard deviation baselines.
4. **Severity Scoring & Interpretation:** Evaluates the business impact of detected anomalies and assigns severity levels (WARNING vs. CRITICAL).
5. **AI Insight Generation:** Integrates with a local `Ollama` LLM to generate executive summaries. **Features a deterministic local fallback generator** to ensure pipeline resilience if the local LLM is offline or unreachable.
6. **Frontend UI:** A responsive, multi-page web application built with `Streamlit` and `Plotly` to visualize trends and flag critical events.

## 🚀 Key Features

*   **Transparent Statistical Modeling:** Uses explicit mathematical thresholds (not black-box ML) to ensure all flagged anomalies are highly interpretable to stakeholders.
*   **System Resilience:** Built-in fault tolerance handling local LLM connection failures gracefully without crashing the data pipeline.
*   **Full-Stack Implementation:** Bridges the gap between backend data modeling/database management and frontend interactive visualization.

## 💻 Tech Stack

*   **Language:** Python 3.x
*   **Data Processing:** Pandas, NumPy
*   **Database:** SQLite
*   **Visualization & UI:** Streamlit, Plotly Express
*   **External Integration:** Ollama (local LLM)

## 🧪 Validation & Known Limitations

**Note on data**: Since real production business data with known ground-truth anomalies isn't publicly available, I built a synthetic data generator (`generate_data.py`) that simulates a year of e-commerce metrics and deliberately injects 4 known anomalies (bot traffic in March, a checkout bug in June, an ad platform glitch in September, a bad product batch in November) at specific dates. This ground-truth approach let me objectively measure detection accuracy rather than just eyeballing results — testing confirmed the Z-score method reliably caught 100% of the injected refund-rate spikes. However, testing also revealed a real limitation of rolling-baseline detection: for sustained multi-day anomalies (e.g., the injected ad-spend spike and conversion-rate drops), the detector typically flags only the first 1-2 days before the rolling window adapts and absorbs the anomaly into the new 'normal.' This is a known trade-off of rolling-window methods and a good direction for future improvement (e.g., comparing against a longer, anomaly-excluded baseline).

## 🛠️ Local Setup & Installation

**1. Clone the repository**
```bash
git clone [https://github.com/YourUsername/business-kpi-anomaly-monitor.git](https://github.com/YourUsername/business-kpi-anomaly-monitor.git)
cd business-kpi-anomaly-monitor