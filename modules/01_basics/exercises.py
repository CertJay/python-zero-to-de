"""Module 01 exercises: values, variables, types, operators.

Run:  python check.py 01
"""


def total_with_service_charge(amount, rate=0.10):
    """Return amount plus a service charge, rounded to 2 decimals.

    >>> total_with_service_charge(100)
    110.0
    >>> total_with_service_charge(80, 0.12)
    89.6
    """
    raise NotImplementedError


def split_bill(total, people):
    """Split a bill equally. Round each share to 2 decimals.

    >>> split_bill(100, 3)
    33.33
    >>> split_bill(250, 2)
    125.0
    """
    raise NotImplementedError


def format_charge(guest_id, outlet, amount):
    """Return a formatted charge line: guest | outlet | USD amount with 2 decimals
    and a thousands separator.

    >>> format_charge("G001", "Bar", 25)
    'G001 | Bar | USD 25.00'
    >>> format_charge("G014", "Boutique", 1250.5)
    'G014 | Boutique | USD 1,250.50'
    """
    raise NotImplementedError


def celsius_to_fahrenheit(c):
    """Convert Celsius to Fahrenheit (F = C * 9/5 + 32), rounded to 1 decimal.

    >>> celsius_to_fahrenheit(30)
    86.0
    >>> celsius_to_fahrenheit(-5)
    23.0
    """
    raise NotImplementedError


def is_even(n):
    """Return True if n is even, otherwise False. Use the % operator.

    >>> is_even(4)
    True
    >>> is_even(7)
    False
    """
    raise NotImplementedError


def seconds_to_hms(seconds):
    """Convert a number of seconds into an "HH:MM:SS" string (zero-padded).

    Useful for printing how long a pipeline run took.

    >>> seconds_to_hms(3725)
    '01:02:05'
    >>> seconds_to_hms(59)
    '00:00:59'
    """
    raise NotImplementedError


def initials(full_name):
    """Return the uppercase initials of a full name.

    >>> initials("Miguel Jay Faustino")
    'MJF'
    >>> initials("ana santos")
    'AS'

    Hint: full_name.split() gives a list of words. Take [0] of each word.
    For now you may use a for loop or ''.join(...) - look ahead to Module 02 if needed.
    """
    raise NotImplementedError


def mask_card(card_number):
    """Mask a 16-digit card number, keeping only the last 4 digits.

    >>> mask_card("4111222233334444")
    '**** **** **** 4444'

    Hint: card_number[-4:] gives the last 4 characters.
    """
    raise NotImplementedError


def type_name(value):
    """Return the name of the value's type as a string.

    >>> type_name(5)
    'int'
    >>> type_name("5")
    'str'
    >>> type_name(None)
    'NoneType'

    Hint: type(value).__name__
    """
    raise NotImplementedError


def parse_amount_text(text):
    """Convert an amount stored as text into a float rounded to 2 decimals.
    The text may have spaces around it.

    >>> parse_amount_text(" 25.50 ")
    25.5
    >>> parse_amount_text("120")
    120.0
    """
    raise NotImplementedError
