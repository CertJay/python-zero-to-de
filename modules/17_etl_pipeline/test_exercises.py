import csv
import sqlite3

import pandas as pd
import pytest

from course_tools.loader import DATA, load

ex = load(__file__)
RAW = DATA / "onboard_charges_raw.csv"
GUESTS = DATA / "guests.csv"


def guest_ids():
    with open(GUESTS, encoding="utf-8") as f:
        return {r["guest_id"] for r in csv.DictReader(f)}


def raw_frame(rows):
    cols = ["charge_id", "guest_id", "outlet", "charge_date", "amount", "charge_type", "currency"]
    return pd.DataFrame(rows, columns=cols).astype(str)


def test_extract():
    raw = ex.extract(RAW)
    assert len(raw) == 566
    assert all(pd.api.types.is_string_dtype(raw[c]) or raw[c].dtype == object for c in raw.columns)
    assert (raw["amount"] == "").sum() > 0, "blank amounts must stay as empty strings"


def test_remove_exact_duplicates():
    raw = ex.extract(RAW)
    deduped, removed = ex.remove_exact_duplicates(raw)
    assert removed == 12
    assert len(deduped) == 554
    assert list(deduped.index) == list(range(554))


def test_transform_small():
    raw = raw_frame([
        ["3", " G001", " the BAR ", "01/10/2026", "25.5", "sale", "USD"],
        ["1", "G002", "Resto", "Oct 02 2026", "", "sale", "USD"],
        ["2", "G999", "Spa", "2026-10-03", "40", "sale", "USD"],
        ["4", "G001", "Spa", "2026/10/03", "40", "sale", "USD"],
        ["5", "G002", "pool deck", "2026-10-04", "-10", " Refund", "USD"],
    ])
    clean, rejected = ex.transform(raw, {"G001", "G002"})
    assert list(clean.columns) == ["charge_id", "guest_id", "outlet", "charge_date", "amount", "charge_type"]
    assert clean.to_dict("records") == [
        {"charge_id": 3, "guest_id": "G001", "outlet": "Bar", "charge_date": "2026-10-01", "amount": 25.5, "charge_type": "sale"},
        {"charge_id": 5, "guest_id": "G002", "outlet": "Pool Deck", "charge_date": "2026-10-04", "amount": -10.0, "charge_type": "refund"},
    ]
    assert rejected["reason"].tolist() == ["invalid amount", "unknown guest_id", "invalid date"]
    assert rejected["charge_id"].tolist() == ["1", "2", "4"]
    assert list(rejected.index) == [0, 1, 2]


def test_transform_real_file():
    deduped, _ = ex.remove_exact_duplicates(ex.extract(RAW))
    clean, rejected = ex.transform(deduped, guest_ids())
    assert len(clean) + len(rejected) == len(deduped)
    counts = rejected["reason"].value_counts().to_dict()
    assert counts.get("unknown guest_id") == 4
    assert counts.get("invalid date", 0) == 0
    assert counts.get("invalid amount") == (deduped["amount"] == "").sum()
    assert set(clean["outlet"]) == {"Bar", "Restaurant", "Spa", "Boutique", "Excursions", "Cafe"}


def test_validate():
    good = pd.DataFrame({"charge_id": [1, 2], "amount": [5.0, -1.0], "charge_type": ["sale", "refund"]})
    assert ex.validate(good) == []
    bad = pd.DataFrame({"charge_id": [1, 1, 2], "amount": [0.0, 5.0, 3.0], "charge_type": ["sale", "sale", "refund"]})
    assert ex.validate(bad) == ["duplicate_charge_id", "sale_not_positive", "refund_not_negative"]
    assert ex.validate(good.iloc[0:0]) == ["no_rows"]


def test_load_is_idempotent():
    conn = sqlite3.connect(":memory:")
    clean = pd.DataFrame({"charge_id": [1, 2], "guest_id": ["G001", "G002"], "outlet": ["Bar", "Spa"],
                          "charge_date": ["2026-10-01", "2026-10-02"], "amount": [5.0, 7.5],
                          "charge_type": ["sale", "sale"]})
    assert ex.load(clean, conn) == 2
    assert ex.load(clean, conn) == 2
    assert conn.execute("SELECT COUNT(*) FROM charges").fetchone()[0] == 2


def test_watermark_and_incremental():
    conn = sqlite3.connect(":memory:")
    assert ex.get_watermark(conn) is None
    clean = pd.DataFrame({"charge_id": [1, 2, 3], "guest_id": ["G001"] * 3, "outlet": ["Bar"] * 3,
                          "charge_date": ["2026-10-01", "2026-10-02", "2026-10-03"], "amount": [1.0, 2.0, 3.0],
                          "charge_type": ["sale"] * 3})
    ex.load(clean.iloc[:2], conn)
    assert ex.get_watermark(conn) == "2026-10-02"
    newer = ex.incremental_filter(clean, "2026-10-02")
    assert newer["charge_id"].tolist() == [3] and list(newer.index) == [0]
    assert len(ex.incremental_filter(clean, None)) == 3


def test_run_pipeline_end_to_end(tmp_path):
    db, rej = tmp_path / "onboard.db", tmp_path / "rejected.csv"
    s1 = ex.run_pipeline(RAW, GUESTS, db, rej)
    assert s1["status"] == "success" and s1["errors"] == []
    assert s1["extracted"] == 566 and s1["duplicates_removed"] == 12 and s1["skipped"] == 0
    assert s1["extracted"] == s1["duplicates_removed"] + s1["rejected"] + s1["skipped"] + s1["loaded"]
    rejected = pd.read_csv(rej)
    assert "reason" in rejected.columns and len(rejected) == s1["rejected"]

    s2 = ex.run_pipeline(RAW, GUESTS, db, rej)
    conn = sqlite3.connect(db)
    assert conn.execute("SELECT COUNT(*) FROM charges").fetchone()[0] == s1["loaded"], "re-runs must not duplicate"
    assert conn.execute("SELECT COUNT(DISTINCT charge_id) FROM charges").fetchone()[0] == s1["loaded"]
    conn.close()
    assert s2["loaded"] == s1["loaded"]

    s3 = ex.run_pipeline(RAW, GUESTS, db, rej, incremental=True)
    assert s3["loaded"] == 0 and s3["skipped"] == s1["loaded"]
    assert s3["extracted"] == s3["duplicates_removed"] + s3["rejected"] + s3["skipped"] + s3["loaded"]


def test_run_pipeline_stops_on_bad_data(tmp_path):
    raw = tmp_path / "raw.csv"
    raw.write_text("charge_id,guest_id,outlet,charge_date,amount,charge_type,currency\n"
                   "1,G001,Bar,2026-10-01,5,sale,USD\n"
                   "1,G001,Bar,2026-10-01,6,sale,USD\n", encoding="utf-8")
    db = tmp_path / "x.db"
    s = ex.run_pipeline(raw, GUESTS, db, tmp_path / "rej.csv")
    assert s["status"] == "failed" and s["loaded"] == 0
    assert "duplicate_charge_id" in s["errors"]
    conn = sqlite3.connect(db)
    exists = conn.execute("SELECT name FROM sqlite_master WHERE name='charges'").fetchone()
    if exists:
        assert conn.execute("SELECT COUNT(*) FROM charges").fetchone()[0] == 0
    conn.close()
