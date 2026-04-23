# Spec Packet B-036: stdlib-logging

**Phase**: B
**Depends on**: B-001 (alias-runtime-v1), B-002 (phase-a-compat-suite)
**Estimated size**: medium
**Owner**: —

## Goal

Ship Arabic aliases for the `logging` module. Logging is a foundational requirement for production software. This packet maps both the module-level convenience functions and the class-level Logger/Handler/Formatter API.

This packet follows the structural pattern established in **B-030** (stdlib-os-pathlib-sys).

## Files

### Files to create

- `arabicpython/aliases/logging.toml` — Floor: 30 entries.
- `tests/aliases/test_logging.py`
- `examples/B36_app_logging.apy` — Demo: Configure file and stream logging.
- `examples/B36_README-ar.md`

## Translation choices (must-include floor)

**`logging.toml` — floor 30:**

| Arabic | Python | Notes |
|---|---|---|
| `احصل_سجل` | `getLogger` | |
| `تصحيح` | `debug` | level & function |
| `معلومات` | `info` | level & function |
| `تحذير` | `warning` | level & function |
| `خطأ` | `error` | level & function |
| `حرج` | `critical` | level & function |
| `تكوين_اساسي` | `basicConfig` | |
| `معالج_ملفات` | `FileHandler` | |
| `معالج_تدفق` | `StreamHandler` | |
| `منسق` | `Formatter` | |
| `فلتر` | `Filter` | |
| `سجل` | `Logger` | The class |
| `سجل_الرسالة` | `LogRecord` | |
| `معالج` | `Handler` | |
| `اضبط_المستوى` | `setLevel` | |
| `اضف_معالج` | `addHandler` | |
| `ازل_معالج` | `removeHandler` | |
| `اضف_فلتر` | `addFilter` | |
| `ازل_فلتر` | `removeFilter` | |
| `سجل_استثناء` | `exception` | method |
| `سجل_رسالة` | `log` | method |
| `اسم_المستوى` | `getLevelName` | |
| `اضف_اسم_مستوى` | `addLevelName` | |
| `اغلاق_السجلات` | `shutdown` | |
| `ليس_مضبوطا` | `NOTSET` | level |
| `تنبيه` | `WARNING` | alias for warning |
| `خطأ_جذري` | `CRITICAL` | alias |
| `منسق_الوقت` | `datefmt` | parameter |
| `تنسيق` | `format` | parameter |
| `مسار_الملف` | `filename` | parameter |

## Test requirements

1. **Module level**: Call `سجل.معلومات("test")` after `basicConfig` and check output.
2. **Class level**: Create a custom `سجل` (Logger), attach a `معالج_ملفات` (FileHandler), and verify the file content.
3. **Levels**: Verify that `سجل.خطأ` > `سجل.معلومات` numerically.

## Acceptance checklist

- [ ] TOML file created (floor 30 entries).
- [ ] Tests passing.
- [ ] Demo `B36_app_logging.apy` runs.
- [ ] Normalization round-trip verified.
