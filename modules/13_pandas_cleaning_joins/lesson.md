# Module 13: pandas II – cleaning, groupby, joins, pivots and window functions

**Time:** 10–12 hours · **Prerequisite:** Module 12 (and the SQL window functions lesson)

## Bakit ko 'to kailangan?

This is the "T" in ETL, and it's the core of most take-home assessments for junior DE and analytics roles: *"Here's a messy file. Clean it, join it to this other table, and produce these summaries."*

You'll work on `data/onboard_charges_raw.csv`: mixed date formats, inconsistent outlet names, blank amounts, double-posted rows, and charges for a guest who doesn't exist. Every one of those is a defect you could meet in a real integration.

**At work:** "reconcile POS charges to folios", "find charges with no matching guest", "daily revenue by outlet" are integration and UAT questions you already ask. Now you can answer them yourself in seconds.

---

## 1. Cleaning text columns with `.str`

```python
s = df["outlet"]
s.str.strip()
s.str.lower()
s.str.replace(r"\s+", " ", regex=True)     # collapse inner spaces
s.str.contains("bar", case=False)
s.str.extract(r"(\d+)")                    # regex capture -> new column
s.str.split(" ").str[0]                    # first word
```

Map variants to standard values with a dictionary:

```python
key = df["outlet"].str.strip().str.lower().str.replace(r"\s+", " ", regex=True)
df["outlet"] = key.map(OUTLET_MAP).fillna(key.str.title())   # unknowns: title case
```

---

## 2. Types and missing values

```python
pd.to_numeric(df["amount"], errors="coerce")   # bad values -> NaN instead of crashing
df["charge_id"].astype(int)
df.isna().sum()                                 # nulls per column
df.dropna(subset=["amount"])                    # drop rows missing amount
df["tier"].fillna("Unknown")
```

`errors="coerce"` is your friend: convert what you can, turn the rest into NaN, then **count and quarantine** the NaNs (don't just drop them silently, Module 07).

### Dates with mixed formats

`pd.to_datetime` with a single explicit format, `errors="coerce"`, once per known format, then combine:

```python
FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%b %d %Y"]
parsed = pd.Series(pd.NaT, index=s.index, dtype="datetime64[ns]")
for fmt in FORMATS:
    parsed = parsed.fillna(pd.to_datetime(s.str.strip(), format=fmt, errors="coerce"))
```

Never let pandas *guess* day-first vs month-first on a production feed. Be explicit.

Date parts: `df["charge_date"].dt.day_name()`, `.dt.month`, `.dt.date`, `.dt.strftime("%Y-%m-%d")`.

---

## 3. Duplicates

```python
df.duplicated().sum()                         # fully identical rows
df.duplicated(subset=["charge_id"]).sum()     # same key
df.drop_duplicates()                          # keep the first copy
df.drop_duplicates(subset=["charge_id"], keep="last")
```

Always ask: is this an *exact* duplicate (double-posted, safe to drop) or the *same key with different values* (an update, or a real conflict to investigate)?

---

## 4. groupby: split, apply, combine

```python
df.groupby("outlet")["amount"].sum()

df.groupby(["charge_date", "outlet"], as_index=False).agg(
    total=("amount", "sum"),          # named aggregation: new_name=(column, function)
    charges=("amount", "count"),
    avg=("amount", "mean"),
)
```

Named aggregation gives clean column names. It's the same as:

```sql
SELECT charge_date, outlet, SUM(amount) AS total, COUNT(amount) AS charges, AVG(amount) AS avg
FROM charges GROUP BY charge_date, outlet;
```

Useful aggregations: `sum, count, mean, median, min, max, nunique, first, last`.

---

## 5. Joins with merge

```python
enriched = charges.merge(guests, on="guest_id", how="left", validate="many_to_one")
```

| `how` | Keeps | SQL |
|---|---|---|
| `"inner"` | only matching rows | `INNER JOIN` |
| `"left"` | all left rows, NaN where no match | `LEFT JOIN` |
| `"right"` | all right rows | `RIGHT JOIN` |
| `"outer"` | everything | `FULL OUTER JOIN` |

`validate="many_to_one"` makes pandas **raise an error** if the right table has duplicate keys. Without it, a duplicated guest silently doubles that guest's charges and your revenue is wrong. Use `validate` every time you join in a pipeline.

### Anti-join: rows with no match (orphans)

```python
m = charges.merge(guests[["guest_id"]], on="guest_id", how="left", indicator=True)
orphans = m[m["_merge"] == "left_only"].drop(columns="_merge")
# or simply:
orphans = charges[~charges["guest_id"].isin(guests["guest_id"])]
```

This is a reconciliation check: charges posted to a guest who doesn't exist in the master.

---

## 6. Pivot tables

```python
df.pivot_table(index="charge_date", columns="outlet", values="amount",
               aggfunc="sum", fill_value=0)
```

The Excel pivot table, as one line of code you can re-run tomorrow.

`melt` goes the other way (wide → long), useful when spreadsheets put months in columns.

---

## 7. Window functions in pandas (match these to the SQL lesson)

Sort first, then use `groupby(...).<function>()`, which keeps every row like SQL's `OVER (PARTITION BY ...)`:

```python
df = df.sort_values(["guest_id", "charge_date", "charge_id"])

df["running_balance"] = df.groupby("guest_id")["amount"].cumsum()   # SUM() OVER (PARTITION BY guest ORDER BY date)
df["previous_amount"] = df.groupby("guest_id")["amount"].shift(1)   # LAG(amount)
df["charge_number"] = df.groupby("guest_id").cumcount() + 1         # ROW_NUMBER()
df["guest_total"] = df.groupby("guest_id")["amount"].transform("sum")  # SUM() OVER (PARTITION BY guest)
df["rank"] = df["total"].rank(method="dense", ascending=False)      # DENSE_RANK()
```

`transform` returns a value for *every row* (same length as df); `agg` returns one row per group. That difference is the pandas version of "GROUP BY collapses, OVER keeps rows".

Latest record per key (the ROW_NUMBER = 1 pattern):

```python
latest = df.sort_values(["charge_date", "charge_id"]).drop_duplicates("guest_id", keep="last")
```

---

## 8. Method chaining (readable transformations)

```python
summary = (
    df[df["charge_type"] == "sale"]
    .groupby("outlet", as_index=False)
    .agg(total=("amount", "sum"))
    .sort_values("total", ascending=False)
    .reset_index(drop=True)
)
```

Wrap in parentheses and put one step per line. It reads like the steps of a spec.

---

## Exercises (`exercises.py`)

1. `parse_mixed_dates(series)`
2. `clean_charges(raw)` – the full clean of the raw file
3. `missing_report(df)`
4. `revenue_by_outlet_day(df)` – named aggregation
5. `guest_summary(df)`
6. `enrich_with_guests(charges, guests)` – safe left join
7. `orphan_charges(charges, guests)` – anti-join
8. `pivot_outlet_by_day(df)`
9. `add_running_balance(df)` – cumsum window
10. `add_previous_amount(df)` – shift / LAG
11. `rank_guests(df)` – dense rank
12. `latest_charge_per_guest(df)` – ROW_NUMBER = 1
13. `flag_duplicates(df, subset)`
14. `revenue_by_tier(charges, guests)`

## Mini project: the Excel cleaner (portfolio piece #1)

Make `excel_cleaner.py`: a script with `argparse` (Module 08) that takes `--input` (a CSV or Excel file), applies your cleaning functions, and writes three files: `clean.csv`, `rejected.csv` (rows that couldn't be fixed, with a `reason` column) and `summary.txt` (rows in, rows out, rows rejected by reason, duplicates removed). Test it on `data/onboard_charges_raw.csv`. Put it in its own GitHub repo with a README showing before/after. This is the "Excel Validation Cleaner" project on your portfolio site.

## Self-check

1. What's the difference between `agg` and `transform`?
2. Why use `validate="many_to_one"` in a merge?
3. How do you find charges whose guest is not in the guest table?
4. Why sort before `cumsum` and `shift`?

<details><summary>Answers</summary>

1. `agg` returns one row per group; `transform` returns a value for every original row (same length as the input).
2. It raises an error if the lookup table has duplicate keys, which would otherwise silently multiply rows.
3. An anti-join: `charges[~charges["guest_id"].isin(guests["guest_id"])]`, or a left merge with `indicator=True` keeping `left_only`.
4. Both depend on row order within each group; without sorting, "running" and "previous" are meaningless.
</details>
