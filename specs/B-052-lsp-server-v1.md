# Spec Packet B-052: lsp-server-v1

**Phase**: B
**Depends on**: B-001, B-002
**Estimated size**: large (3+ sessions)
**Status**: deferred (sponsor-conditional)

## Goal

Implement a Language Server Protocol (LSP) server for Arabic-Python. This provides essential IDE features: code completion for Arabic keywords and identifiers, go-to-definition, and hover information (including Arabic translations for stdlib docstrings where available).

## Non-goals

- **No refactoring tools** (rename, etc.) in v1.
- **No type checking** beyond what the underlying Python LSP (like `pyright`) provides.

## Files

### Files to create

- `arabicpython/lsp/server.py` — LSP server implementation.
- `arabicpython/lsp/handlers.py` — Request handlers.
- `tests/test_lsp.py`

## Implementation constraints

- **Protocol**: LSP 3.17+.
- **Performance**: Completion latency < 100ms.
- **Library**: `pygls` recommended.

## Test requirements

1. `test_completion_keywords`:
   - Input: Partial Arabic keyword.
   - Expected: List of matching Arabic-Python keywords.
2. `test_goto_definition`:
   - Input: Usage of an Arabic identifier.
   - Expected: Location of the identifier's definition.

## Acceptance checklist

- [ ] LSP server implemented and functional.
- [ ] [Phase A Compatibility] Works correctly with Phase A code.
- [ ] `pytest tests/test_lsp.py` passes.
- [ ] `ruff check .` passes.
- [ ] Delivery note `B-052-lsp-server-v1.delivery.md` written.
