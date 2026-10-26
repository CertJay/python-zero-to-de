# Python for Data Engineering: zero to hire-ready

A hands-on course that takes you from zero Python to building and explaining a production-style data pipeline. Every lesson starts with **"Bakit ko 'to kailangan?"**: why the topic matters for a data engineering job and for your current work as a Business Analyst.

- **21 modules**, each with a lesson, auto-graded exercises and a mini project
- **~270 automatic tests** that check your code (`python check.py`)
- **Realistic messy data**: onboard charges with 3 date formats, double-posted rows and unknown guests; a school ICT inventory workbook with title rows and "5 pcs" in number columns; supplier invoice PDFs (one with a wrong total); a paginated API
- **3 portfolio projects** built along the way, ending with the **Onboard Spend Pipeline** capstone
- **Interview prep**: 21 coding problems, 30 concept questions, behavioral story bank

All data is synthetic. No real guests, clients or employers.

## Start here

1. Read [`ROADMAP.md`](ROADMAP.md): the week-by-week plan.
2. Open [`modules/00_setup/lesson.md`](modules/00_setup/lesson.md) and follow it. It walks you through installing Python, VS Code and Git, creating the virtual environment, and passing your first test.

Quick version, once Python is installed:

```bash
# Windows
py -m venv .venv
.venv\Scripts\activate
# Mac / Linux
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python data/generate_data.py
python check.py 00
```

## How every module works

```
modules/03_data_structures/
├── lesson.md          read: concepts, examples, the "bakit", common mistakes, self-check
├── exercises.py       write: replace each `raise NotImplementedError` with your code
└── test_exercises.py  don't edit: the automatic checks
```

```bash
python check.py        # progress across all modules
python check.py 03     # check one module, with readable failure messages
python check.py 03 -x  # stop at the first failing exercise
```

## Modules

| # | Module | Portfolio output |
|---|---|---|
| 00 | Set up your workshop | course repo on GitHub |
| 01 | Values, variables, types, operators | |
| 02 | Conditions and loops | |
| 03 | Data structures | |
| 04 | Functions | |
| 05 | Cleaning text and regex | |
| 06 | Files, CSV, JSON, paths | |
| 07 | Errors, validation, logging | |
| 08 | Project structure, CLI, config | your own `my_toolkit` package |
| 09 | Classes and dataclasses | |
| 10 | Generators, collections, dates, decorators | |
| 11 | Testing code and testing data | your own test suite |
| 12 | pandas I | |
| 13 | pandas II: cleaning, joins, windows | **Excel Validation Cleaner** |
| 14 | NumPy essentials | |
| 15 | Extracting from Excel, PDF, APIs | |
| 16 | Databases from Python | **Invoice PDF to Database** |
| 17 | Designing a real ETL pipeline | |
| 18 | Scheduling, Docker, Airflow, CI | |
| 19 | Capstone | **Onboard Spend Pipeline** |
| 20 | Interview preparation | |

## Rules that make this work

1. **Type every line yourself.** No copying from tutorials or AI before you've tried.
2. **Struggle first, then look.** 45 minutes stuck → re-read the lesson → `check.py -x` → then `solutions/`. Rewrite any solution you read from memory the next day.
3. **Return, don't print.** Tests check what your functions return.
4. **Commit after every module.** Your GitHub history is evidence.
5. **If a week slips, protect the Saturday build** and the capstone. Never the other way round.

## Folder map

```
python-zero-to-de/
├── README.md, ROADMAP.md
├── check.py                 grader
├── requirements.txt
├── data/                    practice datasets + generate_data.py
├── modules/00_… 20_…        lessons, exercises, tests
├── solutions/               reference answers (don't peek early)
├── cheatsheets/             quick references
└── course_tools/            grader internals
```
