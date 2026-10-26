# Module 01: Values, variables, types and operators

**Time:** 5–6 hours · **Prerequisite:** Module 00

## Bakit ko 'to kailangan?

Data engineering is moving values around and changing them on the way: an amount becomes an amount with tax, a date string becomes a real date, `"25.00"` becomes `25.0`. Every one of those steps starts with knowing **what type a value is** and **what you're allowed to do with it**.

**At work:** when an integration posts `"120"` (text) instead of `120` (number), totals break. Types are why. You'll start spotting these defects in UAT before devs do.

---

## 1. Variables

A variable is a name pointing to a value.

```python
guest_id = "G001"
amount = 25.50
nights = 7
is_vip = True
```

Naming rules that every Python team follows (PEP 8):
- `snake_case`: lowercase with underscores: `charge_date`, not `chargeDate` or `ChargeDate`.
- Descriptive: `total_amount`, not `x` or `ta`.
- Constants in CAPS: `SERVICE_CHARGE_RATE = 0.10`.

Variables can be reassigned:

```python
balance = 0
balance = balance + 25     # 25
balance += 120             # 145  (shortcut for balance = balance + 120)
```

---

## 2. The core types

| Type | Example | Used for |
|---|---|---|
| `int` | `7`, `-3`, `1_000_000` | Counts, IDs, quantities |
| `float` | `25.5`, `0.10` | Amounts, rates, measurements |
| `str` | `"Bar"`, `'G001'` | Text, codes, names |
| `bool` | `True`, `False` | Flags: is_refund, is_valid |
| `None` | `None` | "No value" (like SQL `NULL`) |

Check a type with `type()`:

```python
type(7)        # <class 'int'>
type("7")      # <class 'str'>
type(None)     # <class 'NoneType'>
```

### Converting between types (casting)

```python
int("42")          # 42
float("25.50")     # 25.5
str(120)           # "120"
int(25.9)          # 25   <- int() cuts off, it does NOT round
round(25.9)        # 26
bool(0), bool("")  # False, False (empty or zero is "falsy")
bool("Bar")        # True
int("25.50")       # ValueError! convert to float first: int(float("25.50"))
```

**Bakit:** CSV files give you everything as text. Casting is the first transform in almost every pipeline.

### Floats are not exact

```python
0.1 + 0.2          # 0.30000000000000004
round(0.1 + 0.2, 2)  # 0.3
```

Computers store floats in binary, so some decimals can't be represented exactly. For money in real systems, use `decimal.Decimal` or store cents as integers. In this course, `round(x, 2)` is enough.

---

## 3. Operators

```python
10 + 3    # 13   addition
10 - 3    # 7    subtraction
10 * 3    # 30   multiplication
10 / 3    # 3.3333333333333335   division ALWAYS gives a float
10 // 3   # 3    floor division (whole part)
10 % 3    # 1    modulo (remainder)
2 ** 3    # 8    power
```

`//` and `%` together are how you split a big number into units:

```python
total_seconds = 3725
hours = total_seconds // 3600            # 1
minutes = (total_seconds % 3600) // 60   # 2
seconds = total_seconds % 60             # 5
```

**Bakit:** pipeline run durations, batch numbers, "which page is row 1,250 on" all use these.

Comparison operators return `bool`:

```python
25 > 10        # True
"Bar" == "bar" # False (case matters!)
5 != 6         # True
```

---

## 4. Strings: the basics

```python
outlet = "Restaurant"
len(outlet)          # 10
outlet[0]            # "R"    first character (index 0)
outlet[-1]           # "t"    last character
outlet[0:4]          # "Rest" slice: from index 0 up to (not including) 4
outlet[-4:]          # "rant" last 4 characters
outlet.upper()       # "RESTAURANT"
outlet.lower()       # "restaurant"
"  bar ".strip()     # "bar"
"Miguel Jay".split() # ["Miguel", "Jay"]
"Bar" + " " + "Menu" # "Bar Menu"
"=" * 10             # "=========="
```

Strings are **immutable**: methods return a *new* string; the original doesn't change.

```python
name = "bar"
name.upper()     # returns "BAR"
print(name)      # still "bar"
name = name.upper()  # reassign to keep it
```

### f-strings: the way to build text

```python
guest_id, amount = "G001", 25.5
f"{guest_id} spent {amount}"            # "G001 spent 25.5"
f"{amount:.2f}"                          # "25.50"   2 decimals
f"{1250000:,.2f}"                        # "1,250,000.00"  thousands separator
f"{7:03d}"                               # "007"     zero-padded
f"{'Bar':<10}|"                          # "Bar       |"  left-aligned in 10 chars
f"{0.153:.1%}"                           # "15.3%"
```

**Bakit:** log messages, file names (`charges_2026-10-01.csv`), report lines and SQL-free formatting all use f-strings. You'll write hundreds.

---

## 5. print() and input()

```python
print("Loaded", 120, "rows")   # Loaded 120 rows
print(f"Loaded {120} rows")    # same, cleaner
name = input("Your name: ")    # waits for typing; ALWAYS returns a str
```

You'll use `print` for debugging. In real pipelines you'll replace it with `logging` (Module 07).

**Important for this course:** exercises **return** values; they don't `print` them. `print` shows text on screen; `return` hands a value back to the code that called the function. Tests can only check what you return.

---

## Common mistakes

| Mistake | Fix |
|---|---|
| `"Total: " + 25` → TypeError | `f"Total: {25}"` or `"Total: " + str(25)` |
| `int("25.5")` → ValueError | `int(float("25.5"))` |
| Expecting `name.upper()` to change `name` | `name = name.upper()` |
| Using `print` instead of `return` in a function | Functions in this course must `return` |

---

## Exercises (`exercises.py`)

1. `total_with_service_charge(amount, rate=0.10)`
2. `split_bill(total, people)`
3. `format_charge(guest_id, outlet, amount)` – f-string formatting
4. `celsius_to_fahrenheit(c)`
5. `is_even(n)` – the `%` operator
6. `seconds_to_hms(seconds)` – `//` and `%` together
7. `initials(full_name)` – split and index
8. `mask_card(card_number)` – slicing
9. `type_name(value)` – `type()`
10. `parse_amount_text(text)` – casting text to float

## Mini project: receipt printer (`receipt.py`, not graded)

Create `modules/01_basics/receipt.py` that prints a receipt for 3 hardcoded charges:

```
=============================
 ONBOARD RECEIPT  Guest G001
=============================
Bar                     25.00
Spa                    120.00
Restaurant              80.00
-----------------------------
Subtotal               225.00
Service (10%)           22.50
TOTAL                  247.50
=============================
```

Use variables, arithmetic and f-string alignment (`:<20` and `:>9.2f`). Run with `python modules/01_basics/receipt.py`.

## Self-check (answer without running code, then verify in the REPL)

1. What does `7 // 2` return? And `7 / 2`?
2. Why does `"5" * 3` work but `"5" + 3` fail?
3. What's `"G001"[1:]`?
4. What does `bool("False")` return, and why?

<details><summary>Answers</summary>

1. `3` and `3.5`.
2. `str * int` repeats the string (`"555"`); `str + int` is undefined, so Python raises TypeError.
3. `"001"`.
4. `True`. Any non-empty string is truthy, even the text "False".
</details>
