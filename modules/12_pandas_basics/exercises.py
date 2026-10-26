"""Module 12 exercises: pandas basics.

Run:  python check.py 12

Rule: don't modify the DataFrame you receive. Return new objects (use .copy() when
you add columns). Avoid loops over rows.
"""
import pandas as pd  # noqa: F401


def load_charges(path):
    """Read the CSV at `path` into a DataFrame and return it."""
    raise NotImplementedError


def profile(df):
    """Return {"rows": <int>, "columns": <int>, "column_names": <list of str>,
    "null_counts": <dict column -> number of nulls, including columns with 0>}"""
    raise NotImplementedError


def select_columns(df, columns):
    """Return a DataFrame with only the given columns, in the given order."""
    raise NotImplementedError


def filter_outlet(df, outlet):
    """Return rows where outlet equals `outlet`, with the index reset (0, 1, 2...)."""
    raise NotImplementedError


def bar_charges_over(df, min_amount):
    """Return rows where outlet == "Bar" AND amount > min_amount, index reset."""
    raise NotImplementedError


def large_charges(df, threshold):
    """Return rows with amount > threshold, sorted by amount descending, index reset."""
    raise NotImplementedError


def add_amount_with_tax(df, rate):
    """Return a COPY of df with a new column "amount_with_tax" = amount * (1 + rate),
    rounded to 2 decimals. The original df must not change."""
    raise NotImplementedError


def count_by_outlet(df):
    """Return a plain dict outlet -> number of charges."""
    raise NotImplementedError


def total_by_guest(df):
    """Return a DataFrame with exactly two columns ["guest_id", "total"]: total amount per
    guest rounded to 2, sorted by total descending, index reset."""
    raise NotImplementedError


def amount_stats(df):
    """Return {"count": int, "mean": float, "min": float, "max": float} for the amount
    column, floats rounded to 2. Make sure the values are plain Python int/float."""
    raise NotImplementedError


def refund_percentage(df):
    """Percentage of rows whose charge_type is "refund", rounded to 2 decimals
    (e.g. 5.27 means 5.27%). Return 0.0 for an empty DataFrame."""
    raise NotImplementedError


def to_snake_case_columns(df):
    """Return a copy with column names converted to snake_case:
    strip, lowercase, every run of non-alphanumeric characters -> "_", and no "_" at the ends.
      "Guest ID" -> "guest_id", " Charge Date " -> "charge_date", "Amount (USD)" -> "amount_usd"
    """
    raise NotImplementedError
