"""Reference solutions for Module 05."""
import re
import unicodedata

OUTLET_MAP = {
    "bar": "Bar",
    "the bar": "Bar",
    "resto": "Restaurant",
    "restaurant": "Restaurant",
    "spa": "Spa",
    "shore excursions": "Excursions",
    "excursions": "Excursions",
    "cafe": "Cafe",
    "café": "Cafe",
    "boutique": "Boutique",
}

LOG_PATTERN = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) (?P<level>[A-Z]+) "
    r"\[(?P<component>\w+)\] (?P<message>.*)$"
)


def clean_name(name):
    if name is None:
        return None
    collapsed = " ".join(name.split())
    return collapsed.title() if collapsed else None


def normalize_outlet(raw):
    key = " ".join(raw.split()).lower()
    return OUTLET_MAP.get(key, key.title())


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def extract_guest_ids(text):
    return re.findall(r"\bG\d{3}\b", text)


def is_valid_email(email):
    return re.fullmatch(r"[^@\s]+@[^@\s]+\.[A-Za-z]{2,}", email) is not None


def parse_amount(text):
    m = re.search(r"-?\d[\d,]*(?:\.\d+)?", text)
    if not m:
        return None
    return float(m.group().replace(",", ""))


def mask_email(email):
    local, domain = email.split("@", 1)
    if len(local) <= 2:
        masked = local[0] + "*"
    else:
        masked = local[0] + "*" * (len(local) - 2) + local[-1]
    return f"{masked}@{domain}"


def standardize_ph_mobile(phone):
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 12 and digits.startswith("639"):
        digits = digits[2:]
    elif len(digits) == 11 and digits.startswith("09"):
        digits = digits[1:]
    if len(digits) == 10 and digits.startswith("9"):
        return "+63" + digits
    return None


def parse_log_line(line):
    m = LOG_PATTERN.match(line)
    return m.groupdict() if m else None


def count_log_levels(lines):
    counts = {}
    for line in lines:
        parsed = parse_log_line(line)
        if parsed:
            counts[parsed["level"]] = counts.get(parsed["level"], 0) + 1
    return counts


def strip_accents(text):
    return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))
