import argparse
from pathlib import Path

import pytest

from course_tools.loader import load

ex = load(__file__)


def test_build_parser_defaults():
    parser = ex.build_parser()
    assert isinstance(parser, argparse.ArgumentParser)
    args = parser.parse_args(["--input", "raw.csv"])
    assert args.input == "raw.csv"
    assert args.output == "output/charges.csv"
    assert args.batch_size == 500
    assert args.dry_run is False


def test_build_parser_options():
    args = ex.build_parser().parse_args(["--input", "a.csv", "--output", "b.csv", "--batch-size", "50", "--dry-run"])
    assert (args.output, args.batch_size, args.dry_run) == ("b.csv", 50, True)


def test_build_parser_requires_input():
    with pytest.raises(SystemExit):
        ex.build_parser().parse_args([])


def test_describe_run():
    assert ex.describe_run(["--input", "raw.csv", "--dry-run"]) == \
        "DRY RUN: would load raw.csv -> output/charges.csv in batches of 500"
    assert ex.describe_run(["--input", "r.csv", "--output", "o.csv", "--batch-size", "10"]) == \
        "LOAD: r.csv -> o.csv in batches of 10"


def test_parse_bool():
    for v in ["1", "true", "TRUE", " yes ", "Y", "on"]:
        assert ex.parse_bool(v) is True, v
    for v in ["0", "false", "False", "no", "n", "off", ""]:
        assert ex.parse_bool(v) is False, v
    assert ex.parse_bool(None) is False
    assert ex.parse_bool(None, default=True) is True
    with pytest.raises(ValueError):
        ex.parse_bool("maybe")


def test_load_settings():
    s = ex.load_settings({"DB_URL": "sqlite:///x.db", "BATCH_SIZE": "1000", "DRY_RUN": "false", "ENV_NAME": "UAT"})
    assert s == {"db_url": "sqlite:///x.db", "batch_size": 1000, "dry_run": False, "env_name": "uat"}
    s = ex.load_settings({"DB_URL": "sqlite:///x.db"})
    assert s == {"db_url": "sqlite:///x.db", "batch_size": 500, "dry_run": False, "env_name": "dev"}


def test_load_settings_errors():
    with pytest.raises(KeyError):
        ex.load_settings({})
    with pytest.raises(KeyError):
        ex.load_settings({"DB_URL": "  "})
    with pytest.raises(ValueError):
        ex.load_settings({"DB_URL": "x", "BATCH_SIZE": "0"})
    with pytest.raises(ValueError):
        ex.load_settings({"DB_URL": "x", "ENV_NAME": "staging"})
    with pytest.raises(ValueError):
        ex.load_settings({"DB_URL": "x", "DRY_RUN": "perhaps"})


def test_ensure_project_dirs(tmp_path):
    dirs = ex.ensure_project_dirs(tmp_path)
    assert set(dirs) == {"raw", "processed", "rejected", "logs"}
    assert dirs["raw"] == tmp_path / "data" / "raw"
    assert dirs["logs"] == tmp_path / "logs"
    for p in dirs.values():
        assert Path(p).is_dir()
    ex.ensure_project_dirs(tmp_path)  # second call must not fail


def test_build_output_path():
    p = ex.build_output_path("out", "2026-10-01", "charges")
    assert isinstance(p, Path)
    assert p == Path("out") / "charges_20261001.csv"
