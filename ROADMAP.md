# Roadmap: Python for Data Engineering, zero to hire-ready

**Start:** Oct 22, 2026 · **Capstone done:** early March 2027 · **Pace:** 12 hours/week on this course

## The honest math

From zero Python, this course is about 200 hours of real work (reading, coding, failing tests, fixing them, mini projects). At 12 hours a week that's about 19 weeks.

That moves your flagship pipeline from the old Jan 3 target to **early March 2027**. That's the realistic date. Going faster means more hours, not skipping modules: at 15 hours/week you finish around **early February**.

The good news: by mid-January you'll have Python fundamentals, pandas and SQL, which is exactly what the DE Zoomcamp January cohort expects. The Zoomcamp's Docker and orchestration weeks then overlap with Modules 17–18, so the two reinforce each other.

## Your weekly rhythm (same days as before, now with Python at the center)

| Day | Time | What | Bakit |
|---|---|---|---|
| **Mon** | 1.5–2 h | Read the module's lesson, try every example in the REPL | New concepts while you're fresh |
| **Tue** | 1.5 h | SQL practice (DataCamp SQL / DataLemur / your SQL lessons) | SQL is half of every DE interview |
| **Wed** | 2 h | Module exercises: make tests pass | The core practice |
| **Thu** | 1.5 h | Finish exercises, then self-check questions + 1 interview concept question out loud | Explaining is how you find gaps |
| **Fri** | 30–45 min | 5-line learning note (portfolio log) + 1 coding problem from Module 20 (from Week 7) | Proof of consistency |
| **Sat** | 3–4 h | Module mini project, `python check.py`, commit, push | Visible weekly progress |
| **Sun** | 0 | Rest | Burnout kills plans |

**Rule for being stuck:** 45 minutes on one exercise → re-read the lesson section → run `python check.py NN -x` and read the `E` lines → only then open `solutions/`. After reading a solution, close it and rewrite it from memory the next day.

## Week by week

| Wk | Dates | Modules | ~Hours | Milestone (proof you can show) |
|---|---|---|---|---|
| 0 | Oct 22–25 | **00** Setup, start **01** | 4 | `check.py 00` passes; repo pushed to GitHub |
| 1 | Oct 26–Nov 1 | **01** Basics, **02** Control flow | 12 | receipt.py + guess.py |
| 2 | Nov 2–8 | **03** Data structures | 10 | folio.py summary |
| 3 | Nov 9–15 | **04** Functions, start **05** | 12 | cleaner pipeline of functions |
| 4 | Nov 16–22 | **05** Strings & regex, **06** Files | 13 | log_report.py on pipeline.log |
| 5 | Nov 23–29 | **07** Errors & logging, **08** Project structure | 13 | `my_toolkit` package with CLI |
| 6 | Nov 30–Dec 6 | **09** OOP & dataclasses, start **10** | 12 | folios from the real file |
| 7 | Dec 7–13 | **10** Generators & dates, **11** Testing | 13 | 8+ of your own pytest tests; start Module 20 (2 problems/week) |
| 8 | Dec 14–20 | **12** pandas I | 10 | voyage_stats.py |
| 9 | Dec 21–27 | **13** pandas II (holiday week, lighter) | 8 | |
| 10 | Dec 28–Jan 3 | finish **13** | 8 | **Portfolio #1: Excel Validation Cleaner** in its own repo |
| 11 | Jan 4–10 | **14** NumPy, **15** Extraction | 12 | anomaly.py |
| 12 | Jan 11–17 | finish **15**, start **16** | 12 | DE Zoomcamp cohort begins (confirm the date) |
| 13 | Jan 18–24 | **16** Databases | 10 | **Portfolio #2: Invoice PDF to Database** |
| 14 | Jan 25–31 | **17** ETL pipeline | 12 | run.py: idempotent, reconciled run |
| 15 | Feb 1–7 | **18** Docker, Airflow, CI | 12 | pipeline in Docker, tests green on GitHub |
| 16–19 | Feb 8–Mar 7 | **19** Capstone | 10/wk | **Portfolio #3: Onboard Spend Pipeline**, 10/10 acceptance tests |
| 20 | Mar 8–14 | Polish README, record a 3-min walkthrough, update portfolio site and resume | 6 | **Start applying** |

During the Zoomcamp weeks (Jan–Mar), expect 15+ hours/week total. If that's too much, slow this course down rather than dropping the capstone. The capstone matters more than any single Zoomcamp homework.

## Phases

| Phase | Modules | You can say in an interview |
|---|---|---|
| 1. Foundations | 00–07 | "I write clean Python with functions, data structures, file handling, error handling and logging." |
| 2. Engineering habits | 08–11 | "I structure projects as packages with config, CLIs, classes where they fit, generators for big files, and tests." |
| 3. Data libraries | 12–16 | "I clean and join data with pandas, extract from Excel, PDFs and APIs, and load databases safely with parameterized, idempotent SQL." |
| 4. Data engineering | 17–20 | "I've built an end-to-end pipeline with quarantine, data quality gates, idempotent loads, Docker and CI, and I can explain every design decision." |

## Optional DataCamp reinforcement (your scholarship)

Use these **after** the matching module, to reinforce, never instead of the exercises. Course names may change on the platform; search for the closest match.

| Module | DataCamp course |
|---|---|
| 01–02 | Introduction to Python; Intermediate Python |
| 03–04 | Python Toolbox; Introduction to Functions in Python |
| 05 | Regular Expressions in Python |
| 06 | Introduction to Importing Data in Python |
| 07–08 | Introduction to Shell |
| 09 | Object-Oriented Programming in Python |
| 10 | Working with Dates and Times in Python; Writing Efficient Python Code |
| 11 | Introduction to Testing in Python |
| 12–13 | Data Manipulation with pandas; Joining Data with pandas; Cleaning Data in Python |
| 16 | Introduction to Databases in Python |
| 17 | ETL and ELT in Python |
| 18 | Introduction to Docker; Introduction to Airflow in Python |

## How this connects to the rest of your plan

- **Certifications ladder:** HackerRank Python (Basic) fits after Module 04; Problem Solving (Basic) after Module 10; the DataCamp Data Engineer Associate after Module 16. They come almost for free once the skills are there.
- **Portfolio site:** each portfolio piece above replaces a "Planned" card with "Shipped" + a GitHub link.
- **SQL:** keep Tuesdays for SQL every week. Modules 13, 16 and 17 assume you can write joins, CTEs and window functions.
- **Review agent:** paste your `python check.py` output into your weekly check-in.

## Definition of hire-ready

- [ ] `python check.py` shows every module DONE (Module 11 includes your own tests)
- [ ] 3 portfolio repos with READMEs, tests and green CI
- [ ] Capstone passes 10/10 acceptance tests and runs in Docker
- [ ] You can explain your capstone in 3 minutes and answer "why did you do it that way?" for every step
- [ ] You can solve Module 20 problems in under 20 minutes each, talking out loud
- [ ] You've answered the 30 concept questions out loud at least once
