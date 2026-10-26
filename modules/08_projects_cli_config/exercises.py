"""Module 08 exercises: argparse, config, project folders.

Run:  python check.py 08
"""
import argparse  # noqa: F401
from pathlib import Path  # noqa: F401


def build_parser():
    """Return an argparse.ArgumentParser with:
      --input       required, string
      --output      default "output/charges.csv"
      --batch-size  int, default 500
      --dry-run     flag (store_true), default False
    """
    raise NotImplementedError


def describe_run(argv):
    """Parse the list `argv` with build_parser() and return a summary string:

      "DRY RUN: would load <input> -> <output> in batches of <batch_size>"   (if --dry-run)
      "LOAD: <input> -> <output> in batches of <batch_size>"                 (otherwise)

    >>> describe_run(["--input", "raw.csv", "--dry-run"])
    'DRY RUN: would load raw.csv -> output/charges.csv in batches of 500'
    """
    raise NotImplementedError


def parse_bool(value, default=False):
    """Convert a config string to bool.
    "1", "true", "yes", "y", "on"  (any case, surrounding spaces ok) -> True
    "0", "false", "no", "n", "off", ""                                -> False
    None -> default
    Anything else -> raise ValueError(f"not a boolean: {value!r}")
    """
    raise NotImplementedError


def load_settings(env):
    """Build typed settings from a dict of environment variables (strings).

    Return a dict:
      "db_url":     env["DB_URL"]  (required: raise KeyError("DB_URL is required") if missing or blank)
      "batch_size": int(env.get("BATCH_SIZE", "500")); must be >= 1 else ValueError("BATCH_SIZE must be >= 1")
      "dry_run":    parse_bool(env.get("DRY_RUN"), default=False)
      "env_name":   env.get("ENV_NAME", "dev").lower(); must be one of dev/uat/prod else
                    ValueError(f"unknown ENV_NAME: {value}")
    """
    raise NotImplementedError


def ensure_project_dirs(root):
    """Create these folders under `root` (if they don't exist) and return them as a dict
    of Path objects:
      "raw" -> root/data/raw
      "processed" -> root/data/processed
      "rejected" -> root/data/rejected
      "logs" -> root/logs
    Calling it twice must not fail.
    """
    raise NotImplementedError


def build_output_path(folder, run_date, name):
    """Return Path(folder) / "<name>_<YYYYMMDD>.csv" where run_date is "YYYY-MM-DD".

    >>> str(build_output_path("out", "2026-10-01", "charges")).replace("\\\\", "/")
    'out/charges_20261001.csv'
    """
    raise NotImplementedError
