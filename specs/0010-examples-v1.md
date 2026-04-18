# Spec Packet 0010: examples-v1

**Phase**: A (wrap)
**Depends on**: 0001–0009 (all merged)
**Estimated size**: small (1 session)

## Goal

Build a runnable `examples/` directory of 7 progressive `.apy` programs that demonstrate Phase A's full learner-facing feature surface, plus a smoke-test harness that runs each one and asserts on its output. This is the first thing a new user sees after `pip install -e .` and the foundation the upcoming Arabic tutorial will reference. The current state — a single `examples/hello.apy` and one ad-hoc test in `tests/test_cli.py` — was a placeholder; this packet replaces it with a curated, end-to-end-tested suite.

## Non-goals

- **No new transpiler features.** Every example must run on Phase A as it stands today; do not introduce or rely on dictionary changes, new keywords, or unsupported syntax.
- **No I/O-driven examples.** Examples must produce deterministic output without `input()`, network calls, file reads outside the example directory, randomness, or current-time reads.
- **No package examples beyond the import-hook demo.** The `07_imports.apy` + `helper.apy` pair is the only multi-file example; do not introduce sub-packages, `__init__.apy` files, or relative imports (the `from . import x` gap from Packet 0007 still exists).
- **No exception examples that rely on translated class names if the dictionary entry differs from `dictionaries/ar-v1.md` § 5.** Use exactly the canonical names listed there.
- **No examples-as-tutorial.** Comments inside `.apy` files are fine for one-line context; do not write essay-length narration. The tutorial is a separate (planner-authored) doc.

## Files

### Files to create

- `examples/01_hello.apy`
- `examples/02_arithmetic.apy`
- `examples/03_control_flow.apy`
- `examples/04_functions.apy`
- `examples/05_data_structures.apy`
- `examples/06_classes.apy`
- `examples/07_imports.apy`
- `examples/helper.apy`
- `examples/README.md`
- `tests/test_examples.py`

### Files to modify

- `examples/hello.apy` → **delete** (its content is moved to `01_hello.apy`).
- `tests/test_cli.py` — remove `test_examples_hello_runs` (lines 275–282); coverage moves to `tests/test_examples.py`.
- `README.md` — under "Project structure", change the line `└── examples/         Runnable .apy programs (forthcoming)` to `└── examples/         Runnable .apy programs (7 progressive demos)`.

### Files to read (do not modify)

- `dictionaries/ar-v1.md` — the canonical Arabic-to-Python mapping. Every Arabic identifier in every example must be drawn from here. Section 5 (built-in exceptions) is the source of truth for exception class names.
- `arabicpython/cli.py` — for understanding how examples will be invoked.
- `tests/test_cli.py` lines 275–282 — the existing hello smoke-test pattern you are replacing.

## Example file contents

The `.apy` file contents below are **verbatim**. Copy them exactly. Every Arabic identifier has been verified against `dictionaries/ar-v1.md`. Encoding: UTF-8, LF line endings, file ends with a single trailing newline.

### `examples/01_hello.apy`

```
# مرحبا — البرنامج الأول
اطبع("مرحبا، يا عالم")
```

Expected stdout (exact, including trailing newline from `print`):
```
مرحبا، يا عالم
```

### `examples/02_arithmetic.apy`

```
# الحساب والمتغيرات
العمر = 25
السنوات_حتى_التقاعد = 65 - العمر
اطبع(f"باقي {السنوات_حتى_التقاعد} سنة")
```

Expected stdout:
```
باقي 40 سنة
```

### `examples/03_control_flow.apy`

```
# تدفق التحكم: لكل، إذا، وإلا
لكل عدد في نطاق(1, 6):
    إذا عدد % 2 == 0:
        اطبع(f"{عدد}: زوجي")
    وإلا:
        اطبع(f"{عدد}: فردي")
```

Expected stdout:
```
1: فردي
2: زوجي
3: فردي
4: زوجي
5: فردي
```

### `examples/04_functions.apy`

```
# الدوال: تعريف، استدعاء، قيم افتراضية
دالة جمع(أ, ب=10):
    ارجع أ + ب

اطبع(جمع(5))
اطبع(جمع(5, 7))
```

Expected stdout:
```
15
12
```

### `examples/05_data_structures.apy`

```
# القوائم والقواميس
الفواكه = ["تفاح", "موز", "برتقال"]
الأسعار = {"تفاح": 3, "موز": 2, "برتقال": 4}

لكل فاكهة في الفواكه:
    اطبع(f"{فاكهة}: {الأسعار[فاكهة]} ريال")
```

Expected stdout:
```
تفاح: 3 ريال
موز: 2 ريال
برتقال: 4 ريال
```

### `examples/06_classes.apy`

```
# الأصناف: تعريف صنف ودالة بانية
صنف نقطة:
    دالة __init__(الذات, س, ص):
        الذات.س = س
        الذات.ص = ص

    دالة المسافة_من_الأصل(الذات):
        ارجع (الذات.س ** 2 + الذات.ص ** 2) ** 0.5

نقطة_1 = نقطة(3, 4)
اطبع(نقطة_1.المسافة_من_الأصل())
```

Expected stdout:
```
5.0
```

(Note: `الذات` is not a dictionary keyword — it's a user-chosen identifier for `self`. Python treats `self` as convention only, so any identifier works. Same for `نقطة_1` as a variable name.)

### `examples/helper.apy`

```
# وحدة مساعدة تستوردها 07_imports.apy
دالة مربع(عدد):
    ارجع عدد ** 2

دالة مكعب(عدد):
    ارجع عدد ** 3
```

(No expected stdout — this file is imported, not run directly.)

### `examples/07_imports.apy`

```
# استيراد وحدة .apy أخرى عبر import hook
استورد helper كـ مساعد

اطبع(مساعد.مربع(5))
اطبع(مساعد.مكعب(3))
```

Expected stdout:
```
25
27
```

### `examples/README.md`

```markdown
# apython examples

Seven progressive `.apy` programs demonstrating Phase A's feature surface.

| File | Demonstrates |
|---|---|
| `01_hello.apy` | `print` (`اطبع`) and string literals |
| `02_arithmetic.apy` | Variables, integer arithmetic, f-strings |
| `03_control_flow.apy` | `for`/`in`/`range`, `if`/`else`, modulo |
| `04_functions.apy` | `def`, default arguments, `return` |
| `05_data_structures.apy` | Lists, dicts, iteration |
| `06_classes.apy` | `class` with `__init__` and methods |
| `07_imports.apy` (+ `helper.apy`) | The `.apy` import hook in action |

## Running

From the repository root, after `pip install -e .`:

```bash
apython examples/01_hello.apy
apython examples/07_imports.apy   # imports examples/helper.apy via the hook
```

Or run the whole suite as a smoke test:

```bash
python -m pytest tests/test_examples.py
```

## Notes

- All examples are deterministic — no `input()`, randomness, or time-dependent calls.
- Every Arabic identifier is drawn from the canonical dictionary at [`dictionaries/ar-v1.md`](../dictionaries/ar-v1.md).
- For `07_imports.apy` to find `helper.apy`, the working directory must be `examples/` *or* `examples/` must be on `sys.path`. The smoke test handles this by running the example via `subprocess` with `cwd=examples/`.
```

## Public interfaces

This packet adds no new Python public API. The `tests/test_examples.py` module defines its own helpers internally; nothing it exports needs to be importable by other tests.

## Implementation constraints

- **Python version**: 3.11+.
- **Dependencies allowed**: stdlib + pytest only.
- **File encoding**: UTF-8 with LF line endings, single trailing newline. No BOM.
- **Style**: `ruff` and `black` clean on `tests/test_examples.py`.
- **Forbidden**:
  - Any `.apy` example using features outside the verified subset above.
  - Modifying any file under `arabicpython/` — this packet is examples + tests only.
  - Rewriting other tests.
  - Adding `__init__.apy` to `examples/` (would change import semantics).
- **Determinism**: every test must produce identical output across Linux, macOS, Windows on Python 3.11/3.12/3.13. No platform branches in test assertions.

## Test requirements

`tests/test_examples.py` contains the following tests. All examples are run via the in-process `main()` from `arabicpython.cli`, except `07_imports.apy` which is run via `subprocess` so the working directory can be set to `examples/` (the import hook resolves modules relative to `sys.path`, which includes the cwd).

1. `test_01_hello_runs`:
   - Input: `apython examples/01_hello.apy`
   - Expected: exit code 0; stdout exactly `"مرحبا، يا عالم\n"`.

2. `test_02_arithmetic_runs`:
   - Input: `apython examples/02_arithmetic.apy`
   - Expected: exit code 0; stdout exactly `"باقي 40 سنة\n"`.

3. `test_03_control_flow_runs`:
   - Input: `apython examples/03_control_flow.apy`
   - Expected: exit code 0; stdout exactly the 5-line block above (with trailing newline).

4. `test_04_functions_runs`:
   - Input: `apython examples/04_functions.apy`
   - Expected: exit code 0; stdout exactly `"15\n12\n"`.

5. `test_05_data_structures_runs`:
   - Input: `apython examples/05_data_structures.apy`
   - Expected: exit code 0; stdout exactly the 3-line `"تفاح: 3 ريال\n..."` block.

6. `test_06_classes_runs`:
   - Input: `apython examples/06_classes.apy`
   - Expected: exit code 0; stdout exactly `"5.0\n"`.

7. `test_07_imports_runs_via_subprocess`:
   - Run via: `subprocess.run([sys.executable, "-m", "arabicpython.cli", "07_imports.apy"], cwd=<repo>/examples, capture_output=True, text=True, encoding="utf-8")`.
   - Expected: returncode 0; stdout exactly `"25\n27\n"`.
   - Rationale for subprocess: the import hook discovers `helper` via `sys.path`, which includes the cwd at startup; using `subprocess` with `cwd=examples/` is the cleanest way to make `helper.apy` discoverable without mutating `sys.path` in-process.

8. `test_all_expected_examples_present`:
   - Assert every file in the spec's "Files to create" list exists under `examples/`. Catches accidental rename or deletion.

9. `test_examples_readme_exists_and_lists_all_examples`:
   - Assert `examples/README.md` exists.
   - Assert it mentions each example filename (`01_hello.apy` through `07_imports.apy` plus `helper.apy`) at least once.

10. `test_old_hello_apy_removed`:
    - Assert `examples/hello.apy` (the old unnumbered file) does not exist after this packet.

### Edge cases that must be covered

- **UTF-8 encoding**: every `.apy` file is read by Python with explicit `encoding="utf-8"`; assert no `UnicodeDecodeError` is raised during any test.
- **Cross-platform**: tests must use `pathlib.Path` for path construction and never hard-code `/` or `\\` separators in path literals. Output assertions compare strings, not bytes — the UTF-8 stdout fix from PR #11 means `print` of Arabic works on all platforms.

### Test pattern reference

For tests 1–6, mirror the existing pattern at `tests/test_cli.py` lines 275–282 (using `main([str(path)])` and `capsys`). For test 7, mirror the pattern at `tests/test_cli.py` line 286 (`test_subprocess_end_to_end`).

## Reference materials

- Canonical Arabic dictionary: [`dictionaries/ar-v1.md`](../dictionaries/ar-v1.md). Every identifier in every example must be drawn from here.
- ADR 0004 (normalization): [`decisions/0004-normalization-policy.md`](../decisions/0004-normalization-policy.md). Identifiers can be written with or without hamza/ta-marbuta variants — the normalizer folds them. The example files use the dictionary's canonical forms verbatim.
- Existing import-hook demo pattern: `tests/test_import_hook.py` shows how `.apy` modules import each other.
- README structure section: `README.md` line listing `examples/` directory.

## Open questions for the planner

None.

## Acceptance checklist

- [ ] All 10 listed files created (8 `.apy` + `examples/README.md` + `tests/test_examples.py`).
- [ ] `examples/hello.apy` deleted.
- [ ] `tests/test_cli.py` — `test_examples_hello_runs` removed.
- [ ] `README.md` — "forthcoming" line updated.
- [ ] All 10 listed tests present and passing.
- [ ] `ruff check .` passes.
- [ ] `black --check .` passes.
- [ ] `pytest` passes on Python 3.11, 3.12, 3.13 across Linux/macOS/Windows (CI proves this).
- [ ] Manual smoke: `apython examples/07_imports.apy` (run from `examples/` directory) prints `25\n27\n`.
- [ ] Delivery note `0010-examples-v1.delivery.md` written.
