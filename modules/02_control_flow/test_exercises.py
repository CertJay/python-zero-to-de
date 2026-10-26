from course_tools.loader import load

ex = load(__file__)


def test_charge_category():
    cases = {-10: "refund", 0: "complimentary", 0.5: "small", 50: "small", 50.01: "medium",
             200: "medium", 200.01: "large", 9999: "large"}
    for amount, expected in cases.items():
        assert ex.charge_category(amount) == expected, f"charge_category({amount})"


def test_loyalty_tier():
    cases = {0: "Bronze", 4: "Bronze", 5: "Silver", 14: "Silver", 15: "Gold", 29: "Gold", 30: "Platinum", 120: "Platinum"}
    for nights, expected in cases.items():
        assert ex.loyalty_tier(nights) == expected, f"loyalty_tier({nights})"


def test_fizzbuzz():
    assert ex.fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]
    result = ex.fizzbuzz(15)
    assert len(result) == 15
    assert result[14] == "FizzBuzz"
    assert result[8] == "Fizz"
    assert ex.fizzbuzz(0) == []


def test_sum_to():
    assert ex.sum_to(4) == 10
    assert ex.sum_to(100) == 5050
    assert ex.sum_to(0) == 0


def test_count_vowels():
    assert ex.count_vowels("Onboard Spa") == 4
    assert ex.count_vowels("AEIOU aeiou") == 10
    assert ex.count_vowels("rhythm") == 0


def test_first_negative_index():
    assert ex.first_negative_index([25, 120, -40, 80]) == 2
    assert ex.first_negative_index([-1, -2]) == 0
    assert ex.first_negative_index([1, 2]) == -1
    assert ex.first_negative_index([]) == -1


def test_largest():
    assert ex.largest([25, 410, 80]) == 410
    assert ex.largest([-5, -2, -9]) == -2
    assert ex.largest([7]) == 7
    assert ex.largest([]) is None


def test_is_valid_guest_id():
    assert ex.is_valid_guest_id("G001") is True
    assert ex.is_valid_guest_id("G999") is True
    for bad in ["g001", "G01", "G0001", "GABC", "X001", "", "G 01"]:
        assert ex.is_valid_guest_id(bad) is False, f"{bad!r} should be invalid"


def test_compound_balance():
    assert ex.compound_balance(1000, 0.05, 2) == 1102.5
    assert ex.compound_balance(500, 0.1, 0) == 500
    assert ex.compound_balance(100, 0.0, 5) == 100


def test_digits_sum():
    assert ex.digits_sum(1234) == 10
    assert ex.digits_sum(0) == 0
    assert ex.digits_sum(9) == 9
    assert ex.digits_sum(1000001) == 2


def test_attempts_until_success():
    assert ex.attempts_until_success([False, False, True, False]) == 3
    assert ex.attempts_until_success([True]) == 1
    assert ex.attempts_until_success([False, False]) == -1
    assert ex.attempts_until_success([]) == -1
