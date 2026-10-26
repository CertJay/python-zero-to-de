# Module 12: pandas I – DataFrames

**Time:** 8–10 hours · **Prerequisite:** Module 11

## Bakit ko 'to kailangan?

pandas is the most-used Python library in data work. It turns the loops you wrote in Modules 03–06 into one-line operations on whole tables, and it runs them much faster. You'll see it in job descriptions, take-home tests and the DE Zoomcamp.

You did the hard way first on purpose: when `df.groupby("outlet")["amount"].sum()` runs, you now know it's the dictionary accumulator from Module 03, done for you in optimized code.

**At work:** this is Excel with superpowers. Filtering, sorting, pivoting, VLOOKUP-style joins, all repeatable and documented in code instead of a sequence of manual clicks nobody can audit.

---

## 1. Series and DataFrame

```python
import pandas as pd

s = pd.Series([25.0, 120.0, 80.0], name="amount")     # one column
df = pd.DataFrame({
    "guest_id": ["G001", "G001", "G002"],
    "outlet": ["Bar", "Spa", "Bar"],
    "amount": [25.0, 120.0, 40.0],
})                                                      # a table: columns of Series
```

A DataFrame has an **index** (row labels, by default 0, 1, 2...) and **columns**.

---

## 2. Reading and inspecting data

```python
df = pd.read_csv("data/charges_clean.csv")

df.head()            # first 5 rows (df.head(10) for 10)
df.tail(3)
df.shape             # (550, 7)  rows, columns
df.columns           # column names
df.dtypes            # type of each column
df.info()            # columns, non-null counts, types, memory
df.describe()        # count, mean, std, min, quartiles, max of numeric columns
df["outlet"].unique()
df["outlet"].nunique()
df["outlet"].value_counts()
```

**First thing you do with any new dataset:** `shape`, `head()`, `info()`, `describe()`, `value_counts()` on the important text columns. That 5-minute profile catches most surprises.

---

## 3. Selecting columns and rows

```python
df["amount"]                         # one column -> Series
df[["guest_id", "amount"]]           # several columns -> DataFrame (note the double brackets)

df.loc[0]                            # row with index label 0
df.loc[0:4, ["guest_id", "amount"]]  # rows by label, columns by name (inclusive end!)
df.iloc[0:5, 0:2]                    # by position (exclusive end, like Python slicing)
```

### Filtering with boolean masks (you'll do this constantly)

```python
df[df["amount"] > 100]
df[df["outlet"] == "Bar"]
df[(df["outlet"] == "Bar") & (df["amount"] > 30)]      # AND -> &   (parentheses required!)
df[(df["outlet"] == "Bar") | (df["outlet"] == "Cafe")] # OR  -> |
df[~(df["charge_type"] == "refund")]                   # NOT -> ~
df[df["outlet"].isin(["Bar", "Cafe"])]
df[df["amount"].between(50, 200)]
df.query("outlet == 'Bar' and amount > 30")            # string version, handy for exploration
```

Use `&`, `|` and `~`, never `and` / `or` / `not`, with Series. Forgetting the parentheses is the #1 pandas beginner error.

---

## 4. Creating and changing columns

```python
df = df.copy()                                          # work on a copy, keep the original intact
df["amount_with_tax"] = (df["amount"] * 1.12).round(2)  # vectorized: no loop needed
df["is_refund"] = df["charge_type"] == "refund"
df["outlet"] = df["outlet"].str.upper()                 # string methods via .str
df["guest_num"] = df["guest_id"].str[1:].astype(int)    # "G014" -> 14
df = df.rename(columns={"amount": "amount_usd"})
df = df.drop(columns=["currency"])
```

**Vectorized** means the operation runs on the whole column at once in optimized C code. A Python `for` loop over rows is often 100× slower. If you find yourself writing `for i, row in df.iterrows():`, stop and look for a vectorized way.

`.apply()` runs a Python function per value. It's convenient for complex logic, but slower:

```python
df["category"] = df["amount"].apply(charge_category)   # your function from Module 02
```

---

## 5. Sorting

```python
df.sort_values("amount", ascending=False)
df.sort_values(["guest_id", "amount"], ascending=[True, False])
df.reset_index(drop=True)          # renumber rows 0..n-1 after filtering/sorting
```

---

## 6. Basic aggregation

```python
df["amount"].sum(), df["amount"].mean(), df["amount"].max()
df.groupby("outlet")["amount"].sum()
df.groupby("guest_id")["amount"].agg(["count", "sum", "mean"])
```

Module 13 goes deep on groupby, joins and window-style operations.

---

## 7. pandas ↔ SQL (you already know SQL!)

| SQL | pandas |
|---|---|
| `SELECT guest_id, amount FROM t` | `df[["guest_id", "amount"]]` |
| `WHERE amount > 100` | `df[df["amount"] > 100]` |
| `WHERE outlet IN ('Bar','Cafe')` | `df[df["outlet"].isin(["Bar", "Cafe"])]` |
| `ORDER BY amount DESC` | `df.sort_values("amount", ascending=False)` |
| `LIMIT 10` | `df.head(10)` |
| `SELECT DISTINCT outlet` | `df["outlet"].unique()` |
| `COUNT(*)` | `len(df)` |
| `GROUP BY outlet` + `SUM(amount)` | `df.groupby("outlet")["amount"].sum()` |

---

## 8. Writing data

```python
df.to_csv("output/charges_out.csv", index=False)     # index=False: don't write the 0,1,2 column
df.to_json("output/charges.json", orient="records", indent=2)
df.to_excel("output/charges.xlsx", index=False)
df.to_parquet("output/charges.parquet")               # needs: pip install pyarrow
```

---

## Common errors

| Error | Usual cause |
|---|---|
| `KeyError: 'Amount'` | Column name typo or different case. Check `df.columns` |
| `ValueError: The truth value of a Series is ambiguous` | Used `and`/`or` instead of `&`/`|`, or `if df["x"] > 5:` |
| `SettingWithCopyWarning` | Changed a filtered slice. Use `.copy()` after filtering |
| Wrong totals | Column is text, not numeric. Check `df.dtypes` |

---

## Exercises (`exercises.py`)

Work with `data/charges_clean.csv` and small test tables.

1. `load_charges(path)`
2. `profile(df)` – shape, columns, nulls
3. `select_columns(df, columns)`
4. `filter_outlet(df, outlet)`
5. `bar_charges_over(df, min_amount)` – combined conditions
6. `large_charges(df, threshold)` – filter + sort + reset_index
7. `add_amount_with_tax(df, rate)` – new column on a copy
8. `count_by_outlet(df)` – value_counts
9. `total_by_guest(df)` – groupby to a tidy DataFrame
10. `amount_stats(df)` – describe-style numbers
11. `refund_percentage(df)`
12. `to_snake_case_columns(df)` – rename messy headers

## Mini project: voyage dashboard numbers (`voyage_stats.py`, not graded)

From `data/charges_clean.csv`, print: total revenue; revenue per outlet (sorted); top 5 guests by spend; the busiest day by number of charges; average spend per guest. Then save the outlet table to `output/revenue_by_outlet.csv`. Compare how long this took to write versus the same report in Module 06 with pure Python.

## Self-check

1. Why does `df[df["amount"] > 50 and df["outlet"] == "Bar"]` fail?
2. What's the difference between `loc` and `iloc`?
3. Why is `iterrows()` usually a bad idea?

<details><summary>Answers</summary>

1. `and` tries to turn a whole Series into one True/False. Use `&` with parentheses around each condition.
2. `loc` selects by label (index values and column names, inclusive end); `iloc` selects by integer position (exclusive end).
3. It loops row by row in Python, which is far slower than vectorized column operations.
</details>
