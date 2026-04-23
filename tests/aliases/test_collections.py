# tests/aliases/test_collections.py
# B-031 stdlib aliases — collections module tests
#
# Tests cover module-level class aliases and the dotted-path unbound-method
# aliases for Counter and deque.  Unbound methods are called with an explicit
# instance: مجموعات.عناصر(c) ≡ Counter.elements(c).

import collections
import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def مجموعات():
    """Return a ModuleProxy wrapping `collections` via the real collections.toml mapping."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("مجموعات", None, None)
    assert spec is not None, "AliasFinder did not find 'مجموعات'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestCollectionsProxy:
    def test_counter_class_alias(self, مجموعات):
        """عداد maps to collections.Counter."""
        assert مجموعات.عداد is collections.Counter

    def test_ordered_dict_alias(self, مجموعات):
        """قاموس_مرتب maps to collections.OrderedDict."""
        assert مجموعات.قاموس_مرتب is collections.OrderedDict

    def test_default_dict_alias(self, مجموعات):
        """قاموس_تلقائي maps to collections.defaultdict."""
        assert مجموعات.قاموس_تلقائي is collections.defaultdict

    def test_deque_alias(self, مجموعات):
        """طابور_مزدوج maps to collections.deque."""
        assert مجموعات.طابور_مزدوج is collections.deque

    def test_namedtuple_alias(self, مجموعات):
        """صف_باسم maps to collections.namedtuple."""
        assert مجموعات.صف_باسم is collections.namedtuple

    def test_chain_map_alias(self, مجموعات):
        """سلسلة_خرائط maps to collections.ChainMap."""
        assert مجموعات.سلسلة_خرائط is collections.ChainMap

    def test_counter_arithmetic(self, مجموعات):
        """Counter arithmetic works via the Arabic alias."""
        c = مجموعات.عداد("مرحبا")
        assert c["م"] == 1
        assert c["ا"] == 1
        c2 = مجموعات.عداد({"م": 3, "ر": 2})
        total = c + c2
        assert total["م"] == 4

    def test_counter_most_common_unbound(self, مجموعات):
        """الاكثر_شيوعا is Counter.most_common (unbound); calling it works."""
        c = collections.Counter("مرحبا بالعالم")
        result = مجموعات.الاكثر_شيوعا(c, 2)
        assert len(result) == 2
        # Result is [(char, count), ...] sorted descending
        assert result[0][1] >= result[1][1]

    def test_counter_elements_unbound(self, مجموعات):
        """عناصر is Counter.elements (unbound); expands a counter back to elements."""
        c = collections.Counter({"ا": 3, "ب": 2})
        elems = sorted(مجموعات.عناصر(c))
        assert elems == ["ا", "ا", "ا", "ب", "ب"]

    def test_deque_append_both_sides(self, مجموعات):
        """اضف_يمين / اضف_يسار (deque.append / appendleft) work correctly."""
        d = collections.deque([2, 3])
        مجموعات.اضف_يسار(d, 1)  # [1, 2, 3]
        مجموعات.اضف_يمين(d, 4)  # [1, 2, 3, 4]
        assert list(d) == [1, 2, 3, 4]

    def test_deque_pop_both_sides(self, مجموعات):
        """انتزع_يمين / انتزع_يسار (deque.pop / popleft) work correctly."""
        d = collections.deque([10, 20, 30])
        left = مجموعات.انتزع_يسار(d)
        right = مجموعات.انتزع_يمين(d)
        assert left == 10
        assert right == 30
        assert list(d) == [20]

    def test_deque_rotate(self, مجموعات):
        """ادر (deque.rotate) rotates a deque in-place."""
        d = collections.deque([1, 2, 3, 4, 5])
        مجموعات.ادر(d, 2)
        assert list(d) == [4, 5, 1, 2, 3]

    def test_defaultdict_int(self, مجموعات):
        """قاموس_تلقائي(int) works as a counting defaultdict."""
        dd = مجموعات.قاموس_تلقائي(int)
        dd["مفتاح"] += 1
        dd["مفتاح"] += 1
        assert dd["مفتاح"] == 2
        assert dd["جديد"] == 0  # default 0, no KeyError

    def test_namedtuple_creation(self, مجموعات):
        """صف_باسم creates a namedtuple class usable in Arabic code."""
        نقطه = مجموعات.صف_باسم("نقطه", ["س", "ص"])
        p = نقطه(س=3, ص=4)
        assert p.س == 3
        assert p.ص == 4
