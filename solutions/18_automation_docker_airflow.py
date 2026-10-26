"""Reference solutions for Module 18 (Python part). See solutions/18_automation_files/ for
the Dockerfile and DAG."""
from datetime import date, datetime, timedelta


def backoff_delays(attempts, base=1.0, factor=2.0, max_delay=60.0):
    return [float(min(base * factor ** i, max_delay)) for i in range(attempts)]


def daily_cron(hour, minute):
    if not 0 <= hour <= 23 or not 0 <= minute <= 59:
        raise ValueError("hour must be 0-23 and minute 0-59")
    return f"{minute} {hour} * * *"


def is_due(last_run_iso, now_iso, interval_hours):
    if last_run_iso is None:
        return True
    elapsed = datetime.fromisoformat(now_iso) - datetime.fromisoformat(last_run_iso)
    return elapsed >= timedelta(hours=interval_hours)


def backfill_dates(start, end):
    first, last = date.fromisoformat(start), date.fromisoformat(end)
    if last < first:
        raise ValueError("end is before start")
    return [(first + timedelta(days=i)).isoformat() for i in range((last - first).days + 1)]


def backfill_commands(start, end, script="run.py"):
    return [f"python {script} --date {d}" for d in backfill_dates(start, end)]


def should_alert(summary, max_reject_rate=0.05):
    if summary["status"] == "failed":
        return True, "run failed: " + ", ".join(summary["errors"])
    rate = summary["rejected"] / summary["extracted"] if summary["extracted"] else 0
    if rate > max_reject_rate:
        return True, f"reject rate {rate:.1%} above {max_reject_rate:.1%}"
    return False, "ok"
