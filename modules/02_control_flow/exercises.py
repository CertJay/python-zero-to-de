"""Module 02 exercises: conditions and loops.

Run:  python check.py 02
"""


def charge_category(amount):
    """Classify a charge amount.

    amount < 0        -> "refund"
    amount == 0       -> "complimentary"
    0 < amount <= 50  -> "small"
    50 < amount <= 200 -> "medium"
    amount > 200      -> "large"

    >>> charge_category(-10)
    'refund'
    >>> charge_category(50)
    'small'
    >>> charge_category(200.01)
    'large'
    """
    raise NotImplementedError


def loyalty_tier(nights):
    """Return the loyalty tier for a number of nights stayed.

    0-4 -> "Bronze", 5-14 -> "Silver", 15-29 -> "Gold", 30 or more -> "Platinum"

    >>> loyalty_tier(4)
    'Bronze'
    >>> loyalty_tier(15)
    'Gold'
    """
    raise NotImplementedError


def fizzbuzz(n):
    """Return a list of strings for the numbers 1..n:
    "FizzBuzz" if divisible by 3 and 5, "Fizz" if by 3, "Buzz" if by 5,
    otherwise the number as a string.

    >>> fizzbuzz(5)
    ['1', '2', 'Fizz', '4', 'Buzz']
    """
    raise NotImplementedError


def sum_to(n):
    """Return 1 + 2 + ... + n using a loop (not a formula). sum_to(0) is 0.

    >>> sum_to(4)
    10
    """
    raise NotImplementedError


def count_vowels(text):
    """Count the vowels (a, e, i, o, u), upper or lower case.

    >>> count_vowels("Onboard Spa")
    4
    """
    raise NotImplementedError


def first_negative_index(amounts):
    """Return the index of the first negative amount, or -1 if there is none.

    >>> first_negative_index([25, 120, -40, 80])
    2
    >>> first_negative_index([1, 2])
    -1
    """
    raise NotImplementedError


def largest(numbers):
    """Return the largest number WITHOUT using max(). Return None for an empty list.

    >>> largest([25, 410, 80])
    410
    >>> largest([]) is None
    True
    """
    raise NotImplementedError


def is_valid_guest_id(guest_id):
    """A valid guest id is exactly 4 characters: "G" followed by 3 digits.

    >>> is_valid_guest_id("G001")
    True
    >>> is_valid_guest_id("g001")
    False
    >>> is_valid_guest_id("G01")
    False
    >>> is_valid_guest_id("GABC")
    False

    Hint: len(), startswith(), and str.isdigit() on a slice.
    """
    raise NotImplementedError


def compound_balance(principal, rate, years):
    """Grow `principal` by `rate` once per year for `years` years, using a loop.
    Round the final answer to 2 decimals.

    >>> compound_balance(1000, 0.05, 2)
    1102.5
    """
    raise NotImplementedError


def digits_sum(n):
    """Sum the digits of a non-negative integer using a while loop
    (use % 10 and // 10, not str()).

    >>> digits_sum(1234)
    10
    >>> digits_sum(0)
    0
    """
    raise NotImplementedError


def attempts_until_success(results):
    """`results` is a list of booleans: the outcome of each connection attempt.
    Return how many attempts it took to get the first True (1-based).
    Return -1 if every attempt failed.

    >>> attempts_until_success([False, False, True, False])
    3
    >>> attempts_until_success([False, False])
    -1
    """
    raise NotImplementedError
