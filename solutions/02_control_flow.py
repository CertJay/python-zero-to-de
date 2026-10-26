"""Reference solutions for Module 02."""


def charge_category(amount):
    if amount < 0:
        return "refund"
    elif amount == 0:
        return "complimentary"
    elif amount <= 50:
        return "small"
    elif amount <= 200:
        return "medium"
    else:
        return "large"


def loyalty_tier(nights):
    if nights >= 30:
        return "Platinum"
    elif nights >= 15:
        return "Gold"
    elif nights >= 5:
        return "Silver"
    return "Bronze"


def fizzbuzz(n):
    out = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            out.append("FizzBuzz")
        elif i % 3 == 0:
            out.append("Fizz")
        elif i % 5 == 0:
            out.append("Buzz")
        else:
            out.append(str(i))
    return out


def sum_to(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


def count_vowels(text):
    count = 0
    for ch in text.lower():
        if ch in "aeiou":
            count += 1
    return count


def first_negative_index(amounts):
    for i, amount in enumerate(amounts):
        if amount < 0:
            return i
    return -1


def largest(numbers):
    if not numbers:
        return None
    best = numbers[0]
    for n in numbers[1:]:
        if n > best:
            best = n
    return best


def is_valid_guest_id(guest_id):
    return len(guest_id) == 4 and guest_id.startswith("G") and guest_id[1:].isdigit()


def compound_balance(principal, rate, years):
    balance = principal
    for _ in range(years):
        balance = balance * (1 + rate)
    return round(balance, 2)


def digits_sum(n):
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total


def attempts_until_success(results):
    for attempt, ok in enumerate(results, start=1):
        if ok:
            return attempt
    return -1
