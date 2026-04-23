# Spec Packet B-015: aliases-pytest-v1

**Phase**: B
**Depends on**: B-001 (alias-runtime-v1), B-002 (phase-a-compat-suite)
**Estimated size**: medium
**Owner**: —

## Goal

Ship the Arabic alias mapping for `pytest`, enabling Arabic-speaking developers to write test suites in Arabic.

## Non-goals

- No support for complex pytest plugins unless widely used.

## Files

### Files to create

- `arabicpython/aliases/pytest.toml`
- `tests/test_aliases_pytest.py`
- `examples/B15_pytest_demo.apy`
- `examples/B15_README-ar.md`

## Public interfaces

### `arabicpython/aliases/pytest.toml`

[meta]
arabic_name = "باي_تيست"
python_module = "pytest"
dict_version = "ar-v1"
schema_version = 1

[entries]
"تجهيز" = "fixture"
"علامة" = "mark"
"يرفع" = "raises"
"تخصيص_معاملات" = "mark.parametrize"
"تخطي" = "skip"
"تخطي_إذا" = "mark.skipif"
"فشل_متوقع" = "mark.xfail"
"تقريبي" = "approx"
"رئيسي" = "main"
"خروج" = "exit"
"توقف" = "set_trace"

# Common marks
"فلترة_تحذيرات" = "mark.filterwarnings"
"استخدام_تجهيزات" = "mark.usefixtures"

# Configuration / Hooks
"مواصفات_خطاف" = "hookspec"
"تنفيذ_خطاف" = "hookimpl"
"تسجيل_إعادة_كتابة_تأكيد" = "register_assert_rewrite"

# Exceptions
"خطأ_باي_تيست" = "PytestError"
"تحذير_باي_تيست" = "PytestWarning"

# (Adding more to reach 30)
"مواصفات" = "Config"
"بند" = "Item"
"جامع" = "Collector"
"تقرير" = "TestReport"
"استثناء" = "ExceptionInfo"
"فشل" = "fail"
"استيراد_أور_تخطي" = "importorskip"
"تجميد" = "freeze_includes"

# Count: 30 entries.

### `examples/B15_pytest_demo.apy`

```python
استورد باي_تيست

@باي_تيست.تجهيز
دالة بيانات_تجريبية():
    ارجع {"قيمة": 10}

دالة اختبار_التجهيز(بيانات_تجريبية):
    تأكد بيانات_تجريبية["قيمة"] == 10

@باي_تيست.علامة.تخصيص_معاملات("أ,ب,ن", [(1, 2, 3), (4, 5, 9)])
دالة اختبار_الجمع(أ, ب, ن):
    تأكد أ + ب == ن

دالة اختبار_الخطأ():
    مع باي_تيست.يرفع(ValueError):
        ارفع ValueError("خطأ")
```

## Implementation constraints

- **Cite B-010 as structural prior.** This packet follows the same deliverable structure and naming conventions.
- **Method-on-instance limitation:** Like B-010, this packet only maps module-level attributes. Methods on instances (e.g., `config.getoption`) remain in English in this version.
- **Acceptance checklist must include Phase A compat assertion.**
- **Ensure all Arabic names round-trip through `normalize_identifier`.**

## Test requirements

- Verification that `pytest` can discover and run tests written with Arabic aliases.
- Verification of fixture injection.
- Verification of marks and parameterization.

## Acceptance checklist

- [ ] `arabicpython/aliases/pytest.toml` shipped with at least 30 entries.
- [ ] All integration tests pass.
- [ ] `examples/B15_pytest_demo.apy` runs end-to-end.
- [ ] `examples/B15_README-ar.md` written.
- [ ] Phase A compat assertion: `tests/test_phase_a_compat.py` still passes.
