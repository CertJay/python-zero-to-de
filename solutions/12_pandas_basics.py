"""Reference solutions for Module 12."""
import re

import pandas as pd


def load_charges(path):
    return pd.read_csv(path)


def profile(df):
    return {
        "rows": len(df),
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "null_counts": {col: int(n) for col, n in df.isna().sum().items()},
    }


def select_columns(df, columns):
    return df[columns]


def filter_outlet(df, outlet):
    return df[df["outlet"] == outlet].reset_index(drop=True)


def bar_charges_over(df, min_amount):
    return df[(df["outlet"] == "Bar") & (df["amount"] > min_amount)].reset_index(drop=True)


def large_charges(df, threshold):
    return df[df["amount"] > threshold].sort_values("amount", ascending=False).reset_index(drop=True)


def add_amount_with_tax(df, rate):
    out = df.copy()
    out["amount_with_tax"] = (out["amount"] * (1 + rate)).round(2)
    return out


def count_by_outlet(df):
    return {k: int(v) for k, v in df["outlet"].value_counts().items()}


def total_by_guest(df):
    out = df.groupby("guest_id", as_index=False)["amount"].sum()
    out = out.rename(columns={"amount": "total"})
    out["total"] = out["total"].round(2)
    return out.sort_values("total", ascending=False).reset_index(drop=True)


def amount_stats(df):
    a = df["amount"]
    return {"count": int(a.count()), "mean": round(float(a.mean()), 2),
            "min": round(float(a.min()), 2), "max": round(float(a.max()), 2)}


def refund_percentage(df):
    if len(df) == 0:
        return 0.0
    return round(float((df["charge_type"] == "refund").mean() * 100), 2)


def to_snake_case_columns(df):
    def snake(name):
        return re.sub(r"[^a-z0-9]+", "_", name.strip().lower()).strip("_")
    return df.rename(columns={c: snake(c) for c in df.columns})
