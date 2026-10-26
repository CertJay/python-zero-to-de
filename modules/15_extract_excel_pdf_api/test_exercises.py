import json

import pandas as pd
import pytest
import requests

from course_tools.loader import DATA, load

ex = load(__file__)
XLSX = DATA / "ict_inventory_messy.xlsx"
INVOICES = DATA / "invoices"
ANSWERS = {a["invoice_no"]: a for a in json.loads((INVOICES / "_answer_key.json").read_text())}


# ---------------------------------------------------------------- Excel

def test_find_header_row():
    raw = pd.DataFrame([["Title", None], [None, None], ["Item", "Brand"], ["Laptop", "Lenovo"]])
    assert ex.find_header_row(raw, "Item") == 2
    with pytest.raises(ValueError):
        ex.find_header_row(raw, "Missing")


def test_read_inventory_sheet():
    df = ex.read_inventory_sheet(XLSX, "Paliparan ES")
    assert list(df.columns) == ["item", "brand", "qty", "status", "date_acquired"]
    assert len(df) == 5
    assert list(df.index) == [0, 1, 2, 3, 4]
    assert not df["item"].astype(str).str.contains("Prepared by").any()


def test_clean_inventory():
    df = ex.clean_inventory(ex.read_inventory_sheet(XLSX, "Paliparan ES"))
    assert pd.api.types.is_integer_dtype(df["qty"])
    assert set(df["status"]) <= {"Working", "Defective", "For Repair"}
    assert pd.api.types.is_datetime64_any_dtype(df["date_acquired"])
    assert df["date_acquired"].min() >= pd.Timestamp("2017-01-01")


def test_combine_school_sheets():
    df = ex.combine_school_sheets(XLSX)
    assert list(df.columns) == ["school", "item", "brand", "qty", "status", "date_acquired"]
    assert len(df) == 15
    assert set(df["school"]) == {"Paliparan ES", "Salitran NHS", "Burol IS"}
    assert list(df.index) == list(range(15))


# ---------------------------------------------------------------- PDF

def test_extract_pdf_text():
    text = ex.extract_pdf_text(INVOICES / "INV-1001.pdf")
    assert "BUKID FRESH TRADING" in text and "INV-1001" in text and "TOTAL" in text


def test_parse_invoice_text():
    text = """BUKID FRESH TRADING
Invoice No: INV-2000
Date: 2026-10-20
Bill To: Galley Stores Department
Item Qty Unit Price Line Total
Chicken Breast (kg) 22 210.00 4,620.00
Rice 25kg Sack 3 1,350.00 4,050.00
TOTAL 8,670.00"""
    inv = ex.parse_invoice_text(text)
    assert inv["supplier"] == "BUKID FRESH TRADING"
    assert inv["invoice_no"] == "INV-2000"
    assert inv["date"] == "2026-10-20"
    assert inv["lines"] == [
        {"item": "Chicken Breast (kg)", "qty": 22, "unit_price": 210.0, "line_total": 4620.0},
        {"item": "Rice 25kg Sack", "qty": 3, "unit_price": 1350.0, "line_total": 4050.0},
    ]
    assert inv["total"] == 8670.0


def test_invoice_is_consistent():
    good = {"lines": [{"qty": 2, "unit_price": 10.0, "line_total": 20.0}], "total": 20.0}
    assert ex.invoice_is_consistent(good) is True
    assert ex.invoice_is_consistent({**good, "total": 25.0}) is False
    bad_line = {"lines": [{"qty": 2, "unit_price": 10.0, "line_total": 21.0}], "total": 21.0}
    assert ex.invoice_is_consistent(bad_line) is False


def test_load_invoices():
    invoices = ex.load_invoices(INVOICES)
    assert [i["invoice_no"] for i in invoices] == ["INV-1001", "INV-1002", "INV-1003", "INV-1004", "INV-1005"]
    for inv in invoices:
        key = ANSWERS[inv["invoice_no"]]
        assert len(inv["lines"]) == key["lines"]
        assert inv["total"] == pytest.approx(key["printed_total"])
        assert inv["file"] == f"{inv['invoice_no']}.pdf"
    assert [i["invoice_no"] for i in invoices if not i["consistent"]] == ["INV-1004"]


# ---------------------------------------------------------------- API

class FakeResponse:
    def __init__(self, data, status=200):
        self._data, self.status_code = data, status

    def json(self):
        return self._data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} error")


class FakeSession:
    """Serves data/api_pages/page_N.json for https://api.example.com/reviews?page=N"""

    def __init__(self, status=200):
        self.calls, self.status = [], status

    def get(self, url, timeout=None, **kwargs):
        self.calls.append({"url": url, "timeout": timeout})
        page = int(url.rsplit("=", 1)[1])
        data = json.loads((DATA / "api_pages" / f"page_{page}.json").read_text())
        return FakeResponse(data, self.status)


FIRST = "https://api.example.com/reviews?page=1"


def test_fetch_json():
    s = FakeSession()
    data = ex.fetch_json(FIRST, s)
    assert data["page"] == 1 and len(data["results"]) == 10
    assert s.calls[0]["timeout"] is not None, "always pass a timeout"


def test_fetch_json_raises_on_error():
    with pytest.raises(requests.HTTPError):
        ex.fetch_json(FIRST, FakeSession(status=503))


def test_fetch_all_pages():
    s = FakeSession()
    results = ex.fetch_all_pages(FIRST, s)
    assert len(results) == 25
    assert [c["url"][-1] for c in s.calls] == ["1", "2", "3"]
    with pytest.raises(RuntimeError):
        ex.fetch_all_pages(FIRST, FakeSession(), max_pages=2)


def test_reviews_to_dataframe():
    records = ex.fetch_all_pages(FIRST, FakeSession())
    df = ex.reviews_to_dataframe(records)
    assert list(df.columns) == ["review_id", "guest_id", "guest_tier", "outlet", "rating", "submitted_at"]
    assert len(df) == 25
    assert str(df["submitted_at"].dt.tz) == "UTC"
