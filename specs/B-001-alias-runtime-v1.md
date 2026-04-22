# Spec Packet B-001: alias-runtime-v1

**Phase**: B
**Depends on**: Phase A complete (packets 0001–0014 merged), ADR 0008 accepted
**Estimated size**: large (multi-session; split review into runtime + requests mapping + tests)
**Owner**: — (claim via issue; architectural packet; recommend experienced contributor)

## Goal

Build the runtime foundation that lets a `.apy` program write `استورد طلبات` (import requests) and call `طلبات.احصل("https://...")` (`requests.get`). This packet ships three things as one coherent unit: (1) a module-proxy class that forwards attribute access through a translation table, (2) a `sys.meta_path` finder that resolves Arabic module names to proxies, (3) one complete alias mapping file (`requests.toml`) proving the pattern works end-to-end.

This is the **foundation packet** for all of Phase B. Every subsequent SDK packet (B-010 through B-018) and stdlib batch (B-030 through B-038) consumes the public API defined here. Changes to the proxy class API after B-001 merges require a fix-up packet that updates every downstream packet; plan for durability.

The architectural rationale is in ADR 0008 §B.1. This packet implements that decision.

## Non-goals

- **No dictionary changes.** `dictionaries/ar-v1.md` is frozen per ADR 0008.B.0. The alias mechanism is orthogonal to the keyword dictionary.
- **No other libraries.** Only `requests` ships in B-001. Flask (B-010) is a separate packet because it doubles as the Phase B success-criterion test.
- **No stdlib coverage.** `os`, `json`, etc. are B-030+.
- **No auto-transliteration implementation.** The `DeprecationWarning` fallback for unmapped attributes is spec'd here but emits a placeholder message; the real auto-transliteration heuristic is deferred to a later ADR.
- **No performance optimization.** Proxy attribute access has one extra dictionary lookup per call. That's acceptable. Premature optimization (e.g., cached-attribute-descriptor tricks) is explicitly out of scope.
- **No sync of the proxy with reloaded modules.** If `importlib.reload(requests)` is called, proxy behavior after reload is undefined. Document; do not handle.
- **No thread-local state.** The finder and proxies are process-global. Thread safety is guaranteed only to the extent that the underlying wrapped modules are thread-safe.

## Files

### Files to create

- `arabicpython/aliases/__init__.py` — the package module. Exports `install()`, `uninstall()`, `ModuleProxy`, `AliasFinder`, `load_mapping()`.
- `arabicpython/aliases/_proxy.py` — the `ModuleProxy` class.
- `arabicpython/aliases/_finder.py` — the `AliasFinder` meta-path finder.
- `arabicpython/aliases/_loader.py` — TOML mapping loader + validation.
- `arabicpython/aliases/requests.toml` — the `requests` mapping file (~35 entries; full list in §Public interfaces).
- `tests/test_aliases_runtime.py` — unit tests for `ModuleProxy`, `AliasFinder`, `_loader`.
- `tests/test_aliases_requests.py` — integration tests for the `requests` proxy.
- `tests/fixtures/aliases/` — directory with malformed TOML fixtures for loader error tests.
- `tests/fixtures/aliases/valid_minimal.toml` — smallest valid mapping.
- `tests/fixtures/aliases/missing_module.toml` — references a module that doesn't exist.
- `tests/fixtures/aliases/duplicate_arabic.toml` — same Arabic name maps to two Python names.
- `tests/fixtures/aliases/bad_normalization.toml` — Arabic name that doesn't round-trip through `normalize_identifier`.
- `examples/B01_http.apy` — six-line demo fetching a URL. Uses only `requests.get` and `response.status_code`.

### Files to modify

- `arabicpython/__init__.py` — the top-level `install()` now also registers `AliasFinder` on `sys.meta_path` after the existing `.apy` finder. Add a new public export: `from arabicpython.aliases import install as install_aliases, uninstall as uninstall_aliases`. The existing `install()` function gains a new kwarg `aliases: bool = True` — when True (default), it also calls `install_aliases()`.
- `pyproject.toml` — add `tomli>=2.0` to dependencies for Python 3.10 only (3.11+ has `tomllib` in stdlib). Since the project requires Python 3.11+ per Phase A, this is a no-op; document in the file but don't add the dep.
- `README.md` — add one paragraph under "Phase B" in the roadmap section pointing to this packet. Do not rewrite the Phase B section; one line is enough.

### Files to read (do not modify)

- `arabicpython/import_hook.py` — understand how the existing `.apy` finder registers on `sys.meta_path`. The alias finder registers *after* it (lower priority), so `.apy` modules still resolve first.
- `arabicpython/normalize.py` — the `normalize_identifier()` function that all Arabic names in mappings must round-trip through.
- `decisions/0008-phase-b-charter.md` §B.1 — the architectural commitment being implemented.
- Python docs on `importlib.abc.MetaPathFinder` and `importlib.abc.Loader`.
- Python docs on `sys.meta_path` finder ordering.

## Public interfaces

### `arabicpython.aliases.ModuleProxy`

```python
class ModuleProxy:
    """A transparent wrapper around a Python module that forwards attribute
    access through an Arabic→Python name mapping.

    Created by the AliasFinder, not instantiated directly by user code.

    Invariants:
      - ``self._wrapped`` is the underlying Python module object.
      - ``self._mapping`` is a frozen dict of Arabic → Python attribute names.
      - Attribute access on the proxy first checks ``self._mapping``; if the
        requested name is in the mapping, it resolves to ``getattr(self._wrapped, mapping[name])``.
      - If the requested name is NOT in the mapping but IS an Arabic-looking
        identifier, the proxy emits a DeprecationWarning and raises AttributeError
        with guidance text.
      - If the requested name is an English (ASCII) identifier, the proxy
        forwards unchanged — users can still write ``طلبات.get`` if they prefer.

    Examples:
      >>> import requests  # the real module
      >>> mapping = {"احصل": "get", "نشر": "post"}
      >>> proxy = ModuleProxy(requests, mapping, arabic_name="طلبات")
      >>> proxy.احصل  # same object as requests.get
      <function get at ...>
      >>> proxy.get  # English fallthrough works
      <function get at ...>
      >>> proxy.foo  # not mapped; falls through to requests
      Traceback (most recent call last):
        ...
      AttributeError: module 'requests' has no attribute 'foo'
      >>> proxy.مجهول  # Arabic name not in mapping
      Traceback (most recent call last):
        ...
      AttributeError: 'طلبات' has no attribute 'مجهول'. ...
    """

    def __init__(
        self,
        wrapped: "types.ModuleType",
        mapping: "dict[str, str]",
        *,
        arabic_name: str,
    ) -> None: ...

    def __getattr__(self, name: str) -> "Any": ...

    def __dir__(self) -> "list[str]":
        """Returns Arabic names from the mapping + English names from the wrapped module."""

    def __repr__(self) -> str:
        """Returns: <arabic-proxy of requests via طلبات>"""

    @property
    def __class__(self):  # type: ignore[override]
        """Returns self._wrapped.__class__ so isinstance checks work for module types."""
```

**Reflexivity contract:** The proxy must support these idioms:

```python
import types
assert isinstance(proxy, types.ModuleType)                 # via __class__ forwarding
assert proxy.__name__ == requests.__name__                  # dunder passthrough
assert "احصل" in dir(proxy) and "get" in dir(proxy)        # both shown
assert proxy.احصل is requests.get                           # identity preserved
```

**Error path contract:** For unmapped Arabic attributes:

```python
with pytest.warns(DeprecationWarning, match="is not in the curated mapping"):
    try:
        _ = proxy.مجهول
    except AttributeError as e:
        assert "طلبات" in str(e)
        assert "مجهول" in str(e)
        assert "curated mapping" in str(e) or "list available" in str(e)
```

### `arabicpython.aliases.AliasFinder`

```python
class AliasFinder(importlib.abc.MetaPathFinder):
    """Resolves Arabic module names to ModuleProxy objects.

    Registered on sys.meta_path AFTER the Phase A .apy finder so that:
      - .apy modules resolve first (local code wins)
      - Python stdlib and third-party modules resolve next (standard mechanism)
      - THIS finder resolves Arabic-named aliases last
      - An unknown name still raises ModuleNotFoundError correctly

    The finder consults mappings loaded from TOML files in
    arabicpython/aliases/*.toml. Each TOML file declares one alias mapping.

    Thread safety: find_spec is not thread-safe during mapping-reload; it is
    thread-safe during steady-state import.
    """

    def __init__(self, mappings_dir: "pathlib.Path | None" = None) -> None:
        """mappings_dir defaults to arabicpython/aliases/."""

    def find_spec(
        self,
        fullname: str,
        path: "Sequence[str] | None" = None,
        target: "types.ModuleType | None" = None,
    ) -> "importlib.machinery.ModuleSpec | None":
        """Returns a spec that produces a ModuleProxy when loaded, or None
        if fullname is not a registered Arabic alias.
        """

    def reload_mappings(self) -> None:
        """Re-read all TOML files from mappings_dir. For development; not
        called in steady-state.
        """
```

### `arabicpython.aliases.install` / `uninstall`

```python
def install() -> None:
    """Register AliasFinder on sys.meta_path. Idempotent.

    Must be called AFTER arabicpython.install() so that .apy finder is already
    registered and AliasFinder goes to a lower-priority slot.
    """

def uninstall() -> None:
    """Remove AliasFinder from sys.meta_path. Idempotent (safe to call twice).
    Does not invalidate already-imported proxies.
    """
```

### `arabicpython.aliases.load_mapping`

```python
def load_mapping(toml_path: "pathlib.Path") -> "AliasMapping":
    """Parse and validate one alias TOML file.

    Returns an AliasMapping dataclass.

    Raises:
      AliasMappingError: malformed TOML, missing required fields, duplicate
        Arabic or Python names, unnormalizable Arabic names, referenced Python
        module is not importable.
    """

@dataclass(frozen=True)
class AliasMapping:
    arabic_name: str          # e.g. "طلبات"
    python_module: str        # e.g. "requests"
    dict_version: str         # e.g. "ar-v1" (for forward compat; see ADR 0003)
    entries: dict[str, str]   # Arabic attribute → Python attribute
    source_path: pathlib.Path # for error messages
```

### TOML mapping file schema (`requests.toml`)

```toml
# arabicpython/aliases/requests.toml
# Schema version: 1
# This file maps Arabic names to the `requests` library (v2.32+).

[meta]
arabic_name = "طلبات"
python_module = "requests"
dict_version = "ar-v1"      # tracks ADR 0003 dictionary versioning
schema_version = 1
maintainer = "—"            # GitHub handle or "—" for orphaned

[entries]
# Core HTTP verbs
"احصل" = "get"
"نشر" = "post"
"ضع" = "put"
"احذف" = "delete"
"عدل" = "patch"
"رأس" = "head"
"خيارات" = "options"
"اطلب" = "request"

# Session and response
"جلسة" = "Session"
"استجابة" = "Response"
"طلب" = "PreparedRequest"

# Response attributes (nested reference; applied when proxy walks into Response)
"محتوى" = "content"
"نص" = "text"
"جسون" = "json"
"رمز_الحالة" = "status_code"
"رؤوس" = "headers"
"مسار_الانتقال" = "url"
"موافق" = "ok"
"ارفع_للخطأ" = "raise_for_status"
"كوكيز" = "cookies"
"مدة_الاستجابة" = "elapsed"
"ترميز" = "encoding"
"وضوح" = "apparent_encoding"

# Common exceptions
"خطا_طلب" = "RequestException"
"خطا_اتصال" = "ConnectionError"
"خطا_مهله" = "Timeout"
"خطا_كثير_تحويلات" = "TooManyRedirects"
"خطا_بروتوكول" = "HTTPError"
"خطا_ضمن_ssl" = "SSLError"

# Auth
"مصادقه_اساسيه" = "HTTPBasicAuth"
"مصادقه_هضم" = "HTTPDigestAuth"

# Utilities
"ارفع_للخطأ" = "raise_for_status"
"تسلسل_url" = "utils.urljoin"
"تسلسل_رؤوس" = "utils.default_headers"

# Adapters and session config
"محول_http" = "adapters.HTTPAdapter"
"استراتيجيه_اعاده_المحاوله" = "adapters.Retry"
```

**Exactly 35 entries. This is the minimum viable `requests` surface.** Packet implementers for other libraries should aim for the same density: the public surface that a tutorial would touch, not the full API.

**Note on `ارفع_للخطأ`:** appears twice intentionally — once as a `Response` method, once as a top-level helper. The TOML loader must reject actual duplicates but this is a name-space issue: `response.ارفع_للخطأ` vs `requests.ارفع_للخطأ`. Both point to the same underlying method via different access paths. Document in the loader test that this kind of same-name-different-scope is allowed.

Actually — let's avoid the confusion. The loader flatly rejects duplicate Arabic keys in the `[entries]` section. Remove the duplicate from the TOML above. The duplicate is for documentation here only; the real `requests.toml` has 34 unique entries.

### Integration point: `arabicpython/__init__.py`

```python
# Existing function, modified signature
def install(*, aliases: bool = True) -> None:
    """Install .apy import hook and (by default) Arabic alias resolver.

    Args:
      aliases: If True (default), also register the AliasFinder for Phase B
        library aliases. Set False to get Phase A-only behavior.
    """
    _install_apy_import_hook()
    if aliases:
        from arabicpython.aliases import install as _install_aliases
        _install_aliases()
```

## Implementation constraints

- **Python version**: 3.11+ (uses `tomllib`).
- **Dependencies allowed**: stdlib only. No new third-party deps.
- **No `__getattribute__` override on ModuleProxy.** Use `__getattr__` (invoked only when normal lookup fails). This preserves attribute-access performance for ASCII names.
- **No metaclass tricks.** Keep the code readable. The `__class__` property is the only unusual thing, and it's justified by the isinstance-reflexivity requirement.
- **Style**: `ruff` and `black` at project defaults (line length 100).
- **Performance budget**: proxy attribute access overhead ≤ 1 µs over direct attribute access on a modern machine (measure with `pytest-benchmark` in a non-CI local check; not gated in CI).
- **TOML parsing errors must include the source line number.** Use `tomllib`'s error location info in all `AliasMappingError` messages.
- **Error messages in Arabic and English** where feasible. Runtime errors raised to user code include both (see §Public interfaces for examples).

## Test requirements

Tests ARE the acceptance criteria. When tests pass, the packet is done.

### `tests/test_aliases_runtime.py` — unit tests

**ModuleProxy (10 tests):**

1. `test_proxy_resolves_arabic_to_wrapped_attribute`:
   - Input: proxy for a fixture module with mapping `{"هلو": "hello"}`, wrapped module has `hello = "world"`.
   - Expected: `proxy.هلو == "world"` and `proxy.هلو is proxy._wrapped.hello`.

2. `test_proxy_english_fallthrough`:
   - Input: same proxy.
   - Expected: `proxy.hello == "world"` (direct access still works).

3. `test_proxy_unmapped_arabic_raises_and_warns`:
   - Input: same proxy; access `proxy.مجهول`.
   - Expected: `DeprecationWarning` issued with message containing "curated mapping"; `AttributeError` raised with message containing both `"مجهول"` and the proxy's `arabic_name`.

4. `test_proxy_unmapped_english_fallthrough_to_attribute_error`:
   - Input: same proxy; access `proxy.foo` where wrapped has no `foo`.
   - Expected: `AttributeError` raised; message matches CPython's normal error ("module 'X' has no attribute 'foo'"). **No DeprecationWarning.**

5. `test_proxy_dir_includes_arabic_and_english`:
   - Input: proxy with mapping `{"أ": "a", "ب": "b"}`, wrapped has attrs `a`, `b`, `c`.
   - Expected: `set(dir(proxy)) >= {"أ", "ب", "a", "b", "c"}`.

6. `test_proxy_repr`:
   - Input: proxy with `arabic_name="طلبات"` wrapping module named "requests".
   - Expected: `repr(proxy) == "<arabic-proxy of requests via طلبات>"`.

7. `test_proxy_isinstance_module`:
   - Input: proxy wrapping a real module.
   - Expected: `isinstance(proxy, types.ModuleType)` is True.

8. `test_proxy_dunder_passthrough`:
   - Input: proxy wrapping module `M` with `M.__name__ = "M"`, `M.__doc__ = "d"`.
   - Expected: `proxy.__name__ == "M"`, `proxy.__doc__ == "d"`.

9. `test_proxy_identity_preserved`:
   - Input: proxy with mapping `{"ف": "f"}`; wrapped.f is a function.
   - Expected: `proxy.ف is wrapped.f` (True, not a wrapper).

10. `test_proxy_mapping_is_frozen`:
    - Input: construct proxy with mapping `{"أ": "a"}`.
    - Expected: `proxy._mapping["ب"] = "b"` raises (mapping is immutable after construction).

**AliasFinder (8 tests):**

11. `test_finder_returns_none_for_unknown_name`:
    - Input: finder with no mappings; `find_spec("random_name", None, None)`.
    - Expected: returns `None`.

12. `test_finder_resolves_known_arabic_name`:
    - Input: finder with a mapping `طلبات → requests` loaded; `find_spec("طلبات", None, None)`.
    - Expected: returns a `ModuleSpec` whose loader produces a `ModuleProxy`.

13. `test_finder_does_not_shadow_real_module`:
    - Input: finder has no mapping for `os`; import `os`.
    - Expected: `os` is the real `os` module (finder was skipped because it didn't claim the name).

14. `test_finder_sys_meta_path_position`:
    - Input: call `arabicpython.install()` on a clean interpreter.
    - Expected: `AliasFinder` appears in `sys.meta_path` AFTER the `.apy` finder.

15. `test_finder_install_is_idempotent`:
    - Input: call `install()` twice.
    - Expected: exactly one `AliasFinder` in `sys.meta_path`.

16. `test_finder_uninstall_removes_from_meta_path`:
    - Input: install, then uninstall.
    - Expected: no `AliasFinder` in `sys.meta_path`.

17. `test_finder_uninstall_idempotent`:
    - Input: uninstall twice with no install between.
    - Expected: no exception.

18. `test_finder_reload_picks_up_new_toml`:
    - Input: finder with no mappings; write a TOML to the mappings dir; call `reload_mappings()`.
    - Expected: next `find_spec` for the new Arabic name succeeds.

**Loader (7 tests):**

19. `test_loader_parses_valid_minimal`:
    - Input: `tests/fixtures/aliases/valid_minimal.toml` (fixture: one module, two entries).
    - Expected: returns `AliasMapping` with correct fields.

20. `test_loader_rejects_missing_meta`:
    - Input: TOML with `[entries]` but no `[meta]`.
    - Expected: raises `AliasMappingError` with message containing "missing [meta] section".

21. `test_loader_rejects_missing_module`:
    - Input: `tests/fixtures/aliases/missing_module.toml` (references a module that doesn't exist).
    - Expected: raises `AliasMappingError` with message containing both the module name and "not importable".

22. `test_loader_rejects_duplicate_arabic_keys`:
    - Input: TOML with `"احصل" = "get"` twice. (Note: TOML itself rejects this; test that the error surfaces cleanly.)
    - Expected: raises `AliasMappingError` with TOML line number.

23. `test_loader_rejects_duplicate_python_values`:
    - Input: `tests/fixtures/aliases/duplicate_arabic.toml` (two Arabic keys pointing to the same Python name).
    - Expected: raises `AliasMappingError` with message listing both Arabic keys and the shared Python name.

24. `test_loader_rejects_unnormalizable_arabic`:
    - Input: `tests/fixtures/aliases/bad_normalization.toml` (contains an entry with harakat that don't survive `normalize_identifier`).
    - Expected: raises `AliasMappingError` with message containing "does not round-trip through normalize_identifier".

25. `test_loader_validates_python_attribute_exists`:
    - Input: TOML referencing `requests` with entry `"هلو" = "nonexistent_attribute"`.
    - Expected: raises `AliasMappingError` with message listing the missing attribute on the module.

### `tests/test_aliases_requests.py` — integration tests

26. `test_requests_toml_loads_without_error`:
    - Input: load `arabicpython/aliases/requests.toml`.
    - Expected: no exception; returns valid `AliasMapping`.

27. `test_requests_toml_has_minimum_surface`:
    - Input: loaded mapping.
    - Expected: contains entries for `احصل`, `نشر`, `جلسة`, `استجابة`, `رمز_الحالة`, `خطا_طلب`. (The "must-cover-these-six" floor; if these are missing, the packet is broken.)

28. `test_استورد_طلبات_via_import_hook`:
    - Input: after `arabicpython.install()`, execute `"import requests as طلبات"` → but through the finder path: import the Arabic name `طلبات` directly.
    - Expected: the imported object is a `ModuleProxy`; `proxy._wrapped is requests`.

29. `test_proxy_get_returns_real_requests_get`:
    - Input: `طلبات = import_alias("طلبات"); طلبات.احصل`.
    - Expected: same object identity as `requests.get`.

30. `test_proxy_response_attribute_access` (mocked; no network):
    - Input: use `requests_mock` or `unittest.mock` to create a fake `Response`; wrap it and access `response.رمز_الحالة`.
    - **NOTE for implementer:** `Response` is a class, not a module. Attribute forwarding for response instances is handled by Python's normal attribute lookup, NOT by ModuleProxy. The TOML mapping covers module-level names only. Document this limitation; a future packet may introduce class-level proxies.

31. `test_deprecation_warning_for_unmapped_arabic_attribute`:
    - Input: access `طلبات.مجهول_جدا`.
    - Expected: `DeprecationWarning` caught; `AttributeError` raised.

32. `test_examples_B01_http_runs_end_to_end`:
    - Input: execute `examples/B01_http.apy`.
    - Expected: no exception. (The example hits a real URL; mark with `pytest.mark.network` and skip by default in CI; opt-in via env var `RUN_NETWORK_TESTS=1`.)

### Edge cases that must be covered

- Empty mapping dict (proxy still constructs; all access falls through to wrapped).
- Mapping with only one entry.
- Arabic name containing tatweel (ـ U+0640) — must work.
- Arabic name containing harakat — must be rejected by loader (normalization check catches this).
- Module name with a dot (`requests.adapters`) — must work (the TOML can reference nested names via dotted paths in values).
- Circular: a proxy attribute that returns the proxy itself. Document as undefined; don't test.
- `sys.meta_path` already has user-registered finders before `install()` — the alias finder goes after the `.apy` finder but before any user finders are unaffected.

## Reference materials

- `decisions/0008-phase-b-charter.md` §B.1 — the architectural commitment.
- `decisions/0001-architecture.md` — the tokenize-only constraint that rules out AST rewriting.
- `decisions/0004-normalization-policy.md` — the `normalize_identifier()` contract.
- `arabicpython/import_hook.py` — existing meta-path finder as a structural reference.
- Python docs:
  - `sys.meta_path`: https://docs.python.org/3/library/sys.html#sys.meta_path
  - `importlib.abc.MetaPathFinder`: https://docs.python.org/3/library/importlib.html#importlib.abc.MetaPathFinder
  - `importlib.machinery.ModuleSpec`: https://docs.python.org/3/library/importlib.html#importlib.machinery.ModuleSpec
  - `tomllib` (3.11+): https://docs.python.org/3/library/tomllib.html
  - PEP 562 (`__getattr__` on modules): https://peps.python.org/pep-0562/ — useful context for why we proxy instead
- `requests` documentation: https://requests.readthedocs.io/en/latest/api/ — authoritative surface for `requests.toml` entries.
- Prior art: zhpy's module aliasing (simpler; single Chinese alias per module, no attribute translation) — we go further.

## Open questions for the planner

Empty. This spec is complete.

## Acceptance checklist

- [ ] All listed files created.
- [ ] All 32 tests present and passing.
- [ ] `examples/B01_http.apy` runs end-to-end against a real URL (opt-in CI).
- [ ] `arabicpython.aliases.requests.toml` has exactly 34 unique entries, all passing the normalization round-trip check.
- [ ] `ruff check .` passes.
- [ ] `black --check .` passes.
- [ ] `pytest` passes on Python 3.11, 3.12, 3.13 × Linux/macOS/Windows (9 cells).
- [ ] Delivery note `B-001-alias-runtime-v1.delivery.md` written, with explicit sections for: schema decisions made during implementation, any Python-version differences observed, confirmation of the reflexivity invariant, and empty "deviations" if truly none.
- [ ] Phase A compat: the seven `examples/*.apy` files still execute without modification (manual check pending B-002; the automated suite comes later).
- [ ] README.md Phase B paragraph added (one line — do not rewrite the section).
