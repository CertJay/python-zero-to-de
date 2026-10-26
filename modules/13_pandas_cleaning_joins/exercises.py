"""Module 13 exercises: cleaning, groupby, joins, pivots, window functions.

Run:  python check.py 13

Don't modify the DataFrames you receive; return new ones.
"""
import pandas as pd  # noqa: F401

DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%b %d %Y"]

OUTLET_MAP = {
    "bar": "Bar", "the bar": "Bar", "resto": "Restaurant", "restaurant": "Restaurant",
    "spa": "Spa", "shore excursions": "Excursions", "excursions": "Excursions",
    "cafe": "Cafe", "café": "Cafe", "boutique": "Boutique",
}


def parse_mixed_dates(series):
    """Parse a Series of date strings that use any of DATE_FORMATS into a datetime
    Series (unparseable values -> NaT). Strip spaces first. Never guess the format.
    See lesson section 2."""
    raise NotImplementedError


def clean_charges(raw):
    """Clean the raw charges DataFrame (read from onboard_charges_raw.csv). Return a new
    DataFrame where:
      1. exact duplicate rows are removed (keep the first)
      2. outlet is standardized with OUTLET_MAP (collapse spaces, lowercase, map;
         unknown -> title case)
      3. charge_date is a datetime column (parse_mixed_dates)
      4. amount is numeric (pd.to_numeric with errors="coerce")
      5. rows with a missing amount or missing date are dropped
      6. rows are sorted by charge_date then charge_id, index reset
    """
    raise NotImplementedError


def missing_report(df):
    """Return a dict column -> number of nulls, ONLY for columns that have at least one
    null. Values must be plain ints."""
    raise NotImplementedError


def revenue_by_outlet_day(df):
    """Group by charge_date and outlet. Return a DataFrame with columns
    ["charge_date", "outlet", "total", "charges"] where total = sum of amount (rounded 2)
    and charges = number of rows. Sorted by charge_date then outlet, index reset."""
    raise NotImplementedError


def guest_summary(df):
    """One row per guest with columns:
    ["guest_id", "total_spend", "n_charges", "avg_charge", "first_charge", "last_charge"]
      total_spend / avg_charge rounded to 2; first/last_charge = min/max charge_date.
    Sorted by total_spend descending, index reset."""
    raise NotImplementedError


def enrich_with_guests(charges, guests):
    """LEFT join charges to guests[["guest_id", "loyalty_tier", "nationality"]] on guest_id.
    Use validate="many_to_one" so duplicate guest ids raise an error.
    Charges without a matching guest stay in the result (with NaN tier/nationality)."""
    raise NotImplementedError


def orphan_charges(charges, guests):
    """Return the charges whose guest_id does not exist in guests (anti-join), index reset."""
    raise NotImplementedError


def pivot_outlet_by_day(df):
    """Pivot: one row per charge_date (the index), one column per outlet, values = summed
    amount rounded to 2, missing combinations filled with 0."""
    raise NotImplementedError


def add_running_balance(df):
    """Return a copy sorted by guest_id, charge_date, charge_id (index reset) with a new
    column "running_balance": cumulative sum of amount per guest, rounded to 2."""
    raise NotImplementedError


def add_previous_amount(df):
    """Return a copy sorted by guest_id, charge_date, charge_id (index reset) with a new
    column "previous_amount": the guest's previous charge amount (NaN for their first)."""
    raise NotImplementedError


def rank_guests(df):
    """Return a DataFrame ["guest_id", "total_spend", "rank"]: total spend per guest
    (rounded 2) and its DENSE rank (1 = highest), rank as int. Sorted by rank, then
    guest_id. Index reset."""
    raise NotImplementedError


def latest_charge_per_guest(df):
    """For each guest, the row with the latest charge_date (ties broken by the highest
    charge_id). Return them sorted by guest_id, index reset."""
    raise NotImplementedError


def flag_duplicates(df, subset):
    """Return a copy with a boolean column "is_duplicate": True for every row that repeats
    an EARLIER row on the `subset` columns (the first occurrence is False)."""
    raise NotImplementedError


def revenue_by_tier(charges, guests):
    """Join charges to guests and return a dict loyalty_tier -> total amount (rounded 2).
    Charges whose guest is unknown are excluded (inner join). Order the dict from
    highest to lowest revenue."""
    raise NotImplementedError
