"""Module 16 exercises: databases from Python.

Run:  python check.py 16

`conn` is always a sqlite3.Connection. Rows are dicts with keys:
charge_id, guest_id, outlet, charge_date (ISO string), amount, charge_type
"""
import sqlite3  # noqa: F401

import pandas as pd  # noqa: F401
from sqlalchemy import create_engine, text  # noqa: F401

ALLOWED_TABLES = {"charges", "guests"}


def create_charges_table(conn):
    """Create the `charges` table if it doesn't exist:
      charge_id INTEGER PRIMARY KEY, guest_id TEXT NOT NULL, outlet TEXT NOT NULL,
      charge_date TEXT NOT NULL, amount REAL NOT NULL, charge_type TEXT NOT NULL DEFAULT 'sale'
    Calling it twice must not fail. Commit."""
    raise NotImplementedError


def insert_charges(conn, rows):
    """Insert rows with executemany and NAMED placeholders (:charge_id, ...). Commit.
    Return the number of rows inserted (len(rows)). Duplicate charge_ids should raise
    sqlite3.IntegrityError (that's the PRIMARY KEY doing its job)."""
    raise NotImplementedError


def guest_total(conn, guest_id):
    """Return the guest's total amount rounded to 2, using a ? placeholder.
    Return 0.0 if the guest has no charges."""
    raise NotImplementedError


def upsert_charges(conn, rows):
    """Insert rows; if a charge_id already exists, update all its other columns
    (INSERT ... ON CONFLICT(charge_id) DO UPDATE SET ... = excluded....). Commit.
    Return len(rows). Running it twice must not create duplicates."""
    raise NotImplementedError


def load_all_or_nothing(conn, rows):
    """Insert all rows inside ONE transaction (use `with conn:`). If any row fails
    (e.g. amount is None -> NOT NULL constraint), NOTHING from this call is saved and the
    function returns 0. Otherwise return len(rows)."""
    raise NotImplementedError


def running_balances(conn):
    """Return a list of (guest_id, charge_id, running_balance) tuples using a SQL window
    function: SUM(amount) OVER (PARTITION BY guest_id ORDER BY charge_date, charge_id),
    rounded to 2 in SQL. Order the result by guest_id, charge_date, charge_id."""
    raise NotImplementedError


def latest_charge_ids(conn):
    """Return a list of (guest_id, charge_id) for each guest's latest charge
    (latest charge_date, ties -> highest charge_id). Use a CTE with ROW_NUMBER().
    Order by guest_id."""
    raise NotImplementedError


def count_rows(conn, table):
    """Return the number of rows in `table`. Table names can't be placeholders, so first
    check the name is in ALLOWED_TABLES; otherwise raise ValueError(f"table not allowed: {table}")."""
    raise NotImplementedError


def dataframe_round_trip(df, conn, table):
    """Write df to `table` with to_sql(if_exists="replace", index=False), then read it back
    with pd.read_sql_query and return the result."""
    raise NotImplementedError


def revenue_by_outlet_sqlalchemy(url):
    """Use SQLAlchemy: create_engine(url), and with engine.connect() run
    text("SELECT outlet, ROUND(SUM(amount), 2) AS total FROM charges GROUP BY outlet ORDER BY total DESC")
    Return a dict outlet -> total (in that order). Dispose the engine at the end."""
    raise NotImplementedError
