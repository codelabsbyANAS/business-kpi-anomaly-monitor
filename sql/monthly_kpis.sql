-- Calculate Monthly Revenue, Orders, and MoM Revenue Growth
WITH MonthlyStats AS (
    SELECT 
        strftime('%Y-%m', date) AS month,
        SUM(revenue) AS total_revenue,
        SUM(orders) AS total_orders,
        SUM(gross_profit) AS total_profit,
        AVG(conversion_rate) AS avg_conversion_rate
    FROM business_metrics
    GROUP BY 1
)
SELECT 
    month,
    ROUND(total_revenue, 2) AS revenue,
    total_orders AS orders,
    ROUND(total_profit, 2) AS profit,
    ROUND(avg_conversion_rate, 4) AS avg_conversion_rate,
    -- Calculate Month-over-Month Revenue Growth using Window Function LAG()
    ROUND(((total_revenue - LAG(total_revenue) OVER (ORDER BY month)) / LAG(total_revenue) OVER (ORDER BY month)) * 100, 2) AS mom_revenue_growth_pct
FROM MonthlyStats
ORDER BY month;