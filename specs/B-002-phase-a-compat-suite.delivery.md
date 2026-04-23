# B-002 Phase A Compat Suite — Delivery Note

**Packet:** B-002-phase-a-compat-suite  
**Delivered:** 2026-04-23  
**Status:** ✅ Complete — all 11 tests pass, full suite green (414 passed)

---

## Files Delivered

### Tests (new)

| File | Tests |
|------|-------|
| `tests/test_phase_a_compat.py` | 11 tests (7 example snapshots + dict hash + 2 app smoke tests + 1 helper unit test) |

### Snapshots (new)

| File | Purpose |
|------|---------|
| `tests/snapshots/phase_a/dictionary_ar_v1.sha256` | SHA-256 digest of `dictionaries/ar-v1.md` at Phase A ship |
| `tests/snapshots/phase_a/expected_outputs/01_hello.txt` | `مرحبا، يا عالم` |
| `tests/snapshots/phase_a/expected_outputs/02_arithmetic.txt` | `باقي 40 سنة` |
| `tests/snapshots/phase_a/expected_outputs/03_control_flow.txt` | 5-line odd/even output |
| `tests/snapshots/phase_a/expected_outputs/04_functions.txt` | `15\n12` |
| `tests/snapshots/phase_a/expected_outputs/05_data_structures.txt` | 3-line fruit prices |
| `tests/snapshots/phase_a/expected_outputs/06_classes.txt` | `5.0` |
| `tests/snapshots/phase_a/expected_outputs/07_imports.txt` | `25\n27` |

### Modified

| File | Change |
|------|--------|
| `CONTRIBUTING.md` §7 | Removed "(created in B-002)" — file now exists |
| `decisions/0008-phase-b-charter.md` §B.3 | Added "Implementation: B-002 (`tests/test_phase_a_compat.py`)." footnote |

---

## Bootstrap commands used

```bash
# Dictionary hash
python -c "import hashlib; print(hashlib.sha256(open('dictionaries/ar-v1.md', 'rb').read()).hexdigest())"
# → 3affa1278d31c59ddaa1ae7c7db53930620303b743a44fd356d6971e060ef259

# Each example output was verified against the existing test_examples.py values
# (which were already committed and passing), then written to snapshot files.
```

---

## Design decisions

### 07_imports.apy — cwd handling

`07_imports.apy` does `استورد helper` which requires `helper.apy` to be on
`sys.path`. The fix used by `test_examples.py` (and replicated here) is:
`run_apy_program` defaults `cwd` to `path.parent` (the `examples/` directory).
Python adds `""` (cwd) to `sys.path`, so the import hook finds `helper.apy`.

### Apps — cwd=PROJECT_ROOT

`apps/search_engine/cli.apy` opens `"apps/search_engine/docs"` as a relative
path. Subprocess cwd must be the project root, not the app's own directory.
`run_apy_program` accepts an explicit `cwd` kwarg; the smoke tests pass
`cwd=PROJECT_ROOT`.

### Prayer times "next prayer" not asserted

The "صلاة القادمة" countdown line depends on `datetime.now()` — non-deterministic.
The smoke test asserts only the five stable prayer name rows (الفجر through العشاء).
The countdown is exercised (the app runs to completion) but its value is not pinned.

### B01_http.apy excluded

`examples/B01_http.apy` makes a live HTTP call to `httpbin.org`. It is excluded
from the parametrized runner via `_EXCLUDED`. A future packet may add a
`@pytest.mark.network` variant.

---

## Test run (final)

```
414 passed, 21 skipped, 1 warning in 2.47s
```

Zero regressions. The 21 skips are pre-existing (20 × 3.11 f-string tests + 1 readline).

---

## Public API for future packets

```python
from tests.test_phase_a_compat import run_apy_program

rc, stdout, stderr = run_apy_program(
    path,
    timeout=10.0,       # default
    cwd=PROJECT_ROOT,   # override if app needs repo-relative paths
    extra_args=["arg"], # forwarded to the .apy program
)
```
