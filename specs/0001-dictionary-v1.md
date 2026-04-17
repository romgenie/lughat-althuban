# Spec Packet 0001: dictionary-v1

**Phase**: A
**Depends on**: ADRs 0001–0007
**Estimated size**: medium (planner-authored, no Codex implementation this packet)
**Owner**: Claude (planner work; dictionary curation is not delegated)

## Goal

Produce the canonical human-readable Arabic ↔ Python symbol table that governs every later packet. This is the single most consequential artifact in the project because every example, test, tutorial, and downstream library alias eventually binds to these choices.

The output of this packet is a markdown file — pure data, no code. Packet 1.2 turns it into a loadable `arabicpython/dialects/ar.py` module.

## Non-goals

- No code in this packet. The dictionary module (`arabicpython/dialects/ar.py`) is Packet 1.2.
- No translation of stdlib modules, methods outside built-in types, or third-party library symbols. All are Phase B.
- No dunder method translation (`__init__`, `__str__`, etc.). Dunders stay English in Phase A.
- No translation of `self` and `cls`. They are naming conventions, not language syntax; users may pick any first-argument name.
- No alternates or synonyms at runtime (per ADR 0003). Alternates are documented for transparency and for future ADRs.

## Files

### Files to create

- `dictionaries/ar-v1.md` — the canonical table.

## Deliverable structure

`ar-v1.md` contains six sections in this order, each using a compact table format:

1. Control-flow keywords (Python 3.13 `keyword.kwlist` + soft keywords).
2. Literal keywords (False, None, True).
3. Built-in types (int, str, list, ...).
4. Built-in functions (print, len, range, ...).
5. Built-in exceptions (ValueError, TypeError, ...).
6. Common methods on built-in types (.append, .split, .keys, ...).

Every row has: Python name, canonical Arabic, alternates considered, rationale.

## Coverage targets

- **Keywords**: all of `keyword.kwlist` + soft keywords (`match`, `case`, `type`, `_`).
- **Types**: all `types.__builtins__` type objects that a beginner will encounter.
- **Functions**: the ~55 built-in functions most commonly used (intersect of Python docs "Built-in Functions" with common beginner tutorials).
- **Exceptions**: all concrete `Exception` subclasses in stdlib that have a reasonable chance of appearing in beginner code (~40).
- **Methods**: string, list, dict, set methods that appear in typical beginner programs (~28).

Total target: ~180 entries.

## Curation rules

Applied per ADR 0003, in priority order:

1. **Hedy's Arabic translation** where one exists and is unambiguous.
2. **Modern Standard Arabic** over regional dialects.
3. **Shortest defensible translation** when MSA options are equal.
4. **Avoid homographs** with common identifiers; use underscore-composed forms for clarity.

## Acceptance criteria

- [ ] All coverage targets met.
- [ ] Every entry has one canonical translation.
- [ ] No duplicate canonical translations (each Arabic word maps to exactly one Python name).
- [ ] No duplicate Python names (each Python symbol has exactly one canonical Arabic word).
- [ ] Alternates documented for every non-obvious choice.
- [ ] Rationale given in one sentence per entry.
- [ ] File passes the normalizer identity check: `normalize_identifier(entry)` equals the stored entry for every canonical (ensures lookup will work after ADR 0004 normalization).
