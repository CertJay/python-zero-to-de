# Module 05: Cleaning text and regular expressions

**Time:** 7–8 hours · **Prerequisite:** Module 04

## Bakit ko 'to kailangan?

Real data arrives dirty: `" bar "`, `"BAR"` and `"The Bar"` are the same outlet. Phone numbers come as `0917 123 4567`, `+63-917-123-4567` and `9171234567`. Amounts come as `"USD 1,250.50"`. Before anything is loaded, someone has to standardize it. That someone is the data engineer.

**At work:** your DepEd and TESDA work was mostly this, done by hand in Excel. This module turns that experience into code. When a source system sends free text, you'll be able to write the rule that cleans it, and specify that rule precisely in your BA documents.

---

## 1. String methods you'll use every day

```python
s = "  The Bar  "
s.strip()             # "The Bar"        remove outer whitespace
s.lstrip(), s.rstrip()
s.lower(), s.upper(), s.title()   # "  the bar  " ...
"bar".capitalize()    # "Bar"

"Bar,Spa,Cafe".split(",")      # ["Bar", "Spa", "Cafe"]
"a  b   c".split()             # ["a", "b", "c"]  (no argument = any whitespace)
"-".join(["2026", "10", "01"]) # "2026-10-01"

"USD 25".replace("USD ", "")   # "25"
"G001".startswith("G")         # True
"report.csv".endswith(".csv")  # True
"Spa Treatment".find("Treat")  # 4   (-1 if not found)
"Spa" in "Spa Treatment"       # True

"123".isdigit()      # True
"abc".isalpha()      # True
"G001".isalnum()     # True
"7".zfill(3)         # "007"
```

### The cleaning recipe

Almost every text-cleaning function follows the same order:

1. Handle `None` / missing.
2. `strip()` outer whitespace.
3. Collapse inner whitespace: `" ".join(s.split())`.
4. Normalize case (`lower()` for comparison, `title()` for display).
5. Map known variants to a standard value with a dict.

```python
OUTLET_MAP = {"bar": "Bar", "the bar": "Bar", "resto": "Restaurant"}

def normalize_outlet(raw):
    key = " ".join(raw.split()).lower()
    return OUTLET_MAP.get(key, key.title())
```

**Bakit a mapping dict:** business users can review and extend a mapping table. A pile of `if` statements can't be reviewed by anyone. In your BA work, that mapping table is a requirements artifact.

---

## 2. Unicode and encodings (short but important)

`"Café"` vs `"Cafe"`, `"Dasmariñas"` vs `"Dasmarinas"`. When reading files, always say the encoding: `open(path, encoding="utf-8")`. If you see characters like `Ã±` where `ñ` should be, the file was read with the wrong encoding.

To strip accents for matching:

```python
import unicodedata
def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

strip_accents("Café Dasmariñas")   # "Cafe Dasmarinas"
```

---

## 3. Regular expressions (regex)

A regex is a pattern that describes text. Use it when simple string methods aren't enough: extracting IDs, validating formats, parsing log lines.

```python
import re
```

### The building blocks

| Pattern | Matches |
|---|---|
| `\d` | a digit 0–9 |
| `\w` | letter, digit or underscore |
| `\s` | whitespace |
| `.` | any character |
| `[A-Z]` | one uppercase letter |
| `[^0-9]` | anything except a digit |
| `+` | one or more of the previous |
| `*` | zero or more |
| `?` | zero or one (optional) |
| `{3}` | exactly 3 |
| `{2,4}` | 2 to 4 |
| `^` / `$` | start / end of the string |
| `( )` | a capture group |
| `\|` | or |

Always write patterns as raw strings: `r"\d+"` (the `r` stops Python from treating `\d` specially).

### The functions

```python
text = "Charges for G001 and G045 posted; G9 is invalid"

re.findall(r"G\d{3}", text)           # ["G001", "G045"]
re.search(r"G\d{3}", text).group()    # "G001"  first match (None if no match!)
re.fullmatch(r"G\d{3}", "G001")       # match object -> truthy; whole string must match
re.sub(r"\s+", " ", "a   b    c")     # "a b c"  replace
re.split(r"[;,]", "Bar;Spa,Cafe")     # ["Bar", "Spa", "Cafe"]
```

### Capture groups: extract parts

```python
line = "2026-10-01 08:15:02 ERROR [loader] Row 15: missing amount"
pattern = r"^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) \[(\w+)\] (.*)$"
m = re.match(pattern, line)
m.group(1)   # "2026-10-01"
m.group(3)   # "ERROR"
m.groups()   # ("2026-10-01", "08:15:02", "ERROR", "loader", "Row 15: missing amount")
```

Named groups read better:

```python
pattern = r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<level>\w+)"
m = re.search(pattern, line)
m.group("level")     # "ERROR"
m.groupdict()        # {"date": "2026-10-01", "level": "ERROR"}
```

### Parsing an amount with a regex

```python
m = re.search(r"-?\d[\d,]*\.?\d*", "USD 1,250.50")
float(m.group().replace(",", ""))   # 1250.5
```

### Compile patterns you reuse

```python
GUEST_ID = re.compile(r"^G\d{3}$")
GUEST_ID.fullmatch("G001")
```

**Practice tool:** paste your pattern and sample text into <https://regex101.com> (choose the Python flavor). It explains every part of the pattern.

**Warning:** regex is powerful and easy to over-use. If `startswith`, `split` or `in` solves it, prefer those. Readable beats clever.

---

## 4. Validation vs cleaning

- **Validation** answers "is this acceptable?" → returns `True/False` or an error.
- **Cleaning** answers "what's the standard form?" → returns the fixed value, or `None` if it can't be fixed.

Keep them separate. In a pipeline, rows that can't be cleaned are **quarantined** (saved aside for review), not silently dropped. You'll build that in Module 07.

---

## Exercises (`exercises.py`)

1. `clean_name(name)` – the cleaning recipe
2. `normalize_outlet(raw)` – mapping dict
3. `slugify(text)` – file/URL-safe names
4. `extract_guest_ids(text)` – `re.findall`
5. `is_valid_email(email)` – `re.fullmatch`
6. `parse_amount(text)` – amounts with currency and commas
7. `mask_email(email)` – privacy masking
8. `standardize_ph_mobile(phone)` – messy PH mobile numbers
9. `parse_log_line(line)` – named groups
10. `count_log_levels(lines)` – reuse your parser
11. `strip_accents(text)` – unicode

Real data to try afterwards: `data/pipeline.log` (120 log lines) and the `outlet` column of `data/onboard_charges_raw.csv`.

## Mini project: log report (`log_report.py`, not graded)

Read `data/pipeline.log` (`open(path, encoding="utf-8").read().splitlines()`), parse every line with your `parse_log_line`, and print: count per level, count per component, and every ERROR message with its time. You're building the kind of quick report you'd make to answer "why did last night's job fail?"

## Self-check

1. What does `re.search` return when nothing matches, and what happens if you call `.group()` on it?
2. What's the difference between `re.match`, `re.search` and `re.fullmatch`?
3. Why write `r"\d+"` instead of `"\d+"`?

<details><summary>Answers</summary>

1. `None`; calling `.group()` on `None` raises `AttributeError`. Always check `if m:` first.
2. `match` checks only at the start of the string, `search` finds the first match anywhere, `fullmatch` requires the entire string to match.
3. Raw strings keep backslashes literal so the regex engine receives `\d` exactly.
</details>
