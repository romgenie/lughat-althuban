# Spec Packet B-040: dictionary-v1.1-async-match

**Phase**: B
**Depends on**: B-001 (alias-runtime-v1), B-002 (phase-a-compat-suite)
**Estimated size**: small (1 session) — but governance-heavy
**Owner**: — (claim via issue; **requires planner co-sign before merge**)

## Goal

Ship `dictionaries/ar-v1.1.md` — a strict superset of the Phase A core dictionary `ar-v1.md` — adding Arabic keywords for the four Python control-flow surfaces that Phase A explicitly deferred: `async`, `await`, `match`, and `case`. After this packet ships, an Arabic-Python program can express modern asynchronous code and structural pattern matching without falling back to English.

This packet is **small in code** and **large in governance**. Per ADR 0008.B.0, `ar-v1.md` is immutable; ar-v1.1 is the first time the project produces a successor dictionary, and the precedent set here governs every future dictionary packet (v1.2, v2, dialect variants). The acceptance bar is therefore higher: the planner must explicitly co-sign the four chosen Arabic terms before the PR can merge.

## Non-goals

- **No edits to `ar-v1.md`.** That file is forever frozen. v1.1 is a separate file. The translator selects which dictionary to use at parse time (selection mechanism is part of this packet).
- **No coverage of `async for` and `async with` as separate keywords.** Python's grammar treats these as combinations of `async` + `for`/`with`, so once `async` is translated, the combinations come along automatically. The tests verify this rather than the dictionary listing them separately.
- **No coverage of soft keywords beyond `match`/`case`.** `_` (the wildcard pattern) stays as `_` — it is not an identifier the learner types as a word.
- **No translation of `type` (the soft keyword for type aliases, PEP 695).** That is its own packet candidate (defer to a future B-04x); it interacts with the type system, not control flow.
- **No new translator features.** The dictionary-loader infrastructure already supports versioned dictionaries (delivered in Phase A packet 0003). This packet only adds the data file and the selection wiring.
- **No deprecation of v1.** Programs that opt into v1.1 get the four new keywords; programs that don't, behave exactly as before. v1.1 is purely additive.

## Files

### Files to create

- `dictionaries/ar-v1.1.md` — the new dictionary file. Structurally identical to `ar-v1.md`, with four added rows (the four new keywords) and a header note explaining the relationship to v1.
- `tests/test_dictionary_v1_1.py` — integrity, supersetness, and behavioral tests.
- `examples/B40_async_demo.apy` — minimal async/await demo (one coroutine, one `asyncio.run` call).
- `examples/B40_match_demo.apy` — minimal match/case demo (a four-arm match on a tagged shape).
- `examples/B40_README-ar.md` — Arabic walkthrough of both demos.
- `decisions/0009-dictionary-versioning.md` — **new ADR** capturing the precedent this packet sets. Required because this is the first successor dictionary; future packets will cite this ADR.

### Files to modify

- `arabicpython/translate.py` — accept a `dict_version` parameter (default `"ar-v1"` for backward compat); plumb it to the dictionary loader. The CLI gains a `--dict ar-v1.1` flag.
- `arabicpython/cli.py` — add the `--dict` flag and a per-file directive `# arabicpython: dict=ar-v1.1` (parsed from the first 5 lines of the file) so example files can pin their dictionary.
- `ROADMAP-PHASE-B.md` — flip status on merge.
- `specs/INDEX.md` — add the row.

### Files to read (do not modify)

- `dictionaries/ar-v1.md` — the parent dictionary. v1.1 must be a strict superset.
- `decisions/0008-phase-b-charter.md` §B.0 — the immutability promise.
- `decisions/0003-curation-rules.md` — translation principles, fully applicable here.
- `arabicpython/dialect_loader.py` (Phase A packet 0003) — the dictionary loader's existing version-handling.
- Python language reference: [coroutines](https://docs.python.org/3.11/reference/compound_stmts.html#coroutines), [match statements](https://docs.python.org/3.11/reference/compound_stmts.html#the-match-statement).
- PEP 492 (async/await), PEP 634 (structural pattern matching) — for keyword semantics.

## Public interfaces

### Translator API change

```python
# arabicpython/translate.py

def translate(
    source: str,
    *,
    dict_version: str = "ar-v1",  # NEW; default preserves Phase A behavior
) -> str:
    """Translate Arabic-Python source to Python source.

    Args:
      source: The full text of an .apy file (or a fragment for the REPL).
      dict_version: Which dictionary to apply. Must be one of the names listed
        under `dictionaries/`. Defaults to "ar-v1" — Phase A programs that don't
        opt in see no change.

    Raises:
      DictionaryNotFoundError: if `dict_version` doesn't resolve to a file.
      ValueError: if the file selected via per-file directive disagrees with
        the explicit kwarg (caller's choice wins; this is a hard error so
        ambiguity surfaces early).
    """
```

### Per-file directive

The first five lines of an `.apy` file may contain a comment of the form:

```
# arabicpython: dict=ar-v1.1
```

If present, the CLI uses that dictionary. The parsing rule is: exact prefix `# arabicpython: dict=`, followed by the version string up to end-of-line, in any of the first five lines (so a shebang on line 1 doesn't block it). Multiple directives → first wins; explicit `--dict` flag overrides.

### Dictionary file format

`ar-v1.1.md` is a Markdown file with the same table format as `ar-v1.md`:

```markdown
# Arabic Python Dictionary v1.1

Strict superset of v1; adds async/await/match/case. See ADR 0009.

| Arabic | Python | Category | Notes |
|---|---|---|---|
| اطبع | print | builtin | (inherited from v1) |
| ... | ... | ... | (every v1 row reproduced verbatim) |
| متزامن | async | keyword | (new in v1.1) |
| انتظر | await | keyword | (new in v1.1) |
| طابق | match | soft-keyword | (new in v1.1) |
| حالة | case | soft-keyword | (new in v1.1) |
```

The four new rows are listed at the bottom under a `## v1.1 additions` heading so a `git diff` against v1 cleanly shows the delta.

## Implementation constraints

- **Python version**: 3.11+. `match`/`case` are 3.10+; `async`/`await` are 3.5+; both fully available on the supported matrix.
- **Dependencies**: stdlib only.
- **Strict supersetness is enforced by test**, not by trust. The supersetness test loads both files, parses them as the dictionary loader would, and asserts every (Arabic, Python) pair from v1 appears identically in v1.1.
- **Translator default unchanged.** A v1 program with no directive and no flag must produce byte-identical translated output before and after this packet ships. (The Phase A compat suite from B-002 enforces this.)
- **No reflection of v1.1 entries into v1.** If the implementer accidentally adds the four new entries to `ar-v1.md`, the dictionary snapshot test from B-002 will fail. That's the safety net.
- **Style**: `ruff` and `black` at project defaults. Markdown tables formatted to align pipes (the existing v1 file's style).
- **Directive parsing must be UTF-8 safe.** Arabic comments are common; the directive lookup uses regex on decoded text, not bytes.

### Translation choices (governance-critical)

These four terms set precedent. The planner co-signs each before merge. Implementer's recommendations:

| Python | Recommended Arabic | Rationale |
|---|---|---|
| `async` | `متزامن` | "synchronous-with" / "concurrent". MSA term used in academic concurrency literature. Two alternates rejected: `غير_متزامن` ("asynchronous", literal) is too long for a keyword and reads as a negation; `لاتزامني` is dialectal. |
| `await` | `انتظر` | "wait". Direct; matches the verb's ordinary meaning. Reads naturally: `النتيجة = انتظر طلب_شبكي(...)`. Alternate `ترقب` rejected as poetic and rarely used in technical Arabic. |
| `match` | `طابق` | "match against" (Form III verb — literally "to bring into correspondence with"). Reads as a verb at the head of a control-flow block, paralleling `طابق x:`. Alternate `قارن` ("compare") rejected because compare suggests `==`; pattern matching is a different concept. |
| `case` | `حالة` | "case / state". Standard term; learners know it from the loanword `كاسة` if they've seen any English material, and `حالة` is the formal Arabic equivalent. Alternate `نمط` ("pattern") rejected because PEP 634 distinguishes "case" (the syntactic clause) from "pattern" (the matched-against expression); using `نمط` for `case` would block `نمط` from later denoting "pattern" if a teaching tool needs the term. |

The rationale paragraph above must appear verbatim in `ar-v1.1.md`'s header so future contributors have the curation reasoning preserved.

### Curation gates (every entry must pass)

- Round-trips through `arabicpython.normalize.normalize_identifier()` to itself.
- No homograph with any v1 keyword. (None of the four candidates collide.)
- No reuse of an Arabic root that v1 binds to a different concept. (`متزامن` shares the `زمن` "time" root with no v1 keyword; `انتظر` shares the `نظر` root with no v1 keyword; `طابق` and `حالة` are clear.)
- Tokenizes as a single identifier under Python 3.11's tokenizer (the harakat-stripping pipeline already covers this; tested explicitly).

## Test requirements

### `tests/test_dictionary_v1_1.py`

1. `test_v1_1_is_strict_superset_of_v1`:
   - Parse both files via the dictionary loader.
   - For every `(arabic, python)` pair in v1, assert the same pair exists in v1.1.
   - Assert v1.1 has exactly four pairs not in v1: the four new entries.
   - Failure message lists the missing or extra pairs.

2. `test_v1_1_new_entries_are_the_expected_four`:
   - Assert the four-pair set equals `{("متزامن", "async"), ("انتظر", "await"), ("طابق", "match"), ("حالة", "case")}`.
   - This locks the chosen terms once the PR merges; future changes need a new ADR.

3. `test_v1_1_round_trip_normalize`:
   - For every Arabic keyword, assert `normalize_identifier(k) == k`.

4. `test_v1_1_no_v1_homographs`:
   - Already covered by supersetness, but explicit: each new Arabic word is not a v1 keyword.

5. `test_translator_default_unchanged`:
   - Translate a fixed Arabic source string with no `dict_version` argument; assert byte-identical output to a snapshot captured pre-packet.
   - This is the strongest possible Phase A compat assertion for the translator.

6. `test_translator_with_v1_1_handles_async`:
   - Translate `متزامن def f(): انتظر g()` with `dict_version="ar-v1.1"`.
   - Assert the output is `async def f(): await g()` (modulo whitespace).

7. `test_translator_with_v1_1_handles_match`:
   - Translate a four-arm `طابق x: حالة 1: ... حالة 2: ...` block with `dict_version="ar-v1.1"`.
   - Assert the output is the equivalent `match x: case 1: ... case 2: ...`.

8. `test_translator_with_v1_rejects_async`:
   - Translate `متزامن def f(): pass` with default `dict_version="ar-v1"`.
   - Assert that `متزامن` survives untranslated (it's an unknown identifier under v1) — confirming v1 programs aren't silently upgraded.

9. `test_directive_pins_dictionary`:
   - Write a tmp `.apy` file with `# arabicpython: dict=ar-v1.1` on line 2 (after a shebang).
   - Run via `subprocess.run([sys.executable, "-m", "arabicpython.cli", path])`.
   - Assert returncode 0 even though the file uses async syntax.

10. `test_directive_disagreement_is_hard_error`:
    - Write a file with `# arabicpython: dict=ar-v1` and run the CLI with `--dict ar-v1.1`.
    - Assert returncode != 0 and stderr mentions both versions.

11. `test_async_for_and_with_work_under_v1_1`:
    - Translate `متزامن for x in g(): pass` and `متزامن with f() as r: pass`.
    - Assert correct translation to `async for` / `async with`.

12. `test_match_soft_keyword_outside_match_block_is_identifier`:
    - Translate `طابق = 5` (assignment with `طابق` as a variable name).
    - Assert the output preserves it as `match = 5` and that Python parses it (Python's match is a soft keyword).

13. `test_dictionary_v1_unchanged`:
    - Re-run the SHA-256 snapshot from B-002 against `ar-v1.md`.
    - Assert unchanged. (Belt-and-suspenders to the B-002 suite.)

### Demo example tests

14. `test_async_demo_runs`:
    - `subprocess.run` against `examples/B40_async_demo.apy`.
    - Assert returncode 0; stdout contains a known string the demo prints.

15. `test_match_demo_runs`:
    - Same shape against `examples/B40_match_demo.apy`.

### CLI tests

16. `test_cli_dict_flag_listed_in_help`:
    - Run `python -m arabicpython.cli --help`; assert `--dict` appears with `ar-v1.1` mentioned.

## Reference materials

- `decisions/0008-phase-b-charter.md` §B.0 — the immutability constraint this packet operates within.
- `decisions/0003-curation-rules.md` — translation principles.
- `dictionaries/ar-v1.md` — the parent.
- `specs/0001-dictionary-v1.md` — how the original dictionary was built; mirrors apply here.
- `specs/0003-dialect-loader-v1.md` — the loader that already supports versioned dictionaries.
- PEP 492 (async/await), PEP 634 (structural pattern matching).
- Hedy precedent for soft-keyword translation: noted in ADR 0003.

## Open questions for the planner

1. **Should the per-file directive accept `dict=ar-v1.1+` to mean "this version or later"?** Recommended: **no for this packet**. Pinning is more predictable, and the project doesn't yet have enough versions to justify range syntax. Revisit when v1.2 ships.
2. **Should `match`'s soft-keyword nature be reflected in the dictionary's `Category` column?** Recommended: **yes** — column value `soft-keyword` for `match`/`case`, distinguishing from the hard `keyword` of `async`/`await`. The loader doesn't care, but human readers do.

## Acceptance checklist

- [ ] `dictionaries/ar-v1.1.md` created; v1 reproduced verbatim plus the four additions; rationale paragraph included.
- [ ] `dictionaries/ar-v1.md` byte-unchanged (B-002 SHA-256 snapshot still matches).
- [ ] `decisions/0009-dictionary-versioning.md` written and accepted.
- [ ] `arabicpython/translate.py` accepts `dict_version` kwarg with v1 default.
- [ ] `arabicpython/cli.py` accepts `--dict` flag and parses per-file directive.
- [ ] All 16 tests above present and passing on the 9-cell matrix.
- [ ] Both demo files run end-to-end; their READMEs walk through them in Arabic.
- [ ] `pytest tests/test_phase_a_compat.py` passes unchanged.
- [ ] `ruff check .` passes.
- [ ] `black --check .` passes.
- [ ] **Planner has co-signed the four chosen Arabic terms** in the PR review (a separate review comment, not just an approval).
- [ ] Delivery note `B-040-dictionary-v1.1-async-match.delivery.md` written. Required sections: any term the implementer changed from the recommendations (with rationale and planner sign-off reference), the per-file directive parsing edge cases encountered, confirmation that v1 programs are byte-identical post-translate.
