"""Pure metric helpers, separated for testing."""
import pandas as pd


def summarize_sales(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"revenue": 0.0, "profit": 0.0, "orders": 0, "units": 0, "margin_pct": 0.0}
    revenue = float(df["net_revenue"].sum())
    profit = float(df["gross_profit"].sum())
    return {
        "revenue": revenue,
        "profit": profit,
        "orders": int(df["order_id"].nunique()),
        "units": int(df["quantity"].sum()),
        "margin_pct": (profit / revenue * 100) if revenue else 0.0,
    }


def monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["month", "net_revenue", "gross_profit"])
    result = df.assign(month=df["order_date"].dt.to_period("M").astype(str)).groupby("month", as_index=False).agg(
        net_revenue=("net_revenue", "sum"), gross_profit=("gross_profit", "sum")
    )
    return result.sort_values("month")
