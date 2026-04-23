# tests/aliases/test_time.py
# B-032 stdlib aliases — time module tests
#
# "وقت_نظام" wraps Python's `time` module (NOT datetime.time).
# نمه → sleep, وقت_حالي → time(), عداد_الاداء → perf_counter, etc.

import pathlib
import time as _time

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def وقت_نظام():
    """Return a ModuleProxy wrapping `time`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("وقت_نظام", None, None)
    assert spec is not None, "AliasFinder did not find 'وقت_نظام'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestTimeProxy:
    def test_sleep_alias(self, وقت_نظام):
        """نمه maps to time.sleep."""
        assert وقت_نظام.نمه is _time.sleep

    def test_sleep_pauses_briefly(self, وقت_نظام):
        """نمه(0.05) pauses for approximately 50ms."""
        start = _time.perf_counter()
        وقت_نظام.نمه(0.05)
        elapsed = _time.perf_counter() - start
        assert elapsed >= 0.04, f"Sleep was too short: {elapsed:.3f}s"

    def test_time_function_alias(self, وقت_نظام):
        """وقت_حالي maps to time.time (the function)."""
        assert وقت_نظام.وقت_حالي is _time.time

    def test_time_returns_float(self, وقت_نظام):
        """وقت_حالي() returns a float timestamp."""
        t = وقت_نظام.وقت_حالي()
        assert isinstance(t, float)
        assert t > 1_700_000_000  # sanity: after Nov 2023

    def test_gmtime_alias(self, وقت_نظام):
        """وقت_عالمي maps to time.gmtime."""
        assert وقت_نظام.وقت_عالمي is _time.gmtime

    def test_gmtime_returns_struct_time(self, وقت_نظام):
        """وقت_عالمي() returns a struct_time with expected attributes."""
        st = وقت_نظام.وقت_عالمي()
        assert hasattr(st, "tm_year")
        assert st.tm_year >= 2026

    def test_localtime_alias(self, وقت_نظام):
        """وقت_محلي maps to time.localtime."""
        assert وقت_نظام.وقت_محلي is _time.localtime

    def test_perf_counter_alias(self, وقت_نظام):
        """عداد_الاداء maps to time.perf_counter."""
        assert وقت_نظام.عداد_الاداء is _time.perf_counter

    def test_perf_counter_increases(self, وقت_نظام):
        """عداد_الاداء() should increase between two calls."""
        t1 = وقت_نظام.عداد_الاداء()
        وقت_نظام.نمه(0.01)
        t2 = وقت_نظام.عداد_الاداء()
        assert t2 > t1

    def test_monotonic_alias(self, وقت_نظام):
        """وقت_رتيب maps to time.monotonic."""
        assert وقت_نظام.وقت_رتيب is _time.monotonic

    def test_ctime_alias(self, وقت_نظام):
        """نص_الوقت maps to time.ctime."""
        assert وقت_نظام.نص_الوقت is _time.ctime

    def test_struct_time_alias(self, وقت_نظام):
        """بنية_وقت maps to time.struct_time."""
        assert وقت_نظام.بنية_وقت is _time.struct_time

    def test_daylight_attribute(self, وقت_نظام):
        """توقيت_صيفي maps to time.daylight (0 or 1 integer)."""
        assert وقت_نظام.توقيت_صيفي is _time.daylight

    def test_mktime_alias(self, وقت_نظام):
        """اصنع_وقت maps to time.mktime."""
        assert وقت_نظام.اصنع_وقت is _time.mktime
