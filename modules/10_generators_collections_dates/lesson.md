# Module 10: Generators, collections, dates and decorators

**Time:** 7–8 hours · **Prerequisite:** Module 09

## Bakit ko 'to kailangan?

This module covers four tools that separate "can write Python" from "can write Python for data":

- **Generators** let you process a 10 GB file with 50 MB of memory, one row at a time.
- **collections** (`Counter`, `defaultdict`, `deque`, `namedtuple`) replace a lot of hand-written loops.
- **datetime** matters because every row of data has a date, and dates are where bugs hide: time zones, day-first vs month-first, "how many nights between check-in and check-out".
- **Decorators** add behavior (timing, retries, logging) around functions without changing them. Airflow's `@task`, pytest's `@pytest.fixture` and Flask's `@app.route` are all decorators.

**At work:** voyage dates, folio posting times, port days, cut-off times for end-of-day: date logic is everywhere in hospitality systems. Many UAT defects are date defects.

---

## 1. Iterables, iterators and generators

Anything you can loop over is **iterable** (lists, strings, dicts, files). A **generator** produces values one at a time, *only when asked*, instead of building the whole list in memory.

```python
def read_amounts(path):
    with open(path, encoding="utf-8") as f:
        next(f)                           # skip header
        for line in f:
            yield float(line.split(",")[4] or 0)   # yield = hand back one value, pause here

for amount in read_amounts("data/charges_clean.csv"):
    ...                                    # one row in memory at a time
```

`yield` turns a function into a generator. Each `next()` resumes from where it paused.

```python
gen = (x * 2 for x in range(5))   # generator expression: like a list comprehension with ()
next(gen)   # 0
next(gen)   # 2
list(gen)   # [4, 6, 8]  (the rest; a generator is used up after one pass!)
sum(x * 2 for x in range(1_000_000))   # no million-item list is ever created
```

**Bakit:** batch loading. Read a huge file as a stream, group rows into batches of 1,000, load each batch, never hold the whole file:

```python
def batches(rows, size):
    batch = []
    for row in rows:
        batch.append(row)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch
```

Generators also chain into lazy pipelines: `load(validate(clean(read(path))))` where each stage yields rows to the next.

---

## 2. collections

```python
from collections import Counter, defaultdict, deque, namedtuple, OrderedDict

Counter(["Bar", "Spa", "Bar"])                 # Counter({'Bar': 2, 'Spa': 1})
c = Counter()
c["Bar"] += 25.0                               # missing keys start at 0
c.most_common(2)                               # [('Bar', 25.0), ...]

groups = defaultdict(list)                     # missing keys start as []
groups["G001"].append(charge)                  # no setdefault needed

last_five = deque(maxlen=5)                    # keeps only the newest 5 items
for value in stream:
    last_five.append(value)                    # rolling window

Row = namedtuple("Row", ["guest_id", "amount"])
r = Row("G001", 25.0)
r.amount                                       # 25.0, readable AND lightweight
```

---

## 3. itertools: loops you don't have to write

```python
import itertools

list(itertools.chain([1, 2], [3]))                  # [1, 2, 3]
list(itertools.islice(huge_generator, 10))          # first 10 items only
list(itertools.pairwise([10, 15, 12]))              # [(10, 15), (15, 12)]  (Python 3.10+)
list(itertools.accumulate([25, 120, 80]))           # [25, 145, 225] running total
list(itertools.product(["Bar", "Spa"], ["Day1", "Day2"]))  # every combination

# groupby groups CONSECUTIVE equal keys, so sort first!
rows = sorted(rows, key=lambda r: r["guest_id"])
for guest, items in itertools.groupby(rows, key=lambda r: r["guest_id"]):
    print(guest, sum(r["amount"] for r in items))
```

---

## 4. Dates and times

```python
from datetime import date, datetime, timedelta, timezone

d = date(2026, 10, 1)
d.isoformat()                         # "2026-10-01"  <- the format to store and exchange
date.fromisoformat("2026-10-01")
d + timedelta(days=7)                 # date(2026, 10, 8)
(date(2026, 10, 8) - d).days          # 7  -> nights between check-in and check-out
d.weekday()                           # 0=Monday ... 6=Sunday
d.strftime("%d/%m/%Y")                # "01/10/2026"  date -> text
datetime.strptime("01/10/2026", "%d/%m/%Y").date()   # text -> date
```

Format codes you'll use: `%Y` 2026, `%m` 10, `%d` 01, `%b` Oct, `%B` October, `%H` 24-hour, `%M` minutes, `%S` seconds.

### The day-first trap

`01/10/2026` is **1 October** in the Philippines and Europe, **January 10** in the US. Never guess. Know the source system's format (it belongs in the interface spec!) and parse it explicitly. Ambiguous dates are one of the most expensive data defects because they look valid.

### Time zones

A ship crosses time zones; servers run in UTC. Rules:
- Store timestamps in **UTC**: `datetime.now(timezone.utc)`.
- Convert to local time only for display.
- A datetime without tzinfo is "naive". Comparing naive and aware datetimes raises an error, and that's a good thing.

```python
from zoneinfo import ZoneInfo
utc_time = datetime(2026, 10, 1, 4, 0, tzinfo=timezone.utc)
utc_time.astimezone(ZoneInfo("Asia/Manila"))   # 2026-10-01 12:00:00+08:00
```

(On Windows, `zoneinfo` may need `pip install tzdata`.)

---

## 5. Decorators

A decorator is a function that takes a function and returns a new function with extra behavior.

```python
import functools, time

def timed(func):
    @functools.wraps(func)              # keeps the original name and docstring
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start:.3f}s")
        return result
    return wrapper

@timed                                  # same as: load_charges = timed(load_charges)
def load_charges(path):
    ...
```

It's a closure (Module 04) used as a wrapper. Decorators with arguments add one more layer:

```python
def retry(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except ConnectionError:
                    if attempt == times - 1:
                        raise
        return wrapper
    return decorator

@retry(times=3)
def fetch_rates():
    ...
```

`functools.lru_cache` is a built-in decorator that memoizes results (remember Fibonacci in Module 04).

---

## Exercises (`exercises.py`)

1. `batched(iterable, size)` – generator of lists
2. `running_total(numbers)` – generator
3. `stream_csv(path)` – generator over a file
4. `revenue_by_outlet(charges)` – Counter
5. `top_outlets(charges, n)` – Counter.most_common
6. `group_ids(charges)` – defaultdict
7. `last_n(iterable, n)` – deque
8. `dedupe_keep_order(items)`
9. `parse_any_date(text)` – three formats, explicit day-first
10. `nights_between(check_in, check_out)`
11. `daily_counts(timestamps)`
12. `voyage_days(start, n)` – timedelta
13. `to_manila(utc_iso)` – time zones
14. `count_calls` – a decorator that counts
15. `@timed` – a decorator that records duration

## Mini project: memory-friendly loader (`stream_load.py`, not graded)

Use `stream_csv` + `batched` to read `data/charges_clean.csv` in batches of 100. For each batch, print the batch number, row count and batch total. Decorate the main function with your `@timed`. Then explain to yourself (out loud or in your Friday notes) why this design would still work for a 10 GB file.

## Self-check

1. What's the difference between `[x for x in data]` and `(x for x in data)`?
2. Why must you sort before `itertools.groupby`?
3. What date is `"03/04/2026"`? (Trick question.)
4. Why use `functools.wraps` in a decorator?

<details><summary>Answers</summary>

1. The first builds the whole list in memory; the second is a lazy generator producing one item at a time.
2. `groupby` only groups consecutive equal keys; unsorted data produces the same key in several groups.
3. It depends on the source: 3 April (day-first) or March 4 (month-first). You must know the system's format.
4. It keeps the original function's name and docstring on the wrapper, which matters for logs, debugging and tools.
</details>
