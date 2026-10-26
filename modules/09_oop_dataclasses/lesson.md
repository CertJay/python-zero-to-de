# Module 09: Classes, objects and dataclasses

**Time:** 7–8 hours · **Prerequisite:** Module 08

## Bakit ko 'to kailangan?

Most pipeline code is functions, and that's good. But some things are naturally **objects**: a database connection (it has settings *and* actions), a folio (it holds charges *and* calculates a balance), a run report (it collects counts *and* summarizes). Every library you'll use (pandas DataFrame, SQLAlchemy Engine, Airflow DAG, requests Session) is a class. You must be able to read them, and know when to write one.

**At work:** your domain already thinks in objects: a Guest has a Folio, a Folio has Charges, a Charge belongs to an Outlet. Your integration specs describe entities and their fields. Classes are how code models those entities. OOP questions also appear in nearly every junior DE interview.

---

## 1. Class and object

```python
class Folio:
    """A guest's running account."""

    def __init__(self, guest_id):        # runs when you create a Folio
        self.guest_id = guest_id         # attributes: data stored on THIS object
        self.charges = []

    def add(self, amount):               # method: a function that belongs to the object
        self.charges.append(amount)

    def balance(self):
        return sum(self.charges)


f = Folio("G001")      # create an object (an "instance")
f.add(25)
f.add(120)
f.balance()            # 145
f.guest_id             # "G001"

g = Folio("G002")      # a separate object with its own charges
```

- `class` defines the blueprint; each object built from it has its own data.
- `self` is "this particular object". Python passes it automatically: `f.add(25)` really calls `Folio.add(f, 25)`.
- `__init__` sets up the starting state.

---

## 2. Special ("dunder") methods

```python
class Folio:
    ...
    def __repr__(self):                  # how it looks when printed/debugged
        return f"Folio({self.guest_id}, {len(self.charges)} charges)"

    def __len__(self):                   # len(folio)
        return len(self.charges)

    def __eq__(self, other):             # folio_a == folio_b
        return self.guest_id == other.guest_id
```

Always write `__repr__`. When something fails at 2 AM, `Folio(G001, 3 charges)` in a log is useful; `<__main__.Folio object at 0x7f...>` isn't.

---

## 3. Properties: computed attributes

```python
class Folio:
    ...
    @property
    def balance(self):
        return round(sum(self.charges), 2)

f.balance       # no parentheses: reads like an attribute, but is computed every time
```

Use a property when a value is derived from other data and should never get out of sync.

---

## 4. classmethod and staticmethod

```python
class Charge:
    def __init__(self, guest_id, amount):
        self.guest_id = guest_id
        self.amount = amount

    @classmethod
    def from_dict(cls, row):             # alternative constructor
        return cls(row["guest_id"], float(row["amount"]))

    @staticmethod
    def is_valid_amount(value):          # helper that doesn't need self
        return isinstance(value, (int, float))

c = Charge.from_dict({"guest_id": "G001", "amount": "25.5"})
```

`from_dict`, `from_csv_row` and `from_json` classmethods are a very common pattern for turning raw records into objects.

---

## 5. dataclasses: classes for data, with less typing

```python
from dataclasses import dataclass, field

@dataclass
class Charge:
    charge_id: int
    guest_id: str
    outlet: str
    amount: float
    charge_type: str = "sale"            # default value

    @property
    def is_refund(self):
        return self.charge_type == "refund"

c = Charge(1001, "G001", "Bar", 25.0)
c                 # Charge(charge_id=1001, guest_id='G001', outlet='Bar', amount=25.0, charge_type='sale')
c == Charge(1001, "G001", "Bar", 25.0)   # True: __eq__ is generated for you
```

`@dataclass` writes `__init__`, `__repr__` and `__eq__` for you. Use it for records.

Mutable defaults need `field(default_factory=...)` (same trap as Module 04):

```python
@dataclass
class RunReport:
    rows_read: int = 0
    errors: list = field(default_factory=list)    # NOT errors: list = []
```

`@dataclass(frozen=True)` makes objects read-only, which is good for config.

---

## 6. Inheritance and polymorphism

```python
class Extractor:
    """Base class: every extractor returns a list of dict rows."""
    def extract(self):
        raise NotImplementedError

class CSVExtractor(Extractor):
    def __init__(self, path):
        self.path = path
    def extract(self):
        with open(self.path, encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))

class APIExtractor(Extractor):
    def __init__(self, url):
        self.url = url
    def extract(self):
        return requests.get(self.url).json()["results"]

for source in [CSVExtractor("a.csv"), APIExtractor("https://...")]:
    rows = source.extract()       # same call, different behavior: polymorphism
```

This is exactly how ingestion tools (Airbyte connectors, Airflow operators) are designed: one interface, many sources. The rest of your pipeline doesn't care where rows came from.

`super().__init__(...)` calls the parent's `__init__` when a child needs to extend it.

### Composition over inheritance

Prefer "has a" over "is a". A `Pipeline` **has** an extractor, transformer and loader; it isn't a subclass of them. Deep inheritance chains are hard to follow. Use inheritance for a clear shared interface like `Extractor`; use composition for everything else.

---

## 7. When to use a class (and when not to)

| Use a class when... | Use functions when... |
|---|---|
| Data and the actions on it belong together (Folio) | You transform input → output |
| You need several interchangeable implementations (extractors) | There's no state to keep |
| You keep state across calls (a connection, a counter) | A dict or dataclass would do |

Beginners often over-use classes. A pipeline of small functions plus a few dataclasses is a perfectly professional design.

---

## Exercises (`exercises.py`)

1. `Charge` dataclass with a property and a `from_dict` classmethod
2. `Folio` class: `add`, `balance`, `total_by_outlet`, `__len__`, `__repr__`, validation
3. `RunReport` dataclass with `default_factory`
4. `Extractor`, `ListExtractor`, `CSVExtractor` – inheritance
5. `extract_all(extractors)` – polymorphism

## Mini project: folios from the real file (`folios.py`, not graded)

Read `data/charges_clean.csv`, convert rows with `Charge.from_dict`, build a `Folio` per guest in a dict, then print the 5 guests with the highest balance using their `__repr__`. Add a `RunReport` that counts rows read and folios built.

## Self-check

1. What is `self`?
2. What three methods does `@dataclass` generate?
3. Why `field(default_factory=list)` instead of `= []`?
4. Give a real example where inheritance is a good fit in a pipeline.

<details><summary>Answers</summary>

1. The specific object the method was called on.
2. `__init__`, `__repr__`, `__eq__`.
3. A plain `[]` default would be shared by every instance (the mutable default trap).
4. A base `Extractor` with subclasses for CSV, API and database sources, all exposing the same `extract()` method.
</details>
