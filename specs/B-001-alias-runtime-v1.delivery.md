# B-001 Alias Runtime v1 — Delivery Note

**Packet:** B-001-alias-runtime-v1  
**Delivered:** 2026-04-23  
**Status:** ✅ Complete — all 32 tests pass, full suite green (403 passed)

---

## Files Delivered

### Runtime (new)

| File | Purpose |
|------|---------|
| `arabicpython/aliases/__init__.py` | Package: `install()`, `uninstall()`, public `__all__` |
| `arabicpython/aliases/_proxy.py` | `ModuleProxy` — transparent `__getattr__` wrapper |
| `arabicpython/aliases/_loader.py` | `load_mapping()`, `AliasMapping`, `AliasMappingError` |
| `arabicpython/aliases/_finder.py` | `AliasFinder(MetaPathFinder)` + `AliasLoader(Loader)` |
| `arabicpython/aliases/requests.toml` | 34-entry Arabic mapping for `requests` v2.32+ |

### Tests (new)

| File | Tests |
|------|-------|
| `tests/test_aliases_runtime.py` | 25 unit tests: 10 ModuleProxy + 8 AliasFinder + 7 Loader |
| `tests/test_aliases_requests.py` | 7 integration tests against `requests.toml` |

### Fixtures (new)

| File | Purpose |
|------|---------|
| `tests/fixtures/aliases/valid_minimal.toml` | Two-entry `sys` mapping — happy path |
| `tests/fixtures/aliases/missing_module.toml` | Non-existent module → `AliasMappingError` |
| `tests/fixtures/aliases/duplicate_arabic.toml` | Two Arabic keys → same Python value |
| `tests/fixtures/aliases/bad_normalization.toml` | Key with fatha fails `normalize_identifier` round-trip |

### Demo (new)

| File | Purpose |
|------|---------|
| `examples/B01_http.apy` | 6-line demo: `استورد طلبات` / `طلبات.احصل(url)` |

### Modified

| File | Change |
|------|--------|
| `arabicpython/__init__.py` | Exports `install_aliases`, `uninstall_aliases` |
| `pyproject.toml` | `requests>=2.32` in `[dev]`; `network` marker registered |

---

## Design Decisions Made During Implementation

### 1. `requests.toml` — dotted-path entries for non-top-level names

Several `requests` attributes are not exported at the package's top level and
require dotted paths in the TOML `[entries]` table:

```toml
"مصادقه_اساسيه" = "auth.HTTPBasicAuth"
"مصادقه_هضم"    = "auth.HTTPDigestAuth"
"خطا_ssl"       = "exceptions.SSLError"
"خطا_راس_غير_صالح" = "exceptions.InvalidHeader"
"خطا_url_غير_صالح" = "exceptions.InvalidURL"
"خطا_نقص_المخطط"   = "exceptions.MissingSchema"
```

`ModuleProxy.__getattr__` and `load_mapping()` both resolve dotted paths via
`_resolve_dotted_attr()` which walks the attribute chain left-to-right from the
wrapped module.

### 2. `AliasFinder` appended, not inserted

The finder is appended to `sys.meta_path` (lowest priority) so that:
1. Phase A `.apy` finder resolves first
2. Standard Python importlib machinery resolves second
3. Arabic aliases resolve last

This means `import sys` still gives the real `sys` module; only
`import نظام` (if a TOML registers `arabic_name = "نظام"`) goes through the proxy.

### 3. `__class__` property for isinstance reflexivity

`type(proxy)` is `ModuleProxy`, but `isinstance(proxy, types.ModuleType)` must
return `True` for compatibility with code that checks `sys.modules` values.
This is achieved via a `@property` for `__class__` that returns `wrapped.__class__`.

### 4. Broken TOML silent skip

`AliasFinder._load_all_mappings()` catches `AliasMappingError` and silently
skips broken files at startup. This prevents a malformed community TOML from
breaking `import` entirely. Errors surface when `load_mapping()` is called
directly (e.g. in tests or a linting tool).

---

## Test Run (final)

```
403 passed, 21 skipped, 1 warning in 1.50s
```

The 21 skips are pre-existing (20 × Python 3.11-specific f-string tests + 1 readline skip).
Zero regressions.

---

## What B-002 Needs From This Packet

- `AliasFinder` registered and accessible via `arabicpython.aliases`
- `install_aliases()` / `uninstall_aliases()` on `arabicpython`
- `load_mapping()` callable for fixture-based tests
- `AliasMappingError` importable for error-path assertions
- `requests.toml` valid and loadable (confirmed by integration tests)
