# Spec Packet B-072: dialect-precedence-rules-adr

**Phase**: B
**Depends on**: B-001, B-002
**Estimated size**: small (1 session)
**Status**: proposed

## Goal

Create an Architectural Decision Record (ADR) defining the precedence rules when an Arabic token resolves to different Python keywords under multiple active dialects. This ensures deterministic translation and prevents ambiguity.

## Non-goals

- **No code implementation.**

## Files

### Files to create

- `decisions/0010-dialect-precedence-rules.md` — the ADR.

## Implementation constraints

- **Format**: ADR-standard markdown.
- **Content**: Define the ordering rules (e.g., "last declared wins" or "core takes precedence").

## Acceptance checklist

- [ ] ADR 0010 created.
- [ ] [Phase A Compatibility] ADR ensures that Phase A code behavior is preserved.
- [ ] Delivery note `B-072-dialect-precedence-rules-adr.delivery.md` written.
