# Spec Packet B-035: stdlib-math-statistics-random-decimal-fractions

**Phase**: B
**Depends on**: B-001 (alias-runtime-v1), B-002 (phase-a-compat-suite)
**Estimated size**: medium
**Owner**: —

## Goal

Ship Arabic aliases for the primary numeric modules: `math`, `statistics`, `random`, `decimal`, and `fractions`. This packet ensures that Arabic Python learners have a full suite of mathematical and scientific tools available in their native script.

This packet follows the structural pattern established in **B-030** (stdlib-os-pathlib-sys).

## Files

### Files to create

- `arabicpython/aliases/math.toml` — Floor: 15 entries.
- `arabicpython/aliases/statistics.toml` — Floor: 10 entries.
- `arabicpython/aliases/random.toml` — Floor: 10 entries.
- `arabicpython/aliases/decimal.toml` — Floor: 10 entries.
- `arabicpython/aliases/fractions.toml` — Floor: 5 entries.
- `tests/aliases/test_numerics.py` — Combined tests for these five modules.
- `tests/aliases/test_stdlib_B035_cross_consistency.py`
- `examples/B35_scientific_calc.apy` — Demo: Calculate statistics of random Decimals.
- `examples/B35_README-ar.md`

## Translation choices (must-include floor)

**`math.toml` — floor 15:**

| Arabic | Python | Notes |
|---|---|---|
| `جذر` | `sqrt` | |
| `جا` | `sin` | |
| `جتا` | `cos` | |
| `ظا` | `tan` | |
| `ط` | `pi` | |
| `هـ` | `e` | |
| `سقف` | `ceil` | |
| `ارض` | `floor` | |
| `لو` | `log` | |
| `قوة` | `pow` | |
| `مضروب` | `factorial` | |
| `ق_م_أ` | `gcd` | |
| `قريب` | `isclose` | |
| `درجات` | `degrees` | |
| `راديان` | `radians` | |

**`statistics.toml` — floor 10:**

| Arabic | Python | Notes |
|---|---|---|
| `متوسط` | `mean` | |
| `وسيط` | `median` | |
| `منوال` | `mode` | |
| `انحراف_معياري` | `stdev` | |
| `تباين` | `variance` | |
| `وسيط_منخفض` | `median_low` | |
| `وسيط_مرتفع` | `median_high` | |
| `وسيط_مجموعة` | `median_grouped` | |
| `تباين_مجتمع` | `pvariance` | |
| `انحراف_مجتمع` | `pstdev` | |

**`random.toml` — floor 10:**

| Arabic | Python | Notes |
|---|---|---|
| `عشوائي` | `random` | |
| `صحيح_عشوائي` | `randint` | |
| `اختر` | `choice` | |
| `خلط` | `shuffle` | |
| `عينة` | `sample` | |
| `بذرة` | `seed` | |
| `منتظم` | `uniform` | |
| `نطاق_عشوائي` | `randrange` | |
| `مثلثي` | `triangular` | |
| `بيتا` | `betavariate` | |

**`decimal.toml` — floor 10:**

| Arabic | Python | Notes |
|---|---|---|
| `عشري` | `Decimal` | |
| `سياق` | `Context` | |
| `احصل_سياق` | `getcontext` | |
| `اضبط_سياق` | `setcontext` | |
| `قرب_للاعلى` | `ROUND_HALF_UP` | |
| `قرب_للاسفل` | `ROUND_DOWN` | |
| `قرب_للصفر` | `ROUND_CEILING` | |
| `قرب_بعيدا` | `ROUND_FLOOR` | |
| `دقة` | `prec` | |
| `تقريب` | `rounding` | |

**`fractions.toml` — floor 5:**

| Arabic | Python | Notes |
|---|---|---|
| `كسر` | `Fraction` | |
| `بسط` | `numerator` | |
| `مقام` | `denominator` | |
| `من_عدد_عشري` | `from_decimal` | |
| `من_عدد_طافي` | `from_float` | |

## Test requirements

1. **Precision**: `عشري("0.1") + عشري("0.1") + عشري("0.1") == عشري("0.3")`.
2. **Trigonometry**: `رياضيات.جا(رياضيات.ط / 2) == 1.0`.
3. **Randomness**: `عشوائي.بذرة(42)` results in deterministic `عشوائي.عشوائي()` output.

## Acceptance checklist

- [ ] TOML files created (floor 50 total).
- [ ] Tests passing.
- [ ] Demo `B35_scientific_calc.apy` runs.
- [ ] No collisions with Phase A core dictionary.
- [ ] Normalization round-trip verified.
