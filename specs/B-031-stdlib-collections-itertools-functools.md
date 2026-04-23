# Spec Packet B-031: stdlib-collections-itertools-functools

**Phase**: B
**Depends on**: B-001 (alias-runtime-v1), B-002 (phase-a-compat-suite)
**Estimated size**: medium
**Owner**: —

## Goal

Ship Arabic aliases for `collections`, `itertools`, and `functools`. These modules provide high-performance container datatypes and functional programming tools that are essential for intermediate Python development.

This packet follows the structural pattern established in **B-030** (stdlib-os-pathlib-sys).

## Files

### Files to create

- `arabicpython/aliases/collections.toml` — Floor: 15 entries.
- `arabicpython/aliases/itertools.toml` — Floor: 15 entries.
- `arabicpython/aliases/functools.toml` — Floor: 10 entries.
- `tests/aliases/test_collections.py`
- `tests/aliases/test_itertools.py`
- `tests/aliases/test_functools.py`
- `tests/aliases/test_stdlib_B031_cross_consistency.py`
- `examples/B31_functional_data.apy` — Demo: using Counter, groupby, and partial.
- `examples/B31_README-ar.md`

## Translation choices (must-include floor)

**`collections.toml` — floor 15:**

| Arabic | Python | Notes |
|---|---|---|
| `قاموس_مرتب` | `OrderedDict` | |
| `قاموس_تلقائي` | `defaultdict` | |
| `عداد` | `Counter` | |
| `طابور_مزدوج` | `deque` | |
| `صف_باسم` | `namedtuple` | |
| `سلسلة_خرائط` | `ChainMap` | |
| `عناصر` | `elements` | Counter.elements |
| `الاكثر_شيوعا` | `most_common` | Counter.most_common |
| `طرح` | `subtract` | Counter.subtract |
| `اضف_يمين` | `append` | deque.append |
| `اضف_يسار` | `appendleft` | deque.appendleft |
| `انتزع_يمين` | `pop` | deque.pop |
| `انتزع_يسار` | `popleft` | deque.popleft |
| `مدد_يمين` | `extend` | deque.extend |
| `مدد_يسار` | `extendleft` | deque.extendleft |

**`itertools.toml` — floor 15:**

| Arabic | Python | Notes |
|---|---|---|
| `سلسلة` | `chain` | |
| `تجميع_حسب` | `groupby` | |
| `عداد_لانهائي` | `count` | |
| `دورة` | `cycle` | |
| `كرر_قيمة` | `repeat` | |
| `تراكم` | `accumulate` | |
| `ضرب_ديكارتي` | `product` | |
| `تباديل` | `permutations` | |
| `توافيق` | `combinations` | |
| `تصفية_خاطئة` | `filterfalse` | |
| `ضغط` | `compress` | |
| `اسقط_طالما` | `dropwhile` | |
| `خذ_طالما` | `takewhile` | |
| `شريحة_مكرر` | `islice` | |
| `نسخ_مكرر` | `tee` | |

**`functools.toml` — floor 10:**

| Arabic | Python | Notes |
|---|---|---|
| `جزيء` | `partial` | |
| `اختزال` | `reduce` | |
| `ذاكرة_مؤقتة_مؤخرا` | `lru_cache` | |
| `اغلفة` | `wraps` | |
| `ترتيب_كامل` | `total_ordering` | |
| `توزيع_منفرد` | `singledispatch` | |
| `تخزين_مؤقت` | `cache` | (3.9+) |
| `تحديث_الغلاف` | `update_wrapper` | |
| `مقارنة_بمفتاح` | `cmp_to_key` | |
| `خاصية_محسوبة_مرة` | `cached_property` | (3.8+) |

## Test requirements

1. **Cross-consistency**: Ensure no collision with B-030 terms and internal consistency.
2. **Round-trip**: All Arabic names must pass `normalize_identifier`.
3. **Behavioral**: `Counter` arithmetic, `itertools.chain` flattening, and `lru_cache` hit counting must work via Arabic aliases.

## Acceptance checklist

- [ ] TOML files created (floor 40 total).
- [ ] Tests passing.
- [ ] Demo `B31_functional_data.apy` runs.
- [ ] No collisions with Phase A core dictionary.
- [ ] No collisions with B-030 identifiers.
