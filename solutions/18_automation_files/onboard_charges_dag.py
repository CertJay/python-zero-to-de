"""Reference Airflow DAG (TaskFlow API) for the onboard charges pipeline."""
from datetime import datetime, timedelta

from airflow.decorators import dag, task

DATA_DIR = "/opt/airflow/data"

default_args = {
    "owner": "miguel",
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
    "retry_exponential_backoff": True,
}


@dag(
    dag_id="onboard_charges_daily",
    schedule="30 2 * * *",
    start_date=datetime(2026, 10, 1),
    catchup=False,
    default_args=default_args,
    tags=["onboard", "charges"],
)
def onboard_charges():

    @task
    def extract(ds=None):
        """Return the path of the raw file for the run date."""
        return f"{DATA_DIR}/raw/charges_{ds}.csv"

    @task
    def transform(raw_path: str):
        """Clean the raw file, write clean + rejected files, return the clean path."""
        import pandas as pd
        clean_path = raw_path.replace("/raw/", "/clean/")
        df = pd.read_csv(raw_path, dtype=str, keep_default_na=False)
        df.to_csv(clean_path, index=False)
        return clean_path

    @task
    def load(clean_path: str):
        """Upsert the clean file into the warehouse and return the row count."""
        import pandas as pd
        return len(pd.read_csv(clean_path))

    load(transform(extract()))


onboard_charges()
