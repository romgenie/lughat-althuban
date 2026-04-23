# Spec Packet B-070: dialect-egyptian-v0-proposal

**Phase**: B
**Depends on**: B-001, B-002
**Estimated size**: small (1 session)
**Status**: proposed

## Goal

Propose a spec for an Egyptian Arabic dictionary variant (`ar-eg`). This allows learners in Egypt to use keywords and built-ins that match their local dialect (e.g., using `ورينا` instead of `اطبع`). This is a design document, not a code implementation.

## Non-goals

- **No code implementation.**
- **No changes to the core `ar-v1` dictionary.**

## Files

### Files to create

- `proposals/B070-dialect-egyptian-v0.md` — the design document.

## Implementation constraints

- **Output**: Markdown document only.
- **Content**: Must include a mapping table for core keywords and rationale for dialect choices.

## Acceptance checklist

- [ ] `proposals/B070-dialect-egyptian-v0.md` created.
- [ ] [Phase A Compatibility] Proposal explicitly addresses how to maintain compatibility with Phase A code.
- [ ] Proposal follows project ADRs for curation.
- [ ] Delivery note `B-070-dialect-egyptian-v0-proposal.delivery.md` written.
