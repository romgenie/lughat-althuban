# Delivery Note: Packet 0004 pretokenize-v1

**PR**: 5
**Branch**: packet/0004-pretokenize-v1
**Implementation commit**: ffb0d5fdbecf90e2b8ce049dbec4f676fce17e28
**Implementer**: Gemini 3.1 Pro
**Reviewer**: Claude

## What shipped — files created, key implementation choices
- Created `arabicpython/pretokenize.py` matching the public interface from the spec exactly.
- Created `tests/test_pretokenize.py` with all 53 specified tests.
- Implemented a single-pass `O(n)` character-based state machine processing the source string byte-by-byte instead of regex or multiple passes.
- To prevent performance regression with strings containing millions of characters, I built the output list char by char or chunk by chunk and used `"".join(out)` at the end.
- Added strict line and column tracking via manual incrementing to provide completely accurate line and column numbers in `SyntaxError` exceptions.

## Deviations from the spec — anything you did differently and why; "None" if verbatim
None. The implementation followed the spec and corresponding ADRs strictly. 

## Implementation notes worth remembering — non-obvious decisions
- Python escape handling inside strings (`\`) requires that the next character is blindly passed into the string buffer without checking if it might be an end quote. I introduced a small `escape_next` flag for this purpose to make sure that escaped characters (like `\'`) inside a single-quote string do not mistakenly terminate the `STRING_SQ` state.
- Bidi error raising is hardcoded to emit the exact phrase from ADR 0006, ensuring 100% test compatibility. 
- Using `unicodedata.name()` resolves the name dynamically, removing the need for a manually maintained map of the 9 bidi control characters.

## Validation — what you ran and the result
- `python -m pytest tests/test_pretokenize.py -v`: 53 tests passed.
- `python -m ruff check .`: 0 errors.
- `python -m black --check .`: Passes completely.

## Open questions for the planner — anything ambiguous in the spec
None. The spec was completely unambiguous and covered all edge cases.