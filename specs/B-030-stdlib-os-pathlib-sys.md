# Spec Packet B-030: stdlib-os-pathlib-sys

**Phase**: B
**Depends on**: B-001 (alias-runtime-v1), B-002 (phase-a-compat-suite)
**Estimated size**: medium (1–2 sessions)
**Owner**: — (claim via issue)

## Goal

Ship Arabic aliases for the three Python standard-library modules a learner reaches for first when leaving the toy-example phase: `os`, `pathlib`, and `sys`. After this packet ships, an Arabic-Python program can read environment variables, walk the filesystem, manipulate paths, and inspect interpreter state without typing a Latin-script identifier.

This packet doubles as the **stdlib batch template**. B-031 (collections + itertools + functools), B-032 (datetime + time + calendar), B-033 (json + csv + sqlite3), B-034 (re + string + textwrap), B-035 (math + statistics + random + decimal + fractions), B-036 (logging), B-037 (asyncio core), and B-038 (typing) all follow this same shape. Subsequent packets cite this spec as their structural prior; deviations need delivery-note justification.

Three modules in one packet (rather than three packets) is deliberate: `os`, `pathlib`, and `sys` are conceptually paired, share much vocabulary (`path`, `name`, `exists`), and benefit from being curated together so cross-module names line up.

## Non-goals

- **No coverage of `os.path` as a separate module.** `pathlib` is the modern replacement and is what we evangelize. `os.path` functions are reachable via `نظام_تشغيل.path.<thing>` (English `path` tail) without an alias of their own — the implementer documents this in the delivery note instead of inventing a duplicate Arabic surface.
- **No subprocess wrappers.** `subprocess` lives in B-038's "leftovers" sweep. It deserves careful curation (security implications) and shouldn't be rushed into this packet.
- **No `os.environ` write-protection.** We expose `environ` and `getenv` as-is; if a future ADR decides Arabic Python should sandbox env writes, that's a separate packet.
- **No new runtime mechanics.** Everything reuses B-001's `ModuleProxy` and `AliasFinder`. If a stdlib module exposes something B-001 can't proxy (e.g. C-level constants in a way that breaks identity), document it and skip — don't expand the runtime.
- **No coverage of deprecated APIs.** `os.tempnam`, `pathlib.PurePath.is_reserved` for non-Windows, etc., are skipped silently.

## Files

### Files to create

- `arabicpython/aliases/os.toml` — alias mapping for `os`. Floor: 45 entries (see *Translation choices* below for the must-include list).
- `arabicpython/aliases/pathlib.toml` — alias mapping for `pathlib`. Floor: 25 entries (the `Path` class plus its most-used methods/properties).
- `arabicpython/aliases/sys.toml` — alias mapping for `sys`. Floor: 20 entries.
- `tests/aliases/test_os.py` — integrity + behavioral tests for the `os` mapping.
- `tests/aliases/test_pathlib.py` — integrity + behavioral tests for the `pathlib` mapping.
- `tests/aliases/test_sys.py` — integrity + behavioral tests for the `sys` mapping.
- `tests/aliases/test_stdlib_cross_consistency.py` — checks that names shared across the three modules (e.g. `path`, `name`) are translated identically.
- `examples/B30_filesystem_walk.apy` — runnable demo: walk a directory tree, print sizes, exit with the count.
- `examples/B30_README-ar.md` — Arabic walkthrough of the demo.

### Files to modify

- `ROADMAP-PHASE-B.md` — flip B-030 from `drafted` to `merged` once the PR lands.
- `specs/INDEX.md` — add the row for B-030 (status flips on merge).

### Files to read (do not modify)

- `specs/B-001-alias-runtime-v1.md` — the runtime API this packet consumes.
- `specs/B-010-aliases-flask-v1.md` — the SDK template; this is the **stdlib analog**, so structural parity is expected.
- `dictionaries/ar-v1.md` — frozen core dictionary. Do not invent Arabic terms that would shadow a v1 keyword.
- Python stdlib docs for `os`, `pathlib`, `sys` (3.11 baseline; 3.12 and 3.13 must remain compatible).
- `arabicpython/aliases/_runtime.py` — the loader and proxy implementation (delivered by B-001).
- `arabicpython/normalize.py` — `normalize_identifier()` for round-trip checks.

## Public interfaces

This packet exposes no Python functions of its own — it is data + tests. The interfaces consumers see are:

```python
# After this packet ships:
import arabicpython.aliases as _  # registers the AliasFinder (no-op if already done)

# In a .apy file:
# استورد نظام_تشغيل
# استورد مسار_مكتبة
# استورد نظام
#
# نظام_تشغيل.احصل_متغير_بيئة("HOME")
# مسار_مكتبة.مسار(".").موجود()
# نظام.الوسائط
```

The TOML schema is fixed by B-001 and reproduced here for reviewer convenience:

```toml
[meta]
arabic_name = "نظام_تشغيل"        # the import name learners will use
python_module = "os"               # the wrapped stdlib module
dict_version = "ar-v1"             # the core dictionary this mapping aligns with
schema_version = 1                 # B-001's TOML schema version
maintainer = "@github-handle"      # the packet owner; doubles as triage contact

[entries]
احصل_متغير_بيئة = "getenv"
متغيرات_البيئة = "environ"
# ... etc
```

## Implementation constraints

- **Python version**: 3.11+ (matches Phase A). Some `pathlib` methods were added in 3.12 (e.g. `Path.walk`); include them in the mapping, but the test for them must `pytest.skip` on 3.11 with `sys.version_info < (3, 12)`.
- **Dependencies**: stdlib only. No third-party packages.
- **No monkey-patching.** The mapping is data; the runtime is data-driven. A `.toml` edit must be all that's needed to add an entry — if a contributor finds themselves writing Python code in `arabicpython/aliases/`, they're outside this packet's scope and should file an issue against B-001.
- **Curation rules** (from ADR 0003, repeated here so reviewers don't have to flip files):
  - MSA over dialect; pick the term used in formal Arabic computing literature when one exists.
  - Shortest defensible Arabic form; avoid four-word translations of one-word Python identifiers.
  - No homographs with v1 dictionary keywords. (`اطبع` is `print` in v1; nothing in this packet's TOML may map to `اطبع`.)
  - Every Arabic identifier must round-trip through `arabicpython.normalize.normalize_identifier()` to itself. (Test enforces this.)
  - When two modules expose the same Python name (e.g. both `os` and `pathlib` have `path`-flavored things), use the same Arabic root. The cross-consistency test enforces this.
- **Style**: `ruff` and `black` at project defaults. TOML files are sorted alphabetically by Python attribute name (the value), not by Arabic key, so reviewers reading `git diff` against the official Python docs can scan top-to-bottom.
- **Performance budget**: each module's mapping loads in <50ms. The tests measure this; failing the budget is a test failure, not a warning.

### Translation choices (must-include floor)

Implementer may add more, but at minimum the following entries must appear. These are the names a beginner reaches for in their first 100 lines of stdlib usage. **These are non-negotiable per ADR 0008.B.0 — once shipped, they are frozen. Choose carefully.**

**`os.toml` — floor of 45 entries** (a representative subset shown; see Acceptance for the full list to be reviewed):

| Arabic | Python | Notes |
|---|---|---|
| `احصل_متغير_بيئة` | `getenv` | "fetch env-variable" |
| `متغيرات_البيئة` | `environ` | "the env-variables" — exposed as the live mapping |
| `اسم_النظام` | `name` | `posix` / `nt` — the platform name |
| `فاصل_السطر` | `linesep` | line separator |
| `فاصل_المسار` | `sep` | path separator |
| `فاصل_المسار_البديل` | `altsep` | alt separator (None on POSIX) |
| `الدليل_الحالي` | `getcwd` | get current working directory |
| `غير_الدليل` | `chdir` | change directory |
| `اسرد_الدليل` | `listdir` | list directory contents |
| `انشئ_دليل` | `mkdir` | |
| `انشئ_دلائل` | `makedirs` | |
| `احذف_ملف` | `remove` | (also alias `unlink`) |
| `احذف_دليل` | `rmdir` | |
| `احذف_دلائل` | `removedirs` | |
| `اعد_تسمية` | `rename` | |
| `استبدل` | `replace` | os.replace, not str.replace |
| `معلومات_الملف` | `stat` | |
| `سر_شجرة` | `walk` | tree-walk; `os.walk` |
| `معرف_العملية` | `getpid` | |
| `اخرج_فورا` | `_exit` | |
| `الفصل` | `path` | English tail kept; `nizām_tashghīl.path.join(...)` |

(Implementer fills in the remaining ~24 from the [`os` module reference](https://docs.python.org/3.11/library/os.html), prioritizing functions a tutorial would teach in the first three chapters.)

**`pathlib.toml` — floor of 25 entries:**

| Arabic | Python | Notes |
|---|---|---|
| `مسار` | `Path` | The class. Capitalization in Python; Arabic has no case so this is just `مسار`. |
| `مسار_بحت` | `PurePath` | |
| `مسار_بحت_بوزكس` | `PurePosixPath` | transliterated "POSIX" |
| `مسار_بحت_ويندوز` | `PureWindowsPath` | |
| `موجود` | `exists` | method on Path |
| `هل_ملف` | `is_file` | |
| `هل_دليل` | `is_dir` | |
| `هل_رمز_رابط` | `is_symlink` | |
| `الاسم` | `name` | `Path.name` property |
| `اللاحقة` | `suffix` | |
| `اللواحق` | `suffixes` | |
| `الجذع` | `stem` | filename without suffix |
| `الجذر` | `root` | |
| `الام` | `parent` | parent directory |
| `الاباء` | `parents` | iterable of ancestors |
| `الاجزاء` | `parts` | tuple of path components |
| `مطلق` | `resolve` | resolve to absolute |
| `مع_اسم` | `with_name` | |
| `مع_لاحقة` | `with_suffix` | |
| `اقرا_نص` | `read_text` | |
| `اكتب_نص` | `write_text` | |
| `اقرا_بايتات` | `read_bytes` | |
| `اكتب_بايتات` | `write_bytes` | |
| `افتح` | `open` | Path.open; do NOT shadow builtins.open |
| `كرر` | `glob` | "iterate-matching" — chosen over transliterated "گلوب" |

**`sys.toml` — floor of 20 entries:**

| Arabic | Python | Notes |
|---|---|---|
| `الوسائط` | `argv` | command-line args |
| `معيار_الادخال` | `stdin` | |
| `معيار_الاخراج` | `stdout` | |
| `معيار_الخطا` | `stderr` | |
| `المنصة` | `platform` | `linux`, `win32`, etc. |
| `معلومات_الاصدار` | `version_info` | |
| `الاصدار` | `version` | string form |
| `مسارات_الاستيراد` | `path` | `sys.path` (the import-search list) |
| `الوحدات` | `modules` | the module cache |
| `اخرج` | `exit` | `sys.exit` (exits with code) |
| `قاموس_المنفذ` | `executable` | path to the python interpreter |
| `حد_العودية` | `getrecursionlimit` | |
| `اضبط_حد_العودية` | `setrecursionlimit` | |
| `حجم_العداد` | `getsizeof` | |
| `الترميز_الافتراضي` | `getdefaultencoding` | |
| `ترميز_نظام_الملفات` | `getfilesystemencoding` | |
| `معلومات_الترميز` | `flags` | the runtime flags namespace |
| `معلومات_الذاكرة` | `getallocatedblocks` | |
| `بيئة_التنفيذ` | `implementation` | the implementation namespace |
| `هرس_الاستثناء` | `excepthook` | |

**Cross-consistency requirements** (enforced by `test_stdlib_cross_consistency.py`):

- `path` in `os` (kept as English tail), `path` in `sys` (mapped to `مسارات_الاستيراد` — different concept), and `Path` in `pathlib` (mapped to `مسار`) are **deliberately divergent** because they mean different things. Document this explicitly in the delivery note so reviewers know it isn't an oversight.
- `exit` in `sys` → `اخرج`. `_exit` in `os` → `اخرج_فورا`. Both share the `اخرج` root because they share concept; the modifier expresses the difference.
- `name` in `os` → `اسم_النظام` (qualified — `os.name` means the OS name specifically). `name` in `pathlib.Path` → `الاسم` (the path's leaf name). Document the divergence.

## Test requirements

### `tests/aliases/test_os.py`

1. `test_os_mapping_loads`:
   - Import `arabicpython.aliases.os` via the AliasFinder (i.e. the runtime) and assert `proxy.__class__ is types.ModuleType`.
   - Assert `proxy.احصل_متغير_بيئة is os.getenv`.
   - Assert at least 45 entries are present (`len(proxy._alias_map) >= 45`).

2. `test_os_arabic_call_matches_english`:
   - For each of: `getenv("HOME")`, `getcwd()`, `name`, `linesep`, `sep` — call/access via both Arabic and English names and assert the results are identical (`==` for values, `is` for callables).

3. `test_os_walk_yields_same_tree`:
   - Create a tmp directory tree with a known shape via `tmp_path`.
   - Walk it via `نظام_تشغيل.سر_شجرة(tmp_path)` and via `os.walk(tmp_path)`.
   - Assert the two yield-sequences are equal.

4. `test_os_path_tail_passthrough`:
   - Assert `نظام_تشغيل.path.join("a", "b") == os.path.join("a", "b")`.
   - This documents that `os.path` is reached via the English tail; failing this means the proxy is over-eager.

5. `test_os_round_trip_normalize`:
   - For every Arabic key in the TOML, assert `normalize_identifier(key) == key`. (Catches accidental kashida or harakat.)

6. `test_os_no_v1_dictionary_collisions`:
   - Load `dictionaries/ar-v1.md`, extract the keyword set.
   - Assert no Arabic key in `os.toml` is in that set.

### `tests/aliases/test_pathlib.py`

7. `test_pathlib_mapping_loads`: parallel to test 1 (≥25 entries).

8. `test_pathlib_path_class_identity`:
   - `مسار_مكتبة.مسار is pathlib.Path` — must be `is`, not `==`.

9. `test_pathlib_path_methods_work`:
   - `p = مسار_مكتبة.مسار(tmp_path / "x.txt")`
   - `p.اكتب_نص("hello")`
   - `assert p.موجود()`
   - `assert p.اقرا_نص() == "hello"`
   - `assert p.اللاحقة == ".txt"`

10. `test_pathlib_walk_skips_on_311`:
    - If `sys.version_info < (3, 12)`, `pytest.skip`. Else assert a method `سر` exists and walks correctly.

11. `test_pathlib_round_trip_normalize`: parallel to test 5.

12. `test_pathlib_no_v1_collisions`: parallel to test 6.

### `tests/aliases/test_sys.py`

13. `test_sys_mapping_loads`: parallel (≥20 entries).

14. `test_sys_argv_is_live`:
    - `assert نظام.الوسائط is sys.argv` — the proxy must expose the same list object, not a copy. (Mutation through one should be visible through the other.)

15. `test_sys_exit_propagates`:
    - In a subprocess (use `tests/test_phase_a_compat.py::run_apy_program` from B-002 if available; else `subprocess.run`), execute a one-liner that calls `نظام.اخرج(7)` and assert returncode 7.

16. `test_sys_round_trip_normalize`: parallel.

17. `test_sys_no_v1_collisions`: parallel.

### `tests/aliases/test_stdlib_cross_consistency.py`

18. `test_shared_concepts_share_arabic_roots`:
    - Build a table of `(module, python_name, arabic_name)` triples by loading all three TOMLs.
    - For each pair where two modules use the same `python_name`, assert the `arabic_name` either matches or is documented in this test's `KNOWN_DIVERGENCES` constant. (`KNOWN_DIVERGENCES` is a frozenset declared at the top of the file with the three intentional mismatches from the *Cross-consistency requirements* above.)

19. `test_no_arabic_collisions_across_modules`:
    - Assert that across all three TOMLs, no Arabic key maps to two different Python names. (Would mean a learner sees the same Arabic word do two different things depending on which module they imported.)

20. `test_demo_runs`:
    - `subprocess.run([sys.executable, "-m", "arabicpython.cli", "examples/B30_filesystem_walk.apy", str(tmp_dir)])`
    - Assert returncode 0.
    - Assert stdout contains the line `"عدد_الملفات:"` followed by an integer matching the count of files seeded into `tmp_dir`.

### Tests for the demo example

21. `test_demo_phase_a_compat`:
    - Confirm the demo file does not import any Phase A example or modify Phase A artifacts.
    - Confirm `pytest tests/test_phase_a_compat.py` (from B-002) still passes after this packet's files are added to the tree.

## Reference materials

- `specs/B-001-alias-runtime-v1.md` — runtime API.
- `specs/B-010-aliases-flask-v1.md` — the SDK analog of this stdlib packet; structural sibling.
- `decisions/0008-phase-b-charter.md` §B.1 — proxy architecture rationale.
- `decisions/0003-curation-rules.md` — translation principles.
- Python `os` module: https://docs.python.org/3.11/library/os.html
- Python `pathlib` module: https://docs.python.org/3.11/library/pathlib.html
- Python `sys` module: https://docs.python.org/3.11/library/sys.html

## Open questions for the planner

1. **Should `os.path` get its own mapping file in a follow-up packet, or stay forever as the English tail?** Recommended: stay English. Rationale: `pathlib` is the modern replacement, and dual-translating `os.path.join` and `pathlib.Path` invites learner confusion. Decision deferred to B-038.
2. **`sys.modules` is a writable mapping. Should we expose it under a different Arabic name to discourage learner mutation?** Recommended: no — Arabic Python doesn't add training-wheels to stdlib semantics. Document the sharp edge in the example's README.

## Acceptance checklist

- [ ] Three TOML files created with floor entry counts met (45 / 25 / 20).
- [ ] Each TOML's `[meta]` block fully populated.
- [ ] All three TOMLs sorted alphabetically by Python attribute name.
- [ ] All 21 tests above present and passing on Linux + macOS + Windows × Python 3.11 + 3.12 + 3.13 (test #10 skips on 3.11 — that's expected, not a failure).
- [ ] `examples/B30_filesystem_walk.apy` runs end-to-end and produces deterministic output.
- [ ] `examples/B30_README-ar.md` walks through the demo in Arabic, naming each Arabic identifier used.
- [ ] `pytest tests/test_phase_a_compat.py` passes unchanged.
- [ ] `ruff check .` passes.
- [ ] `black --check .` passes.
- [ ] No edits to `dictionaries/ar-v1.md`.
- [ ] No edits to any file under `examples/0*` or `apps/`.
- [ ] Delivery note `B-030-stdlib-os-pathlib-sys.delivery.md` written. Required sections: the cross-consistency divergences and why; any Arabic term in the floor list that the implementer changed (with reason); list of stdlib functions deliberately omitted (with reason).
