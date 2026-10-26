"""Module 06 exercises: files, CSV, JSON, pathlib.

Run:  python check.py 06
Always pass encoding="utf-8" when opening text files, and newline="" for CSV.
"""
import csv  # noqa: F401
import json  # noqa: F401
from pathlib import Path  # noqa: F401


def read_lines(path):
    """Return the file's lines with surrounding whitespace removed, skipping blank lines."""
    raise NotImplementedError


def write_lines(path, lines):
    """Write each string in `lines` on its own line (each ends with "\\n").
    Create the parent folder if it doesn't exist."""
    raise NotImplementedError


def read_csv_rows(path):
    """Read a CSV with a header row and return a list of dicts (values stay strings)."""
    raise NotImplementedError


def write_csv_rows(path, rows, fieldnames):
    """Write a list of dicts to CSV with a header row in `fieldnames` order."""
    raise NotImplementedError


def sum_column(path, column):
    """Sum a numeric column of a CSV, skipping empty cells. Round to 2 decimals.
    Example: amounts "25.5", "", "120" -> 145.5
    """
    raise NotImplementedError


def load_json(path):
    """Read and return the JSON content of the file."""
    raise NotImplementedError


def save_json(path, data):
    """Write `data` as pretty JSON (indent=2, ensure_ascii=False). Create parent folders."""
    raise NotImplementedError


def flatten_guest(guest):
    """Flatten one guest from data/guests.json into:
    {"guest_id", "first_name", "last_name", "nationality", "cabin", "email"}

    Input shape:
    {"guest_id": "G001", "name": {"first": "Ana", "last": "Cruz"}, "nationality": "PH",
     "stay": {"cabin": "A214", ...}, "contact": {"email": "...", "phone": "..."}, ...}

    If "contact" or "email" is missing, use None for email.
    """
    raise NotImplementedError


def guests_json_to_csv(json_path, csv_path):
    """Read guests JSON (a list of guests), flatten each with flatten_guest, write CSV
    with columns in this order: guest_id, first_name, last_name, nationality, cabin, email.
    Return the number of rows written."""
    raise NotImplementedError


def list_files(folder, extension):
    """Return a sorted list of FILE NAMES (not full paths) in `folder` ending with `extension`
    (e.g. ".csv"). Only the top level of the folder."""
    raise NotImplementedError


def append_audit_line(path, timestamp, message):
    """Append one line "<timestamp> | <message>\\n" to the file (create it if missing).
    Existing lines must be kept."""
    raise NotImplementedError


def read_jsonl(path):
    """Read a JSON Lines file (one JSON object per line). Skip blank lines.
    Return a list of dicts."""
    raise NotImplementedError
