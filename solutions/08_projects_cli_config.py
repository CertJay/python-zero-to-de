"""Reference solutions for Module 08."""
import argparse
from pathlib import Path

TRUE_VALUES = {"1", "true", "yes", "y", "on"}
FALSE_VALUES = {"0", "false", "no", "n", "off", ""}


def build_parser():
    parser = argparse.ArgumentParser(description="Load onboard charges")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="output/charges.csv")
    parser.add_argument("--batch-size", type=int, default=500)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def describe_run(argv):
    args = build_parser().parse_args(argv)
    if args.dry_run:
        return f"DRY RUN: would load {args.input} -> {args.output} in batches of {args.batch_size}"
    return f"LOAD: {args.input} -> {args.output} in batches of {args.batch_size}"


def parse_bool(value, default=False):
    if value is None:
        return default
    v = value.strip().lower()
    if v in TRUE_VALUES:
        return True
    if v in FALSE_VALUES:
        return False
    raise ValueError(f"not a boolean: {value!r}")


def load_settings(env):
    db_url = env.get("DB_URL", "").strip()
    if not db_url:
        raise KeyError("DB_URL is required")
    batch_size = int(env.get("BATCH_SIZE", "500"))
    if batch_size < 1:
        raise ValueError("BATCH_SIZE must be >= 1")
    env_name = env.get("ENV_NAME", "dev").lower()
    if env_name not in ("dev", "uat", "prod"):
        raise ValueError(f"unknown ENV_NAME: {env_name}")
    return {"db_url": db_url, "batch_size": batch_size,
            "dry_run": parse_bool(env.get("DRY_RUN"), default=False), "env_name": env_name}


def ensure_project_dirs(root):
    root = Path(root)
    dirs = {
        "raw": root / "data" / "raw",
        "processed": root / "data" / "processed",
        "rejected": root / "data" / "rejected",
        "logs": root / "logs",
    }
    for p in dirs.values():
        p.mkdir(parents=True, exist_ok=True)
    return dirs


def build_output_path(folder, run_date, name):
    return Path(folder) / f"{name}_{run_date.replace('-', '')}.csv"
