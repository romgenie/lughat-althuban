# tests/aliases/test_datetime.py
# B-032 stdlib aliases — datetime module tests
#
# Key mapping notes:
#   مكتبة_تاريخ.الان()          ≡ datetime.datetime.now()        (naive)
#   مكتبة_تاريخ.الان(عالمي)     ≡ datetime.datetime.now(utc)     (aware)
#   مكتبة_تاريخ.نسق_ايزو(dt)   ≡ datetime.datetime.isoformat(dt) (unbound)
#   مكتبة_تاريخ.عالمي           ≡ datetime.timezone.utc           (singleton)

import datetime
import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def مكتبة_تاريخ():
    """Return a ModuleProxy wrapping `datetime`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("مكتبة_تاريخ", None, None)
    assert spec is not None, "AliasFinder did not find 'مكتبة_تاريخ'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestDatetimeProxy:
    # ── Class aliases ─────────────────────────────────────────────────────────

    def test_date_class_alias(self, مكتبة_تاريخ):
        """تاريخ maps to datetime.date."""
        assert مكتبة_تاريخ.تاريخ is datetime.date

    def test_time_class_alias(self, مكتبة_تاريخ):
        """وقت maps to datetime.time."""
        assert مكتبة_تاريخ.وقت is datetime.time

    def test_datetime_class_alias(self, مكتبة_تاريخ):
        """تاريخ_وقت maps to datetime.datetime."""
        assert مكتبة_تاريخ.تاريخ_وقت is datetime.datetime

    def test_timedelta_class_alias(self, مكتبة_تاريخ):
        """فرق_زمني maps to datetime.timedelta."""
        assert مكتبة_تاريخ.فرق_زمني is datetime.timedelta

    def test_timezone_class_alias(self, مكتبة_تاريخ):
        """نطاق_زمني maps to datetime.timezone."""
        assert مكتبة_تاريخ.نطاق_زمني is datetime.timezone

    def test_utc_singleton(self, مكتبة_تاريخ):
        """عالمي resolves to datetime.timezone.utc via dotted path."""
        assert مكتبة_تاريخ.عالمي is datetime.UTC

    # ── Class-method aliases ──────────────────────────────────────────────────

    def test_now_returns_datetime(self, مكتبة_تاريخ):
        """الان() calls datetime.datetime.now() and returns a datetime instance."""
        dt = مكتبة_تاريخ.الان()
        assert isinstance(dt, datetime.datetime)

    def test_now_with_utc_is_aware(self, مكتبة_تاريخ):
        """الان(عالمي) returns a timezone-aware datetime in UTC."""
        dt = مكتبة_تاريخ.الان(مكتبة_تاريخ.عالمي)
        assert dt.tzinfo is not None
        assert dt.tzinfo is datetime.UTC

    def test_today_returns_date(self, مكتبة_تاريخ):
        """اليوم() calls date.today() and returns today's date."""
        d = مكتبة_تاريخ.اليوم()
        assert isinstance(d, datetime.date)

    def test_strptime_parses_date_string(self, مكتبة_تاريخ):
        """حلل_نص parses a date string into a datetime object."""
        dt = مكتبة_تاريخ.حلل_نص("2026-04-23", "%Y-%m-%d")
        assert dt.year == 2026
        assert dt.month == 4
        assert dt.day == 23

    def test_fromisoformat_roundtrip(self, مكتبة_تاريخ):
        """من_ايزو parses an ISO 8601 string into a datetime."""
        dt = مكتبة_تاريخ.من_ايزو("2026-04-23T12:00:00")
        assert dt.year == 2026
        assert dt.hour == 12

    def test_combine_date_and_time(self, مكتبة_تاريخ):
        """ادمج combines a date and a time into a datetime."""
        d = datetime.date(2026, 1, 15)
        t = datetime.time(9, 30)
        dt = مكتبة_تاريخ.ادمج(d, t)
        assert isinstance(dt, datetime.datetime)
        assert dt.day == 15
        assert dt.hour == 9
        assert dt.minute == 30

    # ── Arithmetic ────────────────────────────────────────────────────────────

    def test_timedelta_date_arithmetic(self, مكتبة_تاريخ):
        """date + timedelta works with Arabic aliases."""
        d1 = مكتبة_تاريخ.تاريخ(2023, 1, 1)
        delta = مكتبة_تاريخ.فرق_زمني(days=1)
        d2 = d1 + delta
        assert d2 == datetime.date(2023, 1, 2)

    def test_timedelta_subtraction(self, مكتبة_تاريخ):
        """Two datetime objects subtracted give a timedelta."""
        dt1 = datetime.datetime(2026, 1, 1, 12, 0)
        dt2 = datetime.datetime(2026, 1, 1, 11, 0)
        diff = dt1 - dt2
        assert diff == datetime.timedelta(hours=1)

    # ── Unbound instance method aliases ───────────────────────────────────────

    def test_isoformat_unbound(self, مكتبة_تاريخ):
        """نسق_ايزو is datetime.isoformat (unbound); calling it works."""
        dt = datetime.datetime(2026, 4, 23, 12, 0, 0)
        iso = مكتبة_تاريخ.نسق_ايزو(dt)
        assert iso == "2026-04-23T12:00:00"

    def test_strftime_unbound(self, مكتبة_تاريخ):
        """نسق_نص is datetime.strftime (unbound); formats a datetime."""
        dt = datetime.datetime(2026, 4, 23)
        result = مكتبة_تاريخ.نسق_نص(dt, "%Y/%m/%d")
        assert result == "2026/04/23"

    def test_weekday_unbound(self, مكتبة_تاريخ):
        """يوم_الاسبوع returns the weekday as integer (0=Monday…6=Sunday)."""
        dt = datetime.datetime(2026, 4, 20)  # Monday
        assert مكتبة_تاريخ.يوم_الاسبوع(dt) == 0

    def test_replace_datetime_unbound(self, مكتبة_تاريخ):
        """استبدل_وقت creates a new datetime with specific fields replaced."""
        dt = datetime.datetime(2026, 4, 23, 12, 0)
        dt2 = مكتبة_تاريخ.استبدل_وقت(dt, year=2027, hour=15)
        assert dt2.year == 2027
        assert dt2.hour == 15
        assert dt2.month == 4  # unchanged

    def test_date_isoformat_unbound(self, مكتبة_تاريخ):
        """تاريخ_ايزو is date.isoformat (unbound)."""
        d = datetime.date(2026, 4, 23)
        assert مكتبة_تاريخ.تاريخ_ايزو(d) == "2026-04-23"
