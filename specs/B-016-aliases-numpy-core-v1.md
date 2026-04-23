# Spec Packet B-016: aliases-numpy-core-v1

**Phase**: B
**Depends on**: B-001 (alias-runtime-v1), B-002 (phase-a-compat-suite)
**Estimated size**: medium
**Owner**: —

## Goal

Ship the Arabic alias mapping for `numpy`'s core surface: arrays, mathematical functions (ufuncs), and data types.

## Non-goals

- No specialized sub-packages mapping (beyond basic random/linalg).

## Files

### Files to create

- `arabicpython/aliases/numpy.toml`
- `tests/test_aliases_numpy.py`
- `examples/B16_numpy_demo.apy`
- `examples/B16_README-ar.md`

## Public interfaces

### `arabicpython/aliases/numpy.toml`

[meta]
arabic_name = "نمباي"
python_module = "numpy"
dict_version = "ar-v1"
schema_version = 1

[entries]
# === Array creation ===
"مصفوفة" = "array"
"مدى" = "arange"
"أصفار" = "zeros"
"وحدات" = "ones"
"فارغ" = "empty"
"هوية" = "eye"
"ممتلئ" = "full"
"مساحة_خطية" = "linspace"
"مساحة_لوغاريتمية" = "logspace"

# === Reshaping / Transformation ===
"إعادة_تشكيل" = "reshape"
"تبديل" = "transpose"
"تسطيح" = "flatten"
"توزيع" = "ravel"

# === Reductions ===
"مجموع" = "sum"
"متوسط" = "mean"
"انحراف_معياري" = "std"
"تباين" = "var"
"أدنى" = "min"
"أقصى" = "max"
"موقع_أدنى" = "argmin"
"موقع_أقصى" = "argmax"

# === Ufuncs ===
"مطلق" = "abs"
"جذر" = "sqrt"
"أس" = "exp"
"لوغاريتم" = "log"
"جيب" = "sin"
"جيب_تمام" = "cos"
"ظل" = "tan"
"ضرب_نقطي" = "dot"
"ضرب_اتقاطعي" = "cross"

# === Constants ===
"ليس_رقما" = "nan"
"ما_لانهاية" = "inf"
"ط" = "pi"
"هـ" = "e"

# === Dtypes ===
"نوع_البيانات" = "dtype"
"رقم_صحيح_32" = "int32"
"رقم_صحيح_64" = "int64"
"رقم_عشري_32" = "float32"
"رقم_عشري_64" = "float64"
"منطقي" = "bool_"

# === Submodules (common exports) ===
"عشوائي" = "random"
"جبر_خطي" = "linalg"

# (Adding more to reach 50)
"شكل" = "shape"
"حجم" = "size"
"أبعاد" = "ndim"
"مجموع_تراكمي" = "cumsum"
"تكرار" = "repeat"
"دمج" = "concatenate"
"فرز" = "sort"
"بحث" = "where"
"تربيعي" = "square"
"تقريب" = "round"
"أرضية" = "floor"
"سقف" = "ceil"

# Count: 50 entries.

### `examples/B16_numpy_demo.apy`

```python
استورد نمباي

مصفوفة = نمباي.مصفوفة([1, 2, 3, 4])
اطبع(f"المصفوفة: {مصفوفة}")
اطبع(f"المتوسط: {نمباي.متوسط(مصفوفة)}")

مصفوفة_ثنائية = نمباي.أصفار((3, 3))
اطبع(f"مصفوفة أصفار:\n{مصفوفة_ثنائية}")

قيم = نمباي.مساحة_خطية(0, نمباي.ط, 10)
اطبع(f"قيم جيب التمام: {نمباي.جيب_تمام(قيم)}")
```

## Implementation constraints

- **Cite B-010 as structural prior.** This packet follows the same deliverable structure and naming conventions.
- **Method-on-instance limitation:** Like B-010, this packet only maps module-level attributes. Methods on instances (e.g., `array.reshape`, `array.mean`) remain in English in this version.
- **Acceptance checklist must include Phase A compat assertion.**
- **Ensure all Arabic names round-trip through `normalize_identifier`.**

## Test requirements

- Verification of array creation and shape manipulation.
- Verification of basic mathematical operations (ufuncs).
- Verification of dtypes and constants.

## Acceptance checklist

- [ ] `arabicpython/aliases/numpy.toml` shipped with at least 50 entries.
- [ ] All integration tests pass.
- [ ] `examples/B16_numpy_demo.apy` runs end-to-end.
- [ ] `examples/B16_README-ar.md` written.
- [ ] Phase A compat assertion: `tests/test_phase_a_compat.py` still passes.
