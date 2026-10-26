# Module 14: NumPy essentials

**Time:** 3–4 hours · **Prerequisite:** Module 13

## Bakit ko 'to kailangan?

pandas is built on NumPy. Every DataFrame column is a NumPy array underneath. You won't write much raw NumPy as a data engineer, but you need to understand **vectorization** (why column math is fast), **`np.where`** (the most common NumPy call in pandas code), and basic statistics for anomaly checks like "is today's revenue unusually low?".

**At work:** anomaly detection on daily totals ("Bar revenue dropped 80% vs the average, so the POS feed is probably broken") is a monitoring rule you can specify and now build.

---

## 1. Arrays

```python
import numpy as np

a = np.array([25.0, 120.0, 80.0])
a.shape          # (3,)
a.dtype          # float64
a * 1.12         # array([ 28. , 134.4,  89.6])  every element at once
a + a            # element-wise
a > 50           # array([False,  True,  True])  boolean mask
a[a > 50]        # array([120.,  80.])
a.sum(), a.mean(), a.std(), a.min(), a.max()
np.round(a * 1.12, 2)
```

An array holds **one type**, which is why it's fast: no checking each element's type in a loop.

### 2-D arrays

```python
m = np.array([[25, 120], [40, 95]])   # rows = guests, columns = outlets
m.shape                                # (2, 2)
m.sum(axis=0)                          # column totals -> per outlet
m.sum(axis=1)                          # row totals    -> per guest
```

`axis=0` collapses rows (down the columns), `axis=1` collapses columns (across each row).

---

## 2. Vectorization vs loops

```python
amounts = np.random.default_rng(1).uniform(5, 500, 1_000_000)

# loop: slow
total = 0
for x in amounts:
    total += x * 1.12

# vectorized: about 100x faster
total = (amounts * 1.12).sum()
```

Same rule as pandas: whenever you're about to loop over numbers, look for the array operation.

---

## 3. np.where: vectorized if/else

```python
labels = np.where(a < 0, "refund", "sale")
capped = np.where(a > 100, 100, a)
```

In pandas: `df["type"] = np.where(df["amount"] < 0, "refund", "sale")`.

For more than two outcomes, `np.select`:

```python
conditions = [a < 0, a <= 50, a <= 200]
choices = ["refund", "small", "medium"]
np.select(conditions, choices, default="large")
```

---

## 4. Statistics for data checks

```python
np.mean(a), np.median(a), np.std(a)
np.percentile(a, [25, 50, 75])
q1, q3 = np.percentile(a, [25, 75])
iqr = q3 - q1
outliers = (a < q1 - 1.5 * iqr) | (a > q3 + 1.5 * iqr)     # the IQR rule
z = (a - a.mean()) / a.std()                                 # z-scores
```

The IQR rule and z-scores are the two simplest outlier checks. Say "I flag daily totals more than 3 standard deviations from the 30-day mean" in an interview and you sound like someone who has run pipelines in production.

---

## 5. Handy functions

```python
np.arange(0, 10, 2)          # [0, 2, 4, 6, 8]
np.linspace(0, 1, 5)         # 5 evenly spaced values
np.cumsum(a)                 # running total
np.diff(a)                   # day-over-day change
np.convolve(a, np.ones(3) / 3, mode="valid")    # 3-period moving average
np.isnan(x), np.nan          # missing values in float arrays
np.unique(arr, return_counts=True)
rng = np.random.default_rng(42); rng.integers(1, 10, size=5)   # reproducible random numbers
```

---

## Exercises (`exercises.py`)

1. `apply_tax(amounts, rate)`
2. `label_charges(amounts)` – np.where
3. `categorize(amounts)` – np.select
4. `zscores(values)`
5. `iqr_outlier_indexes(values)`
6. `moving_average(values, window)`
7. `day_over_day_change(values)`
8. `outlet_totals(matrix)` – axis sums
9. `percent_of_total(values)`

## Mini project: revenue anomaly alert (`anomaly.py`, not graded)

Compute daily revenue from `data/charges_clean.csv` (pandas groupby), convert to a NumPy array, and flag days whose z-score is below -1.5 or above 1.5. Print "ALERT: 2026-10-07 revenue 1,234.56 is unusually low (z=-1.8)". This is a basic monitoring rule.

## Self-check

1. What does `axis=0` mean in `m.sum(axis=0)`?
2. Why are NumPy operations faster than Python loops?
3. Write the pandas line that labels amounts below 0 as "refund", else "sale".

<details><summary>Answers</summary>

1. Sum down the rows, giving one result per column.
2. Arrays have one fixed type and the loop runs in compiled C code, avoiding per-element Python overhead.
3. `df["type"] = np.where(df["amount"] < 0, "refund", "sale")`
</details>
