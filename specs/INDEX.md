# Spec packet index

| ID | Title | Phase | Owner | Status |
|---|---|---|---|---|
| 0000 | Template (do not implement) | — | — | reference |
| 0001 | dictionary-v1 | A | Claude | merged |
| 0002 | normalize-v1 | A | Codex | merged |
| 0003 | dialect-loader-v1 | A | Gemini 3.1 Pro | merged |
| 0004 | pretokenize-v1 | A | Gemini 3.1 Pro | merged |
| 0005 | core-translate-v1 | A | Gemini 3.1 Pro | merged |
| 0006 | cli-v1 | A | Gemini 3.1 Pro | merged |
| 0007 | import-hook-v1 | A | Gemini 3.1 Flash | merged |
| 0008 | repl-v1 | A | Gemini 3.1 Flash | merged |
| 0009 | translated-tracebacks-v1 | A | Gemini 3.1 Pro | merged |
| 0010 | examples-v1 | A (wrap) | Gemini 3.1 Pro | merged |
| 0011 | fstring-interior-3-11 | A (post-wrap fix) | Gemini 3.1 Pro | merged |
| 0012 | arabic-docs-translation-v1 | A (doc wrap) | Gemini | merged |
| 0013 | search-engine-v1 | A (showcase) | Gemini Pro | merged |
| 0014 | prayer-times-v1 | A (showcase) | Gemini Pro | merged |
| B-001 | alias-runtime-v1 | B (foundation) | — | drafted |
| B-002 | phase-a-compat-suite | B (foundation) | — | drafted |
| B-010 | aliases-flask-v1 | B (SDK) | — | drafted |
| B-011 | aliases-fastapi-v1 | B (SDK) | — | stub |
| B-012 | aliases-django-core-v1 | B (SDK) | — | stub |
| B-013 | aliases-sqlalchemy-v1 | B (SDK) | — | stub |
| B-014 | aliases-requests-extras-v1 | B (SDK) | — | stub |
| B-015 | aliases-pytest-v1 | B (SDK) | — | stub |
| B-016 | aliases-numpy-core-v1 | B (SDK) | — | stub |
| B-017 | aliases-pandas-core-v1 | B (SDK) | — | stub |
| B-018 | aliases-pillow-v1 | B (SDK) | — | stub |
| B-030 | stdlib-os-pathlib-sys | B (stdlib) | — | drafted |
| B-031 | stdlib-collections-itertools-functools | B (stdlib) | — | stub |
| B-032 | stdlib-datetime-time-calendar | B (stdlib) | — | stub |
| B-033 | stdlib-json-csv-sqlite3 | B (stdlib) | — | stub |
| B-034 | stdlib-re-string-textwrap | B (stdlib) | — | stub |
| B-035 | stdlib-math-statistics-random-decimal-fractions | B (stdlib) | — | stub |
| B-036 | stdlib-logging | B (stdlib) | — | stub |
| B-037 | stdlib-asyncio-core | B (stdlib) | — | stub |
| B-038 | stdlib-leftovers | B (stdlib) | — | stub |
| B-040 | dictionary-v1.1-async-match | B (dictionary) | — | drafted |
| B-041 | traceback-arabic-frames-v1.1 | B (dictionary) | — | stub |
| B-050 | vscode-extension-syntax-v1 | B (tooling) | — | deferred (sponsor) |
| B-051 | formatter-arabic-aware-v1 | B (tooling) | — | deferred (sponsor) |
| B-052 | lsp-server-v1 | B (tooling) | — | deferred (sponsor) |
| B-053 | linter-arabicpython-v1 | B (tooling) | — | deferred (sponsor) |
| B-054 | repl-readline-arabic-v1 | B (tooling) | — | deferred (sponsor) |
| B-060 | tutorial-translation | B (docs) | — | drafted |
| B-061 | cookbook-translation | B (docs) | — | stub |
| B-070 | dialect-egyptian-v0-proposal | B (dialects, proposal) | — | proposed |
| B-071 | dialect-loader-multiplexing-v2 | B (dialects, proposal) | — | proposed |
| B-072 | dialect-precedence-rules-adr | B (dialects, proposal) | — | proposed |

## Legend

- **Status**: `drafted` → `in-progress` → `delivered` → `reviewing` → `merged` | `blocked`
- **Phase B extras**: `stub` (listed in roadmap, spec not yet written — see `B-HANDOFF-FOR-GEMINI.md`); `deferred (sponsor)` (spec written but implementation funding-gated per ADR 0008.B.6); `proposed` (dialect-related design docs that ship as text, not code).
- **Owner**: the implementer assigned to the packet. Phase A used `Codex` for the early packets and switched to `Gemini 3.1 Pro` / `Gemini 3.1 Flash` partway through. `Claude` is the owner for planner-only work (dictionary curation, decision docs, spec authoring). Phase B packets are unclaimed at draft time; contributors claim via the `propose-claim` GitHub issue template.

## Phase B map

For Phase B's 28-packet roadmap with status, dependencies, and contributor onramps, see [`ROADMAP-PHASE-B.md`](../ROADMAP-PHASE-B.md) at the repo root and [`CONTRIBUTING.md`](../CONTRIBUTING.md). Six packets have full specs (B-001, B-002, B-010, B-030, B-040, B-060); the remaining 22 await fan-out per `B-HANDOFF-FOR-GEMINI.md`.
