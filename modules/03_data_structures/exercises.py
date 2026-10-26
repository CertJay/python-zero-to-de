"""Module 03 exercises: lists, tuples, dicts, sets, comprehensions.

Run:  python check.py 03

Rule: never modify the input you receive. Build and return new objects.
"""


def total_by_outlet(charges):
    """Sum amounts per outlet. Round each total to 2 decimals.

    >>> total_by_outlet([
    ...     {"guest_id": "G001", "outlet": "Bar", "amount": 25.0},
    ...     {"guest_id": "G002", "outlet": "Bar", "amount": 40.5},
    ...     {"guest_id": "G001", "outlet": "Spa", "amount": 120.0},
    ... ])
    {'Bar': 65.5, 'Spa': 120.0}
    """
    raise NotImplementedError


def unique_guests(charges):
    """Return a SORTED list of the unique guest_ids in `charges`.

    >>> unique_guests([{"guest_id": "G002"}, {"guest_id": "G001"}, {"guest_id": "G002"}])
    ['G001', 'G002']
    """
    raise NotImplementedError


def top_n_charges(charges, n):
    """Return the n charges with the biggest amounts, biggest first.
    If two amounts tie, the one that appeared first in `charges` comes first.

    Hint: sorted(..., key=lambda c: c["amount"], reverse=True) keeps ties in
    original order (Python's sort is "stable").
    """
    raise NotImplementedError


def invert_mapping(mapping):
    """Swap keys and values.

    >>> invert_mapping({"G001": "A214", "G002": "B110"})
    {'A214': 'G001', 'B110': 'G002'}
    """
    raise NotImplementedError


def merge_profiles(base, updates):
    """Return a NEW dict: everything in `base`, overwritten/extended by `updates`.
    Do not change `base` or `updates`.

    >>> merge_profiles({"name": "Ana", "tier": "Silver"}, {"tier": "Gold", "cabin": "A214"})
    {'name': 'Ana', 'tier': 'Gold', 'cabin': 'A214'}
    """
    raise NotImplementedError


def common_outlets(outlets_a, outlets_b):
    """Return a sorted list of outlets that appear in BOTH lists (no duplicates).

    >>> common_outlets(["Bar", "Spa", "Bar"], ["Spa", "Cafe", "Bar"])
    ['Bar', 'Spa']
    """
    raise NotImplementedError


def missing_ids(source_ids, master_ids):
    """Reconciliation: return a sorted list of ids that are in `source_ids`
    but NOT in `master_ids` (no duplicates).

    Real use: guest ids in the charges feed that don't exist in the guest master.

    >>> missing_ids(["G001", "G999", "G002", "G999"], ["G001", "G002", "G003"])
    ['G999']
    """
    raise NotImplementedError


def squares_of_evens(numbers):
    """Return the squares of the even numbers, in order. Use a list comprehension.

    >>> squares_of_evens([1, 2, 3, 4])
    [4, 16]
    """
    raise NotImplementedError


def group_by(records, key):
    """Group a list of dicts by the value of `key`.
    Return a dict: key value -> list of records (keep original order inside each list).

    >>> group_by([{"g": "A", "n": 1}, {"g": "B", "n": 2}, {"g": "A", "n": 3}], "g")
    {'A': [{'g': 'A', 'n': 1}, {'g': 'A', 'n': 3}], 'B': [{'g': 'B', 'n': 2}]}
    """
    raise NotImplementedError


def find_duplicates(values):
    """Return a sorted list of values that appear more than once.

    >>> find_duplicates(["C1", "C2", "C1", "C3", "C2", "C1"])
    ['C1', 'C2']
    """
    raise NotImplementedError


def chunk(items, size):
    """Split items into consecutive batches of length `size` (the last may be shorter).
    This is how pipelines load big data in batches.

    >>> chunk([1, 2, 3, 4, 5], 2)
    [[1, 2], [3, 4], [5]]
    """
    raise NotImplementedError


def flatten(list_of_lists):
    """Flatten one level of nesting.

    >>> flatten([[1, 2], [3], [], [4, 5]])
    [1, 2, 3, 4, 5]
    """
    raise NotImplementedError


def word_counts(text):
    """Count words, case-insensitive. Words are separated by whitespace.
    Do not use collections.Counter (that comes in Module 10).

    >>> word_counts("Bar spa BAR cafe bar")
    {'bar': 3, 'spa': 1, 'cafe': 1}
    """
    raise NotImplementedError


def rows_to_columns(rows):
    """Convert a list of dicts (rows) into a dict of lists (columns).
    Assume every row has the same keys, in the same order. Empty input -> {}.

    >>> rows_to_columns([{"id": 1, "amt": 25}, {"id": 2, "amt": 40}])
    {'id': [1, 2], 'amt': [25, 40]}
    """
    raise NotImplementedError


def columns_to_rows(columns):
    """The reverse of rows_to_columns.

    >>> columns_to_rows({"id": [1, 2], "amt": [25, 40]})
    [{'id': 1, 'amt': 25}, {'id': 2, 'amt': 40}]
    """
    raise NotImplementedError


def transpose(matrix):
    """Transpose a rectangular list of lists.

    >>> transpose([[1, 2, 3], [4, 5, 6]])
    [[1, 4], [2, 5], [3, 6]]
    """
    raise NotImplementedError
