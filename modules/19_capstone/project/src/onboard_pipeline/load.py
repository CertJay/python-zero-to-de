"""L: write to the database safely."""


def create_tables(conn):
    """TODO: CREATE TABLE IF NOT EXISTS charges (...) and pipeline_runs (...)."""
    raise NotImplementedError


def upsert_charges(conn, clean):
    """TODO: INSERT ... ON CONFLICT(charge_id) DO UPDATE ... inside a transaction. Return row count."""
    raise NotImplementedError


def load_guests(conn, guests):
    """TODO: replace the guests table with the current guest master."""
    raise NotImplementedError


def record_run(conn, started_at, summary):
    """TODO: insert one row into pipeline_runs."""
    raise NotImplementedError
