"""Data loading and validation functions."""
import pandas as pd
from src.queries import SALES_DETAIL


def load_sales(connection):
    df = pd.read_sql(SALES_DETAIL, connection)
    if df.empty:
        return df
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    numeric = ["quantity", "unit_price", "discount_pct", "unit_cost", "net_revenue", "gross_profit"]
    for column in numeric:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    df = df.dropna(subset=["order_id", "order_date", "net_revenue"])
    return df
