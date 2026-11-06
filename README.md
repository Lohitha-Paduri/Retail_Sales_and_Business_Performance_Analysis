# Retail Sales and Business Performance Analysis

A portfolio dashboard built with **MySQL, Python, Pandas, Plotly and Streamlit**. The refreshed UI uses a polished executive analytics layout with a dark navy-to-teal header, KPI cards, monthly revenue/profit trends, category and product rankings, store comparisons, customer insights, automatically generated observations, and CSV export.

## Features
- Six-table relational schema with primary/foreign keys, constraints and indexes
- SQL joins, aggregates, CASE expressions, CTEs, subqueries and window functions
- Filters for date, product category, region and store
- KPI cards for net revenue, gross profit, orders, units sold and profit margin
- Revenue/profit trend chart, category chart, top-product chart and store comparison
- Customer spend table and repeat vs. one-time customer mix
- Generated observations and downloadable filtered CSV report
- Basic metric tests

## Project structure
```text
retail-sales-business-performance/
├── app.py
├── requirements.txt
├── README.md
├── database/
│   ├── schema.sql
│   ├── sample_data.sql
│   └── analysis_queries.sql
├── src/
│   ├── db_connection.py
│   ├── data_processing.py
│   ├── metrics.py
│   └── queries.py
├── pages/
│   └── 1_SQL_Analysis_Guide.py
├── tests/
├── assets/
└── .streamlit/
    └── secrets.toml.example
```

## Important: use a supported Python version
Your traceback shows Python 3.7. Current versions of Streamlit, Pandas and other dependencies no longer support Python 3.7. Install **Python 3.11** (recommended), then create a fresh virtual environment from this project folder.

Check installed Python versions:
```powershell
py -0p
```

Create and activate the environment (assuming Python 3.11 is installed):
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
If PowerShell blocks activation, use Command Prompt and run `.venv\Scripts\activate.bat`, or run `.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.venv\Scripts\python.exe -m streamlit run app.py` without activation.

## Configure MySQL
1. Start MySQL Server and open MySQL Workbench.
2. Run `database/schema.sql` first, then `database/sample_data.sql`.
3. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`.
4. Update the host, port, username, password and database name with your own local MySQL details. Do not upload `secrets.toml` to GitHub.

## Run the dashboard
From the project root, with the virtual environment activated:
```powershell
python -m streamlit run app.py
```

Run tests:
```powershell
python -m pytest
```

## Data notes
- Sample records are fictional.
- Sales totals are calculated from order line items. Payment records are not joined into line-item totals because multiple payments could multiply sales values.
- Cancelled orders are excluded by the query. Returns/refunds are not fully modeled in this starter.
- Verify the metrics against your data before presenting the project in an interview. Do not claim deployment or measured performance improvements until completed and tested.
