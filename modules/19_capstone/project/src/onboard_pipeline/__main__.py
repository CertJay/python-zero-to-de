"""Command-line entry point:  python -m onboard_pipeline --raw ... --guests ... --db ... --out-dir ...

Done for you. Exit code 0 = success, 1 = the run failed (a scheduler uses this to raise an alert).
"""
import argparse
import logging
import sys

from onboard_pipeline.pipeline import run


def build_parser():
    parser = argparse.ArgumentParser(prog="onboard_pipeline", description="Load onboard charges")
    parser.add_argument("--raw", required=True, help="raw charges CSV")
    parser.add_argument("--guests", required=True, help="guest master CSV")
    parser.add_argument("--db", required=True, help="SQLite database path")
    parser.add_argument("--out-dir", required=True, help="folder for rejected.csv and run_summary.json")
    return parser


def main(argv=None):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")
    args = build_parser().parse_args(argv)
    summary = run(args.raw, args.guests, args.db, args.out_dir)
    return 0 if summary.get("status") == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
