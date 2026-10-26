"""Reference solutions for Module 09."""
import csv
from dataclasses import dataclass, field


@dataclass
class Charge:
    charge_id: int
    guest_id: str
    outlet: str
    amount: float
    charge_type: str = "sale"

    @property
    def is_refund(self):
        return self.charge_type == "refund"

    @classmethod
    def from_dict(cls, row):
        return cls(
            charge_id=int(row["charge_id"]),
            guest_id=row["guest_id"].strip(),
            outlet=row["outlet"].strip(),
            amount=float(row["amount"]),
            charge_type=row.get("charge_type", "sale"),
        )


class Folio:
    def __init__(self, guest_id):
        self.guest_id = guest_id
        self.charges = []

    def add(self, charge):
        if charge.guest_id != self.guest_id:
            raise ValueError(f"charge belongs to {charge.guest_id}")
        self.charges.append(charge)
        return self

    @property
    def balance(self):
        return round(sum(c.amount for c in self.charges), 2)

    def total_by_outlet(self):
        totals = {}
        for c in self.charges:
            totals[c.outlet] = totals.get(c.outlet, 0) + c.amount
        return {k: round(v, 2) for k, v in totals.items()}

    def __len__(self):
        return len(self.charges)

    def __repr__(self):
        return f"Folio({self.guest_id}, {len(self)} charges, balance={self.balance:.2f})"


@dataclass
class RunReport:
    name: str
    rows_ok: int = 0
    errors: list = field(default_factory=list)

    def record_ok(self, n=1):
        self.rows_ok += n

    def record_error(self, message):
        self.errors.append(message)

    @property
    def status(self):
        if not self.errors:
            return "success"
        return "failed" if self.rows_ok == 0 else "partial"

    def summary(self):
        return {"name": self.name, "rows_ok": self.rows_ok, "rows_failed": len(self.errors), "status": self.status}


class Extractor:
    def extract(self):
        raise NotImplementedError("subclasses must implement extract()")

    def name(self):
        return type(self).__name__


class ListExtractor(Extractor):
    def __init__(self, rows):
        self.rows = rows

    def extract(self):
        return [dict(r) for r in self.rows]


class CSVExtractor(Extractor):
    def __init__(self, path):
        self.path = path

    def extract(self):
        with open(self.path, encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))


def extract_all(extractors):
    combined = []
    for extractor in extractors:
        for row in extractor.extract():
            combined.append({**row, "_source": extractor.name()})
    return combined
