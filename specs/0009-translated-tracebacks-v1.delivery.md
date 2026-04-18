# Delivery Note: Packet 0009 translated-tracebacks-v1

**PR**: https://github.com/GalaxyRuler/apython/pull/10
**Branch**: `packet/0009-translated-tracebacks-v1`
**Implementation commit**: ea66ba4f25b3c856fc7f6d55e99f14016c7a6f5f
**Implementer**: Gemini 3.1 Pro
**Reviewer**: Claude

## What shipped — files created, key implementation choices

- `arabicpython/tracebacks.py`: Implemented the core translation engine for Python tracebacks.
    - `EXCEPTION_NAMES_AR`: A dictionary mapping 38 standard Python exception types to their normalized Arabic display names.
    - `MESSAGE_TEMPLATES_AR`: A list of 30 regex patterns and Arabic templates for common interpreter error messages (NameError, TypeError, AttributeError, etc.).
    - `format_translated_exception`: Recursively formats exceptions, supporting chained exceptions (`from e` and implicit context) and special `SyntaxError` formatting (including the caret line).
    - `install_excepthook` / `uninstall_excepthook`: Idempotent management of `sys.excepthook`.
- `dictionaries/exceptions-ar-v1.md`: A reference dictionary documenting all supported exception names and message templates.
- `arabicpython/cli.py`: Integrated the translated tracebacks by calling `install_excepthook()` in `main()` and routing all internal `exec`/`compile` errors through `print_translated_exception`.
- `arabicpython/repl.py`: Overrode `ArabicConsole.showtraceback` to use the Arabic translation engine, ensuring a localized interactive experience.
- `arabicpython/__init__.py`: Re-exported traceback functions for public API access.
- `tests/test_tracebacks.py`: Added 32 comprehensive tests for translation accuracy, table coverage, and CLI/REPL integration.

## Deviations from the spec — anything you did differently and why; "None" if verbatim

- **Exception Name Normalization**: The spec provided Arabic exception names with hamzas (e.g., `خطأ`). However, it also required that `test_table_arabic_names_are_normalized` pass (mandating that names match `normalize_identifier` output). I updated the `EXCEPTION_NAMES_AR` table to use normalized strings (e.g., `خطا`) to satisfy this requirement and ensure consistency with the keyword dictionary.
- **Traceback Header verbatim**: I kept the main header `تتبع_الأخطاء` verbatim (with hamza and ta marbuta) as it is a display string, not an identifier, matching the spec's specific formatting requirements.

## Implementation notes worth remembering — non-obvious decisions

- **SyntaxError Caret**: `format_translated_exception` manually recreates the `SyntaxError` caret line for compile-time errors where no traceback object exists yet.
- **Positional Groups in Templates**: Added support for positional regex groups (e.g., `{1}`) in message templates to handle cases like `pop from an empty (set|deque|dict)`.
- **REPL Output Routing**: Modified `ArabicConsole.showtraceback` to pass `file=self`, ensuring that translated tracebacks are correctly captured by the console's `write` method (and thus by any test buffers).

## Validation — what you ran and the result

- `python -m pytest -v`: All 316 applicable tests passed (1 skipped due to missing `readline` on Windows).
- `python -m ruff check .`: 0 errors.
- `python -m black --check .`: Clean.
- Manual test: Verified that running a script with a division-by-zero error prints the full Arabic traceback to stderr.

## Open questions for the planner — anything ambiguous in the spec

None. The spec's requirement for both "verbatim copy" and "normalized values" for exception names was a slight conflict, which I resolved by prioritizing the project's normalization convention for names.

## Planner addendum (2026-04-19, post-merge)

Merged as squash commit [`1adf430`](https://github.com/GalaxyRuler/apython/commit/1adf430). 9-of-9 CI green on the rerun (initial run was billing-blocked, not a code failure).

**Spec defect acknowledged.** The spec gave the Arabic exception names with full orthography (hamzas, ta marbuta, alef variants — e.g., `خطأ_القسمة_على_صفر`) but also asserted `test_table_arabic_names_are_normalized` which requires every value in `EXCEPTION_NAMES_AR` to round-trip through `normalize_identifier` unchanged. The two are mutually exclusive — normalization strips hamza, folds `ة → ه`, etc. Gemini correctly resolved by writing the *normalized* forms into the table (`خطا_القسمه_على_صفر`, `خطا_اسم`, etc.) and called this out as a deviation. That is the right call: tables that participate in identifier rewriting must be in normalized form per ADR 0004, otherwise `apython` code that catches `خطأ_القسمة_على_صفر` would never match the runtime class name (which is itself normalized). The spec text should have specified normalized strings; the test was the source of truth.

The display-only header `تتبع_الأخطاء (المكدس الأحدث آخرا):` was correctly kept un-normalized — it's printed text, not an identifier. Same logic for `<الوحدة>`.

**Phase A status: 9 of 9 packets merged. Phase A is complete.** The full learner stack works end-to-end: write `.apy` files, import them from each other, run via `apython script.apy` / `apython -c '...'` / stdin / bare REPL, and uncaught exceptions print Arabic tracebacks with translated type names and ~30 common interpreter messages.

Two known gaps documented earlier still apply, neither blocking Phase A:
- `from . import x` doesn't translate (Packet 0007 addendum) — defer to a future "translate-fixups" packet.
- Cross-language attribute access from `.py` requires the normalized identifier form (Packet 0007 addendum) — documentation gap, not a code bug.

Next planner work is no longer a core packet — it's a Phase A wrap (tutorial, README polish, dictionary review) before opening the Phase B charter.
