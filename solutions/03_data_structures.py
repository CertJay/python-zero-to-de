"""Reference solutions for Module 03."""


def total_by_outlet(charges):
    totals = {}
    for c in charges:
        totals[c["outlet"]] = totals.get(c["outlet"], 0) + c["amount"]
    return {outlet: round(total, 2) for outlet, total in totals.items()}


def unique_guests(charges):
    return sorted({c["guest_id"] for c in charges})


def top_n_charges(charges, n):
    return sorted(charges, key=lambda c: c["amount"], reverse=True)[:n]


def invert_mapping(mapping):
    return {value: key for key, value in mapping.items()}


def merge_profiles(base, updates):
    return {**base, **updates}


def common_outlets(outlets_a, outlets_b):
    return sorted(set(outlets_a) & set(outlets_b))


def missing_ids(source_ids, master_ids):
    return sorted(set(source_ids) - set(master_ids))


def squares_of_evens(numbers):
    return [n * n for n in numbers if n % 2 == 0]


def group_by(records, key):
    groups = {}
    for record in records:
        groups.setdefault(record[key], []).append(record)
    return groups


def find_duplicates(values):
    seen, dupes = set(), set()
    for v in values:
        if v in seen:
            dupes.add(v)
        seen.add(v)
    return sorted(dupes)


def chunk(items, size):
    return [items[i:i + size] for i in range(0, len(items), size)]


def flatten(list_of_lists):
    return [item for inner in list_of_lists for item in inner]


def word_counts(text):
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def rows_to_columns(rows):
    if not rows:
        return {}
    return {key: [row[key] for row in rows] for key in rows[0]}


def columns_to_rows(columns):
    if not columns:
        return []
    keys = list(columns)
    length = len(columns[keys[0]])
    return [{key: columns[key][i] for key in keys} for i in range(length)]


def transpose(matrix):
    return [list(col) for col in zip(*matrix)]
