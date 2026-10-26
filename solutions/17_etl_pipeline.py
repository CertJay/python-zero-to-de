"""Reference solutions for Module 17."""
import sqlite3

import pandas as pd

DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%b %d %Y"]
OUTLET_MAP = {
    "bar": "Bar", "the bar": "Bar", "resto": "Restaurant", "restaurant": "Restaurant",
    "spa": "Spa", "shore excursions": "Excursions", "excursions": "Excursions",
    "cafe": "Cafe", "café": "Cafe", "boutique": "Boutique",
}
CLEAN_COLUMNS = ["charge_id", "guest_id", "outlet", "charge_date", "amount", "charge_type"]

UPSERT_SQL = """
    INSERT INTO charges (charge_id, guest_id, outlet, charge_date, amount, charge_type)
    VALUES (:charge_id, :guest_id, :outlet, :charge_date, :amount, :charge_type)
    ON CONFLICT(charge_id) DO UPDATE SET
        guest_id = excluded.guest_id, outlet = excluded.outlet, charge_date = excluded.charge_date,
        amount = excluded.amount, charge_type = excluded.charge_type
"""


def _parse_dates(series):
    text = series.astype(str).str.strip()
    parsed = pd.Series(pd.NaT, index=series.index, dtype="datetime64[ns]")
    for fmt in DATE_FORMATS:
        parsed = parsed.fillna(pd.to_datetime(text, format=fmt, errors="coerce"))
    return parsed


def extract(path):
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def remove_exact_duplicates(raw):
    deduped = raw.drop_duplicates().reset_index(drop=True)
    return deduped, len(raw) - len(deduped)


def transform(raw, valid_guest_ids):
    amount = pd.to_numeric(raw["amount"].str.strip(), errors="coerce")
    dates = _parse_dates(raw["charge_date"])
    guest = raw["guest_id"].str.strip()

    reason = pd.Series(None, index=raw.index, dtype="object")
    reason = reason.mask(reason.isna() & amount.isna(), "invalid amount")
    reason = reason.mask(reason.isna() & dates.isna(), "invalid date")
    reason = reason.mask(reason.isna() & ~guest.isin(valid_guest_ids), "unknown guest_id")

    ok = reason.isna()
    rejected = raw[~ok].copy()
    rejected["reason"] = reason[~ok]
    rejected = rejected.reset_index(drop=True)

    key = raw.loc[ok, "outlet"].str.strip().str.lower().str.replace(r"\s+", " ", regex=True)
    clean = pd.DataFrame({
        "charge_id": raw.loc[ok, "charge_id"].str.strip().astype(int),
        "guest_id": guest[ok],
        "outlet": key.map(OUTLET_MAP).fillna(key.str.title()),
        "charge_date": dates[ok].dt.strftime("%Y-%m-%d"),
        "amount": amount[ok].astype(float),
        "charge_type": raw.loc[ok, "charge_type"].str.strip().str.lower(),
    })
    clean = clean.astype({"guest_id": object, "outlet": object, "charge_date": object, "charge_type": object})
    clean = clean.sort_values("charge_id").reset_index(drop=True)
    return clean[CLEAN_COLUMNS], rejected


def validate(clean):
    errors = []
    if clean["charge_id"].duplicated().any():
        errors.append("duplicate_charge_id")
    if ((clean["charge_type"] == "sale") & (clean["amount"] <= 0)).any():
        errors.append("sale_not_positive")
    if ((clean["charge_type"] == "refund") & (clean["amount"] >= 0)).any():
        errors.append("refund_not_negative")
    if clean.empty:
        errors.append("no_rows")
    return errors


def load(clean, conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS charges (
            charge_id INTEGER PRIMARY KEY, guest_id TEXT NOT NULL, outlet TEXT NOT NULL,
            charge_date TEXT NOT NULL, amount REAL NOT NULL, charge_type TEXT NOT NULL DEFAULT 'sale')
    """)
    records = [
        {"charge_id": int(r["charge_id"]), "guest_id": r["guest_id"], "outlet": r["outlet"],
         "charge_date": r["charge_date"], "amount": float(r["amount"]), "charge_type": r["charge_type"]}
        for r in clean.to_dict("records")
    ]
    with conn:
        conn.executemany(UPSERT_SQL, records)
    return len(records)


def get_watermark(conn):
    try:
        return conn.execute("SELECT MAX(charge_date) FROM charges").fetchone()[0]
    except sqlite3.OperationalError:
        return None


def incremental_filter(clean, watermark):
    if watermark is None:
        return clean.reset_index(drop=True)
    return clean[clean["charge_date"] > watermark].reset_index(drop=True)


def run_pipeline(raw_path, guests_path, db_path, rejected_path, incremental=False):
    raw = extract(raw_path)
    deduped, n_dupes = remove_exact_duplicates(raw)
    valid_ids = set(pd.read_csv(guests_path, dtype=str)["guest_id"])
    clean, rejected = transform(deduped, valid_ids)
    rejected.to_csv(rejected_path, index=False)

    summary = {"extracted": len(raw), "duplicates_removed": n_dupes, "rejected": len(rejected),
               "skipped": 0, "loaded": 0, "status": "success", "errors": []}
    errors = validate(clean)
    if errors:
        summary.update(status="failed", errors=errors)
        return summary

    conn = sqlite3.connect(db_path)
    try:
        to_load = clean
        if incremental:
            to_load = incremental_filter(clean, get_watermark(conn))
            summary["skipped"] = len(clean) - len(to_load)
        summary["loaded"] = load(to_load, conn) if len(to_load) else 0
    finally:
        conn.close()
    return summary
