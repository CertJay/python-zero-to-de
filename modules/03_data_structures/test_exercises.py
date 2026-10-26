import copy

from course_tools.loader import load

ex = load(__file__)

CHARGES = [
    {"guest_id": "G002", "outlet": "Bar", "amount": 40.5},
    {"guest_id": "G001", "outlet": "Bar", "amount": 25.0},
    {"guest_id": "G001", "outlet": "Spa", "amount": 120.0},
    {"guest_id": "G003", "outlet": "Restaurant", "amount": 80.1},
    {"guest_id": "G002", "outlet": "Spa", "amount": 120.0},
    {"guest_id": "G001", "outlet": "Restaurant", "amount": 0.2},
]


def test_total_by_outlet():
    original = copy.deepcopy(CHARGES)
    assert ex.total_by_outlet(CHARGES) == {"Bar": 65.5, "Spa": 240.0, "Restaurant": 80.3}
    assert CHARGES == original, "don't modify the input"
    assert ex.total_by_outlet([]) == {}


def test_unique_guests():
    assert ex.unique_guests(CHARGES) == ["G001", "G002", "G003"]
    assert ex.unique_guests([]) == []


def test_top_n_charges():
    top = ex.top_n_charges(CHARGES, 3)
    assert [c["amount"] for c in top] == [120.0, 120.0, 80.1]
    assert top[0]["guest_id"] == "G001", "ties keep original order"
    assert ex.top_n_charges(CHARGES, 0) == []
    assert len(ex.top_n_charges(CHARGES, 99)) == len(CHARGES)


def test_invert_mapping():
    assert ex.invert_mapping({"G001": "A214", "G002": "B110"}) == {"A214": "G001", "B110": "G002"}
    assert ex.invert_mapping({}) == {}


def test_merge_profiles():
    base = {"name": "Ana", "tier": "Silver"}
    updates = {"tier": "Gold", "cabin": "A214"}
    result = ex.merge_profiles(base, updates)
    assert result == {"name": "Ana", "tier": "Gold", "cabin": "A214"}
    assert base == {"name": "Ana", "tier": "Silver"}, "base must not change"
    assert result is not base


def test_common_outlets():
    assert ex.common_outlets(["Bar", "Spa", "Bar"], ["Spa", "Cafe", "Bar"]) == ["Bar", "Spa"]
    assert ex.common_outlets(["Bar"], ["Spa"]) == []


def test_missing_ids():
    assert ex.missing_ids(["G001", "G999", "G002", "G999"], ["G001", "G002", "G003"]) == ["G999"]
    assert ex.missing_ids(["G005", "G004"], []) == ["G004", "G005"]
    assert ex.missing_ids([], ["G001"]) == []


def test_squares_of_evens():
    assert ex.squares_of_evens([1, 2, 3, 4]) == [4, 16]
    assert ex.squares_of_evens([1, 3]) == []
    assert ex.squares_of_evens([0, -2]) == [0, 4]


def test_group_by():
    grouped = ex.group_by(CHARGES, "guest_id")
    assert set(grouped) == {"G001", "G002", "G003"}
    assert [c["outlet"] for c in grouped["G001"]] == ["Bar", "Spa", "Restaurant"]
    assert len(grouped["G002"]) == 2
    assert ex.group_by([], "x") == {}


def test_find_duplicates():
    assert ex.find_duplicates(["C1", "C2", "C1", "C3", "C2", "C1"]) == ["C1", "C2"]
    assert ex.find_duplicates([1, 2, 3]) == []


def test_chunk():
    assert ex.chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
    assert ex.chunk([1, 2, 3], 3) == [[1, 2, 3]]
    assert ex.chunk([], 4) == []
    assert ex.chunk(list(range(10)), 4)[-1] == [8, 9]


def test_flatten():
    assert ex.flatten([[1, 2], [3], [], [4, 5]]) == [1, 2, 3, 4, 5]
    assert ex.flatten([]) == []


def test_word_counts():
    assert ex.word_counts("Bar spa BAR cafe bar") == {"bar": 3, "spa": 1, "cafe": 1}
    assert ex.word_counts("  ") == {}


def test_rows_to_columns():
    assert ex.rows_to_columns([{"id": 1, "amt": 25}, {"id": 2, "amt": 40}]) == {"id": [1, 2], "amt": [25, 40]}
    assert ex.rows_to_columns([]) == {}


def test_columns_to_rows():
    assert ex.columns_to_rows({"id": [1, 2], "amt": [25, 40]}) == [{"id": 1, "amt": 25}, {"id": 2, "amt": 40}]
    assert ex.columns_to_rows({}) == []


def test_round_trip():
    rows = [{"a": i, "b": i * 2} for i in range(5)]
    assert ex.columns_to_rows(ex.rows_to_columns(rows)) == rows


def test_transpose():
    assert ex.transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    assert ex.transpose([[1]]) == [[1]]
