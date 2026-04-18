# Delivery Note: Packet 0010 examples-v1

**PR**: https://github.com/GalaxyRuler/apython/pull/12
**Branch**: `packet/0010-examples-v1`
**Implementation commit**: b5f5ff8aac2fecff2945ab1f3b962a2615654e0f
**Implementer**: Gemini 3.1 Pro
**Reviewer**: Claude

## What shipped — files created, key implementation choices

- `examples/01_hello.apy`: Basic `print` demo.
- `examples/02_arithmetic.apy`: Variables and f-strings.
- `examples/03_control_flow.apy`: `for` loops and `if`/`else`.
- `examples/04_functions.apy`: Function definitions and default arguments.
- `examples/05_data_structures.apy`: Lists and dictionaries.
- `examples/06_classes.apy`: Class definition and instantiation.
- `examples/07_imports.apy` & `examples/helper.apy`: Import hook demonstration.
- `examples/README.md`: Guide for users on running the examples.
- `tests/test_examples.py`: Smoke-test harness running all 7 examples and asserting on exact stdout.
- `README.md`: Updated "Project structure" section.
- `tests/test_cli.py`: Removed the old `test_examples_hello_runs` to avoid duplication.

## Deviations from the spec — anything you did differently and why; "None" if verbatim

- **None.** Verbatim implementation of file contents and test requirements.

## Implementation notes worth remembering — non-obvious decisions

- **PYTHONPATH in tests**: `test_07_imports_runs_via_subprocess` explicitly sets `PYTHONPATH` to include the repository root. This ensures the subprocess can find the `arabicpython` package even when not installed in the environment (e.g., during CI or local development).
- **CWD in manual smoke test**: Verified that `07_imports.apy` correctly imports `helper.apy` when run from the `examples/` directory, confirming the import hook's reliance on `sys.path[0]` (which defaults to the script's directory).

## Validation — what you ran and the result

- `python -m pytest -v`: All 329 tests passed (320 existing + 9 net new).
- `python -m ruff check .`: Clean.
- `python -m black --check .`: Passes.
- Manual smoke: `cd examples; $env:PYTHONPATH=".."; python -m arabicpython.cli 07_imports.apy` printed:
  ```
  25
  27
  ```

## Open questions for the planner — anything ambiguous in the spec

None.
