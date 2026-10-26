"""Capstone acceptance tests: the "definition of done" for your Onboard Spend Pipeline.

They run your pipeline from the command line, exactly like a scheduler would:
    python -m onboard_pipeline --raw ... --guests ... --db ... --out-dir ...
and then inspect the database and output files.

Your project lives in modules/19_capstone/project/ (or set CAPSTONE_PROJECT to another folder,
e.g. your separate GitHub repo).
"""
import ast
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

from course_tools.loader import DATA

DEFAULT = Path(__file__).parent / "project"
PROJECT = Path(os.environ.get("CAPSTONE_PROJECT", DEFAULT))
SRC = PROJECT / "src"
RAW = DATA / "onboard_charges_raw.csv"
GUESTS = DATA / "guests.csv"

if os.environ.get("PYCOURSE_SOLUTIONS") == "1" and "CAPSTONE_PROJECT" not in os.environ:
    pytest.skip("the capstone has no shipped solution: it's yours", allow_module_level=True)


def run_cli(db, out_dir, raw=RAW):
    env = {**os.environ, "PYTHONPATH": str(SRC)}
    cmd = [sys.executable, "-m", "onboard_pipeline", "--raw", str(raw), "--guests", str(GUESTS),
           "--db", str(db), "--out-dir", str(out_dir)]
    return subprocess.run(cmd, cwd=PROJECT, env=env, capture_output=True, text=True, timeout=120)


@pytest.fixture(scope="module")
def first_run(tmp_path_factory):
    base = tmp_path_factory.mktemp("capstone")
    db, out = base / "onboard.db", base / "out"
    result = run_cli(db, out)
    assert result.returncode == 0, f"pipeline failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr[-3000:]}"
    return {"db": db, "out": out, "base": base}


def query(db, sql):
    conn = sqlite3.connect(db)
    try:
        return conn.execute(sql).fetchall()
    finally:
        conn.close()


# ----------------------------------------------------------------- structure

def test_project_structure():
    for rel in ["README.md", "requirements.txt", "Dockerfile", "src/onboard_pipeline/__init__.py",
                "src/onboard_pipeline/__main__.py", "tests"]:
        assert (PROJECT / rel).exists(), f"missing {rel} in {PROJECT}"
    workflows = list((PROJECT / ".github" / "workflows").glob("*.yml"))
    assert workflows, "add a GitHub Actions workflow in .github/workflows/"


def test_readme_sections():
    text = (PROJECT / "README.md").read_text(encoding="utf-8").lower()
    for heading in ["## architecture", "## how to run", "## data quality", "## design decisions"]:
        assert heading in text, f"README needs a '{heading}' section"
    assert "todo" not in text, "replace every TODO in the README"


def test_you_wrote_unit_tests():
    count = 0
    for f in (PROJECT / "tests").glob("test_*.py"):
        tree = ast.parse(f.read_text(encoding="utf-8"))
        count += sum(1 for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith("test_"))
    assert count >= 10, f"found {count} unit tests in tests/; write at least 10"


# ----------------------------------------------------------------- behaviour

def test_tables_exist(first_run):
    names = {r[0] for r in query(first_run["db"], "SELECT name FROM sqlite_master WHERE type IN ('table','view')")}
    for t in ["charges", "guests", "daily_outlet_revenue", "guest_spend", "pipeline_runs"]:
        assert t in names, f"missing table {t}"


def test_charges_table(first_run):
    db = first_run["db"]
    cols = [r[1] for r in query(db, "PRAGMA table_info(charges)")]
    assert cols[:6] == ["charge_id", "guest_id", "outlet", "charge_date", "amount", "charge_type"]
    total, distinct = query(db, "SELECT COUNT(*), COUNT(DISTINCT charge_id) FROM charges")[0]
    assert total == distinct > 500
    outlets = {r[0] for r in query(db, "SELECT DISTINCT outlet FROM charges")}
    assert outlets == {"Bar", "Restaurant", "Spa", "Boutique", "Excursions", "Cafe"}
    assert query(db, "SELECT COUNT(*) FROM charges WHERE charge_date NOT LIKE '2026-10-__'")[0][0] == 0
    orphans = query(db, "SELECT COUNT(*) FROM charges c LEFT JOIN guests g ON c.guest_id = g.guest_id WHERE g.guest_id IS NULL")
    assert orphans[0][0] == 0, "charges for unknown guests must be quarantined, not loaded"


def test_run_summary_reconciles(first_run):
    s = json.loads((first_run["out"] / "run_summary.json").read_text(encoding="utf-8"))
    for key in ["extracted", "duplicates_removed", "rejected", "loaded", "status"]:
        assert key in s, f"run_summary.json needs '{key}'"
    assert s["status"] == "success"
    assert s["extracted"] == 566
    assert s["extracted"] == s["duplicates_removed"] + s["rejected"] + s["loaded"]
    assert s["loaded"] == query(first_run["db"], "SELECT COUNT(*) FROM charges")[0][0]


def test_rejected_file(first_run):
    import pandas as pd
    rej = pd.read_csv(first_run["out"] / "rejected.csv")
    s = json.loads((first_run["out"] / "run_summary.json").read_text(encoding="utf-8"))
    assert "reason" in rej.columns
    assert len(rej) == s["rejected"]
    assert set(rej["reason"]) <= {"invalid amount", "invalid date", "unknown guest_id"}
    assert (rej["reason"] == "unknown guest_id").sum() == 4


def test_serve_tables_match_charges(first_run):
    db = first_run["db"]
    charges_total = query(db, "SELECT ROUND(SUM(amount), 2) FROM charges")[0][0]
    daily_total = query(db, "SELECT ROUND(SUM(total), 2) FROM daily_outlet_revenue")[0][0]
    assert abs(charges_total - daily_total) < 0.05, "daily_outlet_revenue must add up to the charges table"
    spend_total = query(db, "SELECT ROUND(SUM(total_spend), 2) FROM guest_spend")[0][0]
    assert abs(charges_total - spend_total) < 0.05
    top = query(db, "SELECT guest_id, total_spend, rank FROM guest_spend ORDER BY rank, guest_id LIMIT 1")[0]
    best = query(db, "SELECT guest_id, ROUND(SUM(amount), 2) t FROM charges GROUP BY guest_id ORDER BY t DESC LIMIT 1")[0]
    assert top[2] == 1 and top[0] == best[0]


def test_idempotent_rerun(first_run):
    db, out = first_run["db"], first_run["out"]
    before = {t: query(db, f"SELECT COUNT(*) FROM {t}")[0][0]
              for t in ["charges", "guests", "daily_outlet_revenue", "guest_spend"]}
    runs_before = query(db, "SELECT COUNT(*) FROM pipeline_runs")[0][0]
    result = run_cli(db, out)
    assert result.returncode == 0, result.stderr[-2000:]
    after = {t: query(db, f"SELECT COUNT(*) FROM {t}")[0][0] for t in before}
    assert after == before, f"re-running changed row counts: {before} -> {after}"
    assert query(db, "SELECT COUNT(*) FROM pipeline_runs")[0][0] == runs_before + 1, "log every run in pipeline_runs"


def test_bad_batch_is_refused(tmp_path):
    raw = tmp_path / "bad.csv"
    raw.write_text("charge_id,guest_id,outlet,charge_date,amount,charge_type,currency\n"
                   "1,G001,Bar,2026-10-01,5,sale,USD\n1,G001,Bar,2026-10-01,9,sale,USD\n", encoding="utf-8")
    db = tmp_path / "x.db"
    result = run_cli(db, tmp_path / "out", raw=raw)
    assert "NotImplementedError" not in result.stderr, "the pipeline isn't implemented yet"
    assert result.returncode != 0, "a batch with duplicate charge_ids must fail with a non-zero exit code"
    tables = {r[0] for r in query(db, "SELECT name FROM sqlite_master")} if db.exists() else set()
    if "charges" in tables:
        assert query(db, "SELECT COUNT(*) FROM charges")[0][0] == 0
