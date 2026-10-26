"""YOUR tests. Write at least 8.

Steps:
1. Create my_functions.py in this folder and copy in some functions you wrote earlier
   (e.g. normalize_outlet, parse_amount, is_valid_guest_id, split_valid_invalid).
2. Uncomment the import below and write tests.
3. Include at least one @pytest.mark.parametrize, one pytest.raises, and one fixture.
4. Run:  python check.py 11

The examples below are commented out so this file runs cleanly until you start.
"""
# import sys
# from pathlib import Path
# sys.path.insert(0, str(Path(__file__).parent))
# import pytest
# from my_functions import normalize_outlet, parse_amount
#
#
# @pytest.fixture
# def messy_outlets():
#     return [" bar", "The Bar", "RESTO"]
#
#
# def test_normalize_outlet_known_variant():
#     assert normalize_outlet(" the BAR ") == "Bar"
#
#
# @pytest.mark.parametrize("text, expected", [("USD 1,250.50", 1250.5), ("PHP 300", 300.0)])
# def test_parse_amount(text, expected):
#     assert parse_amount(text) == expected
