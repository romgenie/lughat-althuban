# Spec Packet B-002: phase-a-compat-suite

**Phase**: B
**Depends on**: Phase A complete (packets 0001–0014 merged), ADR 0008 accepted
**Estimated size**: small (1 session)
**Owner**: — (claim via issue; **good first packet**)

## Goal

Create the permanent test suite that pins Phase A's user-facing artifacts in CI so no Phase B change can ever silently break them. ADR 0008.B.3 commits to: *"Any program that runs on Phase A's last release runs unchanged on every Phase B release."* This packet implements the enforcement mechanism for that promise.

The suite has two parts: (1) a parametrized test that runs every `.apy` file in `examples/` and `apps/` end-to-end and asserts on its observable output, and (2) a snapshot test for the keyword dictionary that catches any silent edit to `dictionaries/ar-v1.md`.

This packet is small and almost entirely test code — no production code changes — making it an ideal first packet for a new contributor learning the project's conventions.

## Non-goals

- **No new features.** This packet only adds tests.
- **No test rewriting.** Existing test files stay untouched. The new file is additive.
- **No CI workflow changes.** GitHub Actions already runs `pytest`; the new file picks up automatically.
- **No coverage of `tests/`.** The compat suite checks user-facing artifacts only. The `tests/` directory itself can change freely.
- **No coverage of internal APIs.** `arabicpython.translate.translate()` may evolve; only its observable effect on user `.apy` programs is pinned.
- **No translated-output snapshots.** We don't snapshot the *translated* Python source for each `.apy` file because translate-pipeline internals are allowed to evolve. We snapshot only the program's *runtime output*.

## Files

### Files to create

- `tests/test_phase_a_compat.py` — the compat suite.
- `tests/snapshots/phase_a/dictionary_ar_v1.sha256` — single line containing the SHA-256 hex digest of `dictionaries/ar-v1.md` at the Phase A ship commit.
- `tests/snapshots/phase_a/expected_outputs/01_hello.txt` — expected stdout for `examples/01_hello.apy`.
- `tests/snapshots/phase_a/expected_outputs/02_arithmetic.txt` — expected stdout for `examples/02_arithmetic.apy`.
- `tests/snapshots/phase_a/expected_outputs/03_control_flow.txt` — expected stdout for `examples/03_control_flow.apy`.
- `tests/snapshots/phase_a/expected_outputs/04_functions.txt` — expected stdout for `examples/04_functions.apy`.
- `tests/snapshots/phase_a/expected_outputs/05_data_structures.txt` — expected stdout for `examples/05_data_structures.apy`.
- `tests/snapshots/phase_a/expected_outputs/06_classes.txt` — expected stdout for `examples/06_classes.apy`.
- `tests/snapshots/phase_a/expected_outputs/07_imports.txt` — expected stdout for `examples/07_imports.apy`.

### Files to modify

- `CONTRIBUTING.md` § 7 — change "(created in B-002)" to "(in `tests/test_phase_a_compat.py`)" once this packet ships. **Do this in the same PR**, since the doc references this file.
- `decisions/0008-phase-b-charter.md` — add a one-line note at the bottom of the §B.3 section: "Implementation: B-002 (`tests/test_phase_a_compat.py`)." Do not modify the ADR's body otherwise.

### Files to read (do not modify)

- `examples/*.apy` — the seven existing example programs.
- `examples/README.md` and `examples/README-ar.md` — context for what each example demonstrates.
- `apps/search_engine/` and `apps/prayer_times/` — the two showcase apps from packets 0013/0014. Do they have runnable entry points with deterministic output? If yes, include in the suite; if no, document why excluded.
- `dictionaries/ar-v1.md` — the file being snapshotted.

## Public interfaces

This packet exposes one function for use by future packets that need to assert Phase A compat in their own tests:

```python
# tests/test_phase_a_compat.py — exported via __all__

def run_apy_program(path: pathlib.Path, *, timeout: float = 10.0) -> tuple[int, str, str]:
    """Execute an .apy file in a subprocess and capture (returncode, stdout, stderr).

    Uses ``sys.executable -m arabicpython.cli <path>`` to invoke the dialect.
    UTF-8 enforced on both pipes.

    Args:
      path: absolute path to the .apy file.
      timeout: seconds; raises TimeoutExpired if exceeded.

    Returns:
      (returncode, stdout_text, stderr_text). Both texts are decoded as UTF-8
      with errors='replace' so test assertion failures don't crash the test
      harness on encoding mismatch — the assertion itself surfaces the bug.

    Examples:
      >>> rc, out, err = run_apy_program(Path("examples/01_hello.apy"))
      >>> rc
      0
      >>> "مرحبا" in out
      True
    """
```

## Implementation constraints

- **Python version**: 3.11+.
- **Dependencies allowed**: stdlib only (`subprocess`, `pathlib`, `hashlib`, `pytest`).
- **No fixture changes.** Don't share state with other test files. The compat suite is hermetic.
- **Subprocess invocation, not in-process.** Each example runs via `python -m arabicpython.cli` so we test the same code path a real user hits — including `_configure_utf8_streams()`, argv handling, and exit code handling. Calling `arabicpython.translate.translate()` directly would skip the CLI layer and miss those bugs.
- **UTF-8 explicitly forced** on both pipe sides via `subprocess.run(..., encoding="utf-8", errors="replace")`. Phase A documented Windows CP1252 issues; this prevents the suite from being flaky on Windows.
- **Snapshot expected outputs are committed verbatim.** Use `\n` line endings (not `\r\n`) in the snapshot files even on Windows — the test reads them with `newline=""` to suppress translation.
- **Style**: `ruff` and `black` at project defaults.
- **Performance budget**: full compat suite runs in <30 seconds on a modern machine. Each example invocation is its own subprocess with ~200ms startup; 9 examples × 200ms = under 2 seconds plus per-program runtime.

## Test requirements

The suite is itself the deliverable; "tests for the tests" are minimal but real.

### `tests/test_phase_a_compat.py`

**Parametrized example runner (1 test, ~9 cases):**

1. `test_phase_a_example_runs_unchanged`:
   - Parametrized over every file in `examples/*.apy` that is NOT `helper.apy` (it's an importee, not a runnable program).
   - For each example:
     - Run via `run_apy_program(path)`.
     - Assert `returncode == 0`.
     - Assert `stdout` exactly matches the corresponding snapshot file in `tests/snapshots/phase_a/expected_outputs/`.
     - Assert `stderr` is empty.
   - Failure message must include the example name and a unified diff between expected and actual stdout.

**Dictionary snapshot (1 test):**

2. `test_dictionary_ar_v1_unchanged`:
   - Read `dictionaries/ar-v1.md` as bytes, compute SHA-256.
   - Read expected hash from `tests/snapshots/phase_a/dictionary_ar_v1.sha256`.
   - Assert equal.
   - Failure message: "dictionaries/ar-v1.md has changed since Phase A ship. Per ADR 0008.B.0 it is immutable. If a change is genuinely needed, write a superseding ADR introducing ar-v1.1.md or ar-v2.md, do not modify ar-v1.md."

**Apps smoke-test (2 tests):**

3. `test_search_engine_app_runs`:
   - Invoke `apps/search_engine/cli.apy` with a fixed query against a fixed corpus.
   - Assert `returncode == 0`.
   - Assert stdout contains expected result fragments (not full snapshot — search ranking may have legitimate drift; check for "found N results" line and at least one expected document title).
   - **If `apps/search_engine/cli.apy` doesn't take a deterministic input/output path**, mark this test `pytest.skip` with the reason and leave a TODO for a follow-up packet. Don't invent fake test inputs.

4. `test_prayer_times_app_runs`:
   - Invoke `apps/prayer_times/الرئيسي.apy` with a fixed city and date.
   - Assert `returncode == 0`.
   - Assert stdout contains five Arabic prayer names: `الفجر`, `الظهر`, `العصر`, `المغرب`, `العشاء`.
   - **Same skip-with-TODO escape hatch as test 3 if entry point isn't deterministic.**

**Helper function unit test (1 test):**

5. `test_run_apy_program_decodes_arabic_correctly`:
   - Create a temp `.apy` file containing `اطبع("مرحبا")`.
   - Run via `run_apy_program`.
   - Assert `"مرحبا"` appears literally in stdout (not mojibake, not a UnicodeDecodeError replacement char).

### Edge cases

- **Empty stdout snapshots** — if an example legitimately prints nothing, the snapshot file is empty (zero bytes). The test must handle this without hanging on `read()`.
- **Examples that take command-line args** — none currently do, but the runner supports a `args=[]` kwarg for future-proofing.
- **Examples that read stdin** — none currently do; document that they're not supported by this runner.
- **Examples that exit non-zero deliberately** — none currently do; if added later, expand the parametrization to take `(path, expected_returncode)`.

### Generating the snapshots (one-time bootstrap)

The implementer generates the initial snapshots by running each example once and capturing its output, then committing those captures. The generation steps:

```bash
mkdir -p tests/snapshots/phase_a/expected_outputs
for f in examples/*.apy; do
    [ "$(basename $f)" = "helper.apy" ] && continue
    name=$(basename $f .apy)
    python -m arabicpython.cli "$f" > "tests/snapshots/phase_a/expected_outputs/${name}.txt" 2>/dev/null
done

# Dictionary hash:
python -c "import hashlib; print(hashlib.sha256(open('dictionaries/ar-v1.md', 'rb').read()).hexdigest())" \
    > tests/snapshots/phase_a/dictionary_ar_v1.sha256
```

These bootstrap commands are documented in the delivery note for reproducibility, not committed as a script.

## Reference materials

- `decisions/0008-phase-b-charter.md` §B.3 — the compat promise being enforced.
- `decisions/0007-scope.md` §"Phase A" — the original scope this suite pins.
- `tests/test_examples.py` — the existing in-process test for examples. **This new suite is additive; do not delete or modify the existing one.** They cover different layers (in-process translate vs. subprocess CLI).
- `arabicpython/cli.py` — entry point invoked by the subprocess.
- pytest parametrize docs: https://docs.pytest.org/en/stable/how-to/parametrize.html

## Open questions for the planner

Empty.

## Acceptance checklist

- [ ] `tests/test_phase_a_compat.py` created with all 5 tests.
- [ ] All 7 example snapshot files created in `tests/snapshots/phase_a/expected_outputs/`.
- [ ] Dictionary SHA-256 file created.
- [ ] Two app smoke tests either pass or skip with documented TODO.
- [ ] Suite passes locally on Linux, macOS, and Windows.
- [ ] Suite passes in CI on all 9 matrix cells.
- [ ] CONTRIBUTING.md §7 reference updated.
- [ ] ADR 0008 §B.3 footnote added.
- [ ] `ruff check .` passes.
- [ ] `black --check .` passes.
- [ ] Delivery note `B-002-phase-a-compat-suite.delivery.md` written, including: the bootstrap commands actually used, any examples that needed manual snapshot inspection, and confirmation that running the suite against an unmodified Phase A checkout produces zero failures.
