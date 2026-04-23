# tests/aliases/test_calendar.py
# B-032 stdlib aliases — calendar module tests
#
# "روزنامه" wraps Python's `calendar` module.
# Key normalization: هل_كبيسة → هل_كبيسه, ايام_كبيسة → ايام_كبيسه

import calendar
import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def روزنامه():
    """Return a ModuleProxy wrapping `calendar`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("روزنامه", None, None)
    assert spec is not None, "AliasFinder did not find 'روزنامه'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestCalendarProxy:
    def test_isleap_alias(self, روزنامه):
        """هل_كبيسه maps to calendar.isleap."""
        assert روزنامه.هل_كبيسه is calendar.isleap

    def test_isleap_correct_years(self, روزنامه):
        """هل_كبيسه identifies leap years correctly."""
        assert روزنامه.هل_كبيسه(2024) is True
        assert روزنامه.هل_كبيسه(2100) is False
        assert روزنامه.هل_كبيسه(2000) is True

    def test_leapdays_alias(self, روزنامه):
        """ايام_كبيسه maps to calendar.leapdays."""
        assert روزنامه.ايام_كبيسه is calendar.leapdays

    def test_leapdays_count(self, روزنامه):
        """ايام_كبيسه(2000, 2025) counts leap years in range."""
        # Leap years between 2000 and 2025: 2000, 2004, 2008, 2012, 2016, 2020, 2024
        count = روزنامه.ايام_كبيسه(2000, 2025)
        assert count == 7

    def test_monthrange_alias(self, روزنامه):
        """ايام_الشهر maps to calendar.monthrange."""
        assert روزنامه.ايام_الشهر is calendar.monthrange

    def test_monthrange_january_2026(self, روزنامه):
        """ايام_الشهر(2026, 1) returns (weekday_of_1st, days_in_month)."""
        weekday, days = روزنامه.ايام_الشهر(2026, 1)
        assert days == 31
        assert 0 <= weekday <= 6

    def test_month_name_alias(self, روزنامه):
        """اسماء_الاشهر maps to calendar.month_name."""
        assert روزنامه.اسماء_الاشهر is calendar.month_name

    def test_month_name_january(self, روزنامه):
        """اسماء_الاشهر[1] is 'January'."""
        assert روزنامه.اسماء_الاشهر[1] == "January"

    def test_day_name_alias(self, روزنامه):
        """اسماء_الايام maps to calendar.day_name."""
        assert روزنامه.اسماء_الايام is calendar.day_name

    def test_day_name_monday(self, روزنامه):
        """اسماء_الايام[0] is 'Monday'."""
        assert روزنامه.اسماء_الايام[0] == "Monday"

    def test_setfirstweekday_alias(self, روزنامه):
        """ضع_يوم_البدايه maps to calendar.setfirstweekday."""
        assert روزنامه.ضع_يوم_البدايه is calendar.setfirstweekday

    def test_month_display_alias(self, روزنامه):
        """عرض_شهر maps to calendar.month (formatting function)."""
        assert روزنامه.عرض_شهر is calendar.month

    def test_month_display_contains_year(self, روزنامه):
        """عرض_شهر(2026, 1) returns a string containing '2026' and 'January'."""
        output = روزنامه.عرض_شهر(2026, 1)
        assert "2026" in output
        assert "January" in output
