"""Reference solutions for Module 13."""
import pandas as pd

DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%b %d %Y"]

OUTLET_MAP = {
    "bar": "Bar", "the bar": "Bar", "resto": "Restaurant", "restaurant": "Restaurant",
    "spa": "Spa", "shore excursions": "Excursions", "excursions": "Excursions",
    "cafe": "Cafe", "café": "Cafe", "boutique": "Boutique",
}


def parse_mixed_dates(series):
    text = series.astype("string").str.strip()
    parsed = pd.Series(pd.NaT, index=series.index, dtype="datetime64[ns]")
    for fmt in DATE_FORMATS:
        parsed = parsed.fillna(pd.to_datetime(text, format=fmt, errors="coerce"))
    return parsed


def clean_charges(raw):
    df = raw.drop_duplicates().copy()
    key = df["outlet"].astype("string").str.strip().str.lower().str.replace(r"\s+", " ", regex=True)
    df["outlet"] = key.map(OUTLET_MAP).fillna(key.str.title()).astype(str)
    df["charge_date"] = parse_mixed_dates(df["charge_date"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount", "charge_date"])
    return df.sort_values(["charge_date", "charge_id"]).reset_index(drop=True)


def missing_report(df):
    counts = df.isna().sum()
    return {col: int(n) for col, n in counts.items() if n > 0}


def revenue_by_outlet_day(df):
    out = df.groupby(["charge_date", "outlet"], as_index=False).agg(
        total=("amount", "sum"), charges=("amount", "count"))
    out["total"] = out["total"].round(2)
    return out.sort_values(["charge_date", "outlet"]).reset_index(drop=True)


def guest_summary(df):
    out = df.groupby("guest_id", as_index=False).agg(
        total_spend=("amount", "sum"),
        n_charges=("amount", "count"),
        avg_charge=("amount", "mean"),
        first_charge=("charge_date", "min"),
        last_charge=("charge_date", "max"),
    )
    out["total_spend"] = out["total_spend"].round(2)
    out["avg_charge"] = out["avg_charge"].round(2)
    return out.sort_values("total_spend", ascending=False).reset_index(drop=True)


def enrich_with_guests(charges, guests):
    lookup = guests[["guest_id", "loyalty_tier", "nationality"]]
    return charges.merge(lookup, on="guest_id", how="left", validate="many_to_one")


def orphan_charges(charges, guests):
    return charges[~charges["guest_id"].isin(guests["guest_id"])].reset_index(drop=True)


def pivot_outlet_by_day(df):
    return df.pivot_table(index="charge_date", columns="outlet", values="amount",
                          aggfunc="sum", fill_value=0).round(2)


def _sorted(df):
    return df.sort_values(["guest_id", "charge_date", "charge_id"]).reset_index(drop=True)


def add_running_balance(df):
    out = _sorted(df)
    out["running_balance"] = out.groupby("guest_id")["amount"].cumsum().round(2)
    return out


def add_previous_amount(df):
    out = _sorted(df)
    out["previous_amount"] = out.groupby("guest_id")["amount"].shift(1)
    return out


def rank_guests(df):
    out = df.groupby("guest_id", as_index=False)["amount"].sum().rename(columns={"amount": "total_spend"})
    out["total_spend"] = out["total_spend"].round(2)
    out["rank"] = out["total_spend"].rank(method="dense", ascending=False).astype(int)
    return out.sort_values(["rank", "guest_id"]).reset_index(drop=True)


def latest_charge_per_guest(df):
    return (df.sort_values(["charge_date", "charge_id"])
              .drop_duplicates("guest_id", keep="last")
              .sort_values("guest_id")
              .reset_index(drop=True))


def flag_duplicates(df, subset):
    out = df.copy()
    out["is_duplicate"] = out.duplicated(subset=subset, keep="first")
    return out


def revenue_by_tier(charges, guests):
    merged = charges.merge(guests[["guest_id", "loyalty_tier"]], on="guest_id", how="inner")
    totals = merged.groupby("loyalty_tier")["amount"].sum().round(2).sort_values(ascending=False)
    return {tier: float(v) for tier, v in totals.items()}
