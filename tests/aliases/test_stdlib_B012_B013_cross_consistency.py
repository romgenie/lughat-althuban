# tests/aliases/test_stdlib_B012_B013_cross_consistency.py
# B-012 / B-013 cross-consistency — django and sqlalchemy
#
# Verifies no Arabic name collisions between دجانغو / قاعده_علائقيه and all
# earlier B-batch modules (B-016/B-017 numpy/pandas, B-030..B-039 stdlib,
# plus the SDK aliases flask, requests, sqlite3) — and that the two new
# modules don't collide with each other.
#
# Known intentional overlaps: none.  Where the obvious Arabic term was
# already taken (e.g. خطا_تكامل by sqlite3, فهرس by pandas) the B-012/B-013
# TOMLs use a more specific variant — see the inline collision notes in
# django.toml / sqlalchemy.toml.

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


EARLIER_MODULES = [
    # B-016 / B-017 third-party stack
    "نمباي",
    "بانداس",
    # B-010 / B-011 / B-014 SDK aliases
    "فلاسك",
    "طلبات",
    # B-030 stdlib
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
    "قاعدة_بيانات",
    # B-034
    "تعابير_نمطيه",
    "نصوص",
    "تنسيق_نص",
    # B-035
    "رياضيات",
    "احصاء",
    "عشوائيات",
    # B-036
    "تسجيل",
    # B-037
    "اتزامن",
    # B-038
    "هاشلب",
    "مجاري",
    "مدير_سياق",
    # B-039
    "عملية_فرعية",
    "ادوات_ملفات",
    "محلل_وسائط",
    "اسرار",
    "معرفات_فريده",
]

NEW_MODULES = ["دجانغو", "قاعده_علائقيه"]


@pytest.mark.parametrize(
    "new_mod,earlier_mod",
    [(n, e) for n in NEW_MODULES for e in EARLIER_MODULES],
)
def test_no_collision_with_earlier_batches(new_mod, earlier_mod):
    """B-012/013 module shares no Arabic entry keys with an earlier batch."""
    new_keys = _load_keys(new_mod)
    earlier_keys = _load_keys(earlier_mod)
    overlap = new_keys & earlier_keys
    assert not overlap, f"Collision between {new_mod} and {earlier_mod}: {overlap}"


def test_no_collision_between_django_and_sqlalchemy():
    """دجانغو and قاعده_علائقيه don't collide with each other."""
    dj_keys = _load_keys("دجانغو")
    sa_keys = _load_keys("قاعده_علائقيه")
    overlap = dj_keys & sa_keys
    assert not overlap, f"Collision between دجانغو and قاعده_علائقيه: {overlap}"
