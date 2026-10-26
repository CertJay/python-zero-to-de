"""Course grader.

    python check.py            -> progress across every module
    python check.py 03         -> run module 03's tests and show what passed/failed
    python check.py 03 -x      -> stop at the first failing exercise (good when stuck)

You never need to edit this file.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODULES = ROOT / "modules"
BAR_WIDTH = 24


def find_modules():
    return sorted(p for p in MODULES.iterdir() if p.is_dir() and re.match(r"^\d{2}_", p.name))


def find_module(code):
    code = code.zfill(2)
    for m in find_modules():
        if m.name.startswith(code + "_"):
            return m
    return None


def run_pytest(paths, extra, capture):
    env = dict(os.environ)
    if "--solutions" in sys.argv:
        env["PYCOURSE_SOLUTIONS"] = "1"
    cmd = [sys.executable, "-m", "pytest", *[str(p) for p in paths], *extra]
    return subprocess.run(cmd, cwd=ROOT, env=env, capture_output=capture, text=True)


def parse_counts(output):
    counts = {"passed": 0, "failed": 0, "error": 0, "skipped": 0}
    tail = output.strip().splitlines()[-1] if output.strip() else ""
    for number, word in re.findall(r"(\d+) (passed|failed|errors?|skipped)", tail):
        key = "error" if word.startswith("error") else word
        counts[key] += int(number)
    return counts


def bar(done, total):
    if total == 0:
        return "." * BAR_WIDTH
    filled = round(BAR_WIDTH * done / total)
    return "#" * filled + "." * (BAR_WIDTH - filled)


def overall():
    print("\nPython for Data Engineering: progress\n")
    grand_done = grand_total = 0
    for m in find_modules():
        tests = sorted(m.glob("test_*.py"))
        if not tests:
            continue
        result = run_pytest(tests, ["-q", "--tb=no", "--no-header"], capture=True)
        c = parse_counts(result.stdout)
        total = c["passed"] + c["failed"] + c["error"]
        grand_done += c["passed"]
        grand_total += total
        status = "DONE" if total and c["passed"] == total else ""
        print(f"  {m.name:<34} [{bar(c['passed'], total)}] {c['passed']:>3}/{total:<3} {status}")
    pct = 100 * grand_done / grand_total if grand_total else 0
    print(f"\n  Total: {grand_done}/{grand_total} exercises passing ({pct:.0f}%)")
    print("  Next: run  python check.py <module number>  to work on a module.\n")


def show_details(output, limit=3):
    """Print the first few failures in a readable way."""
    section = output.split("= FAILURES =", 1)[-1] if "= FAILURES =" in output else output
    if "= ERRORS =" in output and "= FAILURES =" not in output:
        section = output.split("= ERRORS =", 1)[-1]
    blocks = re.split(r"\n_{3,} (.+?) _{3,}\n", "\n" + section)
    # blocks = [junk, name1, body1, name2, body2, ...]
    pairs = list(zip(blocks[1::2], blocks[2::2]))
    not_written = [name for name, body in pairs if "NotImplementedError" in body]
    real = [(name, body) for name, body in pairs if "NotImplementedError" not in body]
    if not_written:
        print(f"\n  Not written yet ({len(not_written)}): " + ", ".join(n.replace('test_', '') for n in not_written))
        print("  -> open exercises.py and replace `raise NotImplementedError` with your code.")
    for name, body in real[:limit]:
        print(f"\n--- {name.replace('test_', '')} ---")
        lines = [l for l in body.splitlines() if l.strip() and not l.startswith("=")]
        for line in lines[-14:]:
            print("   " + line)
    if len(real) > limit:
        print(f"\n  ...and {len(real) - limit} more. Fix these first, then run again.")
    if real:
        print("\n  How to read this: lines starting with 'E' tell you what went wrong.")
        print("  'assert X == Y' means your function returned X but the test expected Y.")
        print("  In a diff, '-' lines are what the test expected, '+' lines are what you returned.")


def single(code, stop_first):
    m = find_module(code)
    if m is None:
        print(f"No module starting with {code}. Run  python check.py  to see the list.")
        return 1
    tests = sorted(m.glob("test_*.py"))
    if not tests:
        print(f"{m.name} has no automatic tests. Follow the checklist in its lesson.md.")
        return 0
    print(f"\nChecking {m.name} ...\n")
    extra = ["-v", "--tb=short", "--no-header", "-rN"]
    if stop_first:
        extra.append("-x")
    result = run_pytest(tests, extra, capture=True)
    lines = result.stdout.splitlines()
    for line in lines:
        if "PASSED" in line:
            print("  PASS  " + line.split("::")[-1].split(" ")[0])
        elif "::" in line and ("FAILED" in line or "ERROR" in line):
            print("  FAIL  " + line.split("::")[-1].split(" ")[0])
    c = parse_counts(result.stdout)
    total = c["passed"] + c["failed"] + c["error"]
    if c["failed"] or c["error"]:
        show_details(result.stdout)
    print(f"\n  {m.name}: [{bar(c['passed'], total)}] {c['passed']}/{total} passing")
    if total == 0:
        print("  No graded tests ran for this module (skipped).\n")
    elif c["passed"] == total:
        print("  Module complete. Do the mini project in lesson.md, then commit and push to GitHub.\n")
    else:
        print("  Keep going. Fix one failing exercise at a time, then run this again.\n")
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if args:
        sys.exit(single(args[0], "-x" in sys.argv))
    overall()
