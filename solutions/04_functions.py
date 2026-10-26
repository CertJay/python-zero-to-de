"""Reference solutions for Module 04."""


def apply_discount(amount, percent=10):
    return round(amount * (1 - percent / 100), 2)


def summarize(*amounts):
    count = len(amounts)
    total = round(sum(amounts), 2)
    average = round(total / count, 2) if count else 0.0
    return {"count": count, "total": total, "average": average}


def build_record(**fields):
    record = dict(fields)
    record.setdefault("source", "manual")
    return record


def append_to_batch(item, batch=None):
    if batch is None:
        batch = []
    batch.append(item)
    return batch


def make_multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply


def compose(f, g):
    return lambda x: f(g(x))


def run_steps(value, steps):
    for step in steps:
        value = step(value)
    return value


def sort_charges(charges):
    return sorted(charges, key=lambda c: (c["guest_id"], -c["amount"]))


def filter_by(records, predicate):
    return [r for r in records if predicate(r)]


def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
