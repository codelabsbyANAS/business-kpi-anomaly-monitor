-- Find periods with unusually high refund rates (greater than 4%)
SELECT 
    date,
    refund_rate,
    revenue,
    orders
FROM business_metrics
WHERE refund_rate > 0.04
ORDER BY refund_rate DESC
LIMIT 10;