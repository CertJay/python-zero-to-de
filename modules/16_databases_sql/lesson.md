# Module 16: Databases from Python (sqlite3, SQLAlchemy, pandas)

**Time:** 8–10 hours · **Prerequisite:** Module 15 and your SQL basics (joins, CTEs, window functions)

## Bakit ko 'to kailangan?

The "L" in ETL usually means **loading into a database or warehouse**. As a data engineer you'll create tables, insert in batches, make loads safe to re-run, and query results back, all from Python. You'll also need to protect the database from the two classic disasters: **SQL injection** and **duplicate loads**.

**At work:** "the interface ran twice and every charge posted twice" is an integration defect you've probably heard about. In this module you'll learn the technique that prevents it (upserts / idempotent loads), and you'll be able to write it into requirements: *"Re-running the load for the same day must not create duplicates."*

---

## 1. SQLite: a real database in one file

SQLite comes with Python. No server, no install. The database is just a file. Perfect for learning and for your portfolio projects. Everything you learn transfers to PostgreSQL (the most common database in DE job posts) with small syntax changes.

```python
import sqlite3

conn = sqlite3.connect("output/onboard.db")      # creates the file if needed
conn = sqlite3.connect(":memory:")               # a temporary in-memory DB (great for tests)

cur = conn.execute("SELECT sqlite_version()")
cur.fetchone()            # ('3.45.1',)
conn.close()
```

DB Browser for SQLite (<https://sqlitebrowser.org/>) lets you open the `.db` file and look inside. Install it.

---

## 2. Creating tables

```python
conn.execute("""
    CREATE TABLE IF NOT EXISTS charges (
        charge_id    INTEGER PRIMARY KEY,
        guest_id     TEXT    NOT NULL,
        outlet       TEXT    NOT NULL,
        charge_date  TEXT    NOT NULL,     -- ISO "YYYY-MM-DD" (SQLite has no DATE type)
        amount       REAL    NOT NULL,
        charge_type  TEXT    NOT NULL DEFAULT 'sale'
    )
""")
conn.commit()
```

Constraints (`PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `CHECK (amount <> 0)`) are your last line of defense: the database itself refuses bad data.

---

## 3. Inserting safely: parameters, never f-strings

```python
# NEVER do this:
conn.execute(f"SELECT * FROM charges WHERE guest_id = '{guest_id}'")
# If guest_id is   x' OR '1'='1   this returns EVERY row. That's SQL injection.

# ALWAYS use placeholders:
conn.execute("SELECT * FROM charges WHERE guest_id = ?", (guest_id,))       # positional
conn.execute("SELECT * FROM charges WHERE guest_id = :gid", {"gid": guest_id})  # named
```

Placeholders send the value separately from the SQL text, so it can never be executed as code. They also handle quotes in names like `O'Brien`.

Placeholders work for **values only**, not table or column names. If a table name comes from input, check it against an allowed list first.

### Batch inserts

```python
rows = [{"charge_id": 1001, "guest_id": "G001", "outlet": "Bar", "charge_date": "2026-10-01",
         "amount": 25.0, "charge_type": "sale"}, ...]

conn.executemany("""
    INSERT INTO charges (charge_id, guest_id, outlet, charge_date, amount, charge_type)
    VALUES (:charge_id, :guest_id, :outlet, :charge_date, :amount, :charge_type)
""", rows)
conn.commit()
```

`executemany` is much faster than looping `execute`.

---

## 4. Transactions: all or nothing

```python
with conn:                         # starts a transaction
    conn.executemany(INSERT_SQL, rows)
# no error  -> COMMIT automatically
# any error -> ROLLBACK automatically: none of the rows are saved
```

**Bakit:** if row 4,999 of 5,000 fails, you don't want 4,998 rows half-loaded. Atomic loads keep the target consistent. "Atomicity" is the A in ACID, a common interview question.

---

## 5. Idempotent loads with UPSERT

A load is **idempotent** if running it twice gives the same result as running it once. This is one of the most important properties of a pipeline, because jobs get re-run all the time (failures, backfills, someone clicking "retry").

```python
conn.executemany("""
    INSERT INTO charges (charge_id, guest_id, outlet, charge_date, amount, charge_type)
    VALUES (:charge_id, :guest_id, :outlet, :charge_date, :amount, :charge_type)
    ON CONFLICT(charge_id) DO UPDATE SET
        guest_id    = excluded.guest_id,
        outlet      = excluded.outlet,
        charge_date = excluded.charge_date,
        amount      = excluded.amount,
        charge_type = excluded.charge_type
""", rows)
```

New charge_id → inserted. Existing charge_id → updated with the new values. Run it 10 times: still one row per charge. (PostgreSQL uses the same `ON CONFLICT` syntax.)

Other idempotent patterns: **delete-then-insert** for a date partition (`DELETE WHERE charge_date = ?` then insert that day), and **MERGE** in warehouses like Snowflake and BigQuery.

---

## 6. Reading results

```python
cur = conn.execute("SELECT guest_id, SUM(amount) FROM charges GROUP BY guest_id")
cur.fetchall()        # list of tuples
cur.fetchone()        # one tuple, or None

conn.row_factory = sqlite3.Row          # rows behave like dicts: row["guest_id"]
```

### Your SQL window functions, run from Python

```python
conn.execute("""
    SELECT guest_id, charge_id,
           ROUND(SUM(amount) OVER (PARTITION BY guest_id ORDER BY charge_date, charge_id), 2)
    FROM charges
""").fetchall()
```

---

## 7. pandas + databases

```python
import pandas as pd

df.to_sql("charges_staging", conn, if_exists="replace", index=False)    # DataFrame -> table
pd.read_sql_query("SELECT * FROM charges WHERE amount > ?", conn, params=(100,))
```

`if_exists`: `"fail"` (default), `"replace"` (drop and recreate), `"append"`. Note that `to_sql` with `append` is **not** idempotent. A common pattern is: load into a *staging* table with `replace`, then upsert from staging into the final table with SQL.

---

## 8. SQLAlchemy: one interface, many databases

```python
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///output/onboard.db")
# engine = create_engine("postgresql+psycopg://user:pass@localhost:5432/onboard")   # same code, different DB

with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM charges WHERE outlet = :o"), {"o": "Bar"})
    result.scalar()

with engine.begin() as conn:            # begin() = transaction, commits at the end
    conn.execute(text("DELETE FROM charges WHERE charge_date = :d"), {"d": "2026-10-01"})

df = pd.read_sql("SELECT * FROM charges", engine)
df.to_sql("charges_copy", engine, if_exists="replace", index=False)
```

The connection string (URL) is the only thing that changes between SQLite in development and PostgreSQL in production. It belongs in config (Module 08), never in code.

### PostgreSQL next step

When you're comfortable, install PostgreSQL locally (or run it in Docker, Module 18) and repeat this module's mini project against it. The DE Zoomcamp's first week does exactly this.

---

## Exercises (`exercises.py`)

1. `create_charges_table(conn)`
2. `insert_charges(conn, rows)` – executemany with named placeholders
3. `guest_total(conn, guest_id)` – parameterized query
4. `upsert_charges(conn, rows)` – idempotent load
5. `load_all_or_nothing(conn, rows)` – transactions
6. `running_balances(conn)` – window function from Python
7. `latest_charge_ids(conn)` – CTE + ROW_NUMBER
8. `count_rows(conn, table)` – safe dynamic table names
9. `dataframe_round_trip(df, conn, table)` – pandas to_sql / read_sql
10. `revenue_by_outlet_sqlalchemy(url)` – SQLAlchemy engine + text()

## Mini project: load the voyage (`load_voyage.py`, not graded)

Read `data/charges_clean.csv` and `data/guests.csv` with pandas, create `charges` and `guests` tables in `output/onboard.db`, upsert all rows, then run and print three SQL queries: revenue by loyalty tier (join), each guest's running balance (window), and the top outlet per day (CTE + RANK). Run the script twice and confirm the row counts don't change. That's idempotency, proven.

## Self-check

1. What's wrong with `f"... WHERE guest_id = '{gid}'"`?
2. What does idempotent mean, and why does it matter for pipelines?
3. What happens to the inserted rows if an error occurs inside `with conn:`?
4. Why is `to_sql(..., if_exists="append")` risky on re-runs?

<details><summary>Answers</summary>

1. It allows SQL injection and breaks on values containing quotes. Use placeholders.
2. Running the job more than once gives the same result as running it once. Jobs are re-run after failures and for backfills, so non-idempotent loads create duplicates.
3. The transaction is rolled back, so none of them are saved.
4. Every re-run appends the same rows again, creating duplicates.
</details>
