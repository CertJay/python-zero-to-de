import ast
import csv
import os
from pathlib import Path

import pytest

from course_tools.loader import DATA, load

ex = load(__file__)

ROWS = [
    {"charge_id": 1, "guest_id": "G001", "outlet": "Bar", "amount": 25.0},
    {"charge_id": 2, "guest_id": "G002", "outlet": "Spa", "amount": None},
    {"charge_id": 2, "guest_id": "G999", "outlet": "Pool", "amount": 15000},
    {"charge_id": 3, "guest_id": "G001", "outlet": "Cafe", "amount": "12"},
    {"charge_id": 4, "guest_id": "", "outlet": "Bar", "amount": -5},
]


def test_check_not_null():
    assert ex.check_not_null([{"a": 1}, {"a": None}, {}, {"a": "  "}, {"a": 0}], "a") == [1, 2, 3]
    assert ex.check_not_null(ROWS, "guest_id") == [4]
    assert ex.check_not_null(ROWS, "amount") == [1]
    assert ex.check_not_null([], "a") == []


def test_check_unique():
    assert ex.check_unique([{"id": 1}, {"id": 2}, {"id": 1}, {"id": None}, {"id": None}], "id") == [1]
    assert ex.check_unique(ROWS, "charge_id") == [2]
    assert ex.check_unique(ROWS, "outlet") == ["Bar"]


def test_check_in_range():
    assert ex.check_in_range(ROWS, "amount", 0, 10000) == [1, 2, 3, 4]
    assert ex.check_in_range(ROWS, "amount", -10, 20000) == [1, 3]
    assert ex.check_in_range([{"x": True}], "x", 0, 5) == [0], "booleans are not amounts"


def test_check_allowed_values():
    assert ex.check_allowed_values(ROWS, "outlet", {"Bar", "Spa", "Cafe"}) == [2]


def test_check_foreign_key():
    assert ex.check_foreign_key(ROWS, "guest_id", {"G001", "G002"}) == ["", "G999"]


def test_check_foreign_key_real_files():
    with open(DATA / "guests.csv", encoding="utf-8") as f:
        master = {r["guest_id"] for r in csv.DictReader(f)}
    with open(DATA / "onboard_charges_raw.csv", encoding="utf-8") as f:
        charges = list(csv.DictReader(f))
    assert ex.check_foreign_key(charges, "guest_id", master) == ["G999"]


def test_run_checks_and_stop():
    checks = [
        {"name": "amount_not_null", "severity": "error", "func": ex.check_not_null, "args": ["amount"]},
        {"name": "outlet_allowed", "severity": "warning", "func": ex.check_allowed_values,
         "args": ["outlet", {"Bar", "Spa", "Cafe", "Pool"}]},
    ]
    report = ex.run_checks(ROWS, checks)
    assert report == [
        {"name": "amount_not_null", "severity": "error", "passed": False, "failures": [1]},
        {"name": "outlet_allowed", "severity": "warning", "passed": True, "failures": []},
    ]
    assert ex.should_stop_pipeline(report) is True

    warn_only = [{"name": "w", "severity": "warning", "passed": False, "failures": [3]},
                 {"name": "e", "severity": "error", "passed": True, "failures": []}]
    assert ex.should_stop_pipeline(warn_only) is False
    assert ex.should_stop_pipeline([]) is False


@pytest.mark.skipif(os.environ.get("PYCOURSE_SOLUTIONS") == "1", reason="checks the student's own tests")
def test_you_wrote_your_own_tests():
    tree = ast.parse((Path(__file__).parent / "test_mine.py").read_text(encoding="utf-8"))
    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    tests = [f for f in funcs if f.name.startswith("test_")]
    source = ast.unparse(tree)
    assert len(tests) >= 8, f"test_mine.py has {len(tests)} tests; write at least 8"
    assert "parametrize" in source, "use @pytest.mark.parametrize at least once"
    assert "pytest.raises" in source, "use pytest.raises at least once"
    assert "pytest.fixture" in source, "write at least one @pytest.fixture"
