# Module 03: Data structures (lists, tuples, dictionaries, sets)

**Time:** 8–10 hours (the most important foundations module) · **Prerequisite:** Module 02

## Bakit ko 'to kailangan?

Data engineering is moving **collections** of data, not single values. A CSV row becomes a dictionary. A file becomes a list of dictionaries. "Unique guests" is a set. A lookup table from guest_id to cabin is a dictionary. Choosing the right structure is the difference between a script that takes 2 seconds and one that takes 2 hours.

**At work:** your integration matrices map a field in one system to a field in another. That *is* a dictionary. Your RAID log is a list of records. You already think in these structures; now you'll write them.

**In interviews:** almost every Python coding question for DE roles is secretly "do you know when to use a dict or a set?"

---

## 1. Lists: ordered, changeable collections

```python
outlets = ["Bar", "Spa", "Restaurant"]
outlets[0]            # "Bar"
outlets[-1]           # "Restaurant"
outlets[1:]           # ["Spa", "Restaurant"]
len(outlets)          # 3
"Spa" in outlets      # True  (searches the whole list: slow for big lists)
```

Changing a list:

```python
outlets.append("Cafe")          # add to the end
outlets.insert(0, "Lobby")      # add at a position
outlets.remove("Spa")           # remove the first matching value
last = outlets.pop()            # remove and return the last item
outlets.extend(["Gym", "Pool"]) # add many
outlets.sort()                  # sort IN PLACE (changes the list, returns None)
ordered = sorted(outlets)       # returns a NEW sorted list
outlets.reverse()
outlets.index("Bar")            # position of "Bar"
outlets.count("Bar")            # how many times "Bar" appears
```

**Trap:** `outlets = outlets.sort()` makes `outlets` become `None`. `.sort()` changes in place and returns nothing. Use `sorted()` when you want a new list.

Useful built-ins: `sum(amounts)`, `min(amounts)`, `max(amounts)`, `len(amounts)`.

---

## 2. Tuples: ordered, unchangeable

```python
point = (14.5995, 120.9842)     # latitude, longitude
charge = ("G001", "Bar", 25.0)
guest_id, outlet, amount = charge   # unpacking
```

Use a tuple when the values belong together and shouldn't change: coordinates, a database row, a composite key like `("G001", "2026-10-01")`. Tuples can be dictionary keys; lists can't.

---

## 3. Dictionaries: key → value lookups

The single most useful structure in data engineering.

```python
charge = {"guest_id": "G001", "outlet": "Bar", "amount": 25.0}

charge["outlet"]                 # "Bar"
charge["amount"] = 30.0          # update
charge["currency"] = "USD"       # add a new key
del charge["currency"]           # remove
"outlet" in charge               # True (checks KEYS)
charge.get("discount")           # None   (no error if missing)
charge.get("discount", 0)        # 0      (default)
charge["discount"]               # KeyError!
```

Looping:

```python
for key in charge:                    # keys
for value in charge.values():         # values
for key, value in charge.items():     # both (most common)
```

### Lookups are fast

Checking `"G001" in guest_dict` is instant even with a million guests. Checking `"G001" in guest_list` scans every item. This is why you build a dictionary when you need to look things up repeatedly:

```python
cabins = {"G001": "A214", "G002": "B110"}   # build once
cabins["G002"]                               # instant lookup
```

### Counting and summing by key (you'll use this everywhere)

```python
totals = {}
for c in charges:
    outlet = c["outlet"]
    totals[outlet] = totals.get(outlet, 0) + c["amount"]
```

That's `SELECT outlet, SUM(amount) ... GROUP BY outlet` in plain Python.

### Grouping into lists

```python
by_guest = {}
for c in charges:
    by_guest.setdefault(c["guest_id"], []).append(c)
```

### Merging dictionaries

```python
defaults = {"currency": "USD", "charge_type": "sale"}
row = {"amount": 25, "currency": "PHP"}
merged = {**defaults, **row}     # right side wins: currency = "PHP"
merged = defaults | row           # same thing, Python 3.9+
```

---

## 4. Sets: unique values, fast membership

```python
guest_ids = {"G001", "G002", "G001"}   # {"G001", "G002"}  duplicates vanish
guest_ids.add("G003")
"G001" in guest_ids                     # fast

a = {"Bar", "Spa", "Cafe"}
b = {"Spa", "Cafe", "Gym"}
a & b    # intersection {"Spa", "Cafe"}       -> in both
a | b    # union        {"Bar","Spa","Cafe","Gym"}
a - b    # difference   {"Bar"}               -> in a, not in b
```

**Bakit:** reconciliation. *"Which guest IDs are in the charges file but not in the guest master?"* is `charge_ids - master_ids`. That one line is an integration-defect detector.

Sets are **unordered**. If you need a stable order for output, `sorted(my_set)`.

Empty set is `set()`, not `{}` (that's an empty dict).

---

## 5. Rows vs columns: the two shapes of tabular data

```python
# List of dicts (row-oriented): how CSV readers and APIs give you data
rows = [
    {"guest_id": "G001", "amount": 25.0},
    {"guest_id": "G002", "amount": 40.0},
]

# Dict of lists (column-oriented): how pandas thinks internally
columns = {
    "guest_id": ["G001", "G002"],
    "amount": [25.0, 40.0],
}
```

Converting between them is a classic exercise and teaches you how pandas works under the hood.

---

## 6. Comprehensions: build collections in one line

```python
amounts = [25, -10, 120, 80]

# list comprehension: [expression for item in iterable if condition]
positives = [a for a in amounts if a > 0]          # [25, 120, 80]
with_tax = [round(a * 1.12, 2) for a in amounts]

# dict comprehension
names = {"G001": "ana", "G002": "ben"}
upper = {gid: n.title() for gid, n in names.items()}

# set comprehension
outlets = {c["outlet"] for c in charges}
```

Rule of thumb: if a comprehension doesn't fit on one readable line, use a normal loop.

---

## 7. Sorting with `key=`

```python
charges = [{"guest": "G002", "amount": 40}, {"guest": "G001", "amount": 120}]

sorted(charges, key=lambda c: c["amount"])                # smallest first
sorted(charges, key=lambda c: c["amount"], reverse=True)  # biggest first
sorted(charges, key=lambda c: (c["guest"], -c["amount"])) # by guest, then amount desc
```

`lambda c: c["amount"]` is a tiny unnamed function: "given c, return c['amount']". You'll study it properly in Module 04. For now, read it as "sort by this".

---

## 8. Mutability and copying (a classic bug source)

```python
a = ["Bar", "Spa"]
b = a              # b is the SAME list, not a copy
b.append("Cafe")
print(a)           # ["Bar", "Spa", "Cafe"]  surprise!

c = a.copy()       # or list(a) or a[:]  -> a real (shallow) copy
```

Functions that receive a list or dict can change the caller's data. **In this course, never modify the input you're given; build and return a new object.** Good pipelines work the same way: raw data stays untouched.

---

## 9. Which structure should I use?

| Need | Use |
|---|---|
| Ordered items, may repeat | `list` |
| Fixed group of values / composite key | `tuple` |
| Look something up by an ID | `dict` |
| Count or sum per category | `dict` (or `Counter`, Module 10) |
| Unique values, membership tests, compare two sets of IDs | `set` |

**Speed intuition (Big-O):** `x in list` is O(n): it gets slower as the list grows. `x in set` / `x in dict` is O(1): about the same speed at any size. Interviewers love this question.

---

## Exercises (`exercises.py`)

All exercises use small lists of charge dictionaries like `{"guest_id": "G001", "outlet": "Bar", "amount": 25.0}`.

1. `total_by_outlet(charges)`
2. `unique_guests(charges)`
3. `top_n_charges(charges, n)`
4. `invert_mapping(mapping)`
5. `merge_profiles(base, updates)`
6. `common_outlets(outlets_a, outlets_b)`
7. `missing_ids(source_ids, master_ids)` – reconciliation
8. `squares_of_evens(numbers)` – comprehension
9. `group_by(records, key)`
10. `find_duplicates(values)`
11. `chunk(items, size)` – batching
12. `flatten(list_of_lists)`
13. `word_counts(text)`
14. `rows_to_columns(rows)` and `columns_to_rows(columns)`
15. `transpose(matrix)`

## Mini project: guest folio summary (`folio.py`, not graded)

Hardcode 10 charges for 3 guests. Print, per guest: number of charges, total, biggest charge, and the set of outlets visited. Then print the guest IDs that visited **both** Bar and Spa. Use only what this module taught.

## Self-check

1. Why can a tuple be a dict key but a list can't?
2. What's the output of `sorted({3, 1, 2})`?
3. `d = {}; d["x"] += 1` raises what, and how do you fix it?
4. When would you pick a set over a list?

<details><summary>Answers</summary>

1. Dict keys must be hashable (unchangeable). Lists can change, so they can't be hashed.
2. `[1, 2, 3]`, a list.
3. `KeyError`. Use `d["x"] = d.get("x", 0) + 1`.
4. When you need uniqueness or fast "is X in here?" checks and don't care about order.
</details>
