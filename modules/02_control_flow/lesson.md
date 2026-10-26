# Module 02: Making decisions and repeating work

**Time:** 6–7 hours · **Prerequisite:** Module 01

## Bakit ko 'to kailangan?

A pipeline is mostly two ideas repeated: **"for every row, do this"** (loops) and **"if the row looks like this, handle it that way"** (conditions). Refunds go one way, sales another. Bad rows get quarantined. Retries happen until a connection works.

**At work:** your business rules documents are already written in this shape: *"If the charge is a refund and the folio is closed, then..."*. In this module you'll learn to turn a business rule into code that runs.

---

## 1. if / elif / else

```python
amount = 120

if amount < 0:
    category = "refund"
elif amount == 0:
    category = "complimentary"
elif amount <= 50:
    category = "small"
else:
    category = "large"
```

Rules:
- The colon `:` ends every `if`, `elif`, `else` line.
- The body is **indented 4 spaces**. Indentation *is* the syntax in Python.
- Python checks top to bottom and runs **only the first** branch that's True. Order matters: put specific checks before general ones.

### Boolean logic

```python
is_refund = amount < 0
is_vip = tier in ("Gold", "Platinum")     # membership test

if is_vip and amount > 500:               # both must be True
    ...
if outlet == "Bar" or outlet == "Cafe":   # at least one True
    ...
if not is_refund:                          # flips True/False
    ...
if 50 <= amount <= 200:                    # chained comparison
    ...
```

### Truthiness

These are treated as `False` in an `if`: `False`, `None`, `0`, `0.0`, `""`, `[]`, `{}`. Everything else is `True`.

```python
email = ""
if not email:
    print("Missing email")     # runs, because "" is falsy
```

**Careful:** `if amount:` is False when amount is `0`. If 0 is a valid value, test `if amount is None:` instead. This exact bug causes "complimentary items disappeared from the report" defects.

### Conditional expression (one-line if)

```python
label = "refund" if amount < 0 else "sale"
```

---

## 2. for loops

```python
amounts = [25.0, 120.0, 80.0]
total = 0
for amount in amounts:
    total += amount
# total == 225.0
```

### range()

```python
for i in range(5):        # 0, 1, 2, 3, 4
for i in range(1, 6):     # 1, 2, 3, 4, 5
for i in range(0, 10, 2): # 0, 2, 4, 6, 8
```

### Loop over a string

```python
for ch in "G001":
    print(ch)   # G, 0, 0, 1
```

### enumerate(): index and value together

```python
outlets = ["Bar", "Spa", "Cafe"]
for row_number, outlet in enumerate(outlets, start=1):
    print(row_number, outlet)    # 1 Bar / 2 Spa / 3 Cafe
```

**Bakit:** error messages need row numbers: *"Row 15: missing amount"*. You'll use `enumerate` in every validator you write.

### zip(): walk two lists together

```python
guests = ["G001", "G002"]
totals = [225.0, 165.0]
for guest, total in zip(guests, totals):
    print(guest, total)
```

---

## 3. while loops

Use `while` when you don't know in advance how many times to repeat:

```python
attempt = 0
connected = False
while not connected and attempt < 3:
    attempt += 1
    connected = try_connect()     # imagine this sometimes fails
```

Always make sure something inside the loop moves toward stopping, or it runs forever (Ctrl+C to escape).

---

## 4. break, continue, and the accumulator pattern

```python
for amount in amounts:
    if amount is None:
        continue          # skip this one, go to the next
    if amount < 0:
        print("Found a refund, stopping")
        break             # leave the loop completely
```

The **accumulator pattern** is the backbone of reporting:

```python
total = 0          # 1. start with an empty result
count = 0
for amount in amounts:     # 2. loop
    if amount > 0:         # 3. maybe filter
        total += amount    # 4. update the result
        count += 1
average = total / count if count else 0
```

Every `SUM`, `COUNT` and `AVG` you've written in SQL is this pattern underneath.

---

## 5. Nested loops

```python
for guest in ["G001", "G002"]:
    for outlet in ["Bar", "Spa"]:
        print(guest, outlet)     # 4 combinations
```

Nested loops multiply work: 1,000 guests × 1,000 outlets = 1,000,000 steps. Keep that in mind; you'll learn faster ways with dictionaries (Module 03) and pandas (Module 12).

---

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Forgetting `:` | SyntaxError | Add the colon |
| Mixing tabs and spaces | IndentationError | VS Code: use 4 spaces |
| `if x = 5:` | SyntaxError | `==` compares, `=` assigns |
| `return` inside the loop by accident | Function stops after the first item | Indent `return` at the function level |
| `while` condition never becomes False | Infinite loop | Update the variable inside the loop |

---

## Exercises (`exercises.py`)

1. `charge_category(amount)` – if/elif chain
2. `loyalty_tier(nights)` – ranges
3. `fizzbuzz(n)` – the classic interview warm-up
4. `sum_to(n)` – accumulator
5. `count_vowels(text)` – loop over a string
6. `first_negative_index(amounts)` – `enumerate` + early return
7. `largest(numbers)` – no `max()` allowed
8. `is_valid_guest_id(guest_id)` – several conditions
9. `compound_balance(principal, rate, years)` – loop with a running value
10. `digits_sum(n)` – while loop
11. `attempts_until_success(results)` – retry logic

## Mini project: number guessing CLI (`guess.py`, not graded)

Write a program that picks a random number 1–50 (`import random; random.randint(1, 50)`), asks the user to guess with `input()`, says "higher" or "lower", counts attempts, and stops after 7 attempts or a correct guess. It uses every idea in this module.

## Self-check

1. What prints? `for i in range(2, 8, 3): print(i)`
2. Why is `if amount:` risky for amounts?
3. What's the difference between `break` and `continue`?

<details><summary>Answers</summary>

1. `2` and `5`.
2. An amount of `0` is falsy, so a valid 0 would be treated as missing.
3. `break` exits the loop entirely; `continue` skips the rest of the current iteration and moves to the next item.
</details>
