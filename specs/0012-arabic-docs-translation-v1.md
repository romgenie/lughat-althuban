# Spec Packet 0012: arabic-docs-translation-v1

**Phase**: A (documentation wrap)
**Depends on**: 0001–0011 all merged
**Estimated size**: small (1 session)

## Goal

Produce accurate Arabic translations of every user-facing and developer-facing
English documentation file so that Arabic-speaking users and contributors can
read all project documentation in Arabic without switching languages. Four files
are created or overwritten (two are replacements for earlier hand-written Arabic
files that were authored natively rather than translated from the English
originals).

No code is changed. No tests are written. This packet is purely file creation.

## Non-goals

- Does not translate internal planner/implementer artefacts: `specs/`, `decisions/`, `dictionaries/REVIEW-*.md`, `dictionaries/AUDIT-*.md`.
- Does not add a cross-language nav link from `README.md` to `docs/ar/README.md` (future cleanup).
- Does not translate the dictionary files themselves (`ar-v1.md`, `exceptions-ar-v1.md`) — they are already bilingual by design.
- Does not modify any `.py`, `.apy`, or test file.
- Does not translate `docs/ar/overview.md` — that file has no English counterpart and is correct as-is.

## Files

### Files to create

- `docs/ar/README.md` — Arabic translation of `README.md`
- `docs/ar/CHANGELOG.md` — Arabic translation of `CHANGELOG.md`

### Files to overwrite

- `docs/ar/getting-started.md` — replace the hand-written Arabic version with a
  translation of `docs/getting-started-ar.md`
- `examples/README-ar.md` — replace the hand-written Arabic version with a
  translation of `examples/README.md`

### Files to read (source material — do not modify)

- `README.md`
- `CHANGELOG.md`
- `docs/getting-started-ar.md`
- `examples/README.md`

### Files to read (context — do not modify)

- `docs/ar/overview.md` — reference for tone and MSA vocabulary already
  established in this project's Arabic writing
- `dictionaries/ar-v1.md` — authoritative Arabic keyword spellings; any Arabic
  keyword that appears in a code sample must use exactly the form shown here

---

## Translation rules

### 1. RTL wrapper

Every output file must begin with `<div dir="rtl">` on its own line, followed
by a blank line, and end with a blank line followed by `</div>`. No other HTML
is permitted.

```
<div dir="rtl">

[file content]

</div>
```

### 2. Language: Modern Standard Arabic (MSA)

Write in formal Modern Standard Arabic (الفصحى المعاصرة). Match the register
already established in `docs/ar/overview.md`. Avoid dialect, colloquialisms,
and loan-word clutter where a clean Arabic equivalent exists.

### 3. Code blocks — never translate code

Inside any fenced code block (`` ``` `` or `~~~`), translate **only** inline
comments (text after `#`). Do not alter any other line:

```python
# هذا التعليق يُترجَم
دالة مرحبا():          # لا تغيّر الشيفرة
    اطبع("مرحبا")
```

The Arabic apython keywords that already appear in code samples (`اطبع`, `إذا`,
`دالة`, etc.) are NOT English text — leave them exactly as written.

### 4. Inline code spans — never translate

Text inside backticks in prose (`` `apython` ``, `` `dict` ``, `` `.apy` ``,
`` `sys.meta_path` ``, etc.) is never translated. The surrounding prose is
translated; the inline code is preserved verbatim.

### 5. Terms that stay in English everywhere

The following proper names and technical abbreviations must appear in Latin
script in all contexts (prose, headings, tables, bullets):

`apython`, `CPython`, `Python`, `GitHub`, `ADR`, `CLI`, `REPL`, `API`,
`ASCII`, `Unicode`, `RTL`, `LTR`, `MSA`, `pip`, `git`, `pytest`, `black`,
`ruff`, `zhpy`, `Hedy`, `Qalb`, `Apache-2.0`, `sys.path`, `sys.meta_path`,
`Phase A`, `Phase B`, `f-string`, `tokenize`, `pretokenize`, `untokenize`,
`compile`, `exec`, `AST`

### 6. File paths, URLs, version numbers

Never translate file paths (`docs/ar/README.md`), GitHub URLs, version
strings (`v0.1.1`, `3.11`), commit hashes, or section anchors.

### 7. Headings

Translate heading text. Preserve heading level (`#`, `##`, `###`).

### 8. Tables

Translate all cell text that is prose. Do not translate cell text that is
inline code, a file path, a URL, or a term in rule 5.

### 9. Changelog version blocks

In `CHANGELOG.md`, the version line format is:
```
## [0.1.1] — 2026-04-20 — Dictionary rendering + coverage pass
```
Translate only the English description after the date. Keep `[0.1.1]`,
the date, and the `—` separators as-is.

### 10. Anchor links in the table of contents

`docs/getting-started-ar.md` has a TOC with anchor links like
`[Install](#1-install)`. After translating headings, update anchors to match
the Arabic headings using GitHub's anchor rules: lowercase, spaces → `-`,
strip punctuation. If anchor derivation is uncertain, omit the TOC links
(just list the section names without hyperlinks) rather than produce broken
anchors.

---

## Acceptance checklist

- [ ] `docs/ar/README.md` created; content is a complete translation of `README.md`.
- [ ] `docs/ar/CHANGELOG.md` created; content is a complete translation of `CHANGELOG.md`.
- [ ] `docs/ar/getting-started.md` overwritten; content is a complete translation of `docs/getting-started-ar.md`.
- [ ] `examples/README-ar.md` overwritten; content is a complete translation of `examples/README.md`.
- [ ] Every output file starts with `<div dir="rtl">` and ends with `</div>`.
- [ ] No code inside fenced code blocks has been altered (only `#` comments translated).
- [ ] No inline code spans have been translated.
- [ ] All terms in rule 5 appear in Latin script.
- [ ] No `.py`, `.apy`, or test file has been modified.
- [ ] All four files committed in a single commit with message:
  `docs(ar): translate README, CHANGELOG, getting-started, examples guide to Arabic (packet 0012)`
- [ ] Delivery note `specs/0012-arabic-docs-translation-v1.delivery.md` written.
