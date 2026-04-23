# Spec Packet B-071: dialect-loader-multiplexing-v2

**Phase**: B
**Depends on**: B-001, B-072-dialect-precedence-rules-adr
**Estimated size**: small (1 session)
**Status**: proposed

## Goal

Design the requirements for the dictionary loader to support multiple simultaneous dialects per file. This enables a program to mix, for example, MSA and Egyptian Arabic keywords seamlessly, or to use specialized domain-specific dictionaries alongside the core language.

## Non-goals

- **No code implementation.**
- **No changes to the existing loader** in this packet.

## Files

### Files to create

- `proposals/B071-dialect-loader-multiplexing-v2.md` — design document.

## Implementation constraints

- **Output**: Markdown document.
- **Content**: Describe the per-file directive syntax for multiple dialects (e.g., `# arabicpython: dict=ar-v1,ar-eg`).

## Acceptance checklist

- [ ] Design document created.
- [ ] [Phase A Compatibility] Describes how single-dialect Phase A files continue to work.
- [ ] Delivery note `B-071-dialect-loader-multiplexing-v2.delivery.md` written.
