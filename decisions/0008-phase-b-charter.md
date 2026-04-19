# 0008 — Phase B charter

**Status**: accepted
**Date**: 2026-04-19
**Deciders**: project planner

## Context

ADR 0007 settled the *scope* split between Phase A (learning dialect) and Phase B (production replacement) and listed Phase B's eight workstreams in priority order. It also gated Phase B execution on "at least one committed buyer or sponsor." With Phase A now shipped (11 packets merged, end-to-end learner stack functional, all matrix-cell CI green), the question shifts from "what does Phase B contain" to "how does Phase B begin, what does it commit to without a sponsor, and what does it explicitly defer until one materializes."

Three forces shape this ADR:

1. **The Layer 3 problem is the whole game.** Per Nasser, layers 1 and 2 are tractable for a small team; layer 3 (third-party libraries, error messages, ecosystem) is where every prior Arabic-programming project has either stalled or scoped down to teaching. Phase B either solves layer 3 or it isn't Phase B. The architecture for layer 3 must be picked now even if execution is sponsor-conditional, because the wrong architecture would invalidate any later sponsor work.

2. **Unconditional vs sponsor-conditional work.** ADR 0007 says "absent a buyer, Phase B becomes dormant research." Strictly read, that means we do nothing. Practically, doing exactly one well-scoped proof-of-concept — small enough for a solo planner to ship, large enough to validate the architecture — is cheap insurance: it makes the sponsor pitch concrete instead of theoretical, and it catches architecture bugs before they're encoded across 30,000 stdlib symbols.

3. **Phase A users need a stability promise.** A learner who shipped a Phase A `.apy` file should be able to run it unchanged after Phase B ships. This is non-negotiable; without it the project loses the trust that Phase A spent eleven packets earning.

## Decision

### B.0 Phase A is frozen at the dictionary level

`dictionaries/ar-v1.md` is **immutable** as of the ADR 0007 ship date. Any term changes require a new versioned dictionary (`ar-v2.md`) and a superseding ADR; the `# apython: dict=ar-v1` magic comment guarantees existing files keep their original lookup table. Additions for Python features added to v1 post-ship (e.g., Python 3.14 keywords) follow ADR 0003's "additions don't require an ADR" rule but land in `ar-v1.md` only if they don't change any existing entry's behavior.

### B.1 Layer 3 architecture: module-proxy meta-path finder

The Phase B Layer 3 mechanism is a **module-proxy meta-path finder** layered above the existing Phase A import hook. When a `.apy` file writes `استورد طلبات`:

1. The Phase A import hook resolves and translates `استورد` → `import` and `طلبات` (the symbolic name) through the standard Python import machinery.
2. A new `arabicpython.aliases` finder, registered after the `.apy` finder on `sys.meta_path`, consults a **per-library mapping file** (e.g., `arabicpython/aliases/requests.toml`) that declares `طلبات → requests`. On match, it imports the underlying English module and returns a **proxy object** that wraps it.
3. Attribute access on the proxy (`طلبات.احصل("https://…")`) is rewritten through the same per-library mapping (`احصل → get`) and forwarded to the underlying module. Unmapped attributes pass through unchanged with a `DeprecationWarning` recommending the curated Arabic name; this is the **auto-transliteration fallback** mentioned in ADR 0007.
4. Proxies are reflexive: `dir(طلبات)` shows the Arabic surface; `repr` shows `<arabic-proxy of requests>`; `isinstance(x, طلبات.Response)` works because the proxy forwards `__class__` checks to the underlying class.

Mapping files are **per-library TOML**, not entries in the keyword dictionary. The keyword dictionary stays small and learner-focused; library aliases scale into the thousands and live next to the libraries they wrap.

Rejected variants of this architecture are documented under "Alternatives considered."

### B.2 First Phase B packet: B-001 alias-runtime-v1

The single Phase B packet committed to without a sponsor is **B-001: the proxy runtime + one library** (`requests`). Concretely:

- `arabicpython/aliases/__init__.py`: the proxy class, the meta-path finder, the TOML loader.
- `arabicpython/aliases/requests.toml`: ~30 entries covering `requests`'s public surface (`get`, `post`, `Session`, `Response`, the common exceptions, `status_code`, `text`, `json`, `headers`).
- `tests/test_aliases.py`: round-trip tests (`استورد طلبات` → call → assert behavior identical to native `requests`), plus tests for the `DeprecationWarning` fallback and the `isinstance` reflexivity property.
- `examples/B01_http.apy`: a six-line program that fetches a URL and prints the status code, written entirely in Arabic.
- Spec packet `specs/B-001-alias-runtime-v1.md` written before implementation, in the same shape as Phase A spec packets.

B-001 is the **only** unconditional Phase B work. Subsequent packets (B-002+) are sponsor-conditional.

### B.3 Phase A `.apy` compatibility is permanent

Any program that runs on Phase A's last release runs unchanged on every Phase B release. This is enforced by:

- A `tests/test_phase_a_compat.py` suite that pins the seven examples from Packet 0010 and runs them under every new Phase B version.
- A CI gate that fails the build if any Phase A test fails after Phase B changes.
- A versioned-dictionary mechanism (B.0) so that even if `ar-v2` reorders or renames terms, files declaring `ar-v1` keep working.

This promise covers the source-level `.apy` syntax and the keyword dictionary. It does **not** cover internal APIs (`arabicpython.translate`, `arabicpython.dialect`); those may evolve with normal deprecation cycles.

### B.4 Phase B success criterion

Phase B v1 is shippable when **a learner who completed Phase A's tutorial can write a working Flask hello-world entirely in Arabic** — `استورد فلاسك`, decorator names, route handlers, `يعمل()` to start the server, and an Arabic exception type when a route raises. This is the smallest end-to-end demonstration that the Layer 3 model works for a non-trivial framework. It requires B-001 (proxy runtime) plus one curated SDK (Flask, ~60 surface entries) plus enough stdlib coverage that `flask.run()` doesn't break on `os` or `sys` calls inside Flask itself (handled transparently by the proxy fallback).

This criterion is measurable, learner-relevant, and intentionally smaller than 0007's eight-workstream list. The eight workstreams are the full Phase B vision; the success criterion is what makes the *first* Phase B release worth shipping.

### B.5 Explicit deferrals

Charter does not decide:

- **Stdlib coverage strategy** (hand-curated batches vs codegen from `inspect.getmembers`). Defer to ADR 0009 once B-001 ships and we have data on per-library curation cost.
- **CPython fork for localized error messages** (0007 Layer 4). Sponsor-required; charter notes only that the Phase A traceback layer (Packet 0009) is forward-compatible — a CPython fork would replace the wrapper, not require a redesign.
- **Tooling parity** (`apip`, `apytest`, LSP, IDE). Each is its own ADR when scoped.
- **Distribution bundle** (0007 Layer 7). Sponsor-required.
- **Translation reversibility** (Python → Arabic for reading existing English code). Out of scope; the project translates *into* Python, not out of it.
- **Multiple-dialect support** (a `dialects/eg.py` for Egyptian colloquial, etc.). Possible post-v2; charter neither commits to nor forecloses.

### B.6 Funding gate (restated, with refinement)

ADR 0007's gate stands: B-002 onward requires a committed sponsor. "Sponsor" means one of: (a) a paid contract from a government, university, foundation, or company; (b) a grant covering at least 12 months of dedicated work; (c) a community of ≥3 contributors making weekly merged contributions for a sustained quarter. Any of the three unlocks B-002+. None of them is required for B-001.

If 24 months pass after Phase A ship with no sponsor and B-001 attracted no significant external usage, the project's recommended next action is to make the repo public, archive it, and publish the architecture writeup as a reference for the next attempt — not to keep accumulating dormant Phase B research.

## Consequences

**Positive:**
- Layer 3 architecture is committed to before any sponsor work, so a sponsor inherits a designed system, not a blank page.
- B-001 is concrete enough to spec, small enough to ship solo, and self-contained enough that its success or failure is unambiguous.
- Phase A users get a permanent compatibility promise, which is the trust foundation for every future Phase B release.
- The funding-gate refinement gives three explicit unlock conditions instead of the single fuzzy "buyer or sponsor" of 0007, making it easier to recognize when the gate is met.

**Negative:**
- Committing to the proxy-meta-path architecture before B-001 ships risks discovering during implementation that proxies have a fatal flaw (e.g., some library introspects `__module__` in a way that breaks). Mitigation: B-001 is explicitly a validation packet; if proxies fail there, Phase B re-charters from a different architecture before any sponsor work is done.
- The 24-month sunset clause may feel premature. It exists to prevent the project becoming a permanently-paused TODO list. The clause is a default, not a commitment; an active community at month 23 obviously continues.

**Neutral:**
- Per-library TOML mapping files mean Phase B's curation workload scales linearly with library count. ~30 entries per library × 10 priority libraries × maybe two reviewer-passes each = roughly two weeks of curation per library at sustained pace. This is the rate at which Phase B can ship without burning out the curator, sponsor or not.
- The aliases finder runs after the `.apy` finder, so it has zero effect on programs that don't use `استورد` for an aliased library — Phase A's import behavior is bit-identical.

## Alternatives considered

**Single global name registry instead of per-library TOML.** Rejected. A flat `arabic_name → english_name` registry across all libraries collides immediately (`get` exists in `requests`, `dict`, `httpx`, `flask`'s `request.args`, etc.). Per-library scoping mirrors how humans actually disambiguate.

**AST rewriting at import time** (rewrite `طلبات.احصل` → `requests.get` in the AST of the importing module before compile). Rejected. Forces a second compile pass on every importing file, contradicts ADR 0001's "tokenize-only" architecture, and breaks runtime-dynamic attribute access (`getattr(طلبات, "احصل")`).

**`__getattr__` on the imported module without a proxy object.** Rejected. Would let us write `import requests as طلبات; طلبات.احصل` but doesn't let us write `استورد طلبات` and have Python resolve `طلبات` to the right thing — module objects don't override `__getattr__` for the importer's name binding.

**Runtime monkey-patching of imported modules** (mutate `requests` itself to add `احصل = requests.get` on first import). Rejected for the same reason ADR 0001 rejected it for built-ins: destroys introspection, conflicts with other consumers of the same module, and surfaces as "spooky" debugging behavior.

**Auto-transliteration only, no curated mappings.** Rejected. Auto-transliteration of `requests.get` → `طلبات.جت` produces nonsense and forecloses the pedagogical value of curated translations. Auto-transliteration is a fallback for unmapped names, not a primary mechanism.

**Skip B-001, wait for sponsor before any Phase B work.** Rejected. Without B-001, the architecture in B.1 is unvalidated and a sponsor evaluating the project sees only Phase A. The cost of B-001 (one packet, ~2 weeks of solo work) is dwarfed by the cost of pitching Phase B with no working demo.

## References

- ADR 0001 — Architecture (proxy must coexist with the tokenize pipeline; this ADR confirms it does, by layering above)
- ADR 0003 — Keyword dictionary governance (B.0 frozen-dictionary clause builds on 0003's versioning mechanism)
- ADR 0007 — Scope: learning dialect first, production replacement second (this ADR is the charter 0007 promised)
- Ramsey Nasser, *A Personal Computer for Children of All Cultures*, Deconstruct 2019 — the layer-3 framing
- Python `sys.meta_path` documentation: https://docs.python.org/3/library/sys.html#sys.meta_path
- PEP 562 (`__getattr__` on modules): https://peps.python.org/pep-0562/ — referenced in alternatives
