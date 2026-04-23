# Spec Packet B-061: cookbook-translation

**Phase**: B
**Depends on**: B-001, B-002, B-060, docs/cookbook.md
**Estimated size**: medium (2 sessions)
**Status**: blocked (requires docs/cookbook.md)

## Goal

Translate the English cookbook (`docs/cookbook.md`) into Arabic (`docs/cookbook-ar.md`). The cookbook contains practical recipes and patterns for common tasks in Arabic-Python, bridging the gap between the tutorial and real-world application.

## Non-goals

- **No new recipes.** Follow the English version exactly.
- **No translation of library docs** mentioned in recipes unless they are part of the core aliases.

## Files

### Files to create

- `docs/cookbook-ar.md` — the Arabic translation.
- `docs/cookbook-ar-glossary.md` — technical terms used in the cookbook.
- `tests/test_cookbook_ar.py` — verifies that all code blocks in the Arabic cookbook run.

## Implementation constraints

- **Style**: Follow the documentation standards set in B-060.
- **Language**: Modern Standard Arabic (MSA).

## Test requirements

1. `test_cookbook_ar_code_blocks`:
   - Extracts and runs all `apy` code blocks in `docs/cookbook-ar.md`.
   - Expected: All blocks exit with returncode 0.

## Acceptance checklist

- [ ] `docs/cookbook-ar.md` created.
- [ ] [Phase A Compatibility] Examples use Phase A conventions correctly.
- [ ] All code blocks passing via `tests/test_cookbook_ar.py`.
- [ ] Glossary updated.
- [ ] Delivery note `B-061-cookbook-translation.delivery.md` written.
