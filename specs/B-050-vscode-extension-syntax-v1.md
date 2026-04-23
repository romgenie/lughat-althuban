# Spec Packet B-050: vscode-extension-syntax-v1

**Phase**: B
**Depends on**: B-001, B-002
**Estimated size**: medium (2 sessions)
**Status**: deferred (sponsor-conditional)

## Goal

Provide high-quality syntax highlighting for `.apy` files in VS Code using a TextMate grammar. This enables a professional development experience where Arabic keywords, identifiers, and literals are correctly colorized.

## Non-goals

- **No LSP features.** Completion and go-to-definition are in B-052.
- **No debugger integration.**
- **No formatter integration.** Formatter is in B-051.

## Files

### Files to create

- `editors/vscode/package.json` — extension manifest.
- `editors/vscode/syntaxes/arabicpython.tmLanguage.json` — TextMate grammar.
- `editors/vscode/language-configuration.json` — brackets, comments, etc.

## Implementation constraints

- **Grammar format**: TextMate (JSON).
- **Scope names**: Follow standard VS Code naming conventions (e.g., `keyword.control.arabicpython`).
- **RTL handling**: Ensure that the grammar correctly identifies tokens despite being mixed with RTL characters.

## Test requirements

1. `test_syntax_highlighting_keywords`:
   - Input: A file with all Arabic-Python keywords.
   - Expected: Each keyword assigned the correct scope.
2. `test_syntax_highlighting_strings`:
   - Input: Arabic text inside f-strings and regular strings.
   - Expected: Correct scope assignment.

## Acceptance checklist

- [ ] All listed files created.
- [ ] [Phase A Compatibility] Extension correctly highlights Phase A code.
- [ ] VS Code extension builds without errors.
- [ ] `ruff check .` passes (where applicable).
- [ ] Delivery note `B-050-vscode-extension-syntax-v1.delivery.md` written.
