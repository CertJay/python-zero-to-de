import csv
import json

from course_tools.loader import DATA, load

ex = load(__file__)


def test_read_lines(tmp_path):
    p = tmp_path / "in.txt"
    p.write_text("  Bar \n\nSpa\n   \nCafe", encoding="utf-8")
    assert ex.read_lines(p) == ["Bar", "Spa", "Cafe"]


def test_write_lines(tmp_path):
    p = tmp_path / "nested" / "out.txt"
    ex.write_lines(p, ["a", "b"])
    assert p.read_text(encoding="utf-8") == "a\nb\n"


def test_read_csv_rows(tmp_path):
    p = tmp_path / "c.csv"
    p.write_text('guest_id,name,amount\nG001,"Santos, Ana",25.5\nG002,Ben,\n', encoding="utf-8")
    rows = ex.read_csv_rows(p)
    assert rows == [{"guest_id": "G001", "name": "Santos, Ana", "amount": "25.5"},
                    {"guest_id": "G002", "name": "Ben", "amount": ""}]


def test_write_csv_rows(tmp_path):
    p = tmp_path / "w.csv"
    ex.write_csv_rows(p, [{"b": 2, "a": 1}, {"a": 3, "b": 4}], ["a", "b"])
    with open(p, encoding="utf-8", newline="") as f:
        assert list(csv.reader(f)) == [["a", "b"], ["1", "2"], ["3", "4"]]


def test_sum_column(tmp_path):
    p = tmp_path / "s.csv"
    p.write_text("id,amount\n1,25.5\n2,\n3,120\n4,-0.25\n", encoding="utf-8")
    assert ex.sum_column(p, "amount") == 145.25


def test_sum_column_real_file():
    assert ex.sum_column(DATA / "charges_clean.csv", "amount") > 10000


def test_json_round_trip(tmp_path):
    p = tmp_path / "deep" / "x.json"
    data = {"town": "Dasmariñas", "items": [1, 2, None]}
    ex.save_json(p, data)
    assert ex.load_json(p) == data
    assert "Dasmariñas" in p.read_text(encoding="utf-8"), "use ensure_ascii=False"


def test_flatten_guest():
    guest = {"guest_id": "G001", "name": {"first": "Ana", "last": "Cruz"}, "nationality": "PH",
             "loyalty_tier": "Gold", "stay": {"cabin": "A214", "check_in": "2026-10-01"},
             "contact": {"email": "ana@example.com", "phone": "+639171234567"}}
    assert ex.flatten_guest(guest) == {"guest_id": "G001", "first_name": "Ana", "last_name": "Cruz",
                                       "nationality": "PH", "cabin": "A214", "email": "ana@example.com"}
    no_contact = dict(guest)
    del no_contact["contact"]
    assert ex.flatten_guest(no_contact)["email"] is None


def test_guests_json_to_csv(tmp_path):
    out = tmp_path / "guests_flat.csv"
    n = ex.guests_json_to_csv(DATA / "guests.json", out)
    assert n == 60
    with open(out, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["guest_id", "first_name", "last_name", "nationality", "cabin", "email"]
        rows = list(reader)
    assert len(rows) == 60 and rows[0]["guest_id"] == "G001"


def test_list_files(tmp_path):
    for name in ["b.csv", "a.csv", "notes.txt"]:
        (tmp_path / name).write_text("x", encoding="utf-8")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "c.csv").write_text("x", encoding="utf-8")
    assert ex.list_files(tmp_path, ".csv") == ["a.csv", "b.csv"]


def test_append_audit_line(tmp_path):
    p = tmp_path / "audit.log"
    ex.append_audit_line(p, "2026-10-01T08:00", "run started")
    ex.append_audit_line(p, "2026-10-01T08:05", "run finished")
    assert p.read_text(encoding="utf-8") == "2026-10-01T08:00 | run started\n2026-10-01T08:05 | run finished\n"


def test_read_jsonl(tmp_path):
    p = tmp_path / "events.jsonl"
    p.write_text('{"id": 1}\n\n{"id": 2, "ok": true}\n', encoding="utf-8")
    assert ex.read_jsonl(p) == [{"id": 1}, {"id": 2, "ok": True}]
