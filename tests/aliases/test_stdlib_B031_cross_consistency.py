# tests/aliases/test_stdlib_cross_consistency_B031.py
# B-031 cross-consistency tests
#
# Verifies deliberate naming divergences across collections / itertools /
# functools / B-030 modules.  Every test is a positive assertion:
# the name chosen is correct and any surface-level similarity to another
# module's name is intentional.

import pathlib

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"

# ---------------------------------------------------------------------------
# Documented divergences (spec floor for code review)
# ---------------------------------------------------------------------------

KNOWN_DIVERGENCES = {
    # itertools.chain → سلسله
    # collections.ChainMap → سلسلة_خرائط
    # Same root, different concepts: flattening vs dict overlay.
    "itertools.chain vs collections.ChainMap": (
        "سلسله",
        "سلسلة_خرائط",
    ),
    # itertools.count (infinite counter) → عداد_لانهائي
    # collections.Counter (counting multiset) → عداد
    # Both "count" concepts; Arabic disambiguates by adding لانهائي (infinite).
    "itertools.count vs collections.Counter": (
        "عداد_لانهائي",
        "عداد",
    ),
    # functools.reduce → اختزال  (fold / reduction)
    # functools.partial → جزيء  (particle / partial application)
    # Completely different operations; Arabic roots are distinct.
    "functools.reduce vs functools.partial": (
        "اختزال",
        "جزيء",
    ),
}


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _proxy(arabic_name: str):
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec(arabic_name, None, None)
    assert spec is not None, f"AliasFinder did not find {arabic_name!r}"
    return spec.loader.create_module(spec)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestB031CrossConsistency:
    def test_chain_vs_chain_map_names_differ(self):
        """سلسله (itertools.chain) ≠ سلسلة_خرائط (ChainMap): different names."""
        chain_ar, chain_map_ar = KNOWN_DIVERGENCES["itertools.chain vs collections.ChainMap"]
        assert chain_ar != chain_map_ar

        مجموعات = _proxy("مجموعات")
        ادوات_تكرار = _proxy("ادوات_تكرار")

        import collections as _col
        import itertools as _it

        assert ادوات_تكرار.سلسله is _it.chain
        assert مجموعات.سلسلة_خرائط is _col.ChainMap

    def test_count_vs_counter_names_differ(self):
        """عداد_لانهائي (itertools.count) ≠ عداد (Counter): names are distinct."""
        count_ar, counter_ar = KNOWN_DIVERGENCES["itertools.count vs collections.Counter"]
        assert count_ar != counter_ar

        مجموعات = _proxy("مجموعات")
        ادوات_تكرار = _proxy("ادوات_تكرار")

        import collections as _col
        import itertools as _it

        assert ادوات_تكرار.عداد_لانهائي is _it.count
        assert مجموعات.عداد is _col.Counter

    def test_reduce_vs_partial_names_differ(self):
        """اختزال (reduce) ≠ جزيء (partial): unrelated concepts."""
        reduce_ar, partial_ar = KNOWN_DIVERGENCES["functools.reduce vs functools.partial"]
        assert reduce_ar != partial_ar

        ادوات_داليه = _proxy("ادوات_داليه")

        import functools as _ft

        assert ادوات_داليه.اختزال is _ft.reduce
        assert ادوات_داليه.جزيء is _ft.partial

    def test_no_collision_with_B030_names(self):
        """None of the B-031 Arabic names clash with B-030 (os / pathlib / sys) names."""
        نظام_تشغيل = _proxy("نظام_تشغيل")
        مسار_مكتبه = _proxy("مسار_مكتبه")
        نظام = _proxy("نظام")

        b030_names = frozenset(dir(نظام_تشغيل)) | frozenset(dir(مسار_مكتبه)) | frozenset(dir(نظام))

        from arabicpython.aliases._finder import AliasFinder

        finder = AliasFinder(mappings_dir=ALIASES_DIR)
        b031_names = set()
        for module_arabic in ("مجموعات", "ادوات_تكرار", "ادوات_داليه"):
            spec = finder.find_spec(module_arabic, None, None)
            if spec is not None:
                b031_names.update(dir(spec.loader.create_module(spec)))

        # Only check Arabic names (non-ASCII identifiers)
        arabic_b030 = {n for n in b030_names if any("\u0600" <= c <= "\u06ff" for c in n)}
        arabic_b031 = {n for n in b031_names if any("\u0600" <= c <= "\u06ff" for c in n)}

        # There must be no exact collision between B-030 and B-031 Arabic names
        # (English pass-throughs like 'path', 'sep' are allowed to repeat)
        collisions = arabic_b030 & arabic_b031
        assert not collisions, (
            f"Arabic name collision between B-030 and B-031: {collisions}\n"
            f"Each Arabic name must be unique across module proxies."
        )
