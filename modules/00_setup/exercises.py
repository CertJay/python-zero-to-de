"""Module 00 exercises. Replace each `raise NotImplementedError` with your code.

Run:  python check.py 00
"""


from unicodedata import name


def greet(name):
    """Return a greeting for `name`.

    >>> greet("Miguel")
    'Hello, Miguel! Ready to build pipelines.'

    Hint: use an f-string: f"Hello, {name}! ..."
    """
    return f"Hello, {name}! Ready to build pipelines."


def minutes_to_hours(minutes):
    """Convert minutes to hours, rounded to 2 decimal places.

    >>> minutes_to_hours(90)
    1.5
    >>> minutes_to_hours(100)
    1.67

    Hint: divide by 60, then use round(value, 2).
    """
    return round(minutes / 60, 2)


def describe_me():
    """Return a dictionary with three keys: "name", "role", "goal".

    Each value must be a non-empty string about YOU. Example shape:

    {"name": "Miguel", "role": "Business Analyst", "goal": "Data Engineer by 2027"}
    """
    return {
        "name": "Miguel",
        "role": "Business Analyst",
        "goal": "Data Engineer by 2027"
    }
