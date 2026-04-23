# Spec Packet B-033: stdlib-json-csv-sqlite3

**Phase**: B
**Depends on**: B-001 (alias-runtime-v1), B-002 (phase-a-compat-suite)
**Estimated size**: medium
**Owner**: —

## Goal

Ship Arabic aliases for `json`, `csv`, and `sqlite3`. This packet covers common data interchange formats and the embedded database engine, enabling Arabic Python programs to persist and exchange structured data.

This packet follows the structural pattern established in **B-030** (stdlib-os-pathlib-sys).

## Files

### Files to create

- `arabicpython/aliases/json.toml` — Floor: 10 entries.
- `arabicpython/aliases/csv.toml` — Floor: 15 entries.
- `arabicpython/aliases/sqlite3.toml` — Floor: 20 entries.
- `tests/aliases/test_json.py`
- `tests/aliases/test_csv.py`
- `tests/aliases/test_sqlite3.py`
- `tests/aliases/test_stdlib_B033_cross_consistency.py`
- `examples/B33_data_storage.apy` — Demo: Read JSON, write CSV, store in SQLite.
- `examples/B33_README-ar.md`

## Translation choices (must-include floor)

**`json.toml` — floor 10:**

| Arabic | Python | Notes |
|---|---|---|
| `نص` | `dumps` | "to-text" |
| `من_نص` | `loads` | "from-text" |
| `حفظ` | `dump` | "save" |
| `تحميل` | `load` | "load" |
| `مرمز` | `JSONEncoder` | |
| `محلل` | `JSONDecoder` | |
| `مسافة_بادئة` | `indent` | parameter |
| `فرز_المفاتيح` | `sort_keys` | parameter |
| `تاكد_من_اسكي` | `ensure_ascii` | parameter |
| `افتراضي` | `default` | parameter |

**`csv.toml` — floor 15:**

| Arabic | Python | Notes |
|---|---|---|
| `قارئ` | `reader` | |
| `كاتب` | `writer` | |
| `قارئ_قاموس` | `DictReader` | |
| `كاتب_قاموس` | `DictWriter` | |
| `اسماء_الحقول` | `fieldnames` | |
| `فاصل` | `delimiter` | |
| `اقتباس_ادنى` | `QUOTE_MINIMAL` | |
| `اقتباس_الكل` | `QUOTE_ALL` | |
| `اقتباس_غير_رقمي` | `QUOTE_NONNUMERIC` | |
| `بلا_اقتباس` | `QUOTE_NONE` | |
| `اكتب_سطر` | `writerow` | |
| `اكتب_اسطر` | `writerows` | |
| `اكتب_راس` | `writeheader` | |
| `لهجة` | `dialect` | |
| `سجل` | `register_dialect` | |

**`sqlite3.toml` — floor 20:**

| Arabic | Python | Notes |
|---|---|---|
| `اتصل` | `connect` | |
| `مؤشر` | `cursor` | |
| `نفذ` | `execute` | |
| `نفذ_عديد` | `executemany` | |
| `نفذ_نص` | `executescript` | |
| `ثبت` | `commit` | |
| `تراجع` | `rollback` | |
| `اغلق` | `close` | |
| `اجلب_واحد` | `fetchone` | |
| `اجلب_عديد` | `fetchmany` | |
| `اجلب_الكل` | `fetchall` | |
| `صف` | `Row` | The Row factory/class |
| `مصنع_الصفوف` | `row_factory` | |
| `عدد_التغييرات` | `total_changes` | |
| `اخر_معرف_صف` | `lastrowid` | |
| `عملية` | `isolation_level` | |
| `انشئ_دالة` | `create_function` | |
| `انشئ_تجميع` | `create_aggregate` | |
| `انشئ_ترتيب` | `create_collation` | |
| `خطا_قاعدة_بيانات` | `DatabaseError` | |

## Test requirements

1. **JSON Round-trip**: Encode Arabic dict to JSON text and decode back.
2. **CSV Integrity**: Write rows with commas in values and read back correctly.
3. **SQLite Transaction**: Verify that `ثبت` (commit) persists data and `تراجع` (rollback) discards it.
4. **SQLite Row Factory**: Verify that accessing columns by Arabic names works if `Row` is used.

## Acceptance checklist

- [ ] TOML files created (floor 45 total).
- [ ] Tests passing.
- [ ] Demo `B33_data_storage.apy` runs.
- [ ] No collisions with Phase A or previous B packets.
- [ ] Normalization round-trip verified.
