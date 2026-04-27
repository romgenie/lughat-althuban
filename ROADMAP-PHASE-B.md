# Phase B Roadmap

**Status as of 2026-04-27:** Phase A complete. Phase B well underway — all stdlib batches (B-030–B-039) merged, all top-10 SDK packets merged (Flask, requests, requests-extras, Django, SQLAlchemy, numpy, pandas, Pillow, pytest, FastAPI), and traceback expansion (B-041) merged. Active work: tooling layer (B-050–B-054), tutorial translation (B-060), and error-message coverage (B-061).

This file is the **single visible map** of what Phase B contains, what's open for contribution, and what depends on what. To pick up work, see [CONTRIBUTING.md](CONTRIBUTING.md). To understand *why* Phase B is structured this way, see [decisions/0008-phase-b-charter.md](decisions/0008-phase-b-charter.md).

---

## Goal of Phase B

> An Arabic-speaking developer can write a working Flask hello-world entirely in Arabic.

That is the success criterion (ADR 0008.B.4). Every Phase B packet either advances toward it or makes it durable.

---

## How to read this roadmap

Each packet has:

- **ID** — the canonical packet identifier. Used in branch names, commit messages, PR titles.
- **Title** — short name.
- **Depends on** — packets that must be `merged` before this one can start.
- **Size** — S (1 session), M (2–3 sessions), L (break this up if not already broken).
- **Status** — see legend at bottom.
- **Owner** — who's implementing. `—` means open for claim.
- **First-pickup?** — packets explicitly tagged as good entry points for new contributors.

To claim a packet: open a "Claim a packet" issue (template in `.github/ISSUE_TEMPLATE/`). The planner assigns it to you and updates this file.

---

## Foundation (must ship first; gates everything else)

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| [B-001](specs/B-001-alias-runtime-v1.md) | alias-runtime-v1 — proxy meta-path finder + `requests` mapping | — | L | merged | — | no (architectural) |
| [B-002](specs/B-002-phase-a-compat-suite.md) | phase-a-compat-suite — pin Phase A examples in CI permanently | — | S | merged | — | **yes** |

---

## SDK aliases — top 10 libraries

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| [B-010](specs/B-010-aliases-flask-v1.md) | aliases-flask-v1 — ~60 entries; the success-criterion packet | B-001 | M | merged | — | **yes** |
| B-011 | aliases-fastapi-v1 | B-001 | M | merged | — | yes |
| B-012 | aliases-django-core-v1 — urls, views, models, forms | B-001 | L | merged | — | no (large surface) |
| B-013 | aliases-sqlalchemy-v1 | B-001 | M | merged | — | no (semantic depth) |
| B-014 | aliases-requests-extras-v1 — session/auth surface omitted from B-001 | B-001 | S | merged | — | **yes** |
| B-015 | aliases-pytest-v1 | B-001 | M | merged | — | yes |
| B-016 | aliases-numpy-core-v1 | B-001 | L | merged | — | no (large surface) |
| B-017 | aliases-pandas-core-v1 | B-001, B-016 | L | merged | — | no (large surface) |
| B-018 | aliases-pillow-v1 | B-001 | S | merged | — | **yes** |

---

## Stdlib alias batches

| ID | Title | Modules covered | Depends on | Size | Status | Owner |
|---|---|---|---|---|---|---|
| [B-030](specs/B-030-stdlib-os-pathlib-sys.md) | stdlib-os-pathlib-sys | `os`, `pathlib`, `sys` | B-001 | M | merged | — |
| B-031 | stdlib-collections-itertools-functools | `collections`, `itertools`, `functools` | B-001 | M | merged | — |
| B-032 | stdlib-datetime-time-calendar | `datetime`, `time`, `calendar` | B-001 | M | merged | — |
| B-033 | stdlib-json-csv-sqlite3 | `json`, `csv`, `sqlite3` | B-001 | M | merged | — |
| B-034 | stdlib-re-string-textwrap | `re`, `string`, `textwrap` | B-001 | M | merged | — |
| B-035 | stdlib-math-statistics-random | `math`, `statistics`, `random` | B-001 | M | merged | — |
| B-036 | stdlib-logging | `logging` | B-001 | S | merged | — |
| B-037 | stdlib-asyncio-core | `asyncio` core surface | B-001 | M | merged | — |
| B-038 | stdlib-hashlib-io-contextlib | `hashlib`, `io`, `contextlib` | B-001 | M | merged | — |
| B-039 | stdlib-subprocess-shutil-argparse-secrets-uuid | `subprocess`, `shutil`, `argparse`, `secrets`, `uuid` | B-001 | M | merged | — |

---

## Dictionary and traceback expansion

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| [B-040](specs/B-040-dictionary-v1.1-async-match.md) | dictionary-v1.1 — `async`, `await`, `match`, `case` keyword translations | — | S | merged | — | **yes** |
| B-041 | traceback-coverage-v2 — full Python exception hierarchy (69 names) + 55 message templates | — | M | merged | — | yes |

---

## Tooling layer

These ship in order of dependency. All are active targets — no sponsor gate.

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| B-050 | tooling-pip-wrapper — Arabic CLI for `pip install` / `pip list` / `pip uninstall` | B-001 | M | drafted | — | **yes** |
| B-051 | tooling-pytest-wrapper — Arabic test runner (`ثعبان اختبر`) | B-015 | S | drafted | — | **yes** |
| B-052 | lsp-server-v1 — Language server (hover, go-to-def, diagnostics for `.apy`) | — | L | drafted | — | no (infrastructure) |
| B-053 | vscode-extension-v1 — Syntax highlight, completion, error squiggles | B-052 | M | drafted | — | no |
| B-054 | jupyter-kernel-v1 — `.apy` cells in Jupyter notebooks | — | L | drafted | — | no |

**Pickup advice:** B-050 and B-051 are the smallest and most self-contained. B-052 is the prerequisite for editor support; claim it only with LSP experience.

---

## Documentation translation

Open to non-code contributors. See [CONTRIBUTING.md §3c](CONTRIBUTING.md#3c--documentation-translation).

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| [B-060](specs/B-060-tutorial-translation.md) | tutorial-translation — Python tutorial chapters 1–10 in Arabic, with `.apy` examples | — | L (split into 10 sub-packets) | drafted | — | **yes** (any chapter) |
| B-061 | error-message-coverage — audit B-041 template coverage against real CPython messages; fill remaining gaps; produce coverage report | B-041 | S | drafted | — | **yes** |

---

## Status legend

| Status | Meaning |
|---|---|
| `drafted` | Spec is fully written (or scoped). Open for claim. |
| `in-progress` | Claimed by an owner; implementation underway. |
| `delivered` | PR open with delivery note. Awaiting review. |
| `reviewing` | Planner is reviewing. |
| `merged` | Shipped on `main`. |
| `blocked` | Waiting on another packet, an ADR, or an external decision. |

---

## Where to start (decision tree)

- **I want a small, high-impact tooling packet** → claim B-050 (pip wrapper) or B-051 (pytest wrapper).
- **I want a small, high-impact non-code packet** → claim B-061 (error coverage audit) or a single chapter of B-060.
- **I want editor support** → claim B-052 (LSP) if you have language-server experience, then B-053.
- **I want Jupyter integration** → claim B-054.
- **I'm an Arabic linguist** → review translation tables in existing alias TOMLs, or contribute to B-060 tutorial chapters.
- **None of the above fits** → open a "Propose new packet" issue.

---

*This file is updated whenever a packet's status changes. The source of truth is `specs/INDEX.md`; this file is the curated, contributor-friendly view.*
