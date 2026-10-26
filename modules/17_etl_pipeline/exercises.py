"""Module 17 exercises: a complete, idempotent ETL pipeline.

Run:  python check.py 17

Source: data/onboard_charges_raw.csv  ->  target: SQLite table `charges`
You may copy helpers you wrote in Modules 13 and 16.
"""
import sqlite3  # noqa: F401

import pandas as pd  # noqa: F401

DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%b %d %Y"]
OUTLET_MAP = {
    "bar": "Bar", "the bar": "Bar", "resto": "Restaurant", "restaurant": "Restaurant",
    "spa": "Spa", "shore excursions": "Excursions", "excursions": "Excursions",
    "cafe": "Cafe", "café": "Cafe", "boutique": "Boutique",
}
CLEAN_COLUMNS = ["charge_id", "guest_id", "outlet", "charge_date", "amount", "charge_type"]


def extract(path):
    """Read the raw CSV with EVERY column as text: pd.read_csv(path, dtype=str,
    keep_default_na=False). Blank cells become "" (not NaN)."""
    raise NotImplementedError


def remove_exact_duplicates(raw):
    """Return (deduplicated DataFrame with index reset, number of rows removed).
    Only fully identical rows count as duplicates; keep the first."""
    raise NotImplementedError


def transform(raw, valid_guest_ids):
    """Split raw rows into (clean, rejected).

    A row is rejected with the FIRST reason that applies, checked in this order:
      "invalid amount"   amount blank or not a number
      "invalid date"     charge_date doesn't match any of DATE_FORMATS
      "unknown guest_id" guest_id not in valid_guest_ids

    clean: DataFrame with exactly CLEAN_COLUMNS, index reset, sorted by charge_id:
      charge_id int, guest_id stripped str, outlet standardized with OUTLET_MAP
      (collapse spaces + lowercase, unknown -> title case), charge_date ISO string
      "YYYY-MM-DD", amount float, charge_type stripped lowercase str
    rejected: the original raw columns (unchanged values) + a "reason" column, index reset.
    """
    raise NotImplementedError


def validate(clean):
    """Dataset-level checks. Return a list of the names of FAILED checks (empty = OK):
      "duplicate_charge_id"   a charge_id appears more than once
      "sale_not_positive"     a sale with amount <= 0
      "refund_not_negative"   a refund with amount >= 0
      "no_rows"               clean is empty
    Order the list as above."""
    raise NotImplementedError


def load(clean, conn):
    """Create the charges table if needed (same schema as Module 16) and UPSERT every row
    on charge_id. Commit and return the number of rows written. Must be idempotent."""
    raise NotImplementedError


def get_watermark(conn):
    """Return MAX(charge_date) from charges as a string, or None if the table is empty
    or doesn't exist yet."""
    raise NotImplementedError


def incremental_filter(clean, watermark):
    """Return only rows with charge_date > watermark (ISO strings compare correctly).
    If watermark is None, return all rows. Index reset."""
    raise NotImplementedError


def run_pipeline(raw_path, guests_path, db_path, rejected_path, incremental=False):
    """Orchestrate: extract -> remove duplicates -> transform -> validate -> (filter) -> load.

    - valid guest ids come from the guest_id column of the guests CSV
    - write the rejected rows to rejected_path as CSV (index=False), even if there are none
    - if incremental=True, only load rows newer than get_watermark(conn); count the others
      as "skipped"
    - if validate() returns errors, do NOT load: status "failed", loaded 0

    Return:
    {"extracted": int, "duplicates_removed": int, "rejected": int, "skipped": int,
     "loaded": int, "status": "success" | "failed", "errors": [names]}

    Reconciliation (when status is success):
    extracted == duplicates_removed + rejected + skipped + loaded
    """
    raise NotImplementedError
