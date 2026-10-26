import logging

import pytest

from course_tools.loader import load

ex = load(__file__)

GOOD = {"charge_id": 1, "guest_id": "G001", "amount": 25.0, "charge_type": "sale"}


def test_safe_divide():
    assert ex.safe_divide(10, 4) == 2.5
    assert ex.safe_divide(1, 0) is None
    assert ex.safe_divide(0, 5) == 0


def test_parse_int():
    assert ex.parse_int(" 42 ") == 42
    assert ex.parse_int("-7") == -7
    assert ex.parse_int("abc", 0) == 0
    assert ex.parse_int("") is None
    assert ex.parse_int("4.5") is None
    assert ex.parse_int(None, -1) == -1


def test_validate_charge_valid():
    assert ex.validate_charge(GOOD) is True
    assert ex.validate_charge({**GOOD, "amount": -10, "charge_type": "refund"}) is True
    assert ex.validate_charge({**GOOD, "amount": 5}) is True


@pytest.mark.parametrize("charge, message", [
    ({"guest_id": "G001", "amount": 1, "charge_type": "sale"}, "missing field: charge_id"),
    ({**GOOD, "guest_id": None}, "missing field: guest_id"),
    ({"charge_id": 1, "guest_id": "G1"}, "missing field: amount"),
    ({**GOOD, "amount": "25"}, "amount is not a number"),
    ({**GOOD, "amount": True}, "amount is not a number"),
    ({**GOOD, "charge_type": "void"}, "invalid charge_type: void"),
    ({**GOOD, "amount": 0}, "sale must be positive"),
    ({**GOOD, "amount": 10, "charge_type": "refund"}, "refund must be negative"),
])
def test_validate_charge_errors(charge, message):
    with pytest.raises(ValueError) as info:
        ex.validate_charge(charge)
    assert str(info.value) == message


def test_require_rows():
    assert ex.require_rows([1, 2, 3]) == 3
    with pytest.raises(ex.DataQualityError) as info:
        ex.require_rows([], source="charges.csv")
    assert str(info.value) == "no rows received from charges.csv"


def test_split_valid_invalid():
    charges = [GOOD, {**GOOD, "amount": None}, {**GOOD, "charge_id": 2, "amount": 40.0},
               {**GOOD, "charge_type": "void"}]
    valid, rejected = ex.split_valid_invalid(charges)
    assert [c["charge_id"] for c in valid] == [1, 2]
    assert rejected == [{"row": 2, "error": "missing field: amount"},
                        {"row": 4, "error": "invalid charge_type: void"}]
    assert ex.split_valid_invalid([]) == ([], [])


def test_retry_succeeds_after_failures():
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ConnectionError("db down")
        return "ok"

    assert ex.retry(flaky, attempts=3) == "ok"
    assert calls["n"] == 3


def test_retry_gives_up():
    calls = {"n": 0}

    def always_down():
        calls["n"] += 1
        raise TimeoutError("timeout")

    with pytest.raises(TimeoutError):
        ex.retry(always_down, attempts=4)
    assert calls["n"] == 4


def test_retry_does_not_retry_bad_data():
    calls = {"n": 0}

    def bad_data():
        calls["n"] += 1
        raise ValueError("bad row")

    with pytest.raises(ValueError):
        ex.retry(bad_data, attempts=5)
    assert calls["n"] == 1, "ValueError must not be retried"


def test_read_config(tmp_path):
    assert ex.read_config(tmp_path / "missing.json") == {}
    good = tmp_path / "good.json"
    good.write_text('{"batch_size": 500}', encoding="utf-8")
    assert ex.read_config(good) == {"batch_size": 500}
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError) as info:
        ex.read_config(bad)
    assert str(info.value).startswith("invalid config")


def test_get_logger():
    log1 = ex.get_logger("course.test.logger")
    log2 = ex.get_logger("course.test.logger")
    assert log1 is log2
    assert log1.level == logging.INFO
    assert len(log1.handlers) == 1
    assert isinstance(log1.handlers[0], logging.StreamHandler)
    fmt = log1.handlers[0].formatter._fmt
    assert fmt == "%(asctime)s %(levelname)s [%(name)s] %(message)s"


def test_process_all():
    def invert(x):
        return 1 / x

    assert ex.process_all([1, 2, 0, 4, 0], invert) == {"processed": 3, "failed": 2, "status": "partial"}
    assert ex.process_all([1, 2], invert) == {"processed": 2, "failed": 0, "status": "success"}
    assert ex.process_all([], invert) == {"processed": 0, "failed": 0, "status": "success"}
