import csv
from datetime import datetime

import pandas as pd
import pytest

from course_tools.loader import DATA, load

ex = load(__file__)


@pytest.fixture
def small():
    return pd.DataFrame({
        "charge_id": [1, 2, 3, 4, 5, 6, 7],
        "guest_id": ["G001", "G001", "G002", "G001", "G002", "G003", "G999"],
        "outlet": ["Bar", "Spa", "Bar", "Bar", "Cafe", "Spa", "Bar"],
        "charge_date": pd.to_datetime(["2026-10-01", "2026-10-01", "2026-10-01", "2026-10-02",
                                       "2026-10-02", "2026-10-03", "2026-10-03"]),
        "amount": [25.0, 120.0, 40.0, 80.0, 6.5, 200.0, 15.0],
    })


@pytest.fixture
def guests():
    return pd.DataFrame({
        "guest_id": ["G001", "G002", "G003"],
        "loyalty_tier": ["Gold", "Silver", "Gold"],
        "nationality": ["PH", "SG", "US"],
        "cabin": ["A1", "B2", "C3"],
    })


def test_parse_mixed_dates():
    s = pd.Series(["2026-10-01", " 12/10/2026", "Oct 05 2026", "2026/10/01", None])
    out = ex.parse_mixed_dates(s)
    assert pd.api.types.is_datetime64_any_dtype(out)
    assert list(out[:3]) == [pd.Timestamp("2026-10-01"), pd.Timestamp("2026-10-12"), pd.Timestamp("2026-10-05")]
    assert out[3] is pd.NaT or pd.isna(out[3])
    assert pd.isna(out[4])


def _expected_clean_count():
    with open(DATA / "onboard_charges_raw.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    seen, unique = set(), []
    for r in rows:
        key = tuple(r.values())
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return sum(1 for r in unique if r["amount"].strip())


def test_clean_charges():
    raw = pd.read_csv(DATA / "onboard_charges_raw.csv")
    before = raw.copy()
    clean = ex.clean_charges(raw)
    pd.testing.assert_frame_equal(raw, before)
    assert len(clean) == _expected_clean_count()
    assert set(clean["outlet"]) == {"Bar", "Restaurant", "Spa", "Boutique", "Excursions", "Cafe"}
    assert pd.api.types.is_datetime64_any_dtype(clean["charge_date"])
    assert pd.api.types.is_numeric_dtype(clean["amount"])
    assert clean["amount"].notna().all() and clean["charge_date"].notna().all()
    assert not clean.duplicated().any()
    assert clean["charge_date"].min() == pd.Timestamp("2026-10-01")
    assert list(clean.index) == list(range(len(clean)))
    assert clean[["charge_date", "charge_id"]].equals(
        clean[["charge_date", "charge_id"]].sort_values(["charge_date", "charge_id"]).reset_index(drop=True))


def test_missing_report():
    df = pd.DataFrame({"a": [1, None, 3], "b": ["x", "y", "z"], "c": [None, None, 1]})
    report = ex.missing_report(df)
    assert report == {"a": 1, "c": 2}
    assert all(type(v) is int for v in report.values())


def test_revenue_by_outlet_day(small):
    out = ex.revenue_by_outlet_day(small)
    assert list(out.columns) == ["charge_date", "outlet", "total", "charges"]
    first = out.iloc[0]
    assert (first["outlet"], first["total"], first["charges"]) == ("Bar", 65.0, 2)
    assert len(out) == 6


def test_guest_summary(small):
    out = ex.guest_summary(small)
    assert list(out.columns) == ["guest_id", "total_spend", "n_charges", "avg_charge", "first_charge", "last_charge"]
    top = out.iloc[0]
    assert top["guest_id"] == "G001" and top["total_spend"] == 225.0 and top["n_charges"] == 3
    assert top["avg_charge"] == 75.0
    assert top["first_charge"] == pd.Timestamp("2026-10-01") and top["last_charge"] == pd.Timestamp("2026-10-02")
    assert list(out["guest_id"]) == ["G001", "G003", "G002", "G999"]


def test_enrich_with_guests(small, guests):
    out = ex.enrich_with_guests(small, guests)
    assert len(out) == len(small)
    assert "cabin" not in out.columns
    assert out.loc[out["guest_id"] == "G002", "loyalty_tier"].iloc[0] == "Silver"
    assert pd.isna(out.loc[out["guest_id"] == "G999", "loyalty_tier"].iloc[0])


def test_enrich_rejects_duplicate_guests(small, guests):
    dup = pd.concat([guests, guests.iloc[[0]]], ignore_index=True)
    with pytest.raises(pd.errors.MergeError):
        ex.enrich_with_guests(small, dup)


def test_orphan_charges(small, guests):
    out = ex.orphan_charges(small, guests)
    assert list(out["charge_id"]) == [7]
    assert list(out.index) == [0]


def test_pivot_outlet_by_day(small):
    p = ex.pivot_outlet_by_day(small)
    assert sorted(p.columns) == ["Bar", "Cafe", "Spa"]
    assert p.loc[pd.Timestamp("2026-10-01"), "Bar"] == 65.0
    assert p.loc[pd.Timestamp("2026-10-02"), "Spa"] == 0


def test_add_running_balance(small):
    out = ex.add_running_balance(small)
    g1 = out[out["guest_id"] == "G001"]
    assert list(g1["running_balance"]) == [25.0, 145.0, 225.0]
    assert list(out.index) == list(range(len(out)))
    assert "running_balance" not in small.columns


def test_add_previous_amount(small):
    out = ex.add_previous_amount(small)
    g1 = out[out["guest_id"] == "G001"]["previous_amount"].tolist()
    assert pd.isna(g1[0]) and g1[1:] == [25.0, 120.0]


def test_rank_guests():
    df = pd.DataFrame({"guest_id": ["A", "B", "C", "D"], "amount": [100.0, 50.0, 100.0, 10.0]})
    out = ex.rank_guests(df)
    assert out.to_dict("records") == [
        {"guest_id": "A", "total_spend": 100.0, "rank": 1},
        {"guest_id": "C", "total_spend": 100.0, "rank": 1},
        {"guest_id": "B", "total_spend": 50.0, "rank": 2},
        {"guest_id": "D", "total_spend": 10.0, "rank": 3},
    ]


def test_latest_charge_per_guest(small):
    out = ex.latest_charge_per_guest(small)
    assert list(out["guest_id"]) == ["G001", "G002", "G003", "G999"]
    assert list(out["charge_id"]) == [4, 5, 6, 7]


def test_latest_charge_tie_break():
    df = pd.DataFrame({"guest_id": ["A", "A"], "charge_id": [10, 9],
                       "charge_date": pd.to_datetime(["2026-10-01", "2026-10-01"]), "amount": [1.0, 2.0]})
    assert ex.latest_charge_per_guest(df)["charge_id"].tolist() == [10]


def test_flag_duplicates():
    df = pd.DataFrame({"a": [1, 1, 2, 1], "b": ["x", "x", "x", "y"]})
    out = ex.flag_duplicates(df, ["a", "b"])
    assert out["is_duplicate"].tolist() == [False, True, False, False]
    assert ex.flag_duplicates(df, ["a"])["is_duplicate"].tolist() == [False, True, False, True]


def test_revenue_by_tier(small, guests):
    out = ex.revenue_by_tier(small, guests)
    assert out == {"Gold": 425.0, "Silver": 46.5}
    assert list(out) == ["Gold", "Silver"]
