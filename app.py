import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.db_connection import get_connection
from src.data_processing import load_sales
from src.metrics import summarize_sales, monthly_sales

st.set_page_config(page_title="RetailPulse | Sales Intelligence", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

# Visual theme: clean executive retail analytics dashboard.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root { --ink:#14213d; --muted:#68758b; --teal:#0f9d8a; --blue:#4568dc; --line:#e8edf4; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background: #f5f7fb; color:var(--ink); }
.block-container { padding-top:1.6rem; padding-bottom:2rem; max-width:1500px; }
section[data-testid="stSidebar"] { background: #14213d; }
section[data-testid="stSidebar"] * { color:#f4f7fb !important; }
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] span { color:#14213d !important; }
section[data-testid="stSidebar"] [data-testid="stDateInput"] input { color:#14213d !important; }
.hero { background:linear-gradient(115deg,#14213d 0%,#203d66 58%,#0f9d8a 100%); padding:25px 30px; border-radius:18px; color:white; margin-bottom:20px; box-shadow:0 10px 30px rgba(20,33,61,.12); }
.hero h1 { font-family:'Manrope',sans-serif; font-size:30px; font-weight:800; margin:0; color:white; letter-spacing:-.7px; }
.hero p { margin:7px 0 0; color:#dce8f5; font-size:14px; }
.eyebrow { text-transform:uppercase; letter-spacing:2px; font-size:10px; font-weight:700; color:#b7f1e7; margin-bottom:8px; }
.section-title { font-family:'Manrope',sans-serif; font-weight:800; font-size:18px; color:#14213d; margin:8px 0 3px; }
.section-sub { color:#68758b; font-size:12px; margin-bottom:12px; }
div[data-testid="stMetric"] { background:white; border:1px solid #e8edf4; padding:17px 18px; border-radius:14px; box-shadow:0 3px 12px rgba(20,33,61,.035); }
div[data-testid="stMetricLabel"] p { color:#68758b !important; font-size:12px !important; font-weight:600 !important; }
div[data-testid="stMetricValue"] { color:#14213d !important; font-family:'Manrope',sans-serif; font-size:25px !important; font-weight:800 !important; }
div[data-testid="stMetricDelta"] { font-size:11px !important; }
div[data-testid="stPlotlyChart"] { background:white; border:1px solid #e8edf4; border-radius:14px; padding:9px; }
div[data-testid="stDataFrame"] { background:white; border-radius:12px; }
hr { border-color:#e8edf4; }
.stDownloadButton button { background:#0f9d8a; color:white; border:0; border-radius:9px; font-weight:700; }
.stDownloadButton button:hover { background:#0b8273; color:white; }
.small-note { font-size:11px; color:#68758b; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="eyebrow">RETAIL INTELLIGENCE • PERFORMANCE OVERVIEW</div>
  <h1>Retail Sales & Business Performance</h1>
  <p>Understand sales, profitability, product mix and store performance — all in one place.</p>
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def fetch_data():
    connection = get_connection()
    try:
        return load_sales(connection)
    finally:
        connection.close()

try:
    data = fetch_data()
except Exception as exc:
    st.error("The dashboard could not load data from MySQL.")
    st.markdown("**First, install the required packages using the Python version supported by this project:**")
    st.code("py -3.11 -m venv .venv\n.\\.venv\\Scripts\\Activate.ps1\npython -m pip install -r requirements.txt", language="powershell")
    st.markdown("Then check that MySQL is running, both SQL files were executed, and `.streamlit/secrets.toml` has the correct credentials.")
    with st.expander("Technical details"):
        st.code(str(exc))
    st.stop()

if data.empty:
    st.warning("No completed sales were returned. Run database/schema.sql and database/sample_data.sql in MySQL Workbench.")
    st.stop()

# Ensure expected types before filtering.
data["order_date"] = pd.to_datetime(data["order_date"], errors="coerce")
with st.sidebar:
    st.markdown("## 🎛️ Dashboard filters")
    st.caption("Choose a slice of the business to explore.")
    min_date = data.order_date.min().date()
    max_date = data.order_date.max().date()
    date_range = st.date_input("Order date", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    categories = st.multiselect("Product category", sorted(data.category.dropna().unique()), default=sorted(data.category.dropna().unique()))
    regions = st.multiselect("Region", sorted(data.region.dropna().unique()), default=sorted(data.region.dropna().unique()))
    stores = st.multiselect("Store", sorted(data.store_name.dropna().unique()), default=sorted(data.store_name.dropna().unique()))
    st.markdown("---")
    st.caption("Data source: MySQL • Refreshed every 60 seconds")

filtered = data.copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    filtered = filtered[filtered.order_date.dt.date.between(date_range[0], date_range[1])]
if categories:
    filtered = filtered[filtered.category.isin(categories)]
else:
    filtered = filtered.iloc[0:0]
if regions:
    filtered = filtered[filtered.region.isin(regions)]
else:
    filtered = filtered.iloc[0:0]
if stores:
    filtered = filtered[filtered.store_name.isin(stores)]
else:
    filtered = filtered.iloc[0:0]

st.markdown('<div class="section-title">Business at a glance</div><div class="section-sub">Key performance indicators for the selected period</div>', unsafe_allow_html=True)
if filtered.empty:
    st.warning("No sales records match these filters. Select another date range, category, region or store.")
    st.stop()

m = summarize_sales(filtered)
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Net revenue", f"₹{m['revenue']:,.0f}")
k2.metric("Gross profit", f"₹{m['profit']:,.0f}")
k3.metric("Orders", f"{m['orders']:,}")
k4.metric("Units sold", f"{m['units']:,}")
k5.metric("Profit margin", f"{m['margin_pct']:.1f}%")

# Consistent chart styling.
chart_layout = dict(template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=12,r=12,t=50,b=12), font=dict(family="DM Sans, sans-serif", color="#68758b", size=11), title_font=dict(family="Manrope, sans-serif", size=15, color="#14213d"), legend_title_text="")

st.markdown('<div class="section-title">Sales & profitability trends</div><div class="section-sub">Track how revenue and gross profit change over time.</div>', unsafe_allow_html=True)
left, right = st.columns([1.35, 1])
with left:
    monthly = monthly_sales(filtered)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly["month"], y=monthly["net_revenue"], name="Net revenue", mode="lines+markers", line=dict(color="#0f9d8a", width=3), marker=dict(size=7), fill="tozeroy", fillcolor="rgba(15,157,138,.10)"))
    fig.add_trace(go.Scatter(x=monthly["month"], y=monthly["gross_profit"], name="Gross profit", mode="lines+markers", line=dict(color="#4568dc", width=2.5), marker=dict(size=6)))
    fig.update_layout(title="Monthly revenue vs. gross profit", xaxis_title="Month", yaxis_title="Amount (₹)", **chart_layout)
    st.plotly_chart(fig, use_container_width=True)
with right:
    by_category = filtered.groupby("category", as_index=False).agg(net_revenue=("net_revenue", "sum"), gross_profit=("gross_profit", "sum"))
    by_category = by_category.sort_values("net_revenue", ascending=True)
    fig = px.bar(by_category, x="net_revenue", y="category", orientation="h", text_auto=".2s", color_discrete_sequence=["#0f9d8a"], title="Revenue by product category")
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(xaxis_title="Net revenue (₹)", yaxis_title="", **chart_layout)
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-title">Products & store performance</div><div class="section-sub">Identify top-performing products and compare store revenue.</div>', unsafe_allow_html=True)
left, right = st.columns([1.05, 1])
with left:
    products = filtered.groupby("product_name", as_index=False).agg(units_sold=("quantity", "sum"), net_revenue=("net_revenue", "sum"), gross_profit=("gross_profit", "sum")).sort_values("net_revenue", ascending=False)
    fig = px.bar(products.head(8).sort_values("net_revenue"), x="net_revenue", y="product_name", orientation="h", color_discrete_sequence=["#4568dc"], title="Top 8 products by revenue", text_auto=".2s")
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(xaxis_title="Net revenue (₹)", yaxis_title="", **chart_layout)
    st.plotly_chart(fig, use_container_width=True)
with right:
    stores_df = filtered.groupby(["store_name", "region"], as_index=False).agg(net_revenue=("net_revenue", "sum"), gross_profit=("gross_profit", "sum"), orders=("order_id", "nunique")).sort_values("net_revenue", ascending=False)
    fig = px.bar(stores_df, x="store_name", y="net_revenue", color="region", barmode="group", title="Store revenue comparison", color_discrete_sequence=["#0f9d8a", "#4568dc", "#f0a44b", "#9b6de3"])
    fig.update_layout(xaxis_title="Store", yaxis_title="Net revenue (₹)", **chart_layout)
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-title">Customer insights</div><div class="section-sub">Find high-value customers and understand repeat purchasing.</div>', unsafe_allow_html=True)
customer = filtered.groupby("customer", as_index=False).agg(total_spend=("net_revenue", "sum"), orders=("order_id", "nunique"), units=("quantity", "sum")).sort_values("total_spend", ascending=False)
customer["segment"] = customer["orders"].apply(lambda n: "Repeat customer" if n > 1 else "One-time customer")
ca, cb = st.columns([1.4, 1])
with ca:
    st.dataframe(customer.rename(columns={"customer":"Customer", "total_spend":"Total spend (₹)", "orders":"Orders", "units":"Units", "segment":"Customer segment"}), use_container_width=True, hide_index=True)
with cb:
    segments = customer.groupby("segment", as_index=False).agg(customers=("customer", "count"))
    fig = px.pie(segments, names="segment", values="customers", hole=.62, title="Customer type mix", color_discrete_sequence=["#0f9d8a", "#d9e2f2"])
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(**chart_layout)
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-title">Business observations</div><div class="section-sub">Automatically generated from the currently selected data.</div>', unsafe_allow_html=True)
best_category = by_category.sort_values("net_revenue", ascending=False).iloc[0]
best_product = products.iloc[0]
best_store = stores_df.iloc[0]
o1, o2, o3 = st.columns(3)
with o1:
    st.info(f"**Leading category**\n\n{best_category['category']} leads with ₹{best_category['net_revenue']:,.0f} in net revenue.")
with o2:
    st.info(f"**Top product**\n\n{best_product['product_name']} generated ₹{best_product['net_revenue']:,.0f} from {int(best_product['units_sold'])} units.")
with o3:
    st.info(f"**Leading store**\n\n{best_store['store_name']} ({best_store['region']}) generated ₹{best_store['net_revenue']:,.0f}.")

st.markdown('<div class="section-title">Export report</div><div class="section-sub">Download the sales records currently shown by your filters.</div>', unsafe_allow_html=True)
st.download_button("⬇ Download filtered sales CSV", data=filtered.to_csv(index=False).encode("utf-8"), file_name="retail_sales_filtered_report.csv", mime="text/csv")
st.markdown('<p class="small-note">Portfolio project • Sample records are fictional • Metrics reflect the selected filters</p>', unsafe_allow_html=True)
