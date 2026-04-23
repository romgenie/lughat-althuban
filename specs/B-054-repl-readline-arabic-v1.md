# Spec Packet B-054: repl-readline-arabic-v1

**Phase**: B
**Depends on**: B-001, B-002, B-008 (repl-v1)
**Estimated size**: medium (2 sessions)
**Status**: deferred (sponsor-conditional)

## Goal

Improve the Arabic-Python REPL by adding advanced line-editing capabilities via `readline` (or `prompt_toolkit`). This includes better support for Arabic input editing, tab completion for Arabic keywords/identifiers, and persistent history.

## Non-goals

- **No GUI REPL.** Stay in the terminal.
- **No multi-line editing** beyond basic `readline` capabilities unless using `prompt_toolkit`.

## Files

### Files to modify

- `arabicpython/repl.py` — integrate `readline` or `prompt_toolkit`.

## Implementation constraints

- **Dependencies**: `readline` (stdlib) or `prompt_toolkit`.
- **RTL Support**: Must handle cursor movement correctly in mixed RTL/LTR lines.

## Test requirements

1. `test_repl_completion`:
   - Input: `اطب` + `<TAB>`.
   - Expected: Completes to `اطبع`.
2. `test_repl_history`:
   - Input: Enter a command, restart REPL, use up-arrow.
   - Expected: Previous command restored.

## Acceptance checklist

- [ ] REPL editing improved.
- [ ] [Phase A Compatibility] Maintains all Phase A REPL functionality.
- [ ] `pytest` passes.
- [ ] `ruff check .` passes.
- [ ] Delivery note `B-054-repl-readline-arabic-v1.delivery.md` written.
