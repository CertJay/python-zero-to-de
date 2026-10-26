"""Module 09 exercises: classes and dataclasses.

Run:  python check.py 09

The class skeletons are here. Replace each `raise NotImplementedError`.
"""
import csv  # noqa: F401
from dataclasses import dataclass, field  # noqa: F401


@dataclass
class Charge:
    """One charge. (The fields are done for you.)"""
    charge_id: int
    guest_id: str
    outlet: str
    amount: float
    charge_type: str = "sale"

    @property
    def is_refund(self):
        """True if charge_type is "refund"."""
        raise NotImplementedError

    @classmethod
    def from_dict(cls, row):
        """Build a Charge from a CSV-style dict where every value is a string.
        Convert charge_id to int and amount to float. charge_type is optional
        (default "sale"); strip whitespace from guest_id and outlet.

        >>> Charge.from_dict({"charge_id": "1001", "guest_id": " G001", "outlet": "Bar ", "amount": "25.5"})
        Charge(charge_id=1001, guest_id='G001', outlet='Bar', amount=25.5, charge_type='sale')
        """
        raise NotImplementedError


class Folio:
    """A guest's account of charges."""

    def __init__(self, guest_id):
        """Store guest_id and start with an empty list of charges (self.charges)."""
        raise NotImplementedError

    def add(self, charge):
        """Add a Charge. Raise ValueError("charge belongs to <other guest_id>") if the
        charge's guest_id doesn't match this folio. Return self (so calls can chain)."""
        raise NotImplementedError

    @property
    def balance(self):
        """Sum of all charge amounts, rounded to 2 decimals (0 when empty)."""
        raise NotImplementedError

    def total_by_outlet(self):
        """Dict outlet -> total amount (rounded 2)."""
        raise NotImplementedError

    def __len__(self):
        """Number of charges."""
        raise NotImplementedError

    def __repr__(self):
        """Exactly: "Folio(G001, 3 charges, balance=225.00)" """
        raise NotImplementedError


@dataclass
class RunReport:
    """Collects the outcome of a pipeline run."""
    name: str
    rows_ok: int = 0
    errors: list = field(default_factory=list)

    def record_ok(self, n=1):
        """Increase rows_ok by n."""
        raise NotImplementedError

    def record_error(self, message):
        """Append the message to errors."""
        raise NotImplementedError

    @property
    def status(self):
        """"success" if no errors, "failed" if errors and rows_ok == 0, otherwise "partial"."""
        raise NotImplementedError

    def summary(self):
        """Return {"name": ..., "rows_ok": ..., "rows_failed": len(errors), "status": ...}"""
        raise NotImplementedError


class Extractor:
    """Base class. Subclasses must implement extract() returning a list of dicts."""

    def extract(self):
        raise NotImplementedError("subclasses must implement extract()")

    def name(self):
        """Return the class name, e.g. "CSVExtractor". (Done for you.)"""
        return type(self).__name__


class ListExtractor(Extractor):
    """Returns copies of the rows it was created with (useful for tests)."""

    def __init__(self, rows):
        raise NotImplementedError

    def extract(self):
        """Return a NEW list of copies of each row dict (so callers can't change the source)."""
        raise NotImplementedError


class CSVExtractor(Extractor):
    """Reads rows from a CSV file."""

    def __init__(self, path):
        raise NotImplementedError

    def extract(self):
        """Return csv.DictReader rows as a list of dicts. Use encoding="utf-8", newline=""."""
        raise NotImplementedError


def extract_all(extractors):
    """Call extract() on each extractor and return ONE combined list of rows. Add a key
    "_source" to every row with the extractor's name() (e.g. "CSVExtractor")."""
    raise NotImplementedError
