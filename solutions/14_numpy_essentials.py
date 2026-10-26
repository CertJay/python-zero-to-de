"""Reference solutions for Module 14."""
import numpy as np


def apply_tax(amounts, rate):
    return np.round(np.asarray(amounts, dtype=float) * (1 + rate), 2)


def label_charges(amounts):
    return np.where(np.asarray(amounts, dtype=float) < 0, "refund", "sale")


def categorize(amounts):
    a = np.asarray(amounts, dtype=float)
    conditions = [a < 0, a == 0, a <= 50, a <= 200]
    choices = ["refund", "complimentary", "small", "medium"]
    return np.select(conditions, choices, default="large")


def zscores(values):
    a = np.asarray(values, dtype=float)
    std = a.std()
    if std == 0:
        return np.zeros_like(a)
    return np.round((a - a.mean()) / std, 2)


def iqr_outlier_indexes(values):
    a = np.asarray(values, dtype=float)
    q1, q3 = np.percentile(a, [25, 75])
    iqr = q3 - q1
    mask = (a < q1 - 1.5 * iqr) | (a > q3 + 1.5 * iqr)
    return np.flatnonzero(mask).tolist()


def moving_average(values, window):
    a = np.asarray(values, dtype=float)
    return np.round(np.convolve(a, np.ones(window) / window, mode="valid"), 2)


def day_over_day_change(values):
    return np.diff(np.asarray(values))


def outlet_totals(matrix):
    m = np.asarray(matrix)
    return {"per_outlet": m.sum(axis=0), "per_guest": m.sum(axis=1)}


def percent_of_total(values):
    a = np.asarray(values, dtype=float)
    return np.round(a / a.sum() * 100, 2)
