# Spec Packet B-053: linter-arabicpython-v1

**Phase**: B
**Depends on**: B-001, B-002
**Estimated size**: medium (2 sessions)
**Status**: deferred (sponsor-conditional)

## Goal

Provide a linter for Arabic-Python that wraps `ruff` but adds specific rules for Arabic code. This includes checking for inconsistent normalization, improper RTL/LTR mixing in identifiers, and suggesting Arabic alternatives for common English identifiers.

## Non-goals

- **No new linting engine.** Wrap `ruff`.
- **No auto-fix for complex logic changes.**

## Files

### Files to create

- `arabicpython/linter.py` — wrapper and custom rule logic.
- `tests/test_linter.py`

## Implementation constraints

- **Base Linter**: `ruff`.
- **Custom Rules**: Implemented as plugins or post-processing on `ruff` output.

## Test requirements

1. `test_lint_normalization_error`:
   - Input: Code with non-normalized Arabic identifiers.
   - Expected: Warning/Error identifying the line and character.
2. `test_lint_arabic_suggestion`:
   - Input: Code using `print` instead of `اطبع`.
   - Expected: Suggestion to use the Arabic keyword.

## Acceptance checklist

- [ ] `arabicpython/linter.py` created.
- [ ] [Phase A Compatibility] Lints Phase A code correctly.
- [ ] `pytest tests/test_linter.py` passes.
- [ ] `ruff check .` passes.
- [ ] Delivery note `B-053-linter-arabicpython-v1.delivery.md` written.
