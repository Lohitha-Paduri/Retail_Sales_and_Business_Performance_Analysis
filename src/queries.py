"""Central SQL queries. Values are parameterized where user input is used."""
SALES_DETAIL = """
SELECT o.order_id, o.order_date, o.status, c.full_name AS customer,
       s.store_name, s.region, p.product_name, p.category,
       oi.quantity, oi.unit_price, oi.discount_pct, p.unit_cost,
       oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100) AS net_revenue,
       oi.quantity * (oi.unit_price * (1 - oi.discount_pct / 100) - p.unit_cost) AS gross_profit
FROM orders o
JOIN customers c ON c.customer_id=o.customer_id
JOIN stores s ON s.store_id=o.store_id
JOIN order_items oi ON oi.order_id=o.order_id
JOIN products p ON p.product_id=oi.product_id
WHERE o.status='completed'
"""
