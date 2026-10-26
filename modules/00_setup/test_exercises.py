from course_tools.loader import load

ex = load(__file__)


def test_greet():
    assert ex.greet("Miguel") == "Hello, Miguel! Ready to build pipelines."
    assert ex.greet("Ana") == "Hello, Ana! Ready to build pipelines."


def test_minutes_to_hours():
    assert ex.minutes_to_hours(90) == 1.5
    assert ex.minutes_to_hours(100) == 1.67
    assert ex.minutes_to_hours(0) == 0


def test_describe_me():
    me = ex.describe_me()
    assert isinstance(me, dict), "describe_me must return a dict"
    for key in ("name", "role", "goal"):
        assert key in me, f"missing key: {key}"
        assert isinstance(me[key], str) and me[key].strip(), f"{key} must be a non-empty string"
