# Spec Packet B-032: stdlib-datetime-time-calendar

**Phase**: B
**Depends on**: B-001 (alias-runtime-v1), B-002 (phase-a-compat-suite)
**Estimated size**: medium
**Owner**: —

## Goal

Ship Arabic aliases for `datetime`, `time`, and `calendar`. This packet enables handling dates, times, durations, and timezones in Arabic Python. Special care is taken to distinguish between timezone-aware and naive objects.

This packet follows the structural pattern established in **B-030** (stdlib-os-pathlib-sys).

## Files

### Files to create

- `arabicpython/aliases/datetime.toml` — Floor: 20 entries.
- `arabicpython/aliases/time.toml` — Floor: 12 entries.
- `arabicpython/aliases/calendar.toml` — Floor: 8 entries.
- `tests/aliases/test_datetime.py`
- `tests/aliases/test_time.py`
- `tests/aliases/test_calendar.py`
- `tests/aliases/test_stdlib_B032_cross_consistency.py`
- `examples/B32_datetime_math.apy` — Demo: calculate days until next year, handle timezones.
- `examples/B32_README-ar.md`

## Translation choices (must-include floor)

**`datetime.toml` — floor 20:**

| Arabic | Python | Notes |
|---|---|---|
| `تاريخ` | `date` | |
| `وقت` | `time` | |
| `تاريخ_وقت` | `datetime` | |
| `فرق_زمني` | `timedelta` | |
| `نطاق_زمني` | `timezone` | |
| `الان` | `now` | |
| `الان_عالمي` | `utcnow` | UTC now |
| `اليوم` | `today` | |
| `من_طابع_زمني` | `fromtimestamp` | |
| `نسق_نص` | `strftime` | string format time |
| `حلل_نص` | `strptime` | string parse time |
| `نسق_ايزو` | `isoformat` | ISO 8601 |
| `يوم_الاسبوع` | `weekday` | |
| `استبدل` | `replace` | |
| `ساعة` | `hour` | |
| `دقيقة` | `minute` | |
| `ثانية` | `second` | |
| `يوم` | `day` | |
| `شهر` | `month` | |
| `سنة` | `year` | |

**`time.toml` — floor 12:**

| Arabic | Python | Notes |
|---|---|---|
| `نمة` | `sleep` | MSA "slumber/sleep" — synchronous |
| `وقت_الحالي` | `time` | |
| `وقت_عالمي` | `gmtime` | |
| `وقت_محلي` | `localtime` | |
| `نص_الوقت` | `ctime` | |
| `عداد_الاداء` | `perf_counter` | |
| `وقت_رتيب` | `monotonic` | |
| `بنية_وقت` | `struct_time` | |
| `منطقة_الزمن` | `tzname` | |
| `ازاحة` | `timezone` | (integer offset) |
| `توقيت_صيفي` | `daylight` | |
| `اصنع_وقت` | `mktime` | |

**`calendar.toml` — floor 8:**

| Arabic | Python | Notes |
|---|---|---|
| `شهر` | `month` | function |
| `تقويم` | `calendar` | function |
| `هل_كبيسة` | `isleap` | |
| `ايام_كبيسة` | `leapdays` | |
| `نطاق_الشهر` | `monthrange` | |
| `اسم_الشهر` | `month_name` | |
| `اسم_اليوم` | `day_name` | |
| `بداية_الاسبوع` | `setfirstweekday` | |

## Implementation constraints

- **Aware vs Naive**: Documentation must clarify that `datetime.now()` via Arabic returns the default system behavior (naive by default).
- `datetime.replace` vs `os.replace` vs `str.replace`: All use `استبدل`. This is acceptable as they are attributes of different types.

## Test requirements

1. **Awareness**: Test that `تاريخ_وقت.الان(نطاق_زمني.عالمي)` returns a timezone-aware object.
2. **Math**: Test that `تاريخ(2023, 1, 1) + فرق_زمني(ايام=1)` equals `تاريخ(2023, 1, 2)`.
3. **Sleep**: Test that `نمة(0.1)` actually pauses for approximately 100ms.

## Acceptance checklist

- [ ] TOML files created (floor 40 total).
- [ ] Tests passing.
- [ ] Demo `B32_datetime_math.apy` runs.
- [ ] No collisions with Phase A or B-030.
- [ ] Normalization round-trip verified.
