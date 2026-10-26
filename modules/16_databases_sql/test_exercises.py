import sqlite3

import pandas as pd
import pytest

from course_tools.loader import load

ex = load(__file__)


def row(cid, guest, outlet, day, amount, kind="sale"):
    return {"charge_id": cid, "guest_id": guest, "outlet": outlet, "charge_date": day,
            "amount": amount, "charge_type": kind}


ROWS = [
    row(1, "G001", "Bar", "2026-10-01", 25.0),
    row(2, "G001", "Spa", "2026-10-01", 120.0),
    row(3, "G002", "Bar", "2026-10-01", 40.0),
    row(4, "G001", "Restaurant", "2026-10-02", 80.0),
    row(5, "G002", "Restaurant", "2026-10-02", 95.0),
    row(6, "G002", "Bar", "2026-10-03", 30.0),
]


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    yield c
    c.close()


@pytest.fixture
def loaded(conn):
    ex.create_charges_table(conn)
    ex.insert_charges(conn, ROWS)
    return conn


def test_create_charges_table(conn):
    ex.create_charges_table(conn)
    ex.create_charges_table(conn)
    cols = [r[1] for r in conn.execute("PRAGMA table_info(charges)")]
    assert cols == ["charge_id", "guest_id", "outlet", "charge_date", "amount", "charge_type"]
    pk = [r[1] for r in conn.execute("PRAGMA table_info(charges)") if r[5] == 1]
    assert pk == ["charge_id"]


def test_insert_charges(conn):
    ex.create_charges_table(conn)
    assert ex.insert_charges(conn, ROWS) == 6
    assert conn.execute("SELECT COUNT(*) FROM charges").fetchone()[0] == 6
    with pytest.raises(sqlite3.IntegrityError):
        ex.insert_charges(conn, [ROWS[0]])


def test_insert_handles_quotes(conn):
    ex.create_charges_table(conn)
    ex.insert_charges(conn, [row(9, "G'003", "O'Brien's Bar", "2026-10-01", 5.0)])
    assert conn.execute("SELECT outlet FROM charges").fetchone()[0] == "O'Brien's Bar"


def test_guest_total(loaded):
    assert ex.guest_total(loaded, "G001") == 225.0
    assert ex.guest_total(loaded, "G002") == 165.0
    assert ex.guest_total(loaded, "G999") == 0.0
    assert ex.guest_total(loaded, "x' OR '1'='1") == 0.0, "use placeholders, not string formatting"


def test_upsert_is_idempotent(conn):
    ex.create_charges_table(conn)
    ex.upsert_charges(conn, ROWS)
    ex.upsert_charges(conn, ROWS)
    assert conn.execute("SELECT COUNT(*) FROM charges").fetchone()[0] == 6
    changed = [row(2, "G001", "Spa", "2026-10-01", 99.0), row(7, "G003", "Cafe", "2026-10-03", 6.5)]
    assert ex.upsert_charges(conn, changed) == 2
    assert conn.execute("SELECT COUNT(*) FROM charges").fetchone()[0] == 7
    assert conn.execute("SELECT amount FROM charges WHERE charge_id = 2").fetchone()[0] == 99.0


def test_load_all_or_nothing(conn):
    ex.create_charges_table(conn)
    bad_batch = [row(10, "G001", "Bar", "2026-10-04", 5.0), row(11, "G001", "Bar", "2026-10-04", None)]
    assert ex.load_all_or_nothing(conn, bad_batch) == 0
    assert conn.execute("SELECT COUNT(*) FROM charges").fetchone()[0] == 0, "nothing may be saved"
    assert ex.load_all_or_nothing(conn, ROWS) == 6
    assert conn.execute("SELECT COUNT(*) FROM charges").fetchone()[0] == 6


def test_running_balances(loaded):
    assert ex.running_balances(loaded) == [
        ("G001", 1, 25.0), ("G001", 2, 145.0), ("G001", 4, 225.0),
        ("G002", 3, 40.0), ("G002", 5, 135.0), ("G002", 6, 165.0),
    ]


def test_latest_charge_ids(loaded):
    ex.insert_charges(loaded, [row(8, "G001", "Cafe", "2026-10-02", 4.0)])
    assert ex.latest_charge_ids(loaded) == [("G001", 8), ("G002", 6)]


def test_count_rows(loaded):
    assert ex.count_rows(loaded, "charges") == 6
    with pytest.raises(ValueError):
        ex.count_rows(loaded, "charges; DROP TABLE charges")


def test_dataframe_round_trip(conn):
    df = pd.DataFrame(ROWS)
    out = ex.dataframe_round_trip(df, conn, "staging")
    assert len(out) == 6 and list(out.columns) == list(df.columns)
    out2 = ex.dataframe_round_trip(df.head(2), conn, "staging")
    assert len(out2) == 2, "use if_exists='replace'"


def test_revenue_by_outlet_sqlalchemy(tmp_path):
    db = tmp_path / "x.db"
    c = sqlite3.connect(db)
    ex.create_charges_table(c)
    ex.insert_charges(c, ROWS)
    c.close()
    result = ex.revenue_by_outlet_sqlalchemy(f"sqlite:///{db}")
    assert result == {"Restaurant": 175.0, "Spa": 120.0, "Bar": 95.0}
    assert list(result) == ["Restaurant", "Spa", "Bar"]
