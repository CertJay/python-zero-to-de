import pytest

from course_tools.loader import DATA, load

ex = load(__file__)


def make(cid, guest, outlet, amount, kind="sale"):
    return ex.Charge(cid, guest, outlet, amount, kind)


def test_charge_from_dict():
    c = ex.Charge.from_dict({"charge_id": "1001", "guest_id": " G001", "outlet": "Bar ", "amount": "25.5"})
    assert c == ex.Charge(1001, "G001", "Bar", 25.5, "sale")
    r = ex.Charge.from_dict({"charge_id": "7", "guest_id": "G002", "outlet": "Spa", "amount": "-60",
                             "charge_type": "refund"})
    assert r.charge_type == "refund" and r.amount == -60.0


def test_charge_is_refund():
    assert make(1, "G001", "Bar", -5, "refund").is_refund is True
    assert make(2, "G001", "Bar", 5).is_refund is False


def test_folio_basics():
    f = ex.Folio("G001")
    assert f.guest_id == "G001"
    assert len(f) == 0
    assert f.balance == 0
    result = f.add(make(1, "G001", "Bar", 25)).add(make(2, "G001", "Spa", 120)).add(make(3, "G001", "Bar", 80.25))
    assert result is f, "add() must return self"
    assert len(f) == 3
    assert f.balance == 225.25
    assert f.total_by_outlet() == {"Bar": 105.25, "Spa": 120}


def test_folio_rejects_other_guest():
    f = ex.Folio("G001")
    with pytest.raises(ValueError) as info:
        f.add(make(9, "G002", "Bar", 10))
    assert str(info.value) == "charge belongs to G002"


def test_folio_repr():
    f = ex.Folio("G001")
    f.add(make(1, "G001", "Bar", 25)).add(make(2, "G001", "Spa", 200))
    assert repr(f) == "Folio(G001, 2 charges, balance=225.00)"


def test_folios_are_independent():
    a, b = ex.Folio("G001"), ex.Folio("G002")
    a.add(make(1, "G001", "Bar", 25))
    assert len(b) == 0


def test_run_report():
    r = ex.RunReport("charges")
    assert r.status == "success"
    r.record_ok(10)
    r.record_ok()
    r.record_error("row 4: missing amount")
    assert r.summary() == {"name": "charges", "rows_ok": 11, "rows_failed": 1, "status": "partial"}
    other = ex.RunReport("guests")
    assert other.errors == [], "errors list must not be shared between reports"
    other.record_error("file missing")
    assert other.status == "failed"


def test_list_extractor_copies():
    source = [{"id": 1}, {"id": 2}]
    ext = ex.ListExtractor(source)
    rows = ext.extract()
    assert rows == source
    rows[0]["id"] = 999
    assert source[0]["id"] == 1, "extract() must return copies"
    assert isinstance(ext, ex.Extractor)


def test_csv_extractor(tmp_path):
    p = tmp_path / "x.csv"
    p.write_text("a,b\n1,2\n3,4\n", encoding="utf-8")
    ext = ex.CSVExtractor(p)
    assert isinstance(ext, ex.Extractor)
    assert ext.extract() == [{"a": "1", "b": "2"}, {"a": "3", "b": "4"}]
    assert len(ex.CSVExtractor(DATA / "charges_clean.csv").extract()) == 550


def test_extract_all(tmp_path):
    p = tmp_path / "x.csv"
    p.write_text("a\n1\n", encoding="utf-8")
    rows = ex.extract_all([ex.ListExtractor([{"a": "0"}]), ex.CSVExtractor(p)])
    assert rows == [{"a": "0", "_source": "ListExtractor"}, {"a": "1", "_source": "CSVExtractor"}]
    assert ex.extract_all([]) == []
