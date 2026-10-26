# Python core cheat sheet

## Types and conversion
```python
int("42"); float("25.5"); str(120); bool(""); round(2.675, 2)
type(x).__name__; isinstance(x, (int, float))
```

## Strings
```python
s.strip() s.lower() s.upper() s.title() s.split(",") ",".join(items)
s.replace("a", "b") s.startswith("G") s.endswith(".csv") s.find("x") "x" in s
s[0] s[-1] s[1:4] s[::-1]   f"{amount:,.2f}" f"{n:03d}" f"{rate:.1%}"
" ".join(s.split())          # collapse whitespace
```

## Lists, tuples, sets, dicts
```python
lst.append(x) lst.extend(xs) lst.pop() sorted(lst, key=lambda r: r["amount"], reverse=True)
a, b = (1, 2)
s = set(xs); a & b; a | b; a - b
d.get(k, default); d.setdefault(k, []).append(v); d.items(); {**d1, **d2}
[x for x in xs if x > 0]   {k: v for k, v in d.items()}   {x for x in xs}
```

## Control flow
```python
for i, x in enumerate(xs, start=1): ...
for a, b in zip(xs, ys): ...
while cond: ...
break / continue
label = "refund" if amount < 0 else "sale"
```

## Functions
```python
def f(x, rate=0.1, *args, **kwargs) -> float: ...
def f(items=None):            # never items=[]
    items = [] if items is None else items
lambda x: x * 2
```

## Files
```python
from pathlib import Path
with open(path, encoding="utf-8") as f: ...
csv.DictReader(f); csv.DictWriter(f, fieldnames=[...])   # open with newline=""
json.load(f); json.dump(obj, f, indent=2, ensure_ascii=False)
Path("out").mkdir(parents=True, exist_ok=True); sorted(Path("data").glob("*.csv"))
```

## Errors and logging
```python
try: ...
except ValueError as e: ...
else: ...
finally: ...
raise ValueError("clear message")
log = logging.getLogger(__name__); log.info("Loaded %d rows", n); log.exception("failed")
```

## Regex
```python
re.findall(r"\bG\d{3}\b", text); re.search(...).group(); re.fullmatch(...)
re.sub(r"\s+", " ", s); m.groupdict() with (?P<name>...)
```

## Dates
```python
date.fromisoformat("2026-10-01"); d.isoformat(); d + timedelta(days=1)
datetime.strptime("01/10/2026", "%d/%m/%Y"); d.strftime("%Y-%m-%d")
datetime.now(timezone.utc); dt.astimezone(ZoneInfo("Asia/Manila"))
```

## collections / itertools
```python
Counter(xs).most_common(3); defaultdict(list); deque(maxlen=5)
itertools.groupby(sorted_rows, key=...); itertools.accumulate(xs); itertools.islice(gen, 10)
```

## Classes
```python
@dataclass
class Charge:
    charge_id: int
    amount: float
    tags: list = field(default_factory=list)
    @property
    def is_refund(self): return self.amount < 0
    @classmethod
    def from_dict(cls, d): return cls(int(d["charge_id"]), float(d["amount"]))
```
