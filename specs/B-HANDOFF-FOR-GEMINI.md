# Handoff: Phase B Packet Fan-Out for Gemini

**Audience**: Gemini (or any LLM/contributor) tasked with writing the remaining 19 Phase B packet specs.
**Status**: Six template-establishing packets complete. This document is the contract for everything else.
**Owner of this doc**: the project planner (a.o.alkulaib@gmail.com). Update if the templates evolve.

---

## What Claude has already shipped

These six fully-specified packets exist in `specs/` and are the **structural templates** for everything below. Read them before writing anything new:

| Spec | Role | Reuse pattern |
|---|---|---|
| `B-001-alias-runtime-v1.md` | Foundation packet — the runtime every alias mapping consumes. | Cite as a dependency in every B-01x and B-03x packet. |
| `B-002-phase-a-compat-suite.md` | Pinned-output test suite for Phase A's user contract. | Cite as a dependency in every packet that touches `arabicpython/`. |
| `B-010-aliases-flask-v1.md` | **SDK template.** Flask is the Phase B success criterion. | Use this as the structural prior for B-011 through B-018 (other SDK packets). |
| `B-030-stdlib-os-pathlib-sys.md` | **Stdlib template.** | Use this as the structural prior for B-031 through B-038. |
| `B-040-dictionary-v1.1-async-match.md` | Governance-heavy dictionary successor. | If a future packet adds dictionary entries, follow this shape. |
| `B-060-tutorial-translation.md` | **Documentation/translation template.** | Use this as the structural prior for B-061 (cookbook translation) and any future doc-translation packet. |

Also exist as supporting infrastructure:

- `CONTRIBUTING.md` — workflow contract.
- `ROADMAP-PHASE-B.md` — visible map of all 28 packets and their statuses.
- `.github/ISSUE_TEMPLATE/*.md` — claim, bug, term proposal, new packet proposal.
- `.github/PULL_REQUEST_TEMPLATE.md` — PR shape.

---

## What you (Gemini) write

19 spec packets, listed below. **Do not invent new packets**; if you think one is missing, leave a note in this document's "Open questions" section instead of creating a file.

### SDK aliases (B-011 through B-018) — use B-010 as template

| ID | Short name | Notes for the spec |
|---|---|---|
| B-011 | `aliases-fastapi-v1` | FastAPI. Mirror Flask's structure; pay attention to async route handlers (the demo must use `متزامن`/`انتظر` if B-040 is shipped, else stay sync). |
| B-012 | `aliases-django-core-v1` | Django's core: `urls`, `views`, `models`, `forms`. Larger surface than Flask — floor 80 entries instead of 38. Do **not** include the admin or management commands; defer to a future packet. |
| B-013 | `aliases-sqlalchemy-v1` | ORM. `Column`, `Table`, `select`, `insert`, session API. |
| B-014 | `aliases-requests-extras-v1` | The session/auth/adapter surface that B-001's `requests.toml` deliberately omitted. Bridge packet — deliverable is a TOML expansion plus tests. |
| B-015 | `aliases-pytest-v1` | `pytest.fixture`, `pytest.mark.*`, `pytest.raises`, `pytest.parametrize`. Test-writers' surface. |
| B-016 | `aliases-numpy-core-v1` | `numpy.array`, `arange`, `zeros`, `ones`, dtype names, the most-used ufuncs. Floor 50. |
| B-017 | `aliases-pandas-core-v1` | `DataFrame`, `Series`, `read_csv`, `to_csv`, indexing. Floor 40. |
| B-018 | `aliases-pillow-v1` | `Image.open`, `Image.new`, common filters. Smaller surface; floor 25. |

For each SDK packet:
- Floor entry counts approximate Flask's (38) scaled by surface area.
- Demo file name: `examples/B<NN>_<short>.apy`.
- Mirror the test counts (10–13 tests).
- Honestly document the method-on-instance limitation (same paragraph as B-010).
- Phase A compat assertion identical to B-010's.
- Set `Depends on: B-001, B-002` plus B-040 if the demo wants async.

### Stdlib aliases (B-031 through B-038) — use B-030 as template

| ID | Short name | Modules covered |
|---|---|---|
| B-031 | `stdlib-collections-itertools-functools` | The three functional-programming staples. `OrderedDict`, `defaultdict`, `Counter`, `chain`, `groupby`, `partial`, `reduce`, `lru_cache`. |
| B-032 | `stdlib-datetime-time-calendar` | Date/time. Pay attention to timezone-aware vs naive (the README explains the choice). |
| B-033 | `stdlib-json-csv-sqlite3` | Data formats. `json.dumps/loads`, `csv.reader/writer`, sqlite3's connect/cursor/execute. |
| B-034 | `stdlib-re-string-textwrap` | String processing. `re.match/search/sub/findall`, `string.Template`, `textwrap.fill/dedent`. |
| B-035 | `stdlib-math-statistics-random-decimal-fractions` | Numerics. Five small modules in one packet because each is too small alone. |
| B-036 | `stdlib-logging` | Logging gets its own packet because the API has both module-level and class-level surfaces. |
| B-037 | `stdlib-asyncio-core` | `asyncio.run`, `gather`, `sleep`, `Task`, `Queue`, `Lock`. **Depends on B-040** for the demo to be useful. |
| B-038 | `stdlib-leftovers` | The catch-all: `subprocess` (carefully), `tempfile`, `shutil`, `argparse`, `urllib.parse`, `hashlib`, `secrets`, `uuid`. List explicitly which modules are in scope; defer the rest to a future "leftovers-2". |

For each stdlib packet:
- Floor entry counts scaled to surface (small modules: 10–15; large: 40–60).
- Cross-consistency tests (parallel to B-030's `test_stdlib_cross_consistency.py`) — at minimum verify your packet doesn't collide with terms B-030 already shipped.
- Demo file `examples/B<NN>_<short>.apy`.

### Dictionary/traceback (B-041)

| ID | Short name | Notes |
|---|---|---|
| B-041 | `traceback-arabic-frames-v1.1` | Extends Phase A packet 0009's translated tracebacks to cover the new v1.1 keywords. Tiny code change; covered mostly by tests. **Depends on B-040.** |

### Tooling (B-050 through B-054) — sponsor-conditional, mark as `deferred` in spec

These are spec'd as small (1-session) packets, but per ADR 0008.B.6 their *implementation* is gated on funding. Write the specs anyway; mark them `Status: deferred (sponsor-conditional)` in their headers and link to the funding gate in ROADMAP-PHASE-B.md.

| ID | Short name | Notes |
|---|---|---|
| B-050 | `vscode-extension-syntax-v1` | Syntax highlighting for `.apy` files. TextMate grammar. No LSP — that's B-052. |
| B-051 | `formatter-arabic-aware-v1` | Wrapper around `black` that preserves Arabic identifier alignment in column-based code. |
| B-052 | `lsp-server-v1` | Language server: completion, go-to-definition, hover. Largest of the tooling packets. |
| B-053 | `linter-arabicpython-v1` | Wrapper around `ruff` with Arabic-Python-specific rules (e.g. "don't mix v1 and v1.1 keywords in one file"). |
| B-054 | `repl-readline-arabic-v1` | Improved REPL with Arabic input editing, completion, history. Phase A's REPL is functional but minimal. |

### Documentation (B-061)

| ID | Short name | Notes |
|---|---|---|
| B-061 | `cookbook-translation` | Translates a yet-to-be-written English cookbook (`docs/cookbook.md`) into Arabic. **Depends on the English cookbook existing**; if it doesn't, mark as `blocked` and file an issue against `cookbook-en` as a missing prerequisite. |

### Dialects (B-070 through B-072) — exploratory, mark as `proposed`

Per ADR 0008, dialects beyond MSA are explicitly Phase C territory. These specs document *what would be needed* if the project ever takes them on; they ship as written documents (no code) so the architectural shape is captured before anyone forgets it.

| ID | Short name | Notes |
|---|---|---|
| B-070 | `dialect-egyptian-v0-proposal` | Spec for an Egyptian Arabic dictionary variant. Output: a markdown design doc, not code. |
| B-071 | `dialect-loader-multiplexing-v2` | What the loader needs to support multiple simultaneous dialects per file. Design doc only. |
| B-072 | `dialect-precedence-rules-adr` | What the precedence rules look like when a token resolves under multiple dialects. ADR-shaped output. |

---

## How to write each spec

Use `specs/0000-template.md` as the canonical structure. Then look at the matching template packet (B-010 for SDK, B-030 for stdlib, B-060 for docs) and **mirror its sections, headings, and level of detail**.

Required sections in every spec:

1. **Header** — phase, depends-on, size estimate, owner.
2. **Goal** — one paragraph; what shipping this packet means for users.
3. **Non-goals** — bullet list; what this packet explicitly doesn't do.
4. **Files** — three subsections: create / modify / read.
5. **Public interfaces** — function signatures, TOML schemas, CLI flags. Include type annotations.
6. **Implementation constraints** — Python version, dependencies, style, performance, curation rules.
7. **Translation choices** (for alias/dictionary packets only) — the floor list of must-include entries with rationale.
8. **Test requirements** — numbered tests with concrete inputs and expected outputs.
9. **Reference materials** — external docs, ADRs, prior packets.
10. **Open questions for the planner** — things you weren't sure about. Empty is best, but honest questions are better than guesses.
11. **Acceptance checklist** — copy-able into the PR.

### Rules of authorship

- **Be specific.** "Test that the alias works" is not a test requirement. "Assert `proxy.احصل_متغير_بيئة is os.getenv`" is.
- **Cite the templates.** When mirroring B-010's structure, say so in the spec's header so reviewers know the lineage.
- **Don't speculate about scope.** If a stdlib module exposes 200 names and you can't tell which 50 belong in the floor, leave a question for the planner instead of guessing high or low.
- **Translation calls in TOML files**: you may suggest Arabic terms, but flag every one you're not 100% confident in with a `# REVIEW:` comment in the spec. The implementer + planner co-sign the actual term during PR review.
- **Phase A compat is non-negotiable.** Every spec includes the assertion that `pytest tests/test_phase_a_compat.py` passes unchanged. No exceptions.
- **No new ADRs without flagging.** If your packet seems to need a new architectural decision, stop, file an issue against the planner with the question, and wait. Don't bake an unstated decision into a spec.

### Tone and length

Match the existing six templates: precise, terse-but-explanatory prose; no marketing language; no emoji; no encouraging-sounding throat-clearing ("This exciting packet will…"). Length per spec roughly 200–400 lines. SDK and stdlib packets cluster around 250; dictionary and tooling packets around 300; the dialect proposals can be shorter (150) because they ship as design docs, not code specs.

---

## What you do NOT do

- **Do not write delivery notes.** Those are written after the implementation ships, by the implementer.
- **Do not write the production code.** This handoff is for *spec authoring* only. Each spec gets implemented later by a (human or LLM) contributor who claims the packet via the issue template.
- **Do not modify the six templates.** If you find a problem in B-010, file an issue against the planner; don't edit it directly while writing B-011.
- **Do not modify ADR 0008 or any other decision document.** If the work seems to require an ADR change, stop and ask.
- **Do not modify `dictionaries/ar-v1.md`.** Ever.
- **Do not modify `examples/0*.apy` or anything under `apps/`.** Phase A artifacts are frozen.
- **Do not invent new packet IDs.** The IDs listed above are the complete set. If a 29th packet seems necessary, propose it in this doc's "Open questions" section.

---

## Acceptance for this fan-out task

- [ ] All 19 spec files exist in `specs/` with the names listed above.
- [ ] Each spec follows the template-packet structure for its category (SDK / stdlib / dictionary / docs / tooling / dialect).
- [ ] Each spec lists `Depends on:` with at least B-001 and B-002 (plus B-040 where async is involved).
- [ ] Each spec's "Acceptance checklist" includes the Phase A compat assertion.
- [ ] `ROADMAP-PHASE-B.md` is updated so every row links to its spec file.
- [ ] `specs/INDEX.md` is updated with a row per packet, status `drafted`.
- [ ] Open questions you couldn't resolve are listed in the section below — not silently decided.

---

## Open questions (Gemini fills this in as you go)

<!-- Add a bullet for each question. Format: -->
<!-- - **B-XXX**: Question. Recommended answer: ... Why I'm not sure: ... -->

(Empty at handoff time.)

---

*Once all 19 specs are written, ping the planner for review. Do not open PRs for individual specs — open one omnibus PR titled "Phase B: fan out remaining 19 packet specs" so the templates and the fan-out review together as a single coherent batch.*
