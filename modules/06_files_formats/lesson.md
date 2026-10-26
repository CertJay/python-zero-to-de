# Module 06: Files, CSV, JSON and paths

**Time:** 6–7 hours · **Prerequisite:** Module 05

## Bakit ko 'to kailangan?

"Extract" in ETL usually means "read a file someone dropped somewhere". "Load" often means "write a file somewhere else". CSV and JSON are the two formats you'll touch daily: CSV from spreadsheets and old systems, JSON from APIs and modern apps.

**At work:** integrations between systems often exchange CSV or JSON files, and interface specs describe their fields. After this module you can open those files with code, check them against the spec, and convert one format to another.

---

## 1. Paths with pathlib

Never build paths by gluing strings like `"data\\" + name`. Use `pathlib.Path`; it works on Windows, Mac and Linux.

```python
from pathlib import Path

DATA = Path("data")
file = DATA / "guests.csv"        # "/" joins path parts
file.exists()                     # True / False
file.name                         # "guests.csv"
file.stem                         # "guests"
file.suffix                       # ".csv"
file.parent                       # Path("data")
file.resolve()                    # full absolute path

Path("output").mkdir(parents=True, exist_ok=True)   # create folder safely
sorted(DATA.glob("*.csv"))        # all CSV files in data/
sorted(DATA.rglob("*.pdf"))       # recursive search
file.read_text(encoding="utf-8")  # whole file as one string
Path("out.txt").write_text("hello", encoding="utf-8")
```

**Relative paths depend on where you run Python from.** Run course scripts from the course root folder. In real projects, build paths from the script's own location:

```python
ROOT = Path(__file__).resolve().parent
```

---

## 2. Opening files: always with `with`

```python
with open("data/pipeline.log", encoding="utf-8") as f:
    for line in f:              # reads one line at a time: works on huge files
        print(line.rstrip("\n"))
# the file is closed automatically here, even if an error happened
```

Modes: `"r"` read (default), `"w"` write (**erases** existing content), `"a"` append, `"x"` create only if new, add `"b"` for binary (`"rb"`).

**Bakit `with`:** files left open lock them on Windows and can lose data. `with` guarantees closing. Every pipeline you'll write uses it.

---

## 3. CSV with the csv module

```python
import csv

with open("data/charges_clean.csv", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)          # each row becomes a dict
    rows = list(reader)

rows[0]   # {"charge_id": "1001", "guest_id": "G001", ..., "amount": "25.5"}
```

**Everything from a CSV is a string.** `"25.5"` must become `float("25.5")` before you can add it. Empty cells come as `""`, not `None`.

Writing:

```python
fields = ["guest_id", "total"]
with open("output/totals.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows([{"guest_id": "G001", "total": 225.0}])
```

`newline=""` is required on Windows; without it you get blank lines between rows.

Other CSV realities: semicolon-delimited files (`csv.reader(f, delimiter=";")`), quoted fields containing commas (`"Santos, Ana"`, which the csv module handles for you, and why you should never split CSV lines with `.split(",")`).

---

## 4. JSON

JSON maps almost 1:1 to Python:

| JSON | Python |
|---|---|
| object `{}` | `dict` |
| array `[]` | `list` |
| string | `str` |
| number | `int` / `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

```python
import json

with open("data/guests.json", encoding="utf-8") as f:
    guests = json.load(f)               # file -> Python

guests[0]["name"]["first"]              # nested access
guests[0]["contact"].get("email")

text = json.dumps(guests[0], indent=2)  # Python -> string
data = json.loads(text)                 # string -> Python

with open("output/guest.json", "w", encoding="utf-8") as f:
    json.dump(guests[0], f, indent=2, ensure_ascii=False)
```

`ensure_ascii=False` keeps `ñ` readable instead of `ñ`.

### Flattening nested JSON

APIs return nested objects; tables need flat columns. Turning
`{"name": {"first": "Ana"}, "stay": {"cabin": "A214"}}` into
`{"first_name": "Ana", "cabin": "A214"}` is one of the most common DE transforms. pandas has `json_normalize` for this (Module 15), but you'll do it by hand first so you understand it.

---

## 5. Other formats you'll meet (preview)

| Format | What it is | Where |
|---|---|---|
| **Excel (.xlsx)** | spreadsheets, multiple sheets, merged headers | Module 15 |
| **Parquet** | columnar, compressed, typed. The standard for data lakes | pandas `to_parquet` |
| **JSON Lines (.jsonl)** | one JSON object per line, easy to stream | logs, event exports |
| **PDF** | documents, not data. Extracting is painful | Module 15 |

---

## Exercises (`exercises.py`)

Each function receives file paths. The tests create temporary files for you.

1. `read_lines(path)`
2. `write_lines(path, lines)`
3. `read_csv_rows(path)`
4. `write_csv_rows(path, rows, fieldnames)`
5. `sum_column(path, column)` – convert text to numbers, skip blanks
6. `load_json(path)` / `save_json(path, data)`
7. `flatten_guest(guest)` – nested JSON → flat dict
8. `guests_json_to_csv(json_path, csv_path)` – a real format conversion
9. `list_files(folder, extension)`
10. `append_audit_line(path, timestamp, message)`
11. `read_jsonl(path)`

## Mini project: daily outlet report (`report.py`, not graded)

Read `data/charges_clean.csv`, compute total revenue per outlet per day, and write `output/outlet_daily.csv` with columns `charge_date, outlet, total, charge_count`, sorted by date then outlet. Then write the same data as `output/outlet_daily.json`. You've just built the "T" and "L" of a small ETL job by hand.

## Self-check

1. What type is every value read by `csv.DictReader`?
2. What happens if you open an existing file with mode `"w"`?
3. Why should you never parse CSV with `line.split(",")`?

<details><summary>Answers</summary>

1. `str` (empty cells are `""`).
2. Its contents are erased immediately.
3. Fields can contain commas inside quotes, like `"Santos, Ana"`; `split` would break them apart.
</details>
