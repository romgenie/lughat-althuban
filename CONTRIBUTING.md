# Contributing to لغة الثعبان

Thank you for considering a contribution. This document is the single entry point for all contributors — code, translation, dictionary, and bug-report.

If you read nothing else, read this:

> Every implementation unit in this project is a **spec packet** in `specs/`. To contribute code, you pick a packet, implement it exactly as written, and open a PR. To contribute non-code, see [§3 — The four kinds of contribution](#3--the-four-kinds-of-contribution).

---

## Table of contents

1. [Who can help](#1--who-can-help)
2. [Project status and what we're building](#2--project-status-and-what-were-building)
3. [The four kinds of contribution](#3--the-four-kinds-of-contribution)
4. [The packet workflow](#4--the-packet-workflow)
5. [Branch, commit, and PR conventions](#5--branch-commit-and-pr-conventions)
6. [Local setup and quality gates](#6--local-setup-and-quality-gates)
7. [The Phase A compatibility promise](#7--the-phase-a-compatibility-promise)
8. [Review SLA and what to expect](#8--review-sla-and-what-to-expect)
9. [Code of conduct](#9--code-of-conduct)

---

## 1 — Who can help

You do **not** need to be a Python expert. This project depends on three skills, and most of them are not "writing Python":

- **Arabic linguistic judgment** — choosing the right MSA term for a Python concept, or reviewing a proposed term. The single most-needed skill.
- **Python knowledge of one specific library** — if you use Flask in your day job, you can curate the Flask alias packet (B-010) better than a planner who reads Flask's docs once.
- **Translation skill** — Python's official tutorial is largely untranslated into Arabic. This is the biggest visible gap and requires no Python coding.

If you are an Arabic-speaking developer, an Arabic linguist, an educator, or a learner who hit a confusing error message — there is a packet for you. Read [§3](#3--the-four-kinds-of-contribution).

---

## 2 — Project status and what we're building

**Phase A is complete** (April 2026). The dialect, CLI, REPL, import hook, and Arabic tracebacks all work. A learner can write, run, debug, and import `.apy` programs end-to-end.

**Phase B is in progress.** Phase B is the gap between "Python with Arabic keywords" (Phase A) and "an Arabic-speaking developer can build production software entirely in Arabic" (Phase B). The full plan is in [`ROADMAP-PHASE-B.md`](ROADMAP-PHASE-B.md). The architectural commitment is in [`decisions/0008-phase-b-charter.md`](decisions/0008-phase-b-charter.md).

Phase B has 28 packets. Six are fully specified and ready to implement (B-001, B-002, B-010, B-030, B-040, B-060). The rest are stubs awaiting full specification or sponsor commitment. **B-001 is the gate to everything else** — every SDK and stdlib alias packet depends on it.

---

## 3 — The four kinds of contribution

### 3a — Code: implement a Phase B packet

This is the main contribution path.

1. Open [`ROADMAP-PHASE-B.md`](ROADMAP-PHASE-B.md). Find a packet whose status is `drafted` and whose `Depends on` packets are all `merged`.
2. Open a "Claim a packet" issue (the template is in `.github/ISSUE_TEMPLATE/`). Say which packet ID and roughly when you can ship.
3. Wait for the planner to assign the issue to you. **One packet per contributor at a time.** This is enforced — do not start a second packet until your first is merged.
4. Implement the packet exactly as written in `specs/<packet-id>.md`. Tests are the contract; if the tests pass, the packet is done.
5. Write a delivery note at `specs/<packet-id>.delivery.md` explaining what shipped, any deviations, and any open questions.
6. Open a PR. The PR template walks you through the rest.

If a packet is under-specified or you find a real bug in the spec, **stop and ask in the delivery note's "Open questions"** — do not invent a fix. The planner amends the packet or writes a fix-up; chat decisions are not durable.

### 3b — Dictionary curation: propose or review Arabic terms

The Phase A dictionary (`dictionaries/ar-v1.md`) is **frozen** per ADR 0008.B.0. New library or stdlib terms go into per-library TOML files (`arabicpython/aliases/*.toml`).

Two ways to contribute:

- **Propose a translation** for an entry in an open SDK or stdlib alias packet (e.g., what should `pandas.DataFrame.groupby` be in Arabic?). Open a "Propose Arabic term" issue. The template asks for: the Python symbol, your proposed Arabic term, two alternates considered, and a one-sentence rationale.
- **Review a packet's translation table** before it's implemented. Open the spec packet file, read the translation table in its "Public interfaces" section, and comment on specific entries via a GitHub review on the packet's PR (or as a comment on the claim issue if no PR exists yet).

Curation rules (carried over from ADR 0003):

1. Hedy's Arabic translation if one exists and is unambiguous.
2. Modern Standard Arabic over regional dialects.
3. Shortest defensible translation when MSA options are equal.
4. Avoid homographs with common identifiers; use underscore-composed forms for clarity.
5. Translations must round-trip through `arabicpython.normalize.normalize_identifier()` — any term that changes under normalization is rejected (it would be unfindable at runtime).

### 3c — Documentation translation

Three priority targets:

- **The Python tutorial** (Packet B-060). Chapters 1–10 of docs.python.org/3/tutorial, translated into Arabic and adapted to use `.apy` examples. Entirely non-code.
- **Error messages** (Packet B-061). Roughly 120 Python interpreter error messages don't yet have Arabic translations. The format is a TOML table; each entry is one line.
- **Existing Phase A docs** in `docs/ar/` may need clarifications, fixes, or additions as Phase B ships.

Translation contributions follow the same packet workflow as code: claim a packet, work on a branch, open a PR. The "Local setup" step (§6) is lighter — you only need to run `pytest tests/test_examples.py` to check that translated examples still execute.

### 3d — Bug reports and real-world `.apy` programs

The lowest-friction contribution. If you write a `.apy` program and it does something surprising:

1. Open a "Bug report" issue. The template asks for: minimal reproducible `.apy` source, expected behavior, actual behavior, your Python and OS version.
2. Even better — if you have a non-trivial `.apy` program (more than 50 lines) that runs correctly, paste a link or file. We genuinely lack diverse real-world test cases. Programs that exercise async, classes, decorators, or imports are especially valuable.

You are not expected to debug or fix it. Reporting alone is the contribution.

---

## 4 — The packet workflow

The same workflow that shipped Phase A's 14 packets:

```
                   spec packet (drafted)
                            │
                            │  contributor claims it
                            ▼
                   spec packet (in-progress)
                            │
                            │  contributor implements + PR
                            ▼
                   spec packet (delivered)
                            │
                            │  planner reviews
                            ▼
                   spec packet (reviewing)
                            │
                            ├── approve → merged
                            │
                            └── needs changes → fix-up packet
                                  NNNN-short-name.fixup-1.md
```

Status values live in [`specs/INDEX.md`](specs/INDEX.md). The planner updates them.

### Why packets, not "just file a PR for what you think is needed"

Two reasons:

1. **Tests are the contract.** A packet says, in advance, what tests must pass. If your PR makes them pass, the packet is done — even if the planner later realizes something was missing. That's the planner's fault for under-specifying, not yours. This protects implementers from scope creep and from rework.
2. **Phase A compatibility is permanent** (ADR 0008.B.3). Without a written spec, it's easy to make a "small improvement" that breaks an example written six months ago. Spec packets force that conversation up front.

### What if I want to do something that isn't a packet?

Open an issue using the "Propose new packet" template. The planner either drafts the packet (and assigns it back to you to implement) or explains why it's out of scope. Don't open a PR for un-spec'd work — it will be closed.

---

## 5 — Branch, commit, and PR conventions

### Branches

Format: `packet/<packet-id>-<short-name>`

Examples:
- `packet/B-010-aliases-flask-v1`
- `packet/B-040-dictionary-v1.1-async-match`

For fix-ups: `packet/<packet-id>-fixup-<N>` (e.g., `packet/B-010-fixup-1`).

### Commits

The first line of every commit must start with the packet ID:

```
B-010: add Flask request/response alias mapping
B-010: add round-trip tests for proxy attribute access
B-010: address review feedback on `Response.json` semantics
```

Body explains *why*, not *what* (the diff already shows what). Wrap at 72 columns. Sign-off optional.

### PRs

PR title: `B-010: aliases-flask-v1` (the packet's own title).

PR body uses the template in `.github/PULL_REQUEST_TEMPLATE.md`. Required sections:

- Packet ID and link to spec
- Summary of approach (one paragraph)
- Acceptance checklist (copy from the spec, mark each item)
- Delivery note checklist (deviations, open questions)
- CI confirmation (must pass on Linux/macOS/Windows × Python 3.11/3.12/3.13)

PRs that don't follow the template are not rejected — but the planner will ask you to add the missing sections before review, which adds round-trips. Use the template.

### What "merge" means

The planner squash-merges your PR into `main` after review approval. Your commit history becomes one commit on main; the PR's commit history is preserved on the branch. The delivery note in `specs/<packet-id>.delivery.md` is the durable record of the work.

---

## 6 — Local setup and quality gates

### Setup

```bash
git clone https://github.com/GalaxyRuler/lughat-althuban
cd lughat-althuban
python -m venv .venv
source .venv/bin/activate    # or: .venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

Requires Python 3.11+. The dev extras install `pytest`, `pytest-cov`, `ruff`, and `black`.

### Running the test suite

```bash
pytest                           # all tests
pytest tests/test_translate.py   # one file
pytest -k flask                  # one keyword
pytest -x                        # stop at first failure
```

Phase A has 351 passing tests + 21 intentional skips. Phase B packets must add their tests without breaking any existing ones.

### Lint and format

Both must be clean before you open a PR. CI fails on either.

```bash
ruff check .
ruff format .       # or: black .
```

### CI matrix

GitHub Actions runs every PR on:

- Ubuntu, macOS, Windows
- Python 3.11, 3.12, 3.13

That's 9 cells. **Your PR is not mergeable until all 9 cells are green.** If a cell fails, look at the actions log first — most failures are platform-specific encoding issues (Windows defaults to CP1252) or Python 3.11 tokenizer rejecting Arabic harakat in identifiers (a real Phase A issue documented in the search-engine and prayer-times delivery notes).

If a CI failure looks like a project-wide infrastructure issue rather than your packet's bug, comment on the PR — the planner will investigate.

### Common gotchas

1. **Arabic harakat in identifiers crash Python 3.11's tokenizer.** Stick to identifiers without shadda (ّ U+0651), damma (ُ U+064F), or other harakat. The tatweel (ـ U+0640) is safe.
2. **Windows default encoding is CP1252, not UTF-8.** Always pass `encoding="utf-8"` to `open()` in test fixtures. Set `PYTHONIOENCODING=utf-8` in your shell profile.
3. **TOML bare keys must be ASCII.** Arabic keys in `pyproject.toml` or alias TOML files must be quoted: `"طلبات" = "requests"`.
4. **Don't normalize Python identifiers with `camel_tools`.** Python's NFKC does NOT fold hamza variants (per PEP 3131). Use `arabicpython.normalize.normalize_identifier()` for project-internal normalization; never use general-purpose Arabic NLP normalizers.

---

## 7 — The Phase A compatibility promise

ADR 0008.B.3 commits to: **any program that runs on Phase A's last release runs unchanged on every Phase B release.**

Concretely, this means:

- The seven examples in `examples/` (01_hello.apy through 07_imports.apy) and the apps in `apps/` are pinned in CI via `tests/test_phase_a_compat.py` (created in B-002).
- The keyword dictionary `dictionaries/ar-v1.md` is **immutable**. New keywords go into `ar-v1.1.md` (additive only) or `ar-v2.md` (with a superseding ADR). Files declaring `# apython: dict=ar-v1` keep their original lookup table.
- Internal APIs (`arabicpython.translate`, `arabicpython.dialect`, `arabicpython.normalize`) may change with normal deprecation cycles, but the public API listed in README.md does not.

A PR that breaks the Phase A compat suite is rejected on principle, not negotiated. If your packet genuinely cannot proceed without a breaking change, the path is: open an issue proposing a superseding ADR and get it accepted *first*, then write the packet against the new ADR.

---

## 8 — Review SLA and what to expect

The honest version:

- **One reviewer** (the project planner). No team, no rotation.
- **Target review turnaround: 7 days.** Realistic worst case: 14 days during travel or research crunches. If you've waited more than 14 days with no response, ping the PR — that's not impatience, that's expected behavior.
- **Reviews are strict because tests are the contract.** Expect line-by-line feedback on test coverage, edge cases, and whether the implementation matches the spec exactly. This is not personal; it's the same standard Phase A held.
- **Fix-up packets, not force-push.** If review finds something the spec missed, the planner writes `<packet-id>.fixup-1.md` and assigns it. You implement the fix-up as a separate small packet. This keeps the original packet's history intact and the spec/delivery doc honest.
- **Rejection is rare but real.** A PR that doesn't match the spec, breaks Phase A compat, or fails CI is closed. The contributor is welcome to reopen with corrections.

Asynchronous norms apply. Reviews happen by writing in PR comments, not in chat. Decisions made in chat are not durable.

---

## 9 — Code of conduct

This project follows the [Contributor Covenant 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). Read it. The short version: be kind, assume good intent, disagree about technical things in technical terms.

Project-specific clarifications:

- **Religious or political content in `.apy` examples and translations is acceptable** when it is a natural fit (the prayer-times app, Hijri calendar examples, Quranic Arabic test corpora). It is not acceptable when it is gratuitous or exclusionary.
- **Dialect contributions** (planned: Egyptian, Levantine, Maghrebi keyword variants) are welcome and not in tension with the MSA dictionary; they live in separate dialect files. Disputes about "which dialect is correct" do not exist here — all of them are correct in their context.
- **Reports of misconduct** go to a.o.alkulaib@gmail.com. They are handled privately.

---

*This document is itself a Phase B artifact. If something is unclear or wrong, open a PR against `CONTRIBUTING.md` directly — no packet needed.*
