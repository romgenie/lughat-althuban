# tests/aliases/test_stdlib_B039_cross_consistency.py
# B-039 cross-consistency — subprocess, shutil, argparse, secrets, uuid
#
# Verifies no Arabic name collisions between B-039 modules and all
# earlier B-batch modules (B-030 through B-038), and that the five
# B-039 modules don't collide with each other.
#
# Known intentional overlaps: none.

import itertools
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
]

NEW_MODULES = [
    "عملية_فرعية",
    "ادوات_ملفات",
    "محلل_وسائط",
    "اسرار",
    "معرفات_فريده",
]


@pytest.mark.parametrize(
    "new_mod,earlier_mod",
    [(n, e) for n in NEW_MODULES for e in EARLIER_MODULES],
)
def test_no_collision_with_earlier_batches(new_mod, earlier_mod):
    """B-039 module shares no Arabic entry keys with an earlier batch module."""
    new_keys = _load_keys(new_mod)
    earlier_keys = _load_keys(earlier_mod)
    overlap = new_keys & earlier_keys
    assert not overlap, f"Collision between {new_mod} and {earlier_mod}: {overlap}"


@pytest.mark.parametrize(
    "mod_a,mod_b",
    list(itertools.combinations(NEW_MODULES, 2)),
)
def test_no_collision_within_b039(mod_a, mod_b):
    """B-039 modules don't collide with each other."""
    keys_a = _load_keys(mod_a)
    keys_b = _load_keys(mod_b)
    overlap = keys_a & keys_b
    assert not overlap, f"Collision between {mod_a} and {mod_b}: {overlap}"
