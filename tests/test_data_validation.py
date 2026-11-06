import pandas as pd
from src.metrics import monthly_sales


def test_monthly_sales_groups_by_month():
    df = pd.DataFrame({"order_date": pd.to_datetime(["2025-01-01", "2025-01-20", "2025-02-01"]), "net_revenue": [10, 20, 30], "gross_profit": [2, 5, 8]})
    result = monthly_sales(df)
    assert list(result["month"]) == ["2025-01", "2025-02"]
    assert list(result["net_revenue"]) == [30, 30]
