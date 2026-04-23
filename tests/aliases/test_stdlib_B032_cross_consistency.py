# tests/aliases/test_stdlib_B032_cross_consistency.py
# B-032 cross-consistency tests
#
# Verifies deliberate naming divergences across datetime / time / calendar
# and with B-030/B-031 modules.

import pathlib

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"

KNOWN_DIVERGENCES = {
    # The `time` module's time() function vs datetime.time class:
    # Different Arabic names avoid confusion between the epoch float and the class.
    "time.time() vs datetime.time class": (
        "وقت_حالي",  # time.time() → epoch float
        "وقت",  # datetime.time → class
    ),
    # The `time` module's timezone (integer offset) vs datetime.timezone (class):
    "time.timezone (int) vs datetime.timezone (class)": (
        "ازاحه",  # time.timezone integer offset
        "نطاق_زمني",  # datetime.timezone class
    ),
    # sleep (blocking) has a dedicated name different from any clock function:
    "time.sleep vs time.time": (
        "نمه",  # sleep
        "وقت_حالي",  # time()
    ),
}


def _proxy(arabic_name: str):
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec(arabic_name, None, None)
    assert spec is not None, f"AliasFinder did not find {arabic_name!r}"
    return spec.loader.create_module(spec)


class TestB032CrossConsistency:
    def test_time_function_vs_datetime_time_differ(self):
        """وقت_حالي (time.time fn) ≠ وقت (datetime.time class): distinct names."""
        fn_ar, cls_ar = KNOWN_DIVERGENCES["time.time() vs datetime.time class"]
        assert fn_ar != cls_ar

        وقت_نظام = _proxy("وقت_نظام")
        مكتبة_تاريخ = _proxy("مكتبة_تاريخ")

        import datetime as _dt
        import time as _t

        assert وقت_نظام.وقت_حالي is _t.time
        assert مكتبة_تاريخ.وقت is _dt.time

    def test_time_timezone_int_vs_datetime_timezone_class(self):
        """ازاحه (time.timezone int) ≠ نطاق_زمني (datetime.timezone class)."""
        int_ar, cls_ar = KNOWN_DIVERGENCES["time.timezone (int) vs datetime.timezone (class)"]
        assert int_ar != cls_ar

        وقت_نظام = _proxy("وقت_نظام")
        مكتبة_تاريخ = _proxy("مكتبة_تاريخ")

        import datetime as _dt
        import time as _t

        assert وقت_نظام.ازاحه is _t.timezone
        assert مكتبة_تاريخ.نطاق_زمني is _dt.timezone

    def test_sleep_vs_time_function_differ(self):
        """نمه (sleep) ≠ وقت_حالي (time function): clearly different purposes."""
        sleep_ar, time_ar = KNOWN_DIVERGENCES["time.sleep vs time.time"]
        assert sleep_ar != time_ar

    def test_no_collision_with_B030_B031_names(self):
        """B-032 Arabic names do not clash with B-030 or B-031 names."""
        b030_proxies = ("نظام_تشغيل", "مسار_مكتبه", "نظام")
        b031_proxies = ("مجموعات", "ادوات_تكرار", "ادوات_داليه")
        b032_proxies = ("مكتبة_تاريخ", "وقت_نظام", "روزنامه")

        def arabic_names_of(proxy_name):
            try:
                proxy = _proxy(proxy_name)
                return {n for n in dir(proxy) if any("\u0600" <= c <= "\u06ff" for c in n)}
            except AssertionError:
                return set()

        earlier = set()
        for name in b030_proxies + b031_proxies:
            earlier |= arabic_names_of(name)

        b032_all = set()
        for name in b032_proxies:
            b032_all |= arabic_names_of(name)

        collisions = earlier & b032_all
        assert not collisions, f"Arabic name collision between B-030/B-031 and B-032: {collisions}"
