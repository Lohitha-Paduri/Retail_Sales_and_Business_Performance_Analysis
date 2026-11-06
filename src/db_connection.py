"""MySQL connection helpers for the Streamlit app."""
import os
import mysql.connector


def get_connection():
    """Read credentials from Streamlit secrets or environment variables."""
    try:
        import streamlit as st
        cfg = st.secrets.get("mysql", {})
    except Exception:
        cfg = {}
    return mysql.connector.connect(
        host=cfg.get("host", os.getenv("MYSQL_HOST", "localhost")),
        port=int(cfg.get("port", os.getenv("MYSQL_PORT", "3306"))),
        user=cfg.get("user", os.getenv("MYSQL_USER", "root")),
        password=cfg.get("password", os.getenv("MYSQL_PASSWORD", "")),
        database=cfg.get("database", os.getenv("MYSQL_DATABASE", "retail_sales_db")),
    )
