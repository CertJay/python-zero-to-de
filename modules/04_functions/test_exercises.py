import copy

from course_tools.loader import load

ex = load(__file__)


def test_apply_discount():
    assert ex.apply_discount(200) == 180.0
    assert ex.apply_discount(80, percent=25) == 60.0
    assert ex.apply_discount(99.99, 0) == 99.99


def test_summarize():
    assert ex.summarize(25, 120, 80) == {"count": 3, "total": 225, "average": 75.0}
    assert ex.summarize() == {"count": 0, "total": 0, "average": 0.0}
    assert ex.summarize(10, 5, 5) == {"count": 3, "total": 20, "average": 6.67}


def test_build_record():
    assert ex.build_record(guest_id="G001", amount=25) == {"guest_id": "G001", "amount": 25, "source": "manual"}
    assert ex.build_record(guest_id="G002", source="pos") == {"guest_id": "G002", "source": "pos"}
    assert ex.build_record() == {"source": "manual"}


def test_append_to_batch():
    assert ex.append_to_batch(1) == [1]
    assert ex.append_to_batch(2) == [2], "a fresh list must be created on every call"
    existing = [1, 2]
    assert ex.append_to_batch(3, existing) == [1, 2, 3]


def test_make_multiplier():
    triple = ex.make_multiplier(3)
    assert callable(triple)
    assert triple(5) == 15
    assert ex.make_multiplier(0.5)(10) == 5


def test_compose():
    add_one = lambda x: x + 1
    double = lambda x: x * 2
    assert ex.compose(add_one, double)(5) == 11
    assert ex.compose(double, add_one)(5) == 12


def test_run_steps():
    assert ex.run_steps("  the bar ", [str.strip, str.title]) == "The Bar"
    assert ex.run_steps(10, []) == 10
    assert ex.run_steps(2, [lambda x: x + 3, lambda x: x * 10]) == 50


def test_sort_charges():
    charges = [
        {"guest_id": "G002", "amount": 40},
        {"guest_id": "G001", "amount": 25},
        {"guest_id": "G001", "amount": 120},
        {"guest_id": "G002", "amount": 95},
    ]
    original = copy.deepcopy(charges)
    result = ex.sort_charges(charges)
    assert [(c["guest_id"], c["amount"]) for c in result] == [("G001", 120), ("G001", 25), ("G002", 95), ("G002", 40)]
    assert charges == original, "don't modify the input"


def test_filter_by():
    assert ex.filter_by([1, 5, 10], lambda n: n > 3) == [5, 10]
    rows = [{"outlet": "Bar"}, {"outlet": "Spa"}]
    assert ex.filter_by(rows, lambda r: r["outlet"] == "Spa") == [{"outlet": "Spa"}]
    assert ex.filter_by([], lambda r: True) == []


def test_factorial():
    assert ex.factorial(0) == 1
    assert ex.factorial(1) == 1
    assert ex.factorial(5) == 120
    assert ex.factorial(10) == 3628800


def test_fibonacci():
    assert [ex.fibonacci(i) for i in range(8)] == [0, 1, 1, 2, 3, 5, 8, 13]
    assert ex.fibonacci(80) == 23416728348467685
