"""Reference solutions for Module 16."""
import sqlite3

import pandas as pd
from sqlalchemy import create_engine, text

ALLOWED_TABLES = {"charges", "guests"}

INSERT_SQL = """
    INSERT INTO charges (charge_id, guest_id, outlet, charge_date, amount, charge_type)
    VALUES (:charge_id, :guest_id, :outlet, :charge_date, :amount, :charge_type)
"""

UPSERT_SQL = INSERT_SQL + """
    ON CONFLICT(charge_id) DO UPDATE SET
        guest_id = excluded.guest_id,
        outlet = excluded.outlet,
        charge_date = excluded.charge_date,
        amount = excluded.amount,
        charge_type = excluded.charge_type
"""


def create_charges_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS charges (
            charge_id   INTEGER PRIMARY KEY,
            guest_id    TEXT NOT NULL,
            outlet      TEXT NOT NULL,
            charge_date TEXT NOT NULL,
            amount      REAL NOT NULL,
            charge_type TEXT NOT NULL DEFAULT 'sale'
        )
    """)
    conn.commit()


def insert_charges(conn, rows):
    conn.executemany(INSERT_SQL, rows)
    conn.commit()
    return len(rows)


def guest_total(conn, guest_id):
    total = conn.execute("SELECT SUM(amount) FROM charges WHERE guest_id = ?", (guest_id,)).fetchone()[0]
    return round(total, 2) if total is not None else 0.0


def upsert_charges(conn, rows):
    conn.executemany(UPSERT_SQL, rows)
    conn.commit()
    return len(rows)


def load_all_or_nothing(conn, rows):
    try:
        with conn:
            conn.executemany(INSERT_SQL, rows)
    except sqlite3.Error:
        return 0
    return len(rows)


def running_balances(conn):
    return conn.execute("""
        SELECT guest_id, charge_id,
               ROUND(SUM(amount) OVER (PARTITION BY guest_id ORDER BY charge_date, charge_id), 2)
        FROM charges
        ORDER BY guest_id, charge_date, charge_id
    """).fetchall()


def latest_charge_ids(conn):
    return conn.execute("""
        WITH ranked AS (
            SELECT guest_id, charge_id,
                   ROW_NUMBER() OVER (PARTITION BY guest_id ORDER BY charge_date DESC, charge_id DESC) AS rn
            FROM charges
        )
        SELECT guest_id, charge_id FROM ranked WHERE rn = 1 ORDER BY guest_id
    """).fetchall()


def count_rows(conn, table):
    if table not in ALLOWED_TABLES:
        raise ValueError(f"table not allowed: {table}")
    return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


def dataframe_round_trip(df, conn, table):
    df.to_sql(table, conn, if_exists="replace", index=False)
    return pd.read_sql_query(f"SELECT * FROM {table}", conn)


def revenue_by_outlet_sqlalchemy(url):
    engine = create_engine(url)
    try:
        with engine.connect() as conn:
            rows = conn.execute(text(
                "SELECT outlet, ROUND(SUM(amount), 2) AS total FROM charges GROUP BY outlet ORDER BY total DESC"
            )).fetchall()
        return {outlet: total for outlet, total in rows}
    finally:
        engine.dispose()
