USE retail_sales_db;

-- 1. Overall sales and profit (cancelled orders excluded)
SELECT ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 2) AS net_revenue,
       ROUND(SUM(oi.quantity * p.unit_cost), 2) AS cogs,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100) - oi.quantity * p.unit_cost), 2) AS gross_profit
FROM orders o JOIN order_items oi ON o.order_id=oi.order_id
JOIN products p ON p.product_id=oi.product_id
WHERE o.status='completed';

-- 2. Top products by net revenue
SELECT p.product_name, SUM(oi.quantity) AS units_sold,
       ROUND(SUM(oi.quantity*oi.unit_price*(1-oi.discount_pct/100)),2) AS net_revenue
FROM products p JOIN order_items oi ON p.product_id=oi.product_id
JOIN orders o ON o.order_id=oi.order_id WHERE o.status='completed'
GROUP BY p.product_id,p.product_name ORDER BY net_revenue DESC LIMIT 5;

-- 3. Monthly revenue and previous-month comparison (MySQL 8+)
WITH monthly AS (
 SELECT DATE_FORMAT(o.order_date,'%Y-%m') AS month,
        SUM(oi.quantity*oi.unit_price*(1-oi.discount_pct/100)) AS revenue
 FROM orders o JOIN order_items oi ON o.order_id=oi.order_id
 WHERE o.status='completed' GROUP BY DATE_FORMAT(o.order_date,'%Y-%m')
)
SELECT month, ROUND(revenue,2) AS revenue,
       ROUND(LAG(revenue) OVER (ORDER BY month),2) AS previous_month_revenue
FROM monthly ORDER BY month;

-- 4. Customers whose lifetime spend is above average customer spend
WITH customer_spend AS (
 SELECT o.customer_id, SUM(oi.quantity*oi.unit_price*(1-oi.discount_pct/100)) AS spend
 FROM orders o JOIN order_items oi ON o.order_id=oi.order_id
 WHERE o.status='completed' GROUP BY o.customer_id
)
SELECT c.full_name, ROUND(cs.spend,2) AS total_spend FROM customer_spend cs
JOIN customers c ON c.customer_id=cs.customer_id
WHERE cs.spend > (SELECT AVG(spend) FROM customer_spend) ORDER BY spend DESC;

-- 5. Store performance
SELECT s.store_name, s.region, COUNT(DISTINCT o.order_id) AS orders_count,
 ROUND(SUM(oi.quantity*oi.unit_price*(1-oi.discount_pct/100)),2) AS revenue
FROM stores s JOIN orders o ON s.store_id=o.store_id
JOIN order_items oi ON oi.order_id=o.order_id WHERE o.status='completed'
GROUP BY s.store_id,s.store_name,s.region ORDER BY revenue DESC;

-- 6. Category revenue and margin
SELECT p.category,
 ROUND(SUM(oi.quantity*oi.unit_price*(1-oi.discount_pct/100)),2) AS revenue,
 ROUND(SUM(oi.quantity*oi.unit_price*(1-oi.discount_pct/100)-oi.quantity*p.unit_cost),2) AS profit,
 ROUND(100*SUM(oi.quantity*oi.unit_price*(1-oi.discount_pct/100)-oi.quantity*p.unit_cost)
 / NULLIF(SUM(oi.quantity*oi.unit_price*(1-oi.discount_pct/100)),0),2) AS margin_pct
FROM products p JOIN order_items oi ON p.product_id=oi.product_id
JOIN orders o ON o.order_id=oi.order_id WHERE o.status='completed'
GROUP BY p.category ORDER BY revenue DESC;

-- 7. Repeat customer rate
WITH counts AS (
 SELECT customer_id, COUNT(*) AS order_count FROM orders WHERE status='completed' GROUP BY customer_id
)
SELECT ROUND(100*SUM(order_count>1)/COUNT(*),2) AS repeat_customer_rate_pct FROM counts;

-- 8. Discount impact by discount band
SELECT CASE WHEN oi.discount_pct=0 THEN 'No discount'
            WHEN oi.discount_pct<=5 THEN '1-5%'
            WHEN oi.discount_pct<=10 THEN '6-10%' ELSE 'Above 10%' END AS discount_band,
       COUNT(DISTINCT o.order_id) AS orders_count,
       ROUND(SUM(oi.quantity*oi.unit_price*(1-oi.discount_pct/100)),2) AS net_revenue,
       ROUND(SUM(oi.quantity*oi.unit_price*(1-oi.discount_pct/100)-oi.quantity*p.unit_cost),2) AS profit
FROM order_items oi JOIN orders o ON o.order_id=oi.order_id
JOIN products p ON p.product_id=oi.product_id WHERE o.status='completed'
GROUP BY discount_band ORDER BY MIN(oi.discount_pct);

-- Note: don't join payments directly to order_items for revenue calculations; multiple rows can multiply totals.
