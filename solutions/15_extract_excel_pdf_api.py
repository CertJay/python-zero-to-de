"""Reference solutions for Module 15."""
import re
from pathlib import Path

import pandas as pd
import pdfplumber

INVENTORY_COLUMNS = ["item", "brand", "qty", "status", "date_acquired"]
STATUS_MAP = {"working": "Working", "defective": "Defective", "for repair": "For Repair"}

LINE_RE = re.compile(r"^(?P<item>.+?)\s+(?P<qty>\d+)\s+(?P<unit_price>[\d,]+\.\d{2})\s+(?P<line_total>[\d,]+\.\d{2})$")


def _num(text):
    return float(text.replace(",", ""))


def find_header_row(raw, first_header):
    first_col = raw.iloc[:, 0].astype(str).str.strip()
    matches = raw.index[first_col == first_header]
    if len(matches) == 0:
        raise ValueError(f"header {first_header!r} not found")
    return matches[0]


def read_inventory_sheet(path, sheet_name):
    raw = pd.read_excel(path, sheet_name=sheet_name, header=None)
    header = find_header_row(raw, "Item")
    df = raw.iloc[header + 1:].copy()
    df.columns = list(raw.iloc[header])
    df = df[df["Brand"].notna()]
    df.columns = INVENTORY_COLUMNS
    return df.reset_index(drop=True)


def clean_inventory(df):
    out = df.copy()
    out["qty"] = out["qty"].astype(str).str.extract(r"(\d+)")[0].astype(int)
    out["status"] = out["status"].astype(str).str.strip().str.lower().map(STATUS_MAP)
    out["date_acquired"] = pd.to_datetime(out["date_acquired"].astype(str), format="%m/%d/%Y")
    out["item"] = out["item"].astype(str).str.strip()
    out["brand"] = out["brand"].astype(str).str.strip()
    return out


def combine_school_sheets(path):
    frames = []
    for sheet in pd.ExcelFile(path).sheet_names:
        df = clean_inventory(read_inventory_sheet(path, sheet))
        df.insert(0, "school", sheet)
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def extract_pdf_text(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


def parse_invoice_text(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    invoice = {"supplier": lines[0], "invoice_no": None, "date": None, "lines": [], "total": None}
    for line in lines[1:]:
        if m := re.match(r"Invoice No:\s*(\S+)", line):
            invoice["invoice_no"] = m.group(1)
        elif m := re.match(r"Date:\s*(\d{4}-\d{2}-\d{2})", line):
            invoice["date"] = m.group(1)
        elif m := re.match(r"^TOTAL\s+([\d,]+\.\d{2})$", line):
            invoice["total"] = _num(m.group(1))
        elif m := LINE_RE.match(line):
            invoice["lines"].append({"item": m["item"], "qty": int(m["qty"]),
                                     "unit_price": _num(m["unit_price"]), "line_total": _num(m["line_total"])})
    return invoice


def invoice_is_consistent(invoice, tolerance=0.01):
    for line in invoice["lines"]:
        if abs(line["qty"] * line["unit_price"] - line["line_total"]) > tolerance:
            return False
    return abs(sum(l["line_total"] for l in invoice["lines"]) - invoice["total"]) <= tolerance


def load_invoices(folder):
    invoices = []
    for pdf in sorted(Path(folder).glob("*.pdf")):
        inv = parse_invoice_text(extract_pdf_text(pdf))
        inv["file"] = pdf.name
        inv["consistent"] = invoice_is_consistent(inv)
        invoices.append(inv)
    return sorted(invoices, key=lambda i: i["invoice_no"])


def fetch_json(url, session, timeout=10):
    resp = session.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def fetch_all_pages(first_url, session, max_pages=50):
    results, url, pages = [], first_url, 0
    while url:
        pages += 1
        if pages > max_pages:
            raise RuntimeError("too many pages")
        data = fetch_json(url, session)
        results.extend(data["results"])
        url = data.get("next")
    return results


def reviews_to_dataframe(records):
    df = pd.json_normalize(records, sep="_")
    df = df[["review_id", "guest_id", "guest_tier", "outlet", "rating", "submitted_at"]].copy()
    df["submitted_at"] = pd.to_datetime(df["submitted_at"], utc=True)
    return df
