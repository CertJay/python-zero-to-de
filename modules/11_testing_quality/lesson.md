# Module 11: Testing your code and testing your data

**Time:** 6–7 hours · **Prerequisite:** Module 10

## Bakit ko 'to kailangan?

There are two kinds of tests in data engineering:

1. **Code tests** (pytest): does my `clean_amount()` function do what I think, including edge cases?
2. **Data tests** (quality checks): does today's data look right? No null guest IDs, no duplicate charge IDs, amounts within range, outlets from the allowed list.

A pipeline that runs without errors but loads wrong data is worse than one that crashes. Data quality is the part of DE that hiring managers worry about most, and it's the part where **your BA and UAT background is a real advantage**: you've been writing test cases and acceptance criteria for months.

**At work:** a UAT test case ("Given a refund on a closed folio, when posted, then...") maps directly onto a pytest test (arrange → act → assert). Data checks are acceptance criteria that run automatically every day.

---

## 1. pytest basics

You've been *running* pytest tests since Module 00. Now you write them.

```python
# test_cleaning.py   (file name must start with test_)
from cleaning import normalize_outlet

def test_known_variant():                     # function name must start with test_
    assert normalize_outlet(" the BAR ") == "Bar"

def test_unknown_outlet_is_title_cased():
    assert normalize_outlet("pool deck") == "Pool Deck"
```

Run: `pytest` (all tests) or `pytest test_cleaning.py -v` (one file, verbose).

### Arrange, Act, Assert

```python
def test_folio_balance_includes_refunds():
    # Arrange: set up inputs
    folio = Folio("G001")
    folio.add(Charge(1, "G001", "Spa", 120.0))
    folio.add(Charge(2, "G001", "Spa", -20.0, "refund"))
    # Act: run the thing you're testing
    balance = folio.balance
    # Assert: check the outcome
    assert balance == 100.0
```

That's the Given / When / Then of your UAT scripts.

### Testing that errors are raised

```python
import pytest

def test_rejects_other_guest():
    with pytest.raises(ValueError, match="belongs to G002"):
        Folio("G001").add(Charge(1, "G002", "Bar", 10))
```

### Parametrize: many cases, one test

```python
@pytest.mark.parametrize("raw, expected", [
    ("bar", "Bar"),
    (" The Bar ", "Bar"),
    ("Resto", "Restaurant"),
])
def test_normalize_outlet(raw, expected):
    assert normalize_outlet(raw) == expected
```

### Fixtures: shared setup

```python
@pytest.fixture
def sample_charges():
    return [{"guest_id": "G001", "amount": 25.0}, {"guest_id": "G002", "amount": 40.0}]

def test_total(sample_charges):          # pytest passes the fixture in by name
    assert total(sample_charges) == 65.0
```

Built-in fixture `tmp_path` gives each test a fresh temporary folder (you've seen it in Module 06's tests).

### Floating point comparisons

```python
assert 0.1 + 0.2 == pytest.approx(0.3)
```

### What to test

- The **normal case** (happy path).
- **Edge cases:** empty list, `None`, zero, one item, very large values.
- **Bad input:** does it raise the right error?
- **Every bug you fix:** write a test that reproduces it first, then fix it. It can never come back silently.

---

## 2. Data quality checks

Code tests run once, when code changes. Data checks run **every time the pipeline runs**, because the data changes every day.

The six dimensions you'll hear about (and should use in interviews):

| Dimension | Question | Example check |
|---|---|---|
| **Completeness** | Is anything missing? | `guest_id` is never null |
| **Uniqueness** | Any duplicates? | `charge_id` is unique |
| **Validity** | Is the value allowed? | `outlet` in the allowed list; amount format |
| **Accuracy / range** | Is the value plausible? | 0 < amount ≤ 10,000 for sales |
| **Consistency** | Do related things agree? | every `guest_id` exists in the guest master; invoice lines sum to the total |
| **Timeliness** | Is it fresh? | newest `charge_date` is yesterday or today |

### A check returns *what failed*, not just True/False

```python
def check_not_null(rows, column):
    """Return the 0-based indexes of rows where column is missing or blank."""
    return [i for i, row in enumerate(rows) if row.get(column) in (None, "")]
```

Returning the failing rows makes the result actionable: you can quarantine them or show them to the data owner.

### Severity

Not every failed check should stop the pipeline:
- **error** → stop the load (e.g., duplicate primary keys would corrupt the table)
- **warning** → load, but report (e.g., unknown outlet name, mapped to "Other")

Tools like **Great Expectations**, **Soda** and **dbt tests** do exactly this at scale. After this module you'll understand what they're doing, because you'll have built a small version yourself.

---

## Exercises (`exercises.py`)

Data checks (graded):

1. `check_not_null(rows, column)`
2. `check_unique(rows, column)`
3. `check_in_range(rows, column, min_value, max_value)`
4. `check_allowed_values(rows, column, allowed)`
5. `check_foreign_key(rows, column, valid_keys)`
6. `run_checks(rows, checks)` – a mini quality framework with severities
7. `should_stop_pipeline(report)`

## Write your own tests (required, graded by count)

Open `test_mine.py` in this folder. Write **at least 8 tests** for functions you wrote in earlier modules (copy those functions into `my_functions.py` in this folder first). Include at least one `parametrize`, one `pytest.raises`, and one fixture. `python check.py 11` runs your tests together with the course tests.

## Mini project: quality report on the raw file (`quality_report.py`, not graded)

Load `data/onboard_charges_raw.csv` with `csv.DictReader` and run all your checks: amount not null, charge_id unique, outlet allowed (after normalizing), guest_id exists in `data/guests.csv`. Print a report: check name, severity, failures, and 3 example failing rows each. This report is what a data engineer sends to a source-system owner.

## Self-check

1. Why should a check return the failing row indexes instead of just `False`?
2. Give one example each of an "error" check and a "warning" check.
3. What's the difference between a code test and a data test?

<details><summary>Answers</summary>

1. So you can act on them: quarantine those rows, count them, and show examples to the data owner.
2. Error: duplicate `charge_id` (would corrupt the target table). Warning: unrecognised outlet name (load it, but report it).
3. Code tests verify your logic against fixed inputs and run when code changes; data tests verify the actual incoming data and run on every pipeline run.
</details>
