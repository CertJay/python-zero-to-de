"""Module 14 exercises: NumPy. No Python loops over the values. Use array operations.

Run:  python check.py 14

Inputs may be lists or arrays: convert with np.asarray(values, dtype=float) first.
Return NumPy arrays unless the docstring says otherwise.
"""
import numpy as np  # noqa: F401


def apply_tax(amounts, rate):
    """Return amounts * (1 + rate), rounded to 2 decimals (np.round)."""
    raise NotImplementedError


def label_charges(amounts):
    """Return an array of "refund" where amount < 0, else "sale" (np.where)."""
    raise NotImplementedError


def categorize(amounts):
    """np.select: < 0 -> "refund", == 0 -> "complimentary", <= 50 -> "small",
    <= 200 -> "medium", otherwise "large"."""
    raise NotImplementedError


def zscores(values):
    """Return (value - mean) / std, rounded to 2 decimals. Use the population std
    (np.std default). If std is 0, return an array of zeros."""
    raise NotImplementedError


def iqr_outlier_indexes(values):
    """Return a Python list of the indexes of values below Q1 - 1.5*IQR or above
    Q3 + 1.5*IQR (np.percentile with default settings)."""
    raise NotImplementedError


def moving_average(values, window):
    """Return the moving average for every full window, rounded to 2 decimals.
    moving_average([1, 2, 3, 4], 2) -> array([1.5, 2.5, 3.5])"""
    raise NotImplementedError


def day_over_day_change(values):
    """Return the difference between each value and the previous one (np.diff).
    [100, 120, 90] -> array([20, -30])"""
    raise NotImplementedError


def outlet_totals(matrix):
    """`matrix` rows = guests, columns = outlets. Return a dict with
    "per_outlet": column totals (array) and "per_guest": row totals (array)."""
    raise NotImplementedError


def percent_of_total(values):
    """Each value as a percentage of the sum, rounded to 2 decimals.
    [25, 75] -> array([25., 75.])"""
    raise NotImplementedError
