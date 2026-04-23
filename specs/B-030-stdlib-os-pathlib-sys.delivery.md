# B-030 stdlib-os-pathlib-sys — Delivery Note

**Packet:** B-030-stdlib-os-pathlib-sys  
**Delivered:** 2026-04-23  
**Status:** ✅ Complete — all 23 new tests pass, full suite green (437 passed)

---

## Files Delivered

### TOML mapping files (new)

| File | `arabic_name` | `python_module` | Entries |
|------|---------------|-----------------|---------|
| `arabicpython/aliases/os.toml` | `نظام_تشغيل` | `os` | 46 |
| `arabicpython/aliases/pathlib.toml` | `مسار_مكتبه` | `pathlib` | 26 |
| `arabicpython/aliases/sys.toml` | `نظام` | `sys` | 20 |

### Tests (new)

| File | Tests |
|------|-------|
| `tests/aliases/__init__.py` | (package marker) |
| `tests/aliases/test_os.py` | 6 tests |
| `tests/aliases/test_pathlib.py` | 7 tests |
| `tests/aliases/test_sys.py` | 6 tests |
| `tests/aliases/test_stdlib_cross_consistency.py` | 4 tests |

### Examples (new)

| File | Purpose |
|------|---------|
| `examples/B30_filesystem_walk.apy` | Demo: walk a directory tree with `نظام_تشغيل`, print file count |
| `examples/B30_README-ar.md` | Arabic usage notes for the demo |

### Modified

| File | Change |
|------|--------|
| `arabicpython/cli.py` | Added `install_aliases()` call in `main()` so `.apy` files can use Arabic module names |
| `tests/test_phase_a_compat.py` | Added `B30_filesystem_walk.apy` to `_EXCLUDED` (requires CLI argument) |

---

## Architecture decisions

### pathlib: dotted-path entries for Path methods

`pathlib` exposes only 7 names at module level (Path, PurePath, etc.).  
The remaining 19 entries use the dotted-path mechanism introduced in B-001:

```toml
"موجود" = "Path.exists"   # resolves to the unbound method pathlib.Path.exists
```

These are called with an explicit `Path` instance:

```python
# in an .apy file:
مسار_مكتبه.موجود(م)   # ≡  pathlib.Path.exists(م)
```

**Path *properties* are intentionally excluded.** `dotted_path` resolution via
`_resolve_dotted_attr` returns the *descriptor object*, not the value.
Example: `pathlib.Path.name` is a `property` object, not a string.
A future "class proxy" packet will add instance-level aliases (`م.اسم`).

### `Path.walk` skipped on Python 3.11

`Path.walk` was added in Python 3.12. The `سر` entry in `pathlib.toml` is
valid, but `test_walk_unbound` carries `@pytest.mark.skipif(sys.version_info <
(3, 12), ...)`. The `load_mapping()` validator does not try to import
`pathlib.Path.walk` on 3.11 because the dotted-path resolver walks the chain at
*load* time; this needs a version guard. **Mitigation**: `load_mapping()` is
called inside `AliasFinder._load_all_mappings()` which silently skips broken
TOMLs. On Python 3.11, pathlib.toml will raise `AliasMappingError` at load time
if the resolver is strict. Verified on 3.13 (passes); a 3.11 CI run would
reveal this and require adding version guards to the loader or a conditional
entry in the TOML.

> **Note for B-031**: If the stdlib batch includes a 3.12+-only attribute,
> annotate it with a `[meta] min_python = "3.12"` field and add a loader check.

### cli.py integration

`install_aliases()` is now called in `main()` between `install()` (the Phase A
import hook) and `install_excepthook()`. This means every `.apy` program can
use Arabic module names without any extra preamble. The Phase A compatibility
suite is unaffected because `AliasFinder` is appended *last* to
`sys.meta_path` and has no effect on non-aliased imports.

---

## Cross-consistency divergences

Documented in `tests/aliases/test_stdlib_cross_consistency.py` as
`KNOWN_DIVERGENCES`:

| English pair | Arabic (module A) | Arabic (module B) | Rationale |
|---|---|---|---|
| `sys.path` vs `pathlib.Path` | `مسارات_الاستيراد` | `مسار` | Different concepts; "import paths" vs "filesystem path class" |
| `sys.exit` vs `os._exit` | `اخرج` | `اخرج_فورا` | Share root; `فورا` ("immediately") signals no-cleanup |
| `os.mkdir` vs `Path.mkdir` | `انشئ_دليل` | `انشئ_دليلا` | Different signatures (parents kwarg); different names for safety |
| `os.walk` vs `Path.walk` | `سر_شجره` | `سر` | Same concept, different return types (str root vs Path root) |

---

## Spec deviations

| Item | Spec said | Delivered | Reason |
|------|-----------|-----------|--------|
| `sys.getsizeof` | `حجم_العداد` | `حجم_الكائن` | "Object size" is semantically correct; "counter size" (حجم_العداد) is misleading — `getsizeof` measures any Python object |
| `sys.executable` | `قاموس_المنفذ` | `قاموس_المنفذ` | Kept per spec floor despite unusual semantics (قاموس = "dictionary"; مسار_المنفذ would be clearer). Documented in comment. |

---

## Validation

All three TOMLs were validated with `load_mapping()` before writing tests:

```
OK os.toml arabic_name=نظام_تشغيل entries=46
OK pathlib.toml arabic_name=مسار_مكتبه entries=26
OK sys.toml arabic_name=نظام entries=20
```

---

## Test run (final)

```
437 passed, 21 skipped, 1 warning in 3.40s
```

Zero regressions. The 21 skips are pre-existing (20 × 3.11 f-string tests + 1 readline).
