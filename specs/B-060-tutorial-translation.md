# Spec Packet B-060: tutorial-translation

**Phase**: B
**Depends on**: B-001, B-002, B-010, B-030 (so the tutorial can reference real Flask + stdlib aliases). B-040 strongly recommended (so the tutorial can include async/match) but not strictly required — sections that need v1.1 can be marked `(requires --dict ar-v1.1)`.
**Estimated size**: medium-to-large (2–3 sessions of writing)
**Owner**: — (claim via issue; **translation skills required, not coding**)

## Goal

Translate the existing English Phase A tutorial (`docs/tutorial.md`) into a parallel Arabic tutorial (`docs/tutorial-ar.md`), with every example program rewritten in idiomatic Arabic Python and every prose explanation written in clear MSA. After this packet ships, an Arabic-speaking learner can complete the full tutorial without needing to read English at any step.

This packet is the **documentation/translation template**. B-061 (cookbook translation), and any future "translate document X" packet, follow this same shape: side-by-side translation, vocabulary glossary at the end, formal-equivalent prose rather than literal word-by-word, code blocks running under CI.

This is a non-code packet. The deliverable is words, not Python. But it is **not optional fluff** — Phase B's success criterion (ADR 0008.B.4: "a learner writes a working Flask hello-world entirely in Arabic") cannot be met if the path from "I am a beginner" to "I can write Flask" is only documented in English.

## Non-goals

- **No edits to the English tutorial.** `docs/tutorial.md` stays as the source of truth for the English path; the Arabic file is parallel, not derived-by-script.
- **No new examples.** Every example in the Arabic tutorial corresponds to one already in the English tutorial. (The implementer may *add* an Arabic-only example as a clearly-labeled bonus section if a concept needs more explanation in Arabic, but the English tutorial is not retroactively updated to match.)
- **No coverage of Phase B features that haven't shipped.** Reference only what's merged at the time the PR opens. If B-031–038 land later, future packets extend the tutorial; this one doesn't speculate.
- **No machine translation as the source of submission.** The implementer may *consult* MT for vocabulary suggestions, but every paragraph in the final document must be reviewed and rewritten by the human contributor. Reviewer is empowered to reject the PR if MT artifacts (mistranslated technical terms, awkward register-shifts, untranslated English fragments mid-sentence) are detected.
- **No glossary as the sole deliverable.** The glossary is a *companion*; the tutorial prose is the primary deliverable. A 200-word translated tutorial plus a 5000-word glossary is not acceptable.
- **No coverage of installation instructions in this packet.** The README's install section is its own concern; if it needs an Arabic version, that's a separate (small) packet.

## Files

### Files to create

- `docs/tutorial-ar.md` — the Arabic tutorial. Length target: within ±10% of `docs/tutorial.md`'s word count (Arabic prose tends to run slightly shorter; significant deviation in either direction warrants a delivery-note explanation).
- `docs/tutorial-ar-glossary.md` — the technical-term glossary. Each English term used in the tutorial that doesn't have a one-word Arabic equivalent gets a row: English term, chosen Arabic term, one-sentence definition in Arabic, the section of the tutorial where it first appears.
- `tests/test_tutorial_ar.py` — extracts every code block from `docs/tutorial-ar.md`, writes each to a tmp `.apy` file, and runs it via the CLI. Asserts each runs to completion (returncode 0) unless the block is explicitly tagged with `<!-- expected-error -->`.
- `examples/B60_tutorial_excerpts/` — directory containing the longer multi-file tutorial examples (anything > 30 lines), one `.apy` file per example, named to match the section number in the tutorial. Examples ≤ 30 lines stay inline in the markdown.

### Files to modify

- `README.md` — add a top-level link to `docs/tutorial-ar.md` next to the existing link to `docs/tutorial.md`. One line, mirroring the existing pattern.
- `README-ar.md` (if present) — link to the Arabic tutorial from the Arabic README's getting-started section.
- `docs/tutorial.md` — add a single line at the top: `> Arabic version: [tutorial-ar.md](tutorial-ar.md)`. Symmetric link from the Arabic file back to the English one.
- `ROADMAP-PHASE-B.md` — flip status on merge.
- `specs/INDEX.md` — add the row.

### Files to read (do not modify)

- `docs/tutorial.md` — the source of truth.
- `examples/README-ar.md` and `examples/01_hello.apy` through `examples/07_imports.apy` — for tone and example-style consistency.
- `dictionaries/ar-v1.md` (and v1.1 if B-040 has shipped) — vocabulary canon.
- `arabicpython/aliases/*.toml` for any module the tutorial uses — so terms in prose match terms in the alias mappings.
- Any prior Arabic-language Python documentation the implementer can find for style reference (note in the delivery note what they consulted).

## Public interfaces

This packet exposes no Python functions. The interfaces it commits to are:

1. **The Arabic tutorial's table of contents** — ships frozen. Future packets that extend the tutorial add new sections at the end or split sections in place; they do not reorder or rename existing sections, because the README and external links may point to anchor URLs.
2. **The glossary's (English term, Arabic term) pairs** — ship frozen in the same way the dictionary does. Adding a term is fine; changing an existing pair requires a delivery-note justification.

## Implementation constraints

- **Audience**: a beginner who reads MSA fluently. Assume programming background ranges from "complete beginner" to "knows another language well." The English tutorial calibrates this; the Arabic one matches.
- **Register**: Modern Standard Arabic. Avoid dialect (Egyptian, Levantine, Gulf) phrasing even when it would be more natural — the tutorial must read naturally to learners across the Arab world. When MSA gives multiple options for a word, prefer the form most common in computing literature (cite the [Microsoft Arabic Style Guide](https://learn.microsoft.com/en-us/style-guide/arabic/welcome) and/or major university CS curricula in Arabic for precedent — note the source in the glossary's notes column).
- **Technical terms**: when the dictionary or an alias TOML has translated the term, use that translation. When it hasn't (e.g. "decorator", "context manager", "iterator"), the implementer chooses; every such choice is recorded in the glossary with rationale.
- **Bidirectional text in code blocks**: code is left-to-right; surrounding prose is right-to-left. The Markdown renderer handles this correctly for fenced code blocks; the implementer verifies rendering on GitHub before requesting review (screenshot in the PR).
- **Punctuation**: use Arabic punctuation (`،` comma, `؛` semicolon, `؟` question mark) in prose. Code blocks use ASCII punctuation as Python requires.
- **Numbers in prose**: Arabic-Indic digits (٠١٢٣٤٥٦٧٨٩) for narrative numbers; ASCII digits in code. Section numbering follows the English tutorial (1, 2, 3 — for cross-reference).
- **Line length**: no hard wrap on prose paragraphs (Markdown handles it). Code blocks at ≤ 88 columns to match `black`.
- **Examples must run.** Every code block in the tutorial is extracted by the test suite and executed. A non-runnable example must be tagged with an HTML comment marker:
  - `<!-- expected-error -->` — the block is meant to demonstrate a runtime error; the test asserts non-zero exit.
  - `<!-- not-runnable: snippet -->` — the block is a fragment (e.g. shows just a class definition with no driver); the test skips it.
  - `<!-- requires: ar-v1.1 -->` — the block needs the v1.1 dictionary; the test runs it with `--dict ar-v1.1`. If B-040 hasn't merged, the test marks `pytest.skip` with a clear reason.
- **No emoji.** The English tutorial doesn't use them; the Arabic one matches.
- **Style**: documents must pass `prettier --check '**/*.md'` if the project uses prettier (check `package.json` or `.prettierrc`). If not, ad-hoc consistency with the existing `.md` files in the repo.

## Test requirements

### `tests/test_tutorial_ar.py`

1. `test_tutorial_ar_exists_and_is_well_formed`:
   - Assert the file exists and is valid UTF-8.
   - Assert it starts with a level-1 heading (`# `).
   - Assert it contains at least N section headings, where N matches the English tutorial's section count (parametrize from a parsing of `docs/tutorial.md`).

2. `test_tutorial_ar_section_titles_correspond_to_english`:
   - Parse the heading lists from both files.
   - Assert the count matches (or differs by ≤ 1, allowing for an Arabic-only bonus section as documented in non-goals).
   - **Do not assert title equality** — they're different languages. Just count parity.

3. `test_tutorial_ar_code_blocks_run`:
   - Parametrize over every fenced code block whose info string is `apy` or `arabicpython`.
   - For each block:
     - Skip if marked `<!-- not-runnable: snippet -->`.
     - If marked `<!-- requires: ar-v1.1 -->` and B-040 hasn't merged (detected by `pathlib.Path("dictionaries/ar-v1.1.md").exists()`), `pytest.skip`.
     - Write the block to a tmp `.apy` file.
     - Run via the CLI subprocess (reuse `run_apy_program` from B-002).
     - If marked `<!-- expected-error -->`, assert returncode != 0.
     - Else assert returncode == 0 and stderr is empty.
   - Failure message includes the file:line where the block starts.

4. `test_glossary_covers_introduced_terms`:
   - Define a small list of "key terms" the tutorial is expected to introduce: `decorator`, `iterator`, `generator`, `context_manager`, `coroutine`, `module`, `package`, `exception`, `keyword_argument`, `list_comprehension`. (Implementer adjusts to match what their tutorial actually covers.)
   - Assert every entry in this list appears as a row in the glossary.

5. `test_glossary_terms_match_dictionary_when_overlapping`:
   - For every term in the glossary that's also in `ar-v1.md` or any `aliases/*.toml`, assert the Arabic translation matches.
   - Failure means the tutorial would teach learners a term that doesn't match the runtime — a serious confusion source.

6. `test_external_examples_referenced_by_tutorial_exist`:
   - Parse the tutorial for relative paths to `examples/B60_tutorial_excerpts/*.apy`.
   - For each, assert the file exists.

7. `test_external_examples_run`:
   - Parametrize over every file in `examples/B60_tutorial_excerpts/`.
   - Run each via the CLI; assert returncode 0 and stderr empty.

8. `test_phase_a_compat_unchanged`:
   - Re-run B-002's compat suite assertions to be defensive: nothing in this packet should have touched a Phase A artifact.

### Quality gates that are NOT automated

The following are reviewer responsibilities, listed here so the reviewer knows what to check (the spec doesn't try to mechanize what it can't reliably mechanize):

- Prose reads as natural MSA, not English-shaped Arabic.
- Technical accuracy of explanations matches the English tutorial.
- No untranslated English fragments inside Arabic sentences (a common MT artifact).
- Bidirectional rendering looks correct on GitHub's web view (PR includes a screenshot).
- Glossary terms have one-sentence definitions that genuinely define, not just transliterate.

## Reference materials

- `docs/tutorial.md` — the source.
- `dictionaries/ar-v1.md` and (if shipped) `dictionaries/ar-v1.1.md`.
- `arabicpython/aliases/*.toml` for any module the tutorial covers.
- `examples/README-ar.md` — established Arabic prose style.
- Microsoft Arabic Style Guide: https://learn.microsoft.com/en-us/style-guide/arabic/welcome
- ALECSO Arabic computing terminology references (the implementer cites whichever they actually consult).
- ADR 0008.B.4 — the success criterion this tutorial enables.

## Open questions for the planner

1. **Should the glossary be its own file (as specified) or an appendix in `tutorial-ar.md`?** Recommended: separate file, because future tutorials/cookbooks will share it. The tutorial links to it from its first technical-term introduction.
2. **What's the policy on transliteration vs. translation for proper nouns (Flask, pytest, JSON)?** Recommended: keep the English brand name in Latin script when it's a project name (Flask, pytest); translate the underlying noun when used generically (JSON → `جسون` in identifiers per B-010, but spelled `JSON` in prose when referring to the format itself). Implementer documents the chosen rule in the glossary's introduction.

## Acceptance checklist

- [ ] `docs/tutorial-ar.md` written; word count within ±10% of English tutorial.
- [ ] Every English-tutorial section has an Arabic counterpart (titles need not be literal translations).
- [ ] `docs/tutorial-ar-glossary.md` written; covers every key term introduced.
- [ ] `examples/B60_tutorial_excerpts/` populated with the multi-file examples; each runs.
- [ ] All 8 tests above present and passing on the 9-cell matrix.
- [ ] README and English tutorial cross-link to the Arabic version.
- [ ] PR description includes a screenshot of the rendered Arabic tutorial on GitHub.
- [ ] `pytest tests/test_phase_a_compat.py` passes unchanged.
- [ ] `ruff check .` passes (no Python files added/modified outside `tests/`).
- [ ] `black --check .` passes.
- [ ] Reviewer (a separate Arabic-fluent contributor, not the implementer) has signed off on prose quality in a PR review comment, not just an approval.
- [ ] Delivery note `B-060-tutorial-translation.delivery.md` written. Required sections: style references consulted; every glossary term where the implementer chose a translation not previously used in the project (with rationale); any Phase B feature deliberately omitted from coverage (with reason); an Arabic-fluent reviewer's name.
