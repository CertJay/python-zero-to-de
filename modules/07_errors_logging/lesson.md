# Module 07: Errors, validation and logging

**Time:** 6–7 hours · **Prerequisite:** Module 06

## Bakit ko 'to kailangan?

Pipelines fail. Files arrive late, a database goes down, a row has `"abc"` in the amount column. The difference between a junior and a dependable data engineer is what happens next: does the job crash with no explanation, silently drop data, or **quarantine the bad rows, log exactly what happened, retry what can be retried, and finish the rest?**

**At work:** your RAID logs and defect reports describe failures in words. Error handling is how those rules ("reject the row and notify", "retry 3 times then alert") become real behavior. You'll be able to write acceptance criteria for error paths that developers can't argue with.

---

## 1. Exceptions: what Python does when something goes wrong

```python
int("abc")          # ValueError
{"a": 1}["b"]       # KeyError
[1, 2][5]           # IndexError
10 / 0              # ZeroDivisionError
open("nope.csv")    # FileNotFoundError
"5" + 5             # TypeError
None.upper()        # AttributeError
```

Unhandled, an exception stops the program and prints a traceback (read it bottom-up, Module 00).

---

## 2. try / except / else / finally

```python
try:
    amount = float(row["amount"])
except ValueError:
    amount = None                # handle the specific problem
except KeyError:
    raise                        # re-raise: we can't fix a missing column here
else:
    print("parsed fine")         # runs only if NO exception happened
finally:
    print("always runs")         # cleanup: close connections, write status
```

### Rules professionals follow

1. **Catch specific exceptions.** `except ValueError:` not bare `except:`.
2. **Never swallow errors silently.** This is the worst pipeline bug:

   ```python
   try:
       load(row)
   except Exception:
       pass        # data vanished and nobody knows
   ```

3. **Keep the `try` block small**, only around the line that can fail.
4. **Catch where you can actually do something.** If you can't fix it, let it rise.

### Getting the error details

```python
try:
    float("abc")
except ValueError as e:
    print(f"Could not parse: {e}")   # could not convert string to float: 'abc'
```

---

## 3. Raising your own errors

```python
def validate_amount(amount):
    if amount is None:
        raise ValueError("amount is missing")
    if amount < 0:
        raise ValueError(f"negative amount: {amount}")
    return True
```

Clear messages save hours. `"Row 15: amount is missing"` beats `"Error"` every time.

### Custom exception classes

```python
class DataQualityError(Exception):
    """Raised when data fails a quality check."""

raise DataQualityError("0 rows extracted from charges file")
```

Custom exceptions let the caller react to *your* problem specifically: `except DataQualityError:` → alert the data owner; `except ConnectionError:` → retry.

---

## 4. The quarantine pattern (the most important idea in this module)

Don't let one bad row kill a 50,000-row load. Separate good from bad, keep the bad ones with the reason, and report.

```python
valid, rejected = [], []
for row_number, row in enumerate(rows, start=1):
    try:
        validate(row)
        valid.append(row)
    except ValueError as e:
        rejected.append({"row": row_number, "error": str(e), "data": row})

load(valid)
save_for_review(rejected)
log.warning("Rejected %d of %d rows", len(rejected), len(rows))
```

This is how real pipelines behave, and it's a great story for interviews: *"I never drop data silently. Bad rows go to a quarantine table with the reason."*

---

## 5. Retries

Network calls and databases fail temporarily. Retry them, a limited number of times:

```python
import time

def with_retry(func, attempts=3, wait_seconds=2):
    for attempt in range(1, attempts + 1):
        try:
            return func()
        except ConnectionError:
            if attempt == attempts:
                raise                    # give up: let the caller know
            time.sleep(wait_seconds)
```

Only retry errors that can fix themselves (timeouts, connection drops). Retrying a `ValueError` from bad data just fails three times.

---

## 6. Logging: print() for grown-ups

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
log = logging.getLogger("charges_pipeline")

log.debug("Detailed info for developers")     # hidden at INFO level
log.info("Loaded %d rows", 550)
log.warning("Outlet %r not recognised", "Pool Deck")
log.error("Row %d: missing amount", 15)
log.exception("Load failed")    # inside except: also prints the traceback
```

Output:

```
2026-10-01 08:15:02,113 INFO [charges_pipeline] Loaded 550 rows
```

Look familiar? It's the format of `data/pipeline.log` you parsed in Module 05.

**Bakit logging over print:** levels (you can hide DEBUG in production), timestamps, the source name, and you can send logs to files or monitoring tools without changing your code.

**Gotcha:** calling `logger.addHandler(...)` every time a function runs adds duplicate handlers, so every message prints twice, then three times... Check `if not logger.handlers:` first.

---

## 7. Debugging techniques

1. **Read the traceback** bottom-up.
2. **Print/log the actual values** right before the failing line: `log.debug("row=%r", row)`. `%r` shows quotes and hidden spaces: `'Bar '`.
3. **Use the VS Code debugger:** click left of a line number to set a red breakpoint → F5 → inspect every variable. This is faster than print debugging once you're used to it.
4. **Shrink the problem:** reproduce it with 3 rows, not 50,000.
5. **`assert`** for things that must be true during development: `assert len(rows) > 0, "no rows read"`. (Don't use assert for user-input validation; it can be disabled.)

---

## Exercises (`exercises.py`)

1. `safe_divide(a, b)`
2. `parse_int(text, default=None)`
3. `validate_charge(charge)` – raise `ValueError` with exact messages
4. `DataQualityError` + `require_rows(rows)` – custom exception
5. `split_valid_invalid(charges)` – the quarantine pattern
6. `retry(func, attempts=3)` – retry logic
7. `read_config(path)` – handle two different failures differently
8. `get_logger(name)` – no duplicate handlers
9. `process_all(items, func)` – `finally` and run status

## Mini project: validate the raw charges file (`validate_raw.py`, not graded)

Read `data/onboard_charges_raw.csv` with `csv.DictReader`. For each row, try to: parse the amount (fails on blanks), check the guest id format (Module 02), normalize the outlet (Module 05). Use `split_valid_invalid`-style logic, log a summary, and write `output/rejected_rows.csv` with the row number and reason. How many rows were rejected, and why?

## Self-check

1. Why is `except: pass` dangerous in a data pipeline?
2. When should you retry and when shouldn't you?
3. What's the difference between `log.error(...)` and `log.exception(...)`?

<details><summary>Answers</summary>

1. Errors disappear silently, so data goes missing and nobody finds out until a report is wrong.
2. Retry temporary failures (timeouts, dropped connections). Don't retry deterministic ones like bad data or wrong credentials; they'll fail every time.
3. `log.exception` is used inside an `except` block and adds the full traceback; `log.error` logs only the message.
</details>
