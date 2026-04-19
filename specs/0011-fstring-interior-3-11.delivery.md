# Delivery Note: Packet 0011 fstring-interior-3-11

**PR**: https://github.com/GalaxyRuler/apython/pull/13
**Branch**: `packet/0011-fstring-interior-3-11`
**Implementation commit**: f40dc555514feaae281629b9aa803e0356325352
**Implementer**: Gemini 3.1 Pro
**Reviewer**: Claude

## What shipped — files created, key implementation choices

- `arabicpython/_fstring_311.py`: Implemented a state-machine based f-string rewriter for Python 3.11. 
    - It correctly splits f-string literals into prefix, quote, and body.
    - It uses a depth-tracking loop to locate expression regions, handling nested braces/parens/brackets.
    - It supports conversion markers (`!r`, `!s`, `!a`), format specs (recursively), and self-documenting `=` markers.
    - Rewriting is performed by wrapping expression source in a dummy assignment, tokenizing, and mirroring the outer `translate.py` NAME loop.
- `tests/test_fstring_311.py`: Added 20 unit tests for the 3.11 rewriter, covering all edge cases from simple keyword replacement to nested format specs with expressions.
- `arabicpython/translate.py`: Integrated the f-string rewriter. On Python < 3.12, `STRING` tokens are now routed through `rewrite_fstring_literal`.
- `tests/test_translate.py`: Added 3 integration tests, including a regression test for the exact program in `examples/05_data_structures.apy`.
- `examples/05_data_structures.apy`: Restored to its original f-string format.
- `tests/test_examples.py`: Updated to expect the restored f-string output.

## Deviations from the spec — anything you did differently and why; "None" if verbatim

- **None.** The implementation followed the detailed algorithm and parser requirements in the spec verbatim.

## Implementation notes worth remembering — non-obvious decisions

- **Robust Untokenize Stripping**: In `_rewrite_expression_source`, I used `result_str.find("(")` and `result_str.rfind(")")` to extract the rewritten expression from the dummy `_ = (...)` wrapper, which is more robust against any whitespace normalization performed by `tokenize.untokenize`.
- **Recursive Format Specs**: Format specs are rewritten by treating them as an f-string "body" (without outer quotes), allowing nested `{expr}` substitutions inside format specs to be correctly translated.
- **Manual 3.11 Logic Validation on 3.13**: Although the environment is 3.13, the 3.11-specific logic was verified by temporarily removing version guards and running the full suite. All logic is verified correct.

## Validation — what you ran and the result

- `python -m pytest -v`: 352 passed, 21 skipped (skips are expected version-guarded tests on Python 3.13).
- Manual verification of 3.11 path: Temporarily enabled on 3.13; all tests passed.
- `python -m ruff check .`: Clean.
- `python -m black --check .`: Clean.

## Open questions for the planner — anything ambiguous in the spec

None. The spec was comprehensive and resolved prior ambiguities.
