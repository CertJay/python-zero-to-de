import ast
import os
from pathlib import Path

import pytest

from course_tools.loader import ROOT, load

ex = load(__file__)
FILES = ROOT / "solutions" / "18_automation_files" if os.environ.get("PYCOURSE_SOLUTIONS") == "1" else Path(__file__).parent


def test_backoff_delays():
    assert ex.backoff_delays(5) == [1.0, 2.0, 4.0, 8.0, 16.0]
    assert ex.backoff_delays(4, base=10, max_delay=30) == [10.0, 20.0, 30.0, 30.0]
    assert ex.backoff_delays(0) == []
    assert ex.backoff_delays(3, base=2, factor=3) == [2.0, 6.0, 18.0]


def test_daily_cron():
    assert ex.daily_cron(2, 30) == "30 2 * * *"
    assert ex.daily_cron(0, 0) == "0 0 * * *"
    for bad in [(24, 0), (-1, 0), (5, 60)]:
        with pytest.raises(ValueError):
            ex.daily_cron(*bad)


def test_is_due():
    assert ex.is_due(None, "2026-10-01T00:00:00", 24) is True
    assert ex.is_due("2026-10-01T02:30:00", "2026-10-02T02:29:59", 24) is False
    assert ex.is_due("2026-10-01T02:30:00", "2026-10-02T02:30:00", 24) is True
    assert ex.is_due("2026-10-01T00:00:00", "2026-10-01T00:16:00", 0.25) is True


def test_backfill_dates():
    assert ex.backfill_dates("2026-10-30", "2026-11-01") == ["2026-10-30", "2026-10-31", "2026-11-01"]
    assert ex.backfill_dates("2026-10-05", "2026-10-05") == ["2026-10-05"]
    with pytest.raises(ValueError):
        ex.backfill_dates("2026-10-05", "2026-10-01")


def test_backfill_commands():
    assert ex.backfill_commands("2026-10-03", "2026-10-04") == [
        "python run.py --date 2026-10-03", "python run.py --date 2026-10-04"]
    assert ex.backfill_commands("2026-10-03", "2026-10-03", "pipeline.py") == ["python pipeline.py --date 2026-10-03"]


def test_should_alert():
    ok = {"extracted": 100, "rejected": 3, "status": "success", "errors": []}
    assert ex.should_alert(ok) == (False, "ok")
    high = {"extracted": 80, "rejected": 10, "status": "success", "errors": []}
    assert ex.should_alert(high) == (True, "reject rate 12.5% above 5.0%")
    failed = {"extracted": 10, "rejected": 0, "status": "failed", "errors": ["duplicate_charge_id", "no_rows"]}
    assert ex.should_alert(failed) == (True, "run failed: duplicate_charge_id, no_rows")
    empty = {"extracted": 0, "rejected": 0, "status": "success", "errors": []}
    assert ex.should_alert(empty) == (False, "ok")


def _dockerfile_lines():
    text = (FILES / "Dockerfile").read_text(encoding="utf-8")
    return [l.strip() for l in text.splitlines() if l.strip() and not l.strip().startswith("#")]


def test_dockerfile():
    lines = _dockerfile_lines()
    assert lines, "Dockerfile is empty: complete the TODOs"
    upper = [l.upper() for l in lines]
    assert upper[0].startswith("FROM PYTHON:3"), "start FROM an official python:3.x image"
    assert any(l.startswith("WORKDIR /APP") for l in upper), "set WORKDIR /app"
    req = next((i for i, l in enumerate(lines) if l.startswith("COPY") and "requirements.txt" in l), None)
    assert req is not None, "COPY requirements.txt"
    pip = next((i for i, l in enumerate(lines) if l.startswith("RUN") and "pip install" in l), None)
    assert pip is not None and pip > req, "RUN pip install after copying requirements.txt"
    assert "--no-cache-dir" in lines[pip] and "-r requirements.txt" in lines[pip]
    code = next((i for i, l in enumerate(lines) if l.startswith("COPY") and "requirements.txt" not in l), None)
    assert code is not None and code > pip, "COPY the rest of the code AFTER installing requirements"
    assert lines[-1].startswith("CMD [") or any(l.startswith("CMD [") for l in lines), "use JSON-form CMD"


def test_airflow_dag_file():
    source = (FILES / "onboard_charges_dag.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    names = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    task_ids = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.keyword) and node.arg == "task_id" and isinstance(node.value, ast.Constant):
            task_ids.add(node.value.value)
    tasks = names | task_ids
    for t in ("extract", "transform", "load"):
        assert t in tasks, f"define a task named {t}"
    assert "DAG" in source or "@dag" in source, "define a DAG"
    assert "schedule" in source, "set a schedule"
    assert "catchup=False" in source.replace(" ", ""), "set catchup=False"
    assert "start_date" in source, "set a start_date"
    assert "retries" in source, "set retries in default_args"
    compact = source.replace(" ", "")
    chained = "load(transform(extract(" in compact or (">>" in source and "extract" in source)
    assert chained, "chain the tasks: extract -> transform -> load"
