# tests/aliases/test_functools.py
# B-031 stdlib aliases — functools module tests
#
# Arabic key round-trip notes:
#   أغلفة → اغلفه  (أ→ا at start, final ة→ه)
#   خاصية_محسوبة_مرة → خاصية_محسوبة_مره  (final ة→ه; ة mid-identifier stays)

import functools
import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def ادوات_داليه():
    """Return a ModuleProxy wrapping `functools`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("ادوات_داليه", None, None)
    assert spec is not None, "AliasFinder did not find 'ادوات_داليه'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestFunctoolsProxy:
    def test_partial_alias(self, ادوات_داليه):
        """جزيء maps to functools.partial."""
        assert ادوات_داليه.جزيء is functools.partial

    def test_partial_creates_specialised_callable(self, ادوات_داليه):
        """جزيء(pow, 2) creates a 2-power function."""
        قوه_اثنتين = ادوات_داليه.جزيء(pow, 2)
        assert قوه_اثنتين(8) == 256  # 2 ** 8

    def test_reduce_alias(self, ادوات_داليه):
        """اختزال maps to functools.reduce."""
        assert ادوات_داليه.اختزال is functools.reduce

    def test_reduce_sum(self, ادوات_داليه):
        """اختزال(lambda a,b: a+b, [1..5]) gives 15."""
        result = ادوات_داليه.اختزال(lambda a, b: a + b, [1, 2, 3, 4, 5])
        assert result == 15

    def test_lru_cache_alias(self, ادوات_داليه):
        """ذاكرة_مؤقتة_مؤخرا maps to functools.lru_cache."""
        assert ادوات_داليه.ذاكرة_مؤقتة_مؤخرا is functools.lru_cache

    def test_lru_cache_caches_calls(self, ادوات_داليه):
        """ذاكرة_مؤقتة_مؤخرا decorator caches repeated calls."""
        call_count = 0

        @ادوات_داليه.ذاكرة_مؤقتة_مؤخرا(maxsize=128)
        def مضاعف(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        مضاعف(5)
        مضاعف(5)  # cached — call_count stays 1
        assert call_count == 1
        مضاعف(6)
        assert call_count == 2

    def test_cache_alias(self, ادوات_داليه):
        """تخزين_مؤقت maps to functools.cache."""
        assert ادوات_داليه.تخزين_مؤقت is functools.cache

    def test_wraps_alias(self, ادوات_داليه):
        """اغلفه maps to functools.wraps."""
        assert ادوات_داليه.اغلفه is functools.wraps

    def test_wraps_preserves_metadata(self, ادوات_داليه):
        """اغلفه preserves __name__ and __doc__ of wrapped function."""

        def مزين(دالة):
            @ادوات_داليه.اغلفه(دالة)
            def غلاف(*args, **kwargs):
                return دالة(*args, **kwargs)

            return غلاف

        @مزين
        def احسب_مجموع(أ, ب):
            """يحسب مجموع عددين."""
            return أ + ب

        assert احسب_مجموع.__name__ == "احسب_مجموع"
        assert "يحسب" in احسب_مجموع.__doc__

    def test_total_ordering_alias(self, ادوات_داليه):
        """ترتيب_كامل maps to functools.total_ordering."""
        assert ادوات_داليه.ترتيب_كامل is functools.total_ordering

    def test_total_ordering_fills_comparison_methods(self, ادوات_داليه):
        """ترتيب_كامل fills in missing comparison operators from __eq__ and __lt__."""

        @ادوات_داليه.ترتيب_كامل
        class درجه:
            def __init__(self, قيمه):
                self.قيمه = قيمه

            def __eq__(self, other):
                return self.قيمه == other.قيمه

            def __lt__(self, other):
                return self.قيمه < other.قيمه

        أ = درجه(70)
        ب = درجه(85)
        assert أ < ب
        assert ب > أ
        assert أ <= أ
        assert ب >= أ

    def test_singledispatch_alias(self, ادوات_داليه):
        """توزيع_منفرد maps to functools.singledispatch."""
        assert ادوات_داليه.توزيع_منفرد is functools.singledispatch

    def test_cmp_to_key_alias(self, ادوات_داليه):
        """مقارنة_بمفتاح maps to functools.cmp_to_key."""
        assert ادوات_داليه.مقارنة_بمفتاح is functools.cmp_to_key

    def test_cmp_to_key_sorts_correctly(self, ادوات_داليه):
        """مقارنة_بمفتاح converts a comparator to a sort key."""

        def مقارن(أ, ب):
            return (أ > ب) - (أ < ب)

        result = sorted([3, 1, 4, 1, 5], key=ادوات_داليه.مقارنة_بمفتاح(مقارن))
        assert result == [1, 1, 3, 4, 5]
