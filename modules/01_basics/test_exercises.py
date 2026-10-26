from course_tools.loader import load

ex = load(__file__)


def test_total_with_service_charge():
    assert ex.total_with_service_charge(100) == 110.0
    assert ex.total_with_service_charge(80, 0.12) == 89.6
    assert ex.total_with_service_charge(0) == 0


def test_split_bill():
    assert ex.split_bill(100, 3) == 33.33
    assert ex.split_bill(250, 2) == 125.0


def test_format_charge():
    assert ex.format_charge("G001", "Bar", 25) == "G001 | Bar | USD 25.00"
    assert ex.format_charge("G014", "Boutique", 1250.5) == "G014 | Boutique | USD 1,250.50"


def test_celsius_to_fahrenheit():
    assert ex.celsius_to_fahrenheit(30) == 86.0
    assert ex.celsius_to_fahrenheit(-5) == 23.0
    assert ex.celsius_to_fahrenheit(36.6) == 97.9


def test_is_even():
    assert ex.is_even(4) is True
    assert ex.is_even(7) is False
    assert ex.is_even(0) is True


def test_seconds_to_hms():
    assert ex.seconds_to_hms(3725) == "01:02:05"
    assert ex.seconds_to_hms(59) == "00:00:59"
    assert ex.seconds_to_hms(86399) == "23:59:59"


def test_initials():
    assert ex.initials("Miguel Jay Faustino") == "MJF"
    assert ex.initials("ana santos") == "AS"


def test_mask_card():
    assert ex.mask_card("4111222233334444") == "**** **** **** 4444"


def test_type_name():
    assert ex.type_name(5) == "int"
    assert ex.type_name("5") == "str"
    assert ex.type_name(2.5) == "float"
    assert ex.type_name(None) == "NoneType"
    assert ex.type_name(True) == "bool"


def test_parse_amount_text():
    assert ex.parse_amount_text(" 25.50 ") == 25.5
    assert ex.parse_amount_text("120") == 120.0
    assert isinstance(ex.parse_amount_text("7"), float)
