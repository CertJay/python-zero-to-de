"""Reference solutions for Module 10."""
import csv
import functools
import time
from collections import Counter, defaultdict, deque
from datetime import date, datetime, timedelta, timezone  # noqa: F401
from zoneinfo import ZoneInfo

DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%b %d %Y")


def batched(iterable, size):
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch


def running_total(numbers):
    total = 0
    for n in numbers:
        total += n
        yield total


def stream_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            yield row


def revenue_by_outlet(charges):
    totals = Counter()
    for c in charges:
        totals[c["outlet"]] += c["amount"]
    return Counter({k: round(v, 2) for k, v in totals.items()})


def top_outlets(charges, n):
    return revenue_by_outlet(charges).most_common(n)


def group_ids(charges):
    groups = defaultdict(list)
    for c in charges:
        groups[c["guest_id"]].append(c["charge_id"])
    return dict(groups)


def last_n(iterable, n):
    return list(deque(iterable, maxlen=n))


def dedupe_keep_order(items):
    seen = set()
    out = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def parse_any_date(text):
    text = text.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def nights_between(check_in, check_out):
    return (date.fromisoformat(check_out) - date.fromisoformat(check_in)).days


def daily_counts(timestamps):
    counts = Counter(datetime.fromisoformat(ts).date().isoformat() for ts in timestamps)
    return {day: counts[day] for day in sorted(counts)}


def voyage_days(start, n):
    first = date.fromisoformat(start)
    return [(first + timedelta(days=i)).isoformat() for i in range(n)]


def to_manila(utc_iso):
    return datetime.fromisoformat(utc_iso).astimezone(ZoneInfo("Asia/Manila")).isoformat()


def count_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        wrapper.last_seconds = time.perf_counter() - start
        return result
    wrapper.last_seconds = None
    return wrapper
