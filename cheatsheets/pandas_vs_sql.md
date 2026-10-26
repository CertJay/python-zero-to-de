# pandas ↔ SQL cheat sheet

| Task | SQL | pandas |
|---|---|---|
| Read | `SELECT * FROM charges` | `pd.read_csv(p)` / `pd.read_sql(q, conn)` |
| Columns | `SELECT guest_id, amount` | `df[["guest_id", "amount"]]` |
| Filter | `WHERE amount > 100 AND outlet = 'Bar'` | `df[(df.amount > 100) & (df.outlet == "Bar")]` |
| In list | `WHERE outlet IN ('Bar','Cafe')` | `df[df.outlet.isin(["Bar", "Cafe"])]` |
| Null | `WHERE amount IS NULL` | `df[df.amount.isna()]` |
| Sort | `ORDER BY amount DESC` | `df.sort_values("amount", ascending=False)` |
| Limit | `LIMIT 10` | `df.head(10)` |
| Distinct | `SELECT DISTINCT outlet` | `df.outlet.unique()` / `df.drop_duplicates()` |
| Count rows | `COUNT(*)` | `len(df)` |
| Group | `SELECT outlet, SUM(amount) AS total ... GROUP BY outlet` | `df.groupby("outlet", as_index=False).agg(total=("amount", "sum"))` |
| Having | `HAVING COUNT(*) > 5` | `g[g["n"] > 5]` after agg |
| Inner join | `JOIN guests g USING (guest_id)` | `df.merge(guests, on="guest_id")` |
| Left join | `LEFT JOIN guests ...` | `df.merge(guests, on="guest_id", how="left", validate="many_to_one")` |
| Anti join | `LEFT JOIN ... WHERE g.guest_id IS NULL` | `df[~df.guest_id.isin(guests.guest_id)]` |
| Union all | `UNION ALL` | `pd.concat([a, b], ignore_index=True)` |
| Case when | `CASE WHEN amount < 0 THEN 'refund' ELSE 'sale' END` | `np.where(df.amount < 0, "refund", "sale")` |
| Coalesce | `COALESCE(tier, 'Unknown')` | `df.tier.fillna("Unknown")` |
| Running total | `SUM(amount) OVER (PARTITION BY guest ORDER BY date)` | `df.sort_values([...]).groupby("guest_id").amount.cumsum()` |
| LAG | `LAG(amount) OVER (...)` | `df.groupby("guest_id").amount.shift(1)` |
| ROW_NUMBER | `ROW_NUMBER() OVER (PARTITION BY g ORDER BY d)` | `df.groupby("g").cumcount() + 1` |
| DENSE_RANK | `DENSE_RANK() OVER (ORDER BY total DESC)` | `df.total.rank(method="dense", ascending=False)` |
| Group total on every row | `SUM(amount) OVER (PARTITION BY g)` | `df.groupby("g").amount.transform("sum")` |
| Latest per key | CTE + `ROW_NUMBER() ... = 1` | `df.sort_values(d).drop_duplicates("g", keep="last")` |
| Pivot | `SUM(CASE WHEN outlet='Bar' THEN amount END)` | `df.pivot_table(index="d", columns="outlet", values="amount", aggfunc="sum", fill_value=0)` |
| Write | `INSERT INTO ...` | `df.to_sql("t", conn, if_exists="append", index=False)` |
