# tests/aliases/test_stdlib_B057_B058_B059_cross_consistency.py
# B-057 / B-058 / B-059 cross-consistency
#
# Verifies no Arabic key collisions between the three new packets
# (seaborn / scipy / aiohttp) and every earlier alias module.

import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


def _load_keys(arabic_module_name: str) -> set[str]:
    from arabicpython.aliases._finder import AliasFinder
    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec(arabic_module_name, None, None)
    if spec is None:
        pytest.skip(f"Module alias {arabic_module_name!r} not found")
    proxy = spec.loader.create_module(spec)
    return set(proxy._mapping.keys())


# All modules shipped before B-057
EARLIER_MODULES = [
    # B-010 / B-011 / B-012 / B-013
    "فلاسك",
    "واجهه_برمجيه",       # FastAPI — normalized from واجهه_سريعه if needed
    "جانغو",
    "نماذج_جانغو",
    "قالب_بيانات",
    "نموذج_كائنات",
    # B-014
    "طلبات",
    # B-015
    "اختبار",
    # B-016 / B-017
    "نمباي",
    "بانداس",
    # B-018
    "صوره",
    # B-019 — matplotlib uses رسم_مخططات
    "رسم_مخططات",
    # B-020
    "تعلم_الي",
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
    # B-039
    "عملية_فرعية",
    "ادوات_ملفات",
    "محلل_وسائط",
    "اسرار",
    "معرفات_فريده",
]

NEW_MODULES = [
    "رسوم_احصائيه",   # seaborn  B-057
    "علوم_حسابيه",    # scipy    B-058
    "طلبات_غير_متزامنه",  # aiohttp  B-059
]


@pytest.mark.parametrize(
    "new_mod,earlier_mod",
    [(n, e) for n in NEW_MODULES for e in EARLIER_MODULES],
)
def test_no_collision_with_earlier_batches(new_mod, earlier_mod):
    new_keys = _load_keys(new_mod)
    earlier_keys = _load_keys(earlier_mod)
    overlap = new_keys & earlier_keys
    assert not overlap, (
        f"Arabic key collision between {new_mod!r} and {earlier_mod!r}: {overlap}"
    )


@pytest.mark.parametrize(
    "mod_a,mod_b",
    [
        ("رسوم_احصائيه", "علوم_حسابيه"),
        ("رسوم_احصائيه", "طلبات_غير_متزامنه"),
        ("علوم_حسابيه", "طلبات_غير_متزامنه"),
    ],
)
def test_no_collision_among_new_modules(mod_a, mod_b):
    keys_a = _load_keys(mod_a)
    keys_b = _load_keys(mod_b)
    overlap = keys_a & keys_b
    assert not overlap, (
        f"Arabic key collision between {mod_a!r} and {mod_b!r}: {overlap}"
    )
