import pandas as pd
from src.metrics import summarize_sales, monthly_sales


def test_summarize_sales():
    df = pd.DataFrame({"order_id": [1, 1, 2], "quantity": [2, 1, 3], "net_revenue": [100.0, 50.0, 150.0], "gross_profit": [20.0, 10.0, 30.0]})
    result = summarize_sales(df)
    assert result["revenue"] == 300.0
    assert result["profit"] == 60.0
    assert result["orders"] == 2
    assert result["units"] == 6
    assert result["margin_pct"] == 20.0


def test_empty_sales():
    result = summarize_sales(pd.DataFrame())
    assert result["revenue"] == 0.0
    assert result["orders"] == 0
