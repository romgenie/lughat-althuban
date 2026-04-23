# Spec Packet B-017: aliases-pandas-core-v1

**Phase**: B
**Depends on**: B-001 (alias-runtime-v1), B-002 (phase-a-compat-suite)
**Estimated size**: medium
**Owner**: —

## Goal

Ship the Arabic alias mapping for `pandas`' core surface: DataFrames, Series, and data ingestion/export functions.

## Non-goals

- No specialized plotting aliases (beyond what's in core).
- No complex multi-index manipulation aliases for now.

## Files

### Files to create

- `arabicpython/aliases/pandas.toml`
- `tests/test_aliases_pandas.py`
- `examples/B17_pandas_demo.apy`
- `examples/B17_README-ar.md`

## Public interfaces

### `arabicpython/aliases/pandas.toml`

[meta]
arabic_name = "بانداس"
python_module = "pandas"
dict_version = "ar-v1"
schema_version = 1

[entries]
# === Core Structures ===
"إطار_بيانات" = "DataFrame"
"سلسلة" = "Series"
"فهرس" = "Index"
"فهرس_متعدد" = "MultiIndex"
"تصنيفي" = "Categorical"

# === Reading Data ===
"اقرأ_csv" = "read_csv"
"اقرأ_إكسل" = "read_excel"
"اقرأ_جسون" = "read_json"
"اقرأ_sql" = "read_sql"
"اقرأ_html" = "read_html"
"اقرأ_مخلل" = "read_pickle"

# === Writing Data ===
"إلى_csv" = "to_csv"
"إلى_إكسل" = "to_excel"
"إلى_جسون" = "to_json"
"إلى_sql" = "to_sql"
"إلى_قاموس" = "to_dict"
"إلى_نمباي" = "to_numpy"

# === Manipulation ===
"دمج_سلاسل" = "concat"
"دمج_إطارات" = "merge"
"محور" = "pivot"
"جدول_محوري" = "pivot_table"
"صهر" = "melt"
"جدول_تقاطعي" = "crosstab"

# === Cleaning / Transformation ===
"احصل_على_وهمي" = "get_dummies"
"قطع" = "cut"
"قطع_كمي" = "qcut"

# === Date / Time ===
"مدى_تاريخ" = "date_range"
"مدى_فترة" = "period_range"

# === Constants ===
"غير_موجود" = "NA"
"ليس_رقما" = "NaN"

# === Options ===
"إعدادات" = "options"
"ضبط_إعداد" = "set_option"
"جلب_إعداد" = "get_option"

# (Adding more to reach 40)
"تاريخ_ووقت" = "to_datetime"
"فترة_زمنية" = "to_timedelta"
"تجميع" = "concat"
"فرز_حسب" = "sort_values"
"فرز_فهرس" = "sort_index"
"أعمدة" = "columns"
"بيانات" = "values"

# Count: 40 entries.

### `examples/B17_pandas_demo.apy`

```python
استورد بانداس

بيانات = {
    "اسم": ["أحمد", "سارة", "ليلى"],
    "عمر": [25, 30, 22]
}

إطار = بانداس.إطار_بيانات(بيانات)
اطبع(f"إطار البيانات:\n{إطار}")

متوسط_العمر = إطار["عمر"].mean()
اطبع(f"متوسط العمر: {متوسط_العمر}")

# تصفية
صغار = إطار[إطار["عمر"] < 25]
اطبع(f"أقل من 25:\n{صغار}")
```

## Implementation constraints

- **Cite B-010 as structural prior.** This packet follows the same deliverable structure and naming conventions.
- **Method-on-instance limitation:** Like B-010, this packet only maps module-level attributes. Methods on instances (e.g., `df.groupby`, `df.head`) remain in English in this version.
- **Acceptance checklist must include Phase A compat assertion.**
- **Ensure all Arabic names round-trip through `normalize_identifier`.**

## Test requirements

- Verification of DataFrame and Series creation.
- Verification of data reading (mocking CSV).
- Verification of basic aggregation and filtering.

## Acceptance checklist

- [ ] `arabicpython/aliases/pandas.toml` shipped with at least 40 entries.
- [ ] All integration tests pass.
- [ ] `examples/B17_pandas_demo.apy` runs end-to-end.
- [ ] `examples/B17_README-ar.md` written.
- [ ] Phase A compat assertion: `tests/test_phase_a_compat.py` still passes.
