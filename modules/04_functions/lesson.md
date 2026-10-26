# Module 04: Functions

**Time:** 6–8 hours · **Prerequisite:** Module 03

## Bakit ko 'to kailangan?

A pipeline is a chain of functions: `extract()` → `clean()` → `validate()` → `load()`. Good functions are small, named after what they do, take inputs, and return outputs without surprises. That makes them testable, reusable and easy to debug at 2 AM when a job fails.

**At work:** a function is a business rule with a name. "Apply service charge", "classify refund", "map outlet code" are all functions. When you write specs, you're already describing inputs, outputs and edge cases. That's exactly what a function signature and docstring are.

---

## 1. Anatomy of a function

```python
def apply_service_charge(amount: float, rate: float = 0.10) -> float:
    """Return amount plus service charge, rounded to 2 decimals."""
    return round(amount * (1 + rate), 2)
```

| Part | Meaning |
|---|---|
| `def` | "I'm defining a function" |
| `apply_service_charge` | name: a verb, snake_case |
| `amount: float` | parameter with a **type hint** (documentation; Python doesn't enforce it) |
| `rate: float = 0.10` | parameter with a **default value** |
| `-> float` | hint for the return type |
| `"""..."""` | docstring: what it does. VS Code shows this on hover |
| `return` | hands the result back and **ends the function** |

A function with no `return` returns `None`.

### Calling it

```python
apply_service_charge(100)              # 110.0  (uses default rate)
apply_service_charge(100, 0.12)        # 112.0  positional
apply_service_charge(rate=0.12, amount=100)   # keyword arguments: order doesn't matter
```

Use keyword arguments when a call would otherwise be unclear: `load(df, table="charges", if_exists="append")` reads better than `load(df, "charges", "append")`.

---

## 2. Default value trap: never use a mutable default

```python
def add_charge(charge, batch=[]):     # BUG
    batch.append(charge)
    return batch

add_charge(1)   # [1]
add_charge(2)   # [1, 2]   the SAME list is reused between calls!
```

Fix:

```python
def add_charge(charge, batch=None):
    if batch is None:
        batch = []
    batch.append(charge)
    return batch
```

This is a well-known interview question.

---

## 3. *args and **kwargs

```python
def total(*amounts):          # any number of positional args -> a tuple
    return sum(amounts)

total(25, 120, 80)            # 225

def build_row(**fields):      # any number of keyword args -> a dict
    return fields

build_row(guest_id="G001", amount=25)   # {"guest_id": "G001", "amount": 25}
```

Unpacking when calling:

```python
amounts = [25, 120, 80]
total(*amounts)               # same as total(25, 120, 80)

settings = {"amount": 100, "rate": 0.12}
apply_service_charge(**settings)
```

You'll see `**kwargs` a lot in library code: `pd.read_csv(path, **options)`.

---

## 4. Scope

Variables created inside a function exist only inside it.

```python
rate = 0.10            # global

def charge(amount):
    tax = amount * rate    # can READ the global
    return amount + tax

print(tax)             # NameError: tax only existed inside charge()
```

Avoid changing global variables from inside functions. Pass values in, return values out. Pipelines built this way can be re-run safely.

---

## 5. Functions are values

You can store functions in variables, put them in lists, pass them to other functions and return them from functions.

```python
def strip_text(s): return s.strip()
def to_title(s): return s.title()

steps = [strip_text, to_title]
value = "  the bar "
for step in steps:
    value = step(value)
# value == "The Bar"
```

That loop is a **mini pipeline**: a list of transformation steps applied in order. Real frameworks work on the same idea.

### lambda: small anonymous functions

```python
double = lambda x: x * 2
sorted(charges, key=lambda c: c["amount"])
```

Use lambdas only for short, one-expression functions, mostly as `key=` arguments.

### map, filter

```python
amounts = [25, -10, 120]
list(map(lambda a: a * 1.12, amounts))     # apply to each
list(filter(lambda a: a > 0, amounts))     # keep matching
```

List comprehensions usually read better: `[a * 1.12 for a in amounts]`.

### Closures: functions that remember

```python
def make_tax_function(rate):
    def apply(amount):
        return round(amount * (1 + rate), 2)
    return apply

ph_vat = make_tax_function(0.12)
ph_vat(100)    # 112.0
```

`apply` remembers `rate` even after `make_tax_function` finished. Closures are the foundation of decorators (Module 10).

---

## 6. Recursion (brief)

A function that calls itself, with a stopping condition:

```python
def factorial(n):
    if n <= 1:          # base case: stop here
        return 1
    return n * factorial(n - 1)
```

In DE you'll use recursion mainly to walk nested JSON (a dict inside a dict inside a list...). You'll do that in the interview module.

---

## 7. Writing good functions: checklist

- **One job.** If the name needs "and", split it.
- **Name it with a verb:** `parse_date`, `load_charges`, `is_valid_email`.
- **Return, don't print.** Let the caller decide what to do with the result.
- **Don't modify inputs.** Return new data.
- **Handle the empty case:** what happens with `[]`, `""`, `None`, `0`?
- **Docstring with an example.** Future you will thank you.

---

## Exercises (`exercises.py`)

1. `apply_discount(amount, percent=10)` – defaults
2. `summarize(*amounts)` – *args, returns a dict
3. `build_record(**fields)` – **kwargs with a default field
4. `append_to_batch(item, batch=None)` – the safe mutable-default pattern
5. `make_multiplier(factor)` – closure
6. `compose(f, g)` – functions as values
7. `run_steps(value, steps)` – mini pipeline
8. `sort_charges(charges)` – multi-key sort with lambda
9. `filter_by(records, predicate)` – pass a function in
10. `factorial(n)` and `fibonacci(n)` – recursion

## Mini project: text cleaning pipeline (`cleaner.py`, not graded)

Write 5 small functions: `strip_spaces`, `collapse_inner_spaces`, `to_title`, `fix_known_typos` (use a dict like `{"Resto": "Restaurant"}`), `remove_trailing_dots`. Put them in a list and run 10 messy outlet names through them with `run_steps`. Print before → after.

## Self-check

1. What does a function return if it has no `return` statement?
2. Why is `def f(x, items=[])` dangerous?
3. What's the difference between `print(result)` and `return result` inside a function?
4. What does `sorted(rows, key=lambda r: (r["guest"], -r["amount"]))` do?

<details><summary>Answers</summary>

1. `None`.
2. The same list object is shared across every call, so data leaks between calls.
3. `print` shows text on screen and the function still returns `None`; `return` passes the value back so other code can use it.
4. Sorts by guest ascending, then by amount descending within each guest.
</details>
