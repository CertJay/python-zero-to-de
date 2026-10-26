"""TODO: write an Airflow DAG for the onboard charges pipeline (see lesson.md section 5).

You don't need Airflow installed: the tests only read this file. It must:
  - be valid Python
  - define a DAG (with the @dag decorator or `with DAG(...)`)
  - set a schedule (cron string), catchup=False, a start_date, and retries in default_args
  - define three tasks named extract, transform and load
  - chain them: extract -> transform -> load
    (TaskFlow: load(transform(extract()))   or   classic: extract_task >> transform_task >> load_task)
"""
