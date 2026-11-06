import streamlit as st
st.title("SQL Analysis Guide")
st.markdown("""
Use `database/analysis_queries.sql` in MySQL Workbench to explore:
1. Overall revenue, cost of goods sold, and gross profit
2. Top products by net revenue
3. Monthly revenue with `LAG()` window function
4. Customers spending above the average
5. Store and regional performance
6. Category profitability and margin
7. Repeat customer rate
8. Revenue and profit by discount band

**Metric definitions**
- Net revenue = quantity × unit price × (1 − discount percentage / 100)
- Cost of goods sold (COGS) = quantity × product unit cost
- Gross profit = net revenue − COGS
- Gross margin = gross profit / net revenue × 100

The starter dataset is fictional and intended for learning/demo purposes.
""")
