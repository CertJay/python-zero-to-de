"""Reference solutions for Module 11."""


def _is_blank(value):
    return value is None or (isinstance(value, str) and not value.strip())


def check_not_null(rows, column):
    return [i for i, row in enumerate(rows) if _is_blank(row.get(column))]


def check_unique(rows, column):
    seen, dupes = set(), set()
    for row in rows:
        value = row.get(column)
        if value is None:
            continue
        if value in seen:
            dupes.add(value)
        seen.add(value)
    return sorted(dupes)


def check_in_range(rows, column, min_value, max_value):
    failures = []
    for i, row in enumerate(rows):
        value = row.get(column)
        is_number = isinstance(value, (int, float)) and not isinstance(value, bool)
        if not is_number or not (min_value <= value <= max_value):
            failures.append(i)
    return failures


def check_allowed_values(rows, column, allowed):
    return [i for i, row in enumerate(rows) if row.get(column) not in allowed]


def check_foreign_key(rows, column, valid_keys):
    return sorted({row.get(column) for row in rows} - set(valid_keys))


def run_checks(rows, checks):
    report = []
    for check in checks:
        failures = check["func"](rows, *check.get("args", []))
        report.append({"name": check["name"], "severity": check["severity"],
                       "passed": not failures, "failures": failures})
    return report


def should_stop_pipeline(report):
    return any(r["severity"] == "error" and not r["passed"] for r in report)
