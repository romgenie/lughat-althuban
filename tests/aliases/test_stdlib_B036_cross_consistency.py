# tests/aliases/test_stdlib_B036_cross_consistency.py
# B-036 cross-consistency — logging
#
# Verifies no Arabic name collisions between تسجيل (logging) and all
# earlier B-batch modules (B-030 through B-035).

import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


def _load_keys(arabic_module_name: str) -> set[str]:
    """Return the set of Arabic entry keys for a given module alias name."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec(arabic_module_name, None, None)
    if spec is None:
        pytest.skip(f"Module alias {arabic_module_name!r} not found — skipping")
    proxy = spec.loader.create_module(spec)
    return set(proxy._mapping.keys())


# ── Documented divergences (logging uses some generic words) ──────────────────


def test_تسجيل_اغلق_vs_sqlite3_اغلق():
    """Both تسجيل (logging.shutdown) and قاعدة_بيانات (Connection.close) use اغلق.

    This is an intentional name collision: اغلق is the natural Arabic word for
    'close/shutdown'. The two usages are in completely separate module namespaces
    so there is no runtime conflict. Documented here as a conscious tradeoff.
    """
    logging_keys = _load_keys("تسجيل")
    sqlite_keys = _load_keys("قاعدة_بيانات")
    assert "اغلق" in logging_keys, "تسجيل must keep اغلق for logging.shutdown"
    assert "اغلق" in sqlite_keys, "قاعدة_بيانات must keep اغلق for Connection.close"
    # Both modules intentionally use the same word in separate namespaces


# ── B-036 vs earlier B-batches (excluding known intentional overlaps) ─────────

EARLIER_MODULES = [
    # B-030
    "نظام_تشغيل",
    "مسار_مكتبه",
    "نظام",
    # B-031
    "مجموعات",
    "ادوات_تكرار",
    "ادوات_داليه",
    # B-032
    "مكتبة_تاريخ",
    "وقت_نظام",
    "روزنامه",
    # B-033
    "جيسون",
    "ملفات_csv",
    # B-034
    "تعابير_نمطيه",
    "نصوص",
    "تنسيق_نص",
    # B-035
    "رياضيات",
    "احصاء",
    "عشوائيات",
]

# اغلق appears in both logging and sqlite3 (intentional) — excluded from
# parametrized check.  The sqlite3 module is tested in the dedicated test above.
INTENTIONAL_OVERLAPS = {"اغلق"}


@pytest.mark.parametrize("earlier_mod", EARLIER_MODULES)
def test_no_collision_with_earlier_batches(earlier_mod):
    """تسجيل shares no Arabic entry keys (beyond intentional overlaps)
    with an earlier batch module."""
    logging_keys = _load_keys("تسجيل")
    earlier_keys = _load_keys(earlier_mod)
    overlap = (logging_keys & earlier_keys) - INTENTIONAL_OVERLAPS
    assert not overlap, f"Unexpected collision between تسجيل and {earlier_mod}: {overlap}"
