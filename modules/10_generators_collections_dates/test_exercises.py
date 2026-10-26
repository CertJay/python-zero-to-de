import inspect
import time
from collections import Counter
from datetime import date

from course_tools.loader import DATA, load

ex = load(__file__)

CHARGES = [
    {"charge_id": 1, "guest_id": "G001", "outlet": "Bar", "amount": 25.0},
    {"charge_id": 2, "guest_id": "G002", "outlet": "Spa", "amount": 120.0},
    {"charge_id": 3, "guest_id": "G001", "outlet": "Bar", "amount": 40.5},
    {"charge_id": 4, "guest_id": "G003", "outlet": "Cafe", "amount": 6.25},
    {"charge_id": 5, "guest_id": "G001", "outlet": "Spa", "amount": 90.0},
]


def test_batched_is_generator():
    assert inspect.isgeneratorfunction(ex.batched), "use yield"
    assert list(ex.batched(range(5), 2)) == [[0, 1], [2, 3], [4]]
    assert list(ex.batched([], 3)) == []
    gen = (i for i in range(7))
    assert list(ex.batched(gen, 3)) == [[0, 1, 2], [3, 4, 5], [6]]


def test_running_total():
    assert inspect.isgeneratorfunction(ex.running_total)
    assert list(ex.running_total([25, 120, 80])) == [25, 145, 225]
    assert list(ex.running_total([])) == []


def test_stream_csv():
    assert inspect.isgeneratorfunction(ex.stream_csv)
    first = next(ex.stream_csv(DATA / "charges_clean.csv"))
    assert set(first) >= {"charge_id", "guest_id", "outlet", "amount"}
    assert sum(1 for _ in ex.stream_csv(DATA / "charges_clean.csv")) == 550


def test_revenue_by_outlet():
    result = ex.revenue_by_outlet(CHARGES)
    assert isinstance(result, Counter)
    assert dict(result) == {"Bar": 65.5, "Spa": 210.0, "Cafe": 6.25}


def test_top_outlets():
    assert ex.top_outlets(CHARGES, 2) == [("Spa", 210.0), ("Bar", 65.5)]


def test_group_ids():
    result = ex.group_ids(CHARGES)
    assert type(result) is dict, "convert the defaultdict to a normal dict before returning"
    assert result == {"G001": [1, 3, 5], "G002": [2], "G003": [4]}


def test_last_n():
    assert ex.last_n(range(10), 3) == [7, 8, 9]
    assert ex.last_n([1, 2], 5) == [1, 2]
    assert ex.last_n((x for x in "abcdef"), 2) == ["e", "f"]


def test_dedupe_keep_order():
    assert ex.dedupe_keep_order(["G2", "G1", "G2", "G3", "G1"]) == ["G2", "G1", "G3"]
    assert ex.dedupe_keep_order([]) == []


def test_parse_any_date():
    assert ex.parse_any_date("2026-10-01") == date(2026, 10, 1)
    assert ex.parse_any_date("01/10/2026") == date(2026, 10, 1)
    assert ex.parse_any_date("12/10/2026") == date(2026, 10, 12)
    assert ex.parse_any_date(" Oct 05 2026 ") == date(2026, 10, 5)
    assert ex.parse_any_date("2026/10/01") is None
    assert ex.parse_any_date("31/02/2026") is None
    assert ex.parse_any_date("") is None


def test_parse_any_date_real_file():
    import csv
    with open(DATA / "onboard_charges_raw.csv", encoding="utf-8") as f:
        dates = [ex.parse_any_date(r["charge_date"]) for r in csv.DictReader(f)]
    assert all(d is not None for d in dates)
    assert min(dates) == date(2026, 10, 1) and max(dates) <= date(2026, 10, 14)


def test_nights_between():
    assert ex.nights_between("2026-10-01", "2026-10-08") == 7
    assert ex.nights_between("2026-12-30", "2027-01-02") == 3


def test_daily_counts():
    ts = ["2026-10-02T09:00:00", "2026-10-01T08:15:00", "2026-10-01T23:59:59"]
    result = ex.daily_counts(ts)
    assert result == {"2026-10-01": 2, "2026-10-02": 1}
    assert list(result) == ["2026-10-01", "2026-10-02"]


def test_voyage_days():
    assert ex.voyage_days("2026-10-30", 4) == ["2026-10-30", "2026-10-31", "2026-11-01", "2026-11-02"]
    assert ex.voyage_days("2026-10-01", 0) == []


def test_to_manila():
    assert ex.to_manila("2026-10-01T04:00:00+00:00") == "2026-10-01T12:00:00+08:00"
    assert ex.to_manila("2026-10-01T20:30:00+00:00") == "2026-10-02T04:30:00+08:00"


def test_count_calls():
    @ex.count_calls
    def add(a, b):
        """Add two numbers."""
        return a + b

    assert add.calls == 0
    assert add(2, 3) == 5
    add(1, 1)
    assert add.calls == 2
    assert add.__name__ == "add" and add.__doc__ == "Add two numbers."


def test_timed():
    @ex.timed
    def slow(x):
        time.sleep(0.05)
        return x * 2

    assert slow.last_seconds is None
    assert slow(4) == 8
    assert 0.04 <= slow.last_seconds < 1.0
    assert slow.__name__ == "slow"
