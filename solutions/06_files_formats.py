"""Reference solutions for Module 06."""
import csv
import json
from pathlib import Path


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def write_lines(path, lines):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


def read_csv_rows(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv_rows(path, rows, fieldnames):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def sum_column(path, column):
    total = 0.0
    for row in read_csv_rows(path):
        value = row[column].strip()
        if value:
            total += float(value)
    return round(total, 2)


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def flatten_guest(guest):
    return {
        "guest_id": guest["guest_id"],
        "first_name": guest["name"]["first"],
        "last_name": guest["name"]["last"],
        "nationality": guest.get("nationality"),
        "cabin": guest.get("stay", {}).get("cabin"),
        "email": guest.get("contact", {}).get("email"),
    }


def guests_json_to_csv(json_path, csv_path):
    rows = [flatten_guest(g) for g in load_json(json_path)]
    fields = ["guest_id", "first_name", "last_name", "nationality", "cabin", "email"]
    write_csv_rows(csv_path, rows, fields)
    return len(rows)


def list_files(folder, extension):
    return sorted(p.name for p in Path(folder).iterdir() if p.is_file() and p.suffix == extension)


def append_audit_line(path, timestamp, message):
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | {message}\n")


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]
