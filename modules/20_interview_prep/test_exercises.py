import random
import time

from course_tools.loader import load

ex = load(__file__)


def test_two_sum():
    assert ex.two_sum([25, 120, 80, 40], 105) == (0, 2)
    assert ex.two_sum([3, 3], 6) == (0, 1)
    assert ex.two_sum([1, 2], 10) is None


def test_two_sum_is_fast():
    nums = list(range(200_000))
    start = time.perf_counter()
    assert ex.two_sum(nums, 399_997) == (199_998, 199_999)
    assert time.perf_counter() - start < 1.0, "use a dict for O(n)"


def test_is_anagram():
    assert ex.is_anagram("Dormitory", "Dirty room") is True
    assert ex.is_anagram("bar", "bra") is True
    assert ex.is_anagram("bar", "barr") is False


def test_first_unique_char():
    assert ex.first_unique_char("barbarian") == 6
    assert ex.first_unique_char("aabb") == -1
    assert ex.first_unique_char("") == -1


def test_merge_intervals():
    assert ex.merge_intervals([[5, 8], [1, 3], [2, 4], [8, 10]]) == [[1, 4], [5, 10]]
    assert ex.merge_intervals([]) == []
    assert ex.merge_intervals([[1, 10], [2, 3]]) == [[1, 10]]


def test_group_anagrams():
    assert ex.group_anagrams(["tea", "eat", "bar", "ate", "bra"]) == [["ate", "eat", "tea"], ["bar", "bra"]]
    assert ex.group_anagrams([]) == []


def test_top_k_frequent():
    assert ex.top_k_frequent(["Bar", "Spa", "Bar", "Cafe", "Spa", "Bar"], 2) == ["Bar", "Spa"]
    assert ex.top_k_frequent(["b", "a", "c"], 2) == ["a", "b"]


def test_valid_brackets():
    assert ex.valid_brackets("{ids: [1, 2, (3)]}") is True
    assert ex.valid_brackets("(]") is False
    assert ex.valid_brackets("((") is False
    assert ex.valid_brackets(")(") is False
    assert ex.valid_brackets("") is True


def test_longest_unique_substring():
    assert ex.longest_unique_substring("abcabcbb") == 3
    assert ex.longest_unique_substring("bbbb") == 1
    assert ex.longest_unique_substring("pwwkew") == 3
    assert ex.longest_unique_substring("") == 0


def test_max_subarray_sum():
    assert ex.max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert ex.max_subarray_sum([-3, -1, -2]) == -1
    assert ex.max_subarray_sum([5]) == 5


def test_missing_numbers():
    assert ex.missing_numbers([1001, 1003, 1004, 1007], 1001, 1007) == [1002, 1005, 1006]
    assert ex.missing_numbers([1, 2, 3], 1, 3) == []


def test_flatten_json():
    obj = {"guest": {"id": "G001", "tags": ["vip", "repeat"]}, "amount": 25}
    assert ex.flatten_json(obj) == {"guest.id": "G001", "guest.tags.0": "vip", "guest.tags.1": "repeat", "amount": 25}
    assert ex.flatten_json({"a": {"b": {"c": 1}}, "e": {}}, sep="_") == {"a_b_c": 1}
    assert ex.flatten_json({"l": [{"x": 1}, {"x": 2}]}) == {"l.0.x": 1, "l.1.x": 2}


def test_merge_sorted():
    assert ex.merge_sorted([1, 4, 9], [2, 3, 10]) == [1, 2, 3, 4, 9, 10]
    assert ex.merge_sorted([], [1]) == [1]
    assert ex.merge_sorted([1, 1], [1]) == [1, 1, 1]


def test_rolling_average():
    assert ex.rolling_average([10, 20, 30, 40], 2) == [15.0, 25.0, 35.0]
    assert ex.rolling_average([1, 2, 4], 3) == [2.33]
    assert ex.rolling_average([1, 2], 3) == []


def test_dedupe_latest():
    recs = [{"id": 2, "ts": 2, "v": "c"}, {"id": 1, "ts": 1, "v": "a"}, {"id": 1, "ts": 3, "v": "b"},
            {"id": 2, "ts": 2, "v": "d"}]
    assert ex.dedupe_latest(recs, "id", "ts") == [{"id": 1, "ts": 3, "v": "b"}, {"id": 2, "ts": 2, "v": "d"}]


def test_diff_records():
    old = [{"id": 1, "tier": "Gold"}, {"id": 2, "tier": "Silver"}, {"id": 3, "tier": "Bronze"}]
    new = [{"id": 1, "tier": "Gold"}, {"id": 2, "tier": "Gold"}, {"id": 4, "tier": "Silver"}]
    assert ex.diff_records(old, new, "id") == {"added": [4], "removed": [3], "changed": [2]}


def test_parse_csv_line():
    assert ex.parse_csv_line('G001,"Santos, Ana","He said ""hi""",25') == ["G001", "Santos, Ana", 'He said "hi"', "25"]
    assert ex.parse_csv_line("a,,b") == ["a", "", "b"]
    assert ex.parse_csv_line("") == [""]
    assert ex.parse_csv_line('"x",') == ["x", ""]


def test_compress_runs():
    assert ex.compress_runs("aaabcc") == "a3b1c2"
    assert ex.compress_runs("") == ""
    assert ex.compress_runs("z") == "z1"


def test_binary_search():
    data = [3, 8, 15, 21, 40]
    for i, v in enumerate(data):
        assert ex.binary_search(data, v) == i
    assert ex.binary_search(data, 9) == -1
    assert ex.binary_search([], 1) == -1
    big = list(range(0, 2_000_000, 2))
    assert ex.binary_search(big, 1_234_568) == 617_284


def test_sessionize():
    ts = ["2026-10-01T08:00:00", "2026-10-01T08:20:00", "2026-10-01T09:00:00",
          "2026-10-01T09:30:00", "2026-10-01T10:00:01"]
    assert ex.sessionize(ts) == [1, 1, 2, 2, 3]
    assert ex.sessionize([]) == []
    assert ex.sessionize(ts, gap_minutes=60) == [1, 1, 1, 1, 1]


def test_second_highest():
    assert ex.second_highest([120, 80, 120, 40]) == 80
    assert ex.second_highest([5, 5]) is None
    assert ex.second_highest([]) is None


def test_pivot_records():
    recs = [{"d": "Oct1", "o": "Bar", "a": 5}, {"d": "Oct1", "o": "Bar", "a": 2},
            {"d": "Oct1", "o": "Spa", "a": 9}, {"d": "Oct2", "o": "Bar", "a": 1}]
    assert ex.pivot_records(recs, "d", "o", "a") == {"Oct1": {"Bar": 7, "Spa": 9}, "Oct2": {"Bar": 1}}


def test_random_cross_checks():
    rng = random.Random(7)
    for _ in range(50):
        values = [rng.randint(-50, 50) for _ in range(rng.randint(1, 30))]
        best = max(sum(values[i:j]) for i in range(len(values)) for j in range(i + 1, len(values) + 1))
        assert ex.max_subarray_sum(values) == best
        a, b = sorted(rng.sample(range(100), 5)), sorted(rng.sample(range(100), 7))
        assert ex.merge_sorted(a, b) == sorted(a + b)
