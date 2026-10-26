"""Module 04 exercises: functions.

Run:  python check.py 04
"""


def apply_discount(amount, percent=10):
    """Return amount after a percentage discount, rounded to 2 decimals.

    >>> apply_discount(200)
    180.0
    >>> apply_discount(80, percent=25)
    60.0
    """
    raise NotImplementedError


def summarize(*amounts):
    """Accept any number of amounts and return a dict with
    "count", "total" (rounded 2) and "average" (rounded 2; 0.0 if no amounts).

    >>> summarize(25, 120, 80)
    {'count': 3, 'total': 225, 'average': 75.0}
    >>> summarize()
    {'count': 0, 'total': 0, 'average': 0.0}
    """
    raise NotImplementedError


def build_record(**fields):
    """Return a dict of the given keyword arguments. If "source" was not given,
    add "source": "manual".

    >>> build_record(guest_id="G001", amount=25)
    {'guest_id': 'G001', 'amount': 25, 'source': 'manual'}
    >>> build_record(guest_id="G002", source="pos")
    {'guest_id': 'G002', 'source': 'pos'}
    """
    raise NotImplementedError


def append_to_batch(item, batch=None):
    """Append item to batch and return the batch. If no batch is given, start a NEW
    empty list every time (avoid the mutable default bug).

    >>> append_to_batch(1)
    [1]
    >>> append_to_batch(2)
    [2]
    >>> append_to_batch(3, [1, 2])
    [1, 2, 3]
    """
    raise NotImplementedError


def make_multiplier(factor):
    """Return a FUNCTION that multiplies its input by `factor`.

    >>> triple = make_multiplier(3)
    >>> triple(5)
    15
    """
    raise NotImplementedError


def compose(f, g):
    """Return a new function h where h(x) == f(g(x)).

    >>> add_one = lambda x: x + 1
    >>> double = lambda x: x * 2
    >>> compose(add_one, double)(5)
    11
    """
    raise NotImplementedError


def run_steps(value, steps):
    """Apply each function in `steps` to `value`, in order, and return the result.
    With no steps, return value unchanged.

    >>> run_steps("  the bar ", [str.strip, str.title])
    'The Bar'
    """
    raise NotImplementedError


def sort_charges(charges):
    """Return charges sorted by guest_id ascending, then by amount DESCENDING.
    Do not modify the input list.
    """
    raise NotImplementedError


def filter_by(records, predicate):
    """Return the records for which predicate(record) is True.
    `predicate` is a function you receive as an argument.

    >>> filter_by([1, 5, 10], lambda n: n > 3)
    [5, 10]
    """
    raise NotImplementedError


def factorial(n):
    """Return n! using recursion. factorial(0) == 1.

    >>> factorial(5)
    120
    """
    raise NotImplementedError


def fibonacci(n):
    """Return the n-th Fibonacci number: fibonacci(0) == 0, fibonacci(1) == 1,
    fibonacci(n) == fibonacci(n-1) + fibonacci(n-2).

    It must be fast for n = 80 (plain recursion is far too slow).
    Hint: use a loop, or recursion with a dict that remembers results (memoization).

    >>> fibonacci(10)
    55
    """
    raise NotImplementedError
