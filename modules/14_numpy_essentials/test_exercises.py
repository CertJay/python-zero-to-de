import numpy as np

from course_tools.loader import load

ex = load(__file__)


def test_apply_tax():
    out = ex.apply_tax([25, 120, 80], 0.12)
    assert isinstance(out, np.ndarray)
    assert out.tolist() == [28.0, 134.4, 89.6]


def test_label_charges():
    assert list(ex.label_charges([25, -5, 0])) == ["sale", "refund", "sale"]


def test_categorize():
    assert list(ex.categorize([-1, 0, 50, 51, 200, 201])) == \
        ["refund", "complimentary", "small", "medium", "medium", "large"]


def test_zscores():
    assert ex.zscores([2, 4, 4, 4, 5, 5, 7, 9]).tolist() == [-1.5, -0.5, -0.5, -0.5, 0.0, 0.0, 1.0, 2.0]
    assert ex.zscores([3, 3, 3]).tolist() == [0.0, 0.0, 0.0]


def test_iqr_outlier_indexes():
    values = [10, 12, 11, 13, 12, 95, 11, -40]
    assert ex.iqr_outlier_indexes(values) == [5, 7]
    assert isinstance(ex.iqr_outlier_indexes(values), list)
    assert ex.iqr_outlier_indexes([1, 2, 3]) == []


def test_moving_average():
    assert ex.moving_average([1, 2, 3, 4], 2).tolist() == [1.5, 2.5, 3.5]
    assert ex.moving_average([10, 20, 30, 40, 50], 3).tolist() == [20.0, 30.0, 40.0]


def test_day_over_day_change():
    assert ex.day_over_day_change([100, 120, 90]).tolist() == [20, -30]


def test_outlet_totals():
    out = ex.outlet_totals([[25, 120, 0], [40, 0, 6]])
    assert out["per_outlet"].tolist() == [65, 120, 6]
    assert out["per_guest"].tolist() == [145, 46]


def test_percent_of_total():
    assert ex.percent_of_total([25, 75]).tolist() == [25.0, 75.0]
    assert ex.percent_of_total([1, 1, 1]).tolist() == [33.33, 33.33, 33.33]
