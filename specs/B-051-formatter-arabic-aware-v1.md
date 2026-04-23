# Spec Packet B-051: formatter-arabic-aware-v1

**Phase**: B
**Depends on**: B-001, B-002
**Estimated size**: medium (2 sessions)
**Status**: deferred (sponsor-conditional)

## Goal

Create a code formatter for Arabic-Python that wraps `black` but is "Arabic-aware." Specifically, it must handle the alignment of Arabic identifiers in column-based code (like tables of constants or long argument lists) where standard `black` might cause visually jarring misalignments due to RTL/LTR mixing.

## Non-goals

- **No custom formatting engine.** Must delegate to `black` for all standard Python formatting.
- **No modification of Python semantics.**

## Files

### Files to create

- `arabicpython/formatter.py` — the wrapper logic.
- `tests/test_formatter.py`

## Implementation constraints

- **Base Formatter**: `black` (latest stable).
- **Style**: Preserve `black` defaults (line length 100) except where Arabic alignment requires adjustment.
- **Performance**: Should not be significantly slower than running `black` directly.

## Test requirements

1. `test_format_arabic_identifiers`:
   - Input: Unformatted Arabic-Python code.
   - Expected: Output matches `black` formatting but preserves visual alignment of RTL identifiers.
2. `test_format_mixed_scripts`:
   - Input: Code with mixed Arabic and English identifiers.
   - Expected: Consistent spacing and indentation.

## Acceptance checklist

- [ ] `arabicpython/formatter.py` created.
- [ ] [Phase A Compatibility] Formats Phase A code correctly.
- [ ] `pytest tests/test_formatter.py` passes.
- [ ] `ruff check .` passes.
- [ ] `black --check .` passes.
- [ ] Delivery note `B-051-formatter-arabic-aware-v1.delivery.md` written.
