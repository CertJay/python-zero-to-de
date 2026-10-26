from course_tools.loader import DATA, load

ex = load(__file__)


def test_clean_name():
    assert ex.clean_name("  miguel   jay  FAUSTINO ") == "Miguel Jay Faustino"
    assert ex.clean_name("ana") == "Ana"
    assert ex.clean_name("   ") is None
    assert ex.clean_name(None) is None


def test_normalize_outlet():
    assert ex.normalize_outlet("  The   BAR ") == "Bar"
    assert ex.normalize_outlet("bar") == "Bar"
    assert ex.normalize_outlet("Resto") == "Restaurant"
    assert ex.normalize_outlet("Shore Excursions") == "Excursions"
    assert ex.normalize_outlet("Café") == "Cafe"
    assert ex.normalize_outlet("pool   deck") == "Pool Deck"


def test_normalize_outlet_on_real_file():
    import csv
    with open(DATA / "onboard_charges_raw.csv", encoding="utf-8") as f:
        outlets = {ex.normalize_outlet(row["outlet"]) for row in csv.DictReader(f)}
    assert outlets == {"Bar", "Restaurant", "Spa", "Boutique", "Excursions", "Cafe"}


def test_slugify():
    assert ex.slugify("Onboard Spend Report: Oct 2026!") == "onboard-spend-report-oct-2026"
    assert ex.slugify("  --Hello__World--  ") == "hello-world"
    assert ex.slugify("abc") == "abc"


def test_extract_guest_ids():
    assert ex.extract_guest_ids("G001 paid; G045 refunded; G9 and G1234 are invalid") == ["G001", "G045"]
    assert ex.extract_guest_ids("no ids here") == []


def test_is_valid_email():
    for good in ["miguel@example.com", "a.b+tag@mail.co", "x@y.ph"]:
        assert ex.is_valid_email(good) is True, good
    for bad in ["miguel@example", "miguel example.com", "@example.com", "miguel@@example.com", "a b@c.com", ""]:
        assert ex.is_valid_email(bad) is False, bad


def test_parse_amount():
    assert ex.parse_amount("USD 1,250.50") == 1250.5
    assert ex.parse_amount("PHP 300") == 300.0
    assert ex.parse_amount("-45.20 USD") == -45.2
    assert ex.parse_amount("$ 12,000") == 12000.0
    assert ex.parse_amount("n/a") is None
    assert ex.parse_amount("") is None


def test_mask_email():
    assert ex.mask_email("miguel@example.com") == "m****l@example.com"
    assert ex.mask_email("jo@example.com") == "j*@example.com"
    assert ex.mask_email("a@example.com") == "a*@example.com"
    assert ex.mask_email("abc@x.com") == "a*c@x.com"


def test_standardize_ph_mobile():
    for raw in ["0917 123 4567", "+63 917-123-4567", "9171234567", "(0917)1234567", "639171234567"]:
        assert ex.standardize_ph_mobile(raw) == "+639171234567", raw
    for bad in ["12345", "0817 123 4567", "+1 917 123 4567", "", "0917 123 456"]:
        assert ex.standardize_ph_mobile(bad) is None, bad


def test_parse_log_line():
    parsed = ex.parse_log_line("2026-10-01 08:15:02 ERROR [load] Row 15: missing amount")
    assert parsed == {"date": "2026-10-01", "time": "08:15:02", "level": "ERROR",
                      "component": "load", "message": "Row 15: missing amount"}
    assert ex.parse_log_line("not a log line") is None


def test_parse_real_log_file():
    lines = (DATA / "pipeline.log").read_text(encoding="utf-8").splitlines()
    parsed = [ex.parse_log_line(line) for line in lines]
    assert all(p is not None for p in parsed), "every line in data/pipeline.log should parse"


def test_count_log_levels():
    lines = ["2026-10-01 01:00:00 INFO [load] ok", "garbage", "2026-10-01 01:00:01 ERROR [load] bad",
             "2026-10-01 01:00:02 INFO [extract] ok"]
    assert ex.count_log_levels(lines) == {"INFO": 2, "ERROR": 1}
    assert ex.count_log_levels([]) == {}


def test_strip_accents():
    assert ex.strip_accents("Café Dasmariñas") == "Cafe Dasmarinas"
    assert ex.strip_accents("plain") == "plain"
