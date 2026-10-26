"""Reference solutions for Module 01."""


def total_with_service_charge(amount, rate=0.10):
    return round(amount * (1 + rate), 2)


def split_bill(total, people):
    return round(total / people, 2)


def format_charge(guest_id, outlet, amount):
    return f"{guest_id} | {outlet} | USD {amount:,.2f}"


def celsius_to_fahrenheit(c):
    return round(c * 9 / 5 + 32, 1)


def is_even(n):
    return n % 2 == 0


def seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def initials(full_name):
    return "".join(word[0].upper() for word in full_name.split())


def mask_card(card_number):
    return "**** **** **** " + card_number[-4:]


def type_name(value):
    return type(value).__name__


def parse_amount_text(text):
    return round(float(text.strip()), 2)
