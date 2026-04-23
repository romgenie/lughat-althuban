# Spec Packet B-038: stdlib-leftovers

**Phase**: B
**Depends on**: B-001 (alias-runtime-v1), B-002 (phase-a-compat-suite)
**Estimated size**: large
**Owner**: —

## Goal

Ship Arabic aliases for the remaining essential standard library modules: `subprocess`, `tempfile`, `shutil`, `argparse`, `urllib.parse`, `hashlib`, `secrets`, and `uuid`. This "catch-all" packet completes the Phase B standard library coverage for general-purpose scripting and system tasks.

This packet follows the structural pattern established in **B-030** (stdlib-os-pathlib-sys).

## Files

### Files to create

- `arabicpython/aliases/subprocess.toml` — Floor: 10 entries.
- `arabicpython/aliases/tempfile.toml` — Floor: 8 entries.
- `arabicpython/aliases/shutil.toml` — Floor: 10 entries.
- `arabicpython/aliases/argparse.toml` — Floor: 8 entries.
- `arabicpython/aliases/urllib_parse.toml` — Floor: 10 entries.
- `arabicpython/aliases/hashlib.toml` — Floor: 5 entries.
- `arabicpython/aliases/secrets.toml` — Floor: 5 entries.
- `arabicpython/aliases/uuid.toml` — Floor: 4 entries.
- `tests/aliases/test_leftovers.py`
- `examples/B38_system_script.apy` — Demo: Parse args, copy files, hash content.
- `examples/B38_README-ar.md`

## Translation choices (must-include floor)

**`subprocess.toml` — floor 10:**

| Arabic | Python | Notes |
|---|---|---|
| `شغل` | `run` | |
| `انبوب` | `PIPE` | |
| `المعيار_الخارجي` | `STDOUT` | |
| `عدم` | `DEVNULL` | |
| `فتح_عملية` | `Popen` | |
| `استدعاء` | `call` | |
| `تأكد_من_الاستدعاء` | `check_call` | |
| `تأكد_من_المخرجات` | `check_output` | |
| `انتظر` | `wait` | |
| `تواصل` | `communicate` | |

**`tempfile.toml` — floor 8:**

| Arabic | Python | Notes |
|---|---|---|
| `ملف_مؤقت_باسم` | `NamedTemporaryFile` | |
| `دليل_مؤقت` | `TemporaryDirectory` | |
| `دليل_المؤقتات` | `gettempdir` | |
| `انشئ_ملف_مؤقت` | `mkstemp` | |
| `انشئ_دليل_مؤقت` | `mkdtemp` | |
| `ملف_مؤقت` | `TemporaryFile` | |
| `ملف_تخزين_مؤقت` | `SpooledTemporaryFile` | |
| `بادئة` | `prefix` | parameter |

**`shutil.toml` — floor 10:**

| Arabic | Python | Notes |
|---|---|---|
| `انسخ` | `copy` | |
| `انسخ_كامل` | `copy2` | copy with metadata |
| `انسخ_شجرة` | `copytree` | |
| `انقل` | `move` | |
| `احذف_شجرة` | `rmtree` | |
| `استخدام_القرص` | `disk_usage` | |
| `اين` | `which` | find executable |
| `اصنع_ارشيف` | `make_archive` | |
| `فك_ارشيف` | `unpack_archive` | |
| `امتلاك` | `chown` | |

**`argparse.toml` — floor 8:**

| Arabic | Python | Notes |
|---|---|---|
| `محلل_الوسائط` | `ArgumentParser` | |
| `اضف_وسيط` | `add_argument` | |
| `حلل_الوسائط` | `parse_args` | |
| `مساحة_اسماء` | `Namespace` | |
| `وصف` | `description` | |
| `مساعدة` | `help` | |
| `مطلوب` | `required` | |
| `افتراضي` | `default` | |

**`urllib_parse.toml` — floor 10:**

| Arabic | Python | Notes |
|---|---|---|
| `حلل_رابط` | `urlparse` | |
| `ركب_رابط` | `urlunparse` | |
| `قسم_رابط` | `urlsplit` | |
| `اجمع_رابط` | `urljoin` | |
| `ترميز` | `quote` | |
| `فك_ترميز` | `unquote` | |
| `ترميز_زائد` | `quote_plus` | |
| `حلل_استعلام` | `parse_qs` | |
| `حلل_قائمة_استعلام` | `parse_qsl` | |
| `مخطط` | `scheme` | |

**`hashlib.toml` — floor 5:**

| Arabic | Python | Notes |
|---|---|---|
| `شا_256` | `sha256` | |
| `ام_دي_5` | `md5` | |
| `جديد` | `new` | |
| `حدث` | `update` | |
| `بصمة_ست_عشرية` | `hexdigest` | |

**`secrets.toml` — floor 5:**

| Arabic | Python | Notes |
|---|---|---|
| `بايتات_سرية` | `token_bytes` | |
| `نص_سري` | `token_hex` | |
| `رابط_سري` | `token_urlsafe` | |
| `اختر_سري` | `choice` | |
| `عشوائي_تحت` | `randbelow` | |

**`uuid.toml` — floor 4:**

| Arabic | Python | Notes |
|---|---|---|
| `معرف_عالمي_4` | `uuid4` | |
| `معرف_عالمي` | `UUID` | |
| `بايتات` | `bytes` | |
| `نص` | `hex` | |

## Test requirements

1. **Subprocess**: Run `echo` via `عملية_فرعية.شغل` and capture output.
2. **Shutil/Tempfile**: Create a `TemporaryDirectory`, create a file, copy it, and verify the copy exists.
3. **Argparse**: Simulate CLI args and verify `محلل_الوسائط` parses them into the correct Arabic fields.
4. **URL**: Parse a URL and verify `مخطط` (scheme) is `https`.

## Acceptance checklist

- [ ] TOML files created (floor 60 total).
- [ ] Tests passing.
- [ ] Demo `B38_system_script.apy` runs.
- [ ] Normalization round-trip verified.
- [ ] No collisions with previous packets or Phase A.
