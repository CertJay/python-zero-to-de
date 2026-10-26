"""Orchestration: runs every step in order and reports what happened."""
import logging

log = logging.getLogger("onboard_pipeline")


def run(raw_path, guests_path, db_path, out_dir):
    """TODO: extract -> dedupe -> transform -> write rejected.csv -> quality checks ->
    (stop on errors) -> upsert charges + load guests -> build serve tables ->
    record the run in pipeline_runs -> write run_summary.json -> log a summary line.

    Return the summary dict:
    {"extracted", "duplicates_removed", "rejected", "loaded", "status", "errors"}
    """
    raise NotImplementedError
