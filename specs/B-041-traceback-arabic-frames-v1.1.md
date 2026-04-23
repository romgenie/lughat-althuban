# Spec Packet B-041: traceback-arabic-frames-v1.1

**Phase**: B
**Depends on**: B-001 (alias-runtime-v1), B-002 (phase-a-compat-suite), B-040 (dictionary-v1.1-async-match)
**Estimated size**: small (1 session)
**Owner**: —

## Goal

Extend the translated traceback system (delivered in Phase A packet 0009) to support the new keywords introduced in v1.1: `متزامن` (async), `انتظر` (await), `مطابقة` (match), and `حالة` (case). This ensures that syntax and runtime errors involving these keywords are presented to the learner in Arabic, maintaining the immersion established in Phase A.

## Non-goals

- **No new traceback infrastructure.** Use the existing `arabicpython/tracebacks.py` logic.
- **No translation of general library exceptions.** Only interpreter-level messages involving the four new keywords.
- **No changes to ar-v1 tracebacks.** This packet only adds to the v1.1 surface.

## Files

### Files to modify

- `arabicpython/tracebacks.py` — add new regex patterns to `MESSAGE_TEMPLATES_AR`.
- `tests/test_tracebacks.py` — add test cases for the new messages.

### Files to read (do not modify)

- `arabicpython/tracebacks.py` — for current message patterns.
- `dictionaries/ar-v1.1.md` — for keyword consistency.

## Public interfaces

This packet modifies internal data tables in `arabicpython/tracebacks.py` but does not change the public API of the `tracebacks` module.

## Implementation constraints

- **Python version**: 3.11+.
- **Dependencies**: stdlib only.
- **Phase A compatibility**: Must not break existing traceback translations for v1 keywords.
- **Keywords**: Use `متزامن`, `انتظر`, `مطابقة`, and `حالة` as specified in the v1.1 requirements.

## Test requirements

1. `test_traceback_await_outside_async`:
   - Input: Source using `انتظر` outside a `متزامن` function.
   - Expected: Arabic traceback containing "انتظر" and its corresponding error message.
2. `test_traceback_match_syntax_error`:
   - Input: Invalid `مطابقة` statement.
   - Expected: Arabic traceback with "مطابقة".

## Acceptance checklist

- [ ] All listed files modified.
- [ ] New tests for v1.1 keywords added and passing.
- [ ] [Phase A Compatibility] `pytest tests/test_tracebacks.py` passes for all Phase A cases.
- [ ] `ruff check .` passes.
- [ ] `black --check .` passes.
- [ ] Delivery note `B-041-traceback-arabic-frames-v1.1.delivery.md` written.
