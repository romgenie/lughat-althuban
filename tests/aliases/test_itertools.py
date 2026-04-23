# tests/aliases/test_itertools.py
# B-031 stdlib aliases — itertools module tests
#
# All itertools aliases are module-level functions (no unbound methods).
# Arabic key round-trip: final ة → ه (e.g. دورة → دوره, سلسلة → سلسله).

import itertools
import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def ادوات_تكرار():
    """Return a ModuleProxy wrapping `itertools`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("ادوات_تكرار", None, None)
    assert spec is not None, "AliasFinder did not find 'ادوات_تكرار'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestItertoolsProxy:
    def test_chain_alias(self, ادوات_تكرار):
        """سلسله maps to itertools.chain."""
        assert ادوات_تكرار.سلسله is itertools.chain

    def test_chain_flattens(self, ادوات_تكرار):
        """سلسله([1,2],[3,4]) flattens to [1,2,3,4]."""
        result = list(ادوات_تكرار.سلسله([1, 2], [3, 4]))
        assert result == [1, 2, 3, 4]

    def test_count_alias(self, ادوات_تكرار):
        """عداد_لانهائي maps to itertools.count."""
        assert ادوات_تكرار.عداد_لانهائي is itertools.count

    def test_count_generates_sequence(self, ادوات_تكرار):
        """عداد_لانهائي(5, 2) generates 5, 7, 9, 11…"""
        gen = ادوات_تكرار.عداد_لانهائي(5, 2)
        first_three = [next(gen) for _ in range(3)]
        assert first_three == [5, 7, 9]

    def test_cycle_alias(self, ادوات_تكرار):
        """دوره maps to itertools.cycle."""
        assert ادوات_تكرار.دوره is itertools.cycle

    def test_repeat_alias(self, ادوات_تكرار):
        """كرر_قيمه maps to itertools.repeat."""
        assert ادوات_تكرار.كرر_قيمه is itertools.repeat

    def test_repeat_limited(self, ادوات_تكرار):
        """كرر_قيمه('x', 3) yields 'x' three times."""
        result = list(ادوات_تكرار.كرر_قيمه("x", 3))
        assert result == ["x", "x", "x"]

    def test_accumulate_alias(self, ادوات_تكرار):
        """تراكم maps to itertools.accumulate."""
        assert ادوات_تكرار.تراكم is itertools.accumulate

    def test_accumulate_running_sum(self, ادوات_تكرار):
        """تراكم([1,2,3,4]) gives running sums [1,3,6,10]."""
        result = list(ادوات_تكرار.تراكم([1, 2, 3, 4]))
        assert result == [1, 3, 6, 10]

    def test_groupby_alias(self, ادوات_تكرار):
        """تجميع_حسب maps to itertools.groupby."""
        assert ادوات_تكرار.تجميع_حسب is itertools.groupby

    def test_groupby_groups_correctly(self, ادوات_تكرار):
        """تجميع_حسب groups a sorted iterable by key."""
        data = [("أ", 1), ("أ", 2), ("ب", 3)]
        groups = {k: list(v) for k, v in ادوات_تكرار.تجميع_حسب(data, key=lambda x: x[0])}
        assert len(groups["أ"]) == 2
        assert len(groups["ب"]) == 1

    def test_product_alias(self, ادوات_تكرار):
        """ضرب_ديكارتي maps to itertools.product."""
        assert ادوات_تكرار.ضرب_ديكارتي is itertools.product

    def test_product_cartesian(self, ادوات_تكرار):
        """ضرب_ديكارتي([0,1],[0,1]) gives all pairs."""
        result = list(ادوات_تكرار.ضرب_ديكارتي([0, 1], [0, 1]))
        assert (0, 0) in result
        assert (1, 1) in result
        assert len(result) == 4

    def test_permutations_alias(self, ادوات_تكرار):
        """تباديل maps to itertools.permutations."""
        assert ادوات_تكرار.تباديل is itertools.permutations

    def test_combinations_alias(self, ادوات_تكرار):
        """توافيق maps to itertools.combinations."""
        assert ادوات_تكرار.توافيق is itertools.combinations

    def test_combinations_count(self, ادوات_تكرار):
        """توافيق([1,2,3,4], 2) gives C(4,2)=6 pairs."""
        result = list(ادوات_تكرار.توافيق([1, 2, 3, 4], 2))
        assert len(result) == 6

    def test_islice_alias(self, ادوات_تكرار):
        """شريحة_مكرر maps to itertools.islice."""
        assert ادوات_تكرار.شريحة_مكرر is itertools.islice

    def test_islice_limits(self, ادوات_تكرار):
        """شريحة_مكرر takes first N items from an infinite iterator."""
        result = list(ادوات_تكرار.شريحة_مكرر(ادوات_تكرار.عداد_لانهائي(0), 5))
        assert result == [0, 1, 2, 3, 4]

    def test_takewhile_alias(self, ادوات_تكرار):
        """خذ_طالما maps to itertools.takewhile."""
        result = list(ادوات_تكرار.خذ_طالما(lambda x: x < 5, [1, 4, 6, 4, 1]))
        assert result == [1, 4]

    def test_dropwhile_alias(self, ادوات_تكرار):
        """اسقط_طالما maps to itertools.dropwhile."""
        result = list(ادوات_تكرار.اسقط_طالما(lambda x: x < 5, [1, 4, 6, 4, 1]))
        assert result == [6, 4, 1]

    def test_filterfalse_alias(self, ادوات_تكرار):
        """تصفية_خاطئه maps to itertools.filterfalse."""
        assert ادوات_تكرار.تصفية_خاطئه is itertools.filterfalse

    def test_tee_alias(self, ادوات_تكرار):
        """نسخ_مكرر maps to itertools.tee."""
        gen1, gen2 = ادوات_تكرار.نسخ_مكرر([1, 2, 3])
        assert list(gen1) == [1, 2, 3]
        assert list(gen2) == [1, 2, 3]
