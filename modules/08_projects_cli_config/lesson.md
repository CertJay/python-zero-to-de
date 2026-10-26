# Module 08: Modules, project structure, command-line tools and config

**Time:** 5–6 hours · **Prerequisite:** Module 07

## Bakit ko 'to kailangan?

So far you've written functions in one file. Real pipelines are projects: several files, a config, secrets that must never be committed, and a command someone (or a scheduler) runs like `python -m pipeline --date 2026-10-01`. Hiring managers open your GitHub and judge the **structure** before they read a single function.

**At work:** environment settings (DEV / UAT / PROD URLs, batch sizes, feature flags) are part of every deployment you document. After this module you'll understand how code picks the right environment, and why "it works in UAT but not PROD" so often turns out to be a config problem.

---

## 1. Modules and imports

Every `.py` file is a **module**. You import what you need:

```python
import json                       # whole module
from pathlib import Path          # one name
from datetime import date, timedelta
import pandas as pd               # alias (convention)
```

Your own files work the same way. With this layout:

```
charges_pipeline/
├── cleaning.py        # def normalize_outlet(...)
└── main.py
```

`main.py` can do `from cleaning import normalize_outlet`.

### `if __name__ == "__main__":`

```python
def main():
    print("running pipeline")

if __name__ == "__main__":
    main()
```

Code under that line runs **only** when you execute the file directly (`python main.py`), not when another file imports it. Every runnable script should have this; otherwise importing it would trigger the whole pipeline.

---

## 2. Packages: folders of modules

A folder with an `__init__.py` file is a **package**:

```
onboard_pipeline/                 # repo root
├── README.md
├── requirements.txt
├── .env.example                  # documents settings, no real secrets
├── .gitignore
├── src/
│   └── onboard_pipeline/
│       ├── __init__.py
│       ├── __main__.py           # lets you run: python -m onboard_pipeline
│       ├── config.py             # reads settings
│       ├── extract.py
│       ├── transform.py
│       ├── load.py
│       └── quality.py
├── tests/
│   ├── test_transform.py
│   └── test_quality.py
└── data/
    ├── raw/
    └── processed/
```

This layout (extract / transform / load / quality / config as separate modules, plus tests) is what your capstone will use. Recruiters recognize it instantly.

Run a package as a program: `python -m onboard_pipeline`. Python runs `__main__.py`.

---

## 3. pip, requirements and virtual environments (deeper)

```bash
pip install pandas==2.2.3        # exact version
pip list                         # what's installed
pip freeze > requirements.txt    # pin everything you have now
pip install -r requirements.txt  # recreate on another machine
```

**Bakit pin versions:** a pipeline that worked in October can break in December because a library released a new version. Pinned requirements make runs reproducible. In interviews, "reproducibility" is a magic word.

---

## 4. Command-line arguments with argparse

Schedulers and colleagues run your pipeline from the terminal with options:

```python
import argparse

def build_parser():
    parser = argparse.ArgumentParser(description="Load onboard charges")
    parser.add_argument("--input", required=True, help="path to the raw CSV")
    parser.add_argument("--output", default="output/charges.csv")
    parser.add_argument("--batch-size", type=int, default=500)
    parser.add_argument("--dry-run", action="store_true", help="validate only, don't load")
    return parser

args = build_parser().parse_args()
args.input, args.batch_size, args.dry_run    # note: --batch-size becomes batch_size
```

```bash
python load_charges.py --input data/raw.csv --dry-run
python load_charges.py --help     # free documentation
```

`parse_args(["--input", "x.csv"])` accepts a list, which is how you test it.

**`--dry-run`** is a habit worth having: run all the checks, change nothing. It's a safe way to test against production data.

---

## 5. Configuration and secrets

Settings that change between environments do **not** belong in code.

### Environment variables

```python
import os
db_url = os.environ.get("DB_URL", "sqlite:///local.db")   # default for local dev
```

Set them:

```bash
# Windows PowerShell
$env:DB_URL = "postgresql://user:pass@host/db"
# Mac / Linux
export DB_URL="postgresql://user:pass@host/db"
```

### .env files with python-dotenv

```
# .env  (NEVER commit this file; it's in .gitignore)
DB_URL=postgresql://miguel:secret@localhost:5432/onboard
BATCH_SIZE=1000
DRY_RUN=false
```

```python
from dotenv import load_dotenv
load_dotenv()                      # copies .env values into os.environ
```

Commit a `.env.example` with fake values so others know which settings exist.

**Everything in environment variables is a string.** `"false"` is a non-empty string, so it's truthy! You must convert explicitly:

```python
dry_run = os.environ.get("DRY_RUN", "false").strip().lower() in ("1", "true", "yes", "y")
batch_size = int(os.environ.get("BATCH_SIZE", "500"))
```

This bug ("I set DRY_RUN=false but it still didn't load!") happens in real teams. You'll write the parser that prevents it.

### Never commit secrets

If a password reaches GitHub, consider it leaked even if you delete it later (it stays in history). Rotate it immediately. Recruiters do notice `.env` files with passwords in portfolio repos, and not in a good way.

---

## 6. Code style tools (set up once)

- **ruff**: finds bugs and style problems, formats code. `pip install ruff` → `ruff check .` and `ruff format .`
- **Type hints + VS Code (Pylance)** catch wrong types as you type.

Clean, consistently formatted code signals professionalism in a portfolio.

---

## Exercises (`exercises.py`)

1. `build_parser()` – argparse with 4 options
2. `describe_run(argv)` – parse a list of args and return a summary string
3. `parse_bool(value)` – the "false" is truthy bug
4. `load_settings(env)` – typed settings from an env dict, with defaults and validation
5. `ensure_project_dirs(root)` – create the standard data folders
6. `build_output_path(folder, run_date, name)` – consistent, date-stamped file names

## Mini project: restructure your earlier work (not graded, but do it, it's portfolio material)

Create `my_toolkit/` inside this repo:

```
my_toolkit/
├── __init__.py
├── text.py       # clean_name, normalize_outlet, slugify (from Module 05)
├── files.py      # read_csv_rows, write_csv_rows, load_json (from Module 06)
├── quality.py    # validate_charge, split_valid_invalid (from Module 07)
└── __main__.py   # argparse: --input, --dry-run; validates a CSV and prints a summary
```

Then run `python -m my_toolkit --input data/onboard_charges_raw.csv --dry-run`. You now own a small reusable library you wrote yourself.

## Self-check

1. What does `if __name__ == "__main__":` prevent?
2. Why is `bool(os.environ["DRY_RUN"])` wrong?
3. What goes in `.env` vs `.env.example`?

<details><summary>Answers</summary>

1. It stops the script's main code from running when the file is imported by another module.
2. Environment values are strings; any non-empty string, including "false", is truthy.
3. `.env` has real values and secrets and is git-ignored; `.env.example` lists the same keys with fake values and is committed.
</details>
