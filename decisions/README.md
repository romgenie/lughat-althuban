# Architectural Decision Records (ADRs)

This directory contains numbered, immutable design decisions for the `apython` project. Each file documents **one** decision, the context that forced it, alternatives considered, and the consequences.

## Conventions

- Files are named `NNNN-short-kebab-title.md`, zero-padded four digits.
- Numbers are allocated sequentially and never reused.
- Accepted ADRs are **immutable**. To change a decision, create a new ADR with status `accepted` and set the old one's status to `superseded by NNNN`.
- Every ADR's `Status` field must be one of: `proposed`, `accepted`, `superseded by NNNN`, or `deprecated`.

## Format

```markdown
# NNNN — <Title>

**Status**: accepted
**Date**: YYYY-MM-DD
**Deciders**: <who>

## Context
Why is this a decision we need to make? What forces are at play?

## Decision
What we chose.

## Consequences
What follows from this decision — good, bad, and neutral.

## Alternatives considered
What else we looked at, and why it was rejected.
```

## Phase 0 index

| ID | Title | Status |
|---|---|---|
| 0001 | Architecture: source-to-source preprocessor | accepted |
| 0002 | File extension: `.apy` | accepted |
| 0003 | Keyword dictionary governance | accepted |
| 0004 | Identifier normalization policy | accepted |
| 0005 | Arabic numerals and punctuation in source | accepted |
| 0006 | Bidi control character policy | accepted |
| 0007 | Scope: learning dialect first, production replacement second | accepted |
| 0008 | Phase B charter | accepted |
