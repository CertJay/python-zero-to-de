"""Module 10 exercises: generators, collections, dates, decorators.

Run:  python check.py 10
"""
import csv  # noqa: F401
import functools  # noqa: F401
import time  # noqa: F401
from collections import Counter, defaultdict, deque  # noqa: F401
from datetime import date, datetime, timedelta, timezone  # noqa: F401
from zoneinfo import ZoneInfo  # noqa: F401


def batched(iterable, size):
    """GENERATOR: yield lists of up to `size` items from any iterable (works with
    generators too, not only lists). Use `yield`.

    >>> list(batched(range(5), 2))
    [[0, 1], [2, 3], [4]]
    """
    raise NotImplementedError


def running_total(numbers):
    """GENERATOR: yield the running total after each number.

    >>> list(running_total([25, 120, 80]))
    [25, 145, 225]
    """
    raise NotImplementedError


def stream_csv(path):
    """GENERATOR: yield one dict per CSV row (csv.DictReader), keeping the file open
    only while iterating (use `with` inside the generator)."""
    raise NotImplementedError


def revenue_by_outlet(charges):
    """Return a Counter: outlet -> total amount (round values to 2 decimals)."""
    raise NotImplementedError


def top_outlets(charges, n):
    """Return the n outlets with the highest revenue as a list of (outlet, total)
    tuples, highest first. Use revenue_by_outlet and Counter.most_common."""
    raise NotImplementedError


def group_ids(charges):
    """Return a normal dict: guest_id -> list of charge_ids, using defaultdict(list)
    internally. Keep original order."""
    raise NotImplementedError


def last_n(iterable, n):
    """Return a list of the last n items of any iterable, using deque(maxlen=n).

    >>> last_n(range(10), 3)
    [7, 8, 9]
    """
    raise NotImplementedError


def dedupe_keep_order(items):
    """Remove duplicates but keep the first occurrence order.

    >>> dedupe_keep_order(["G2", "G1", "G2", "G3", "G1"])
    ['G2', 'G1', 'G3']
    """
    raise NotImplementedError


def parse_any_date(text):
    """Parse a date in one of these formats and return a datetime.date:
      "2026-10-01"   (ISO)
      "01/10/2026"   (DAY first: this is 1 October)
      "Oct 01 2026"  (month abbreviation)
    Strip surrounding spaces. Return None if none of the formats match.
    Hint: try datetime.strptime with each format in a loop; catch ValueError.
    """
    raise NotImplementedError


def nights_between(check_in, check_out):
    """Number of nights between two ISO date strings.

    >>> nights_between("2026-10-01", "2026-10-08")
    7
    """
    raise NotImplementedError


def daily_counts(timestamps):
    """Given ISO datetime strings like "2026-10-01T08:15:00", return a dict
    "YYYY-MM-DD" -> number of timestamps on that day, with keys in sorted order."""
    raise NotImplementedError


def voyage_days(start, n):
    """Return a list of n ISO date strings starting at `start` (ISO string), one per day.

    >>> voyage_days("2026-10-30", 4)
    ['2026-10-30', '2026-10-31', '2026-11-01', '2026-11-02']
    """
    raise NotImplementedError


def to_manila(utc_iso):
    """Convert a UTC timestamp string like "2026-10-01T04:00:00+00:00" to Manila time and
    return it in ISO format.

    >>> to_manila("2026-10-01T04:00:00+00:00")
    '2026-10-01T12:00:00+08:00'
    """
    raise NotImplementedError


def count_calls(func):
    """DECORATOR: return a wrapper that calls func and counts calls in wrapper.calls
    (start at 0). Use functools.wraps so the wrapper keeps func's __name__."""
    raise NotImplementedError


def timed(func):
    """DECORATOR: return a wrapper that runs func, stores the duration in seconds
    (time.perf_counter) in wrapper.last_seconds, and returns func's result.
    Before the first call, wrapper.last_seconds is None. Use functools.wraps."""
    raise NotImplementedError
