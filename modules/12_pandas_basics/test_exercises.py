import pandas as pd
import pytest

from course_tools.loader import DATA, load

ex = load(__file__)


@pytest.fixture
def small():
    return pd.DataFrame({
        "charge_id": [1, 2, 3, 4, 5, 6],
        "guest_id": ["G001", "G002", "G001", "G003", "G002", "G001"],
        "outlet": ["Bar", "Bar", "Spa", "Bar", "Cafe", "Bar"],
        "amount": [25.0, 40.5, 120.0, 12.0, 6.25, -10.0],
        "charge_type": ["sale", "sale", "sale", "sale", "sale", "refund"],
    })


@pytest.fixture
def real():
    return pd.read_csv(DATA / "charges_clean.csv")


def test_load_charges():
    df = ex.load_charges(DATA / "charges_clean.csv")
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (550, 7)


def test_profile(small):
    df = small.copy()
    df.loc[1, "amount"] = None
    p = ex.profile(df)
    assert p["rows"] == 6 and p["columns"] == 5
    assert p["column_names"] == ["charge_id", "guest_id", "outlet", "amount", "charge_type"]
    assert p["null_counts"] == {"charge_id": 0, "guest_id": 0, "outlet": 0, "amount": 1, "charge_type": 0}


def test_select_columns(small):
    out = ex.select_columns(small, ["amount", "guest_id"])
    assert list(out.columns) == ["amount", "guest_id"]
    assert len(out) == 6


def test_filter_outlet(small):
    out = ex.filter_outlet(small, "Bar")
    assert list(out["charge_id"]) == [1, 2, 4, 6]
    assert list(out.index) == [0, 1, 2, 3]


def test_bar_charges_over(small):
    out = ex.bar_charges_over(small, 20)
    assert list(out["charge_id"]) == [1, 2]
    assert list(out.index) == [0, 1]


def test_large_charges(small):
    out = ex.large_charges(small, 20)
    assert list(out["amount"]) == [120.0, 40.5, 25.0]
    assert list(out.index) == [0, 1, 2]


def test_add_amount_with_tax(small):
    before = small.copy()
    out = ex.add_amount_with_tax(small, 0.12)
    assert "amount_with_tax" not in small.columns, "don't modify the input"
    pd.testing.assert_frame_equal(small, before)
    assert list(out["amount_with_tax"]) == [28.0, 45.36, 134.4, 13.44, 7.0, -11.2]


def test_count_by_outlet(small):
    assert ex.count_by_outlet(small) == {"Bar": 4, "Spa": 1, "Cafe": 1}


def test_total_by_guest(small):
    out = ex.total_by_guest(small)
    assert list(out.columns) == ["guest_id", "total"]
    assert out.to_dict("records") == [
        {"guest_id": "G001", "total": 135.0},
        {"guest_id": "G002", "total": 46.75},
        {"guest_id": "G003", "total": 12.0},
    ]


def test_total_by_guest_real(real):
    out = ex.total_by_guest(real)
    assert len(out) == 60
    assert out["total"].is_monotonic_decreasing


def test_amount_stats(small):
    stats = ex.amount_stats(small)
    assert stats == {"count": 6, "mean": 32.29, "min": -10.0, "max": 120.0}
    assert type(stats["count"]) is int and type(stats["mean"]) is float


def test_refund_percentage(small, real):
    assert ex.refund_percentage(small) == 16.67
    assert ex.refund_percentage(small.iloc[0:0]) == 0.0
    assert 0 < ex.refund_percentage(real) < 15


def test_to_snake_case_columns():
    df = pd.DataFrame(columns=["Guest ID", " Charge Date ", "Amount (USD)", "outlet"])
    out = ex.to_snake_case_columns(df)
    assert list(out.columns) == ["guest_id", "charge_date", "amount_usd", "outlet"]
    assert list(df.columns)[0] == "Guest ID", "don't modify the input"
