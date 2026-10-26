# Module 20: Interview preparation

**Time:** ongoing, 2–3 hours a week from Module 10 onward · **Prerequisite:** Module 10 for the coding problems

## Bakit ko 'to kailangan?

Interviews test a specific skill: solving and explaining problems **under time pressure, out loud**. That's different from building projects, so it needs its own practice. Junior DE interviews in the Philippines and for remote roles usually include:

1. **Python coding** (30–45 min): dictionaries, sets, strings, sorting, small algorithms. Rarely hard algorithms.
2. **SQL** (30–45 min): joins, GROUP BY, window functions, CTEs, "find duplicates", "top N per group".
3. **Concepts:** ETL vs ELT, idempotency, data modeling, data quality, batch vs streaming.
4. **Project deep-dive:** "walk me through your pipeline".
5. **Behavioral:** teamwork, conflict, learning, failure.

Your BA background is an advantage in 3, 4 and 5. This module makes sure 1 and 2 don't hold you back.

---

## 1. How to solve a coding problem in an interview

1. **Repeat the problem** in your own words. Ask about edge cases: empty input? duplicates? negative numbers? sorted?
2. **Give a simple solution first**, even if slow. Say its complexity: "This is O(n²) because of the nested loop."
3. **Improve it**, usually with a dict or set: "If I store what I've seen in a set, lookups are O(1), so the whole thing becomes O(n)."
4. **Code it while talking.**
5. **Test it by hand** with a small example and one edge case.

Interviewers grade your thinking and communication as much as the final code. Silence is the enemy.

### Patterns that solve most DE coding questions

| Pattern | Use when | Exercises |
|---|---|---|
| **Hash map (dict) counting** | frequencies, duplicates, "seen before?" | two_sum, top_k_frequent, first_unique_char |
| **Set membership / difference** | reconcile two lists | missing_numbers, diff_records |
| **Sort then scan** | overlaps, grouping, merging | merge_intervals, sessionize |
| **Two pointers** | sorted arrays, merging | merge_sorted |
| **Sliding window** | "longest/shortest substring", rolling metrics | longest_unique_substring, rolling_average |
| **Running state** | best streak, running totals | max_subarray_sum |
| **Recursion** | nested JSON | flatten_json |

Note how many are data problems in disguise: sessionizing events, flattening JSON, keeping the latest record per key, change-data-capture diffs. If you recognize that, say so: *"This is like deduplicating CDC records, keep the latest version per key."*

---

## 2. SQL interview checklist

You must be able to write these without notes:

- [ ] INNER vs LEFT JOIN, and finding rows with no match (`LEFT JOIN ... WHERE right.id IS NULL`)
- [ ] GROUP BY with HAVING
- [ ] Duplicates: `GROUP BY key HAVING COUNT(*) > 1`
- [ ] Top N per group: `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)` in a CTE, filter `rn <= N`
- [ ] Running total: `SUM() OVER (PARTITION BY ... ORDER BY ...)`
- [ ] Previous / next row: `LAG`, `LEAD`
- [ ] RANK vs DENSE_RANK vs ROW_NUMBER
- [ ] Second highest value (`DENSE_RANK() = 2`, or `MAX` below the max)
- [ ] Month-over-month change (`LAG` on a monthly aggregate)
- [ ] CASE WHEN for bucketing
- [ ] COALESCE for nulls; why `NULL = NULL` isn't true
- [ ] UNION vs UNION ALL

Practice platforms: DataLemur (free tier, made for data roles), LeetCode SQL 50, StrataScratch, HackerRank SQL (which also feeds your certification ladder).

---

## 3. Concept questions (answer each in 3–4 sentences, out loud)

**Pipelines**
1. What's the difference between ETL and ELT? When would you choose each?
2. What does idempotent mean? How do you make a load idempotent?
3. What's an incremental load? What's a watermark?
4. What's a backfill and what makes it safe?
5. How do you handle bad rows in a pipeline?
6. Batch vs streaming: give an example of each from hospitality.
7. What happens if your pipeline runs twice at the same time?
8. How do you know your pipeline worked correctly last night?

**Data modeling**
9. What's a fact table and a dimension table? Give examples from onboard charges.
10. What's a star schema? Why is it good for BI tools?
11. What's a slowly changing dimension (Type 1 vs Type 2)? Example: a guest's loyalty tier changes mid-voyage.
12. Normalization vs denormalization: when do you want each?
13. What's the grain of a table? What's the grain of `daily_outlet_revenue`?
14. Primary key vs foreign key vs surrogate key.

**Data quality**
15. Name the data quality dimensions and give a check for each.
16. A dashboard shows revenue doubled overnight. How do you investigate?
17. How would you detect that a source file is missing or late?
18. What's a data contract?

**Storage and tools**
19. Row-oriented vs columnar storage. Why is Parquet popular?
20. Data lake vs data warehouse vs lakehouse.
21. What does an orchestrator like Airflow do that cron doesn't?
22. Why use Docker for pipelines?
23. What's partitioning, and why does it make queries faster?
24. When would you use pandas vs Spark?

**Python**
25. List vs tuple vs set vs dict: when to use each?
26. What's a generator and why does it matter for big files?
27. What's the mutable default argument problem?
28. How do you handle exceptions in a pipeline? What should never be done?
29. What's a virtual environment and why pin versions?
30. How would you test a transformation function?

For each, write your answer in your Friday notes, then say it out loud in under 60 seconds. Use examples from your own projects and your hospitality domain wherever you can. That's what makes answers memorable.

---

## 4. Behavioral questions: use STAR, use your BA experience

**S**ituation → **T**ask → **A**ction → **R**esult (with a number if possible).

Prepare 6 stories from your real work:

| Theme | Where to find your story |
|---|---|
| Data quality problem you found | DepEd inventory consolidation across 45 schools; TESDA record validation |
| Working with difficult stakeholders | discovery workshops, conflicting requirements |
| Learning something fast | teaching yourself LAMP/LEMP and multi-ISP setup; this course |
| A mistake and what you changed | be honest; show the process you added afterwards |
| Translating business needs into technical specs | gap analysis, integration matrices, UAT plans |
| Delivering under pressure | a deadline or go-live you supported |

**"Why data engineering, when you're a BA?"** Have a crisp answer, for example: *"In every role I've had, the work I enjoyed most was making data trustworthy: consolidating, validating, reconciling. As a BA I write the rules for how data should move between systems; I want to be the one who builds and owns that movement. My BA background means I start from the requirement, which helps me build pipelines people actually trust."*

---

## 5. Take-home assignments

Common format: "here's a CSV/API, build a small pipeline, document it, 3–5 days". Win them with:
- A README that explains assumptions and decisions (your BA superpower)
- Tests
- Clear handling of bad data (quarantine + counts)
- Idempotent loading
- A short "what I'd do with more time" section

Your capstone is a rehearsal for exactly this.

---

## Exercises (`exercises.py`): 21 problems

Time yourself: aim for under 20 minutes each. Do each problem twice: once now, once a week later from scratch.

## Self-check

Explain to a non-technical friend (in Taglish is fine) what idempotency is, using a cruise example. If they understand it, you understand it.
