"""Module 05 exercises: cleaning text and regex.

Run:  python check.py 05
"""
import re  # noqa: F401  (you'll need it)
import unicodedata  # noqa: F401

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


def clean_name(name):
    """Strip outer spaces, collapse inner spaces, title-case.
    Return None if name is None or blank.

    >>> clean_name("  miguel   jay  FAUSTINO ")
    'Miguel Jay Faustino'
    >>> clean_name("   ") is None
    True
    """
    raise NotImplementedError


def normalize_outlet(raw):
    """Map a messy outlet name to its standard name using OUTLET_MAP.
    Steps: collapse whitespace, lowercase, look up. Unknown names -> title case
    of the collapsed text.

    >>> normalize_outlet("  The   BAR ")
    'Bar'
    >>> normalize_outlet("Resto")
    'Restaurant'
    >>> normalize_outlet("pool deck")
    'Pool Deck'
    """
    raise NotImplementedError


def slugify(text):
    """Make a lowercase, file-safe name: keep letters and digits, turn every run
    of other characters into a single "-", and remove "-" at both ends.

    >>> slugify("Onboard Spend Report: Oct 2026!")
    'onboard-spend-report-oct-2026'
    """
    raise NotImplementedError


def extract_guest_ids(text):
    """Return all guest ids (G + exactly 3 digits, as a whole word) in order.

    >>> extract_guest_ids("G001 paid; G045 refunded; G9 and G1234 are invalid")
    ['G001', 'G045']

    Hint: \\b marks a word boundary: r"\\bG\\d{3}\\b"
    """
    raise NotImplementedError


def is_valid_email(email):
    """Simple email check: something@something.something with no spaces.
    Pattern idea: r"[^@\\s]+@[^@\\s]+\\.[A-Za-z]{2,}"  (must match the WHOLE string).

    >>> is_valid_email("miguel@example.com")
    True
    >>> is_valid_email("miguel@example")
    False
    """
    raise NotImplementedError


def parse_amount(text):
    """Extract the number from a money string and return it as a float.
    Handles currency codes/symbols, commas, and negatives. Return None if no number.

    >>> parse_amount("USD 1,250.50")
    1250.5
    >>> parse_amount("PHP 300")
    300.0
    >>> parse_amount("-45.20 USD")
    -45.2
    >>> parse_amount("n/a") is None
    True
    """
    raise NotImplementedError


def mask_email(email):
    """Mask the part before @: keep the first and last character, replace the
    middle with "*" (same length). If that part has 2 characters or fewer,
    keep the first character and add a single "*".

    >>> mask_email("miguel@example.com")
    'm****l@example.com'
    >>> mask_email("jo@example.com")
    'j*@example.com'
    """
    raise NotImplementedError


def standardize_ph_mobile(phone):
    """Convert a PH mobile number to +63XXXXXXXXXX (10 digits after +63, starting with 9).
    Accepts forms like "0917 123 4567", "+63 917-123-4567", "9171234567", "(0917)1234567".
    Return None if it can't be a valid PH mobile number.

    >>> standardize_ph_mobile("0917 123 4567")
    '+639171234567'
    >>> standardize_ph_mobile("12345") is None
    True

    Hint: first keep only digits with re.sub(r"\\D", "", phone), then look at the
    length and the first digits.
    """
    raise NotImplementedError


def parse_log_line(line):
    """Parse a line like
    "2026-10-01 08:15:02 ERROR [load] Row 15: missing amount"
    into a dict with keys: date, time, level, component, message.
    Return None if the line doesn't match the format.

    >>> parse_log_line("2026-10-01 08:15:02 ERROR [load] Row 15: missing amount")["component"]
    'load'
    """
    raise NotImplementedError


def count_log_levels(lines):
    """Count log lines per level using parse_log_line. Skip lines that don't parse.

    >>> count_log_levels(["2026-10-01 01:00:00 INFO [load] ok", "garbage",
    ...                   "2026-10-01 01:00:01 ERROR [load] bad"])
    {'INFO': 1, 'ERROR': 1}
    """
    raise NotImplementedError


def strip_accents(text):
    """Remove accents: "Café Dasmariñas" -> "Cafe Dasmarinas". (See the lesson.)"""
    raise NotImplementedError
