"""Reference solutions for Module 20. Read the complexity notes as much as the code."""
from collections import Counter, defaultdict
from datetime import datetime, timedelta


def two_sum(nums, target):
    # O(n): remember each value's index; for each new value, look up its complement.
    seen = {}
    for j, n in enumerate(nums):
        if target - n in seen:
            return (seen[target - n], j)
        seen.setdefault(n, j)
    return None


def is_anagram(a, b):
    # O(n): compare letter counts.
    clean = lambda s: Counter(s.replace(" ", "").lower())
    return clean(a) == clean(b)


def first_unique_char(s):
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1


def merge_intervals(intervals):
    # O(n log n): sort by start, then extend or start a new interval.
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


def group_anagrams(words):
    groups = defaultdict(list)
    for w in words:
        groups["".join(sorted(w))].append(w)
    return sorted((sorted(g) for g in groups.values()), key=lambda g: g[0])


def top_k_frequent(items, k):
    counts = Counter(items)
    return sorted(counts, key=lambda x: (-counts[x], x))[:k]


def valid_brackets(s):
    # Stack: push openers, pop on closers and check they match.
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack


def longest_unique_substring(s):
    # Sliding window: move `left` past the previous occurrence of a repeated char.
    last, left, best = {}, 0, 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best


def max_subarray_sum(nums):
    # Kadane: best run ending here = max(this value, previous run + this value).
    best = current = nums[0]
    for n in nums[1:]:
        current = max(n, current + n)
        best = max(best, current)
    return best


def missing_numbers(ids, start, end):
    return sorted(set(range(start, end + 1)) - set(ids))


def flatten_json(obj, sep="."):
    out = {}

    def walk(value, prefix):
        if isinstance(value, dict):
            for k, v in value.items():
                walk(v, f"{prefix}{sep}{k}" if prefix else str(k))
        elif isinstance(value, list):
            for i, v in enumerate(value):
                walk(v, f"{prefix}{sep}{i}" if prefix else str(i))
        else:
            out[prefix] = value

    walk(obj, "")
    return out


def merge_sorted(a, b):
    # Two pointers.
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    return out + a[i:] + b[j:]


def rolling_average(values, window):
    if len(values) < window:
        return []
    total = sum(values[:window])
    out = [round(total / window, 2)]
    for i in range(window, len(values)):
        total += values[i] - values[i - window]
        out.append(round(total / window, 2))
    return out


def dedupe_latest(records, key, ts_field):
    latest = {}
    for r in records:
        k = r[key]
        if k not in latest or r[ts_field] >= latest[k][ts_field]:
            latest[k] = r
    return [latest[k] for k in sorted(latest)]


def diff_records(old, new, key):
    o = {r[key]: r for r in old}
    n = {r[key]: r for r in new}
    return {
        "added": sorted(n.keys() - o.keys()),
        "removed": sorted(o.keys() - n.keys()),
        "changed": sorted(k for k in o.keys() & n.keys() if o[k] != n[k]),
    }


def parse_csv_line(line):
    fields, field, in_quotes, i = [], [], False, 0
    while i < len(line):
        ch = line[i]
        if in_quotes:
            if ch == '"':
                if i + 1 < len(line) and line[i + 1] == '"':
                    field.append('"'); i += 1
                else:
                    in_quotes = False
            else:
                field.append(ch)
        elif ch == '"':
            in_quotes = True
        elif ch == ",":
            fields.append("".join(field)); field = []
        else:
            field.append(ch)
        i += 1
    fields.append("".join(field))
    return fields


def compress_runs(s):
    if not s:
        return ""
    out, current, count = [], s[0], 1
    for ch in s[1:]:
        if ch == current:
            count += 1
        else:
            out.append(f"{current}{count}"); current, count = ch, 1
    out.append(f"{current}{count}")
    return "".join(out)


def binary_search(sorted_values, target):
    lo, hi = 0, len(sorted_values) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_values[mid] == target:
            return mid
        if sorted_values[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def sessionize(timestamps, gap_minutes=30):
    sessions, current, previous = [], 0, None
    for ts in timestamps:
        t = datetime.fromisoformat(ts)
        if previous is None or t - previous > timedelta(minutes=gap_minutes):
            current += 1
        sessions.append(current)
        previous = t
    return sessions


def second_highest(values):
    distinct = sorted(set(values), reverse=True)
    return distinct[1] if len(distinct) >= 2 else None


def pivot_records(records, row_key, col_key, value_key):
    out = {}
    for r in records:
        row = out.setdefault(r[row_key], {})
        row[r[col_key]] = row.get(r[col_key], 0) + r[value_key]
    return out
