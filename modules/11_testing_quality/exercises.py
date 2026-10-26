"""Module 11 exercises: data quality checks.

Run:  python check.py 11

Every check returns a LIST describing what failed (empty list = passed).
"rows" is always a list of dicts.
"""


def check_not_null(rows, column):
    """Return 0-based indexes of rows where `column` is missing, None, or a blank string
    (only spaces counts as blank).

    >>> check_not_null([{"a": 1}, {"a": None}, {}, {"a": "  "}, {"a": 0}], "a")
    [1, 2, 3]
    """
    raise NotImplementedError


def check_unique(rows, column):
    """Return a sorted list of the values of `column` that appear more than once.
    Ignore rows where the value is None.

    >>> check_unique([{"id": 1}, {"id": 2}, {"id": 1}, {"id": None}, {"id": None}], "id")
    [1]
    """
    raise NotImplementedError


def check_in_range(rows, column, min_value, max_value):
    """Return indexes of rows whose value is outside [min_value, max_value] (inclusive)
    or is not a number (int/float). Missing values count as failures too."""
    raise NotImplementedError


def check_allowed_values(rows, column, allowed):
    """Return indexes of rows whose value is not in `allowed`."""
    raise NotImplementedError


def check_foreign_key(rows, column, valid_keys):
    """Return a sorted list of the DISTINCT values in `column` that are not in valid_keys
    (orphans). Example: guest ids in charges that don't exist in the guest master."""
    raise NotImplementedError


def run_checks(rows, checks):
    """Run several checks and build a report.

    `checks` is a list of dicts like:
      {"name": "amount_not_null", "severity": "error", "func": check_not_null, "args": ["amount"]}
      {"name": "outlet_ok", "severity": "warning", "func": check_allowed_values,
       "args": ["outlet", {"Bar", "Spa"}]}

    For each check call func(rows, *args). Return a list of results in the same order:
      {"name": ..., "severity": ..., "passed": <bool>, "failures": <the list the check returned>}
    """
    raise NotImplementedError


def should_stop_pipeline(report):
    """Return True if any FAILED check in the report has severity "error"."""
    raise NotImplementedError
