# Module 15: Extracting data from Excel, PDFs and APIs

**Time:** 8–10 hours · **Prerequisite:** Module 13

## Bakit ko 'to kailangan?

Clean CSVs are a luxury. In real life, data is trapped in spreadsheets with title rows and footers, in PDF invoices, and behind web APIs. **Extraction is the first step of every pipeline**, and it's where most of the mess is.

**At work:**
- **Excel:** your DepEd inventory work. Every school's sheet had its own title rows, "5 pcs" in a number column, and statuses typed five different ways. You'll automate exactly that.
- **PDF:** supplier invoices and statements. Extract line items, then check that they add up to the printed total (one of the bundled invoices doesn't, on purpose).
- **APIs:** modern systems (including onboard and property platforms) expose REST APIs that return JSON. Integration specs describe endpoints, pagination and auth, so you'll understand what those specs mean in practice.

---

## 1. Excel with pandas and openpyxl

```python
import pandas as pd

xl = pd.ExcelFile("data/ict_inventory_messy.xlsx")
xl.sheet_names                                    # ['Paliparan ES', 'Salitran NHS', 'Burol IS']

df = pd.read_excel(xl, sheet_name="Paliparan ES", header=3)   # header is on the 4th row (0-based 3)
all_sheets = pd.read_excel(xl, sheet_name=None)               # dict: sheet name -> DataFrame
```

### Don't hardcode the header row

Next month, someone adds a line to the title and `header=3` silently reads garbage. Find the header instead:

```python
raw = pd.read_excel(xl, sheet_name="Paliparan ES", header=None)   # read everything as data
header_row = raw.index[raw[0].astype(str).str.strip() == "Item"][0]
df = raw.iloc[header_row + 1:].copy()
df.columns = raw.iloc[header_row]
```

Then drop blank rows and footers ("Prepared by: ..."). A reliable rule: keep rows where a required column (like Brand) is filled.

### Typical Excel clean-up

```python
df["qty"] = df["qty"].astype(str).str.extract(r"(\d+)")[0].astype(int)   # "34 pcs" -> 34
df["status"] = df["status"].str.strip().str.lower().map(STATUS_MAP)
df["date_acquired"] = pd.to_datetime(df["date_acquired"], format="%m/%d/%Y")  # this file is MONTH-first
```

Note: this inventory file is **month-first** (`05/25/2023`), the onboard charges file is **day-first**. Different sources, different conventions. That's why formats belong in the interface spec.

**openpyxl** works at a lower level (individual cells, formatting, formulas, merged cells). Use it when you need to *write* formatted reports or read cell styles. pandas uses it under the hood for `.xlsx`.

---

## 2. PDFs with pdfplumber

PDFs store text positioned on a page, not as rows and columns. Extraction gives you lines of text; you rebuild the structure with string methods and regex (Module 05).

```python
import pdfplumber

with pdfplumber.open("data/invoices/INV-1001.pdf") as pdf:
    text = "\n".join(page.extract_text() or "" for page in pdf.pages)
print(text)
```

```
BUKID FRESH TRADING
Invoice No: INV-1001
Date: 2026-10-04
Bill To: Galley Stores Department
Item Qty Unit Price Line Total
Chicken Breast (kg) 22 210.00 4,620.00
...
TOTAL 15,080.00
```

Parse each line with a regex:

```python
LINE = re.compile(r"^(?P<item>.+?)\s+(?P<qty>\d+)\s+(?P<unit_price>[\d,]+\.\d{2})\s+(?P<line_total>[\d,]+\.\d{2})$")
```

`.+?` is a *lazy* match: as few characters as possible, so the item name stops before the numbers.

pdfplumber also has `page.extract_table()` for PDFs with ruled tables. Scanned PDFs (images) need OCR (Tesseract), a whole other level of pain. Avoid it unless you have to.

### Always validate what you extracted

Extraction can misread a line. Cross-check: does `qty × unit price = line total`? Do the lines sum to the printed total? If not, quarantine the document for a human. That's how invoice-processing systems work.

---

## 3. APIs with requests

An API is a URL that returns data (usually JSON) instead of a web page.

```python
import requests

resp = requests.get(
    "https://api.open-meteo.com/v1/forecast",
    params={"latitude": 14.33, "longitude": 120.94, "current": "temperature_2m"},  # Dasmariñas
    timeout=10,                         # ALWAYS set a timeout; the default waits forever
)
resp.status_code          # 200 = OK
resp.raise_for_status()   # raises an error for 4xx / 5xx
data = resp.json()        # parsed JSON -> dict
```

That's a real, free API with no key. Try it.

### Status codes to know

| Code | Meaning | What you do |
|---|---|---|
| 200 | OK | process |
| 400 | bad request | fix your parameters (don't retry) |
| 401 / 403 | not authenticated / not allowed | check credentials (don't retry) |
| 404 | not found | check the URL |
| 429 | too many requests | wait and retry (respect `Retry-After`) |
| 500 / 502 / 503 | server problem | retry with backoff |

### Authentication

```python
headers = {"Authorization": f"Bearer {os.environ['API_TOKEN']}"}   # token from env, never in code
requests.get(url, headers=headers, timeout=10)
```

### Sessions

```python
session = requests.Session()
session.headers.update({"Authorization": f"Bearer {token}"})
session.get(url, timeout=10)      # reuses the connection and headers
```

Passing a session into your functions (instead of calling `requests.get` directly) also makes them testable: tests pass in a fake session. The exercises do exactly this.

### Pagination

APIs return large results in pages:

```json
{"page": 1, "results": [...], "next": "https://api.example.com/reviews?page=2"}
```

Keep requesting `next` until it's `null`. Add a safety limit on the number of pages so a buggy API can't loop forever.

### Flattening JSON with pandas

```python
pd.json_normalize(records, sep="_")
# {"guest": {"id": "G001", "tier": "Gold"}} -> columns guest_id, guest_tier
```

---

## Exercises (`exercises.py`)

Excel:
1. `find_header_row(raw, first_header)`
2. `read_inventory_sheet(path, sheet_name)`
3. `clean_inventory(df)`
4. `combine_school_sheets(path)`

PDF:
5. `extract_pdf_text(path)`
6. `parse_invoice_text(text)`
7. `invoice_is_consistent(invoice)`
8. `load_invoices(folder)`

API (tested with a fake session; no internet needed):
9. `fetch_json(url, session)`
10. `fetch_all_pages(first_url, session)`
11. `reviews_to_dataframe(records)`

## Mini project: invoice loader (portfolio piece #2, start here, finish after Module 16)

`invoice_loader.py`: read every PDF in a folder, parse it, flag inconsistent invoices into `output/invoices_to_review.csv`, and write consistent line items to `output/invoice_lines.csv` (one row per line, with invoice_no and date). After Module 16, load them into a database instead. That's the "Invoice PDF to Database" project on your portfolio site.

## Self-check

1. Why find the header row instead of using `header=3`?
2. Why always pass `timeout=` to `requests.get`?
3. Which HTTP errors are worth retrying?
4. How do you know when you've fetched the last page?

<details><summary>Answers</summary>

1. Sheet layouts change; a hardcoded header row silently reads the wrong row when someone adds a line above it.
2. Without it, a request to an unresponsive server can hang forever and freeze the pipeline.
3. 429 (after waiting) and 5xx server errors. Not 4xx client errors like 400, 401, 403, 404.
4. When the response's `next` field is null/None (or the results come back empty, depending on the API).
</details>
