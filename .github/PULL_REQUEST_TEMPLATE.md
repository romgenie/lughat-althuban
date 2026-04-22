<!--
Title format: B-NNN: <packet-short-name>
Examples:
  B-010: aliases-flask-v1
  B-040: dictionary-v1.1-async-match
  B-010: aliases-flask-v1 (fixup-1)
-->

## Packet

- **ID:** <!-- e.g. B-010 -->
- **Spec:** <!-- e.g. specs/B-010-aliases-flask-v1.md -->
- **Claim issue:** <!-- e.g. #42 -->
- **Delivery note:** <!-- e.g. specs/B-010-aliases-flask-v1.delivery.md (must exist in this PR) -->

## Summary of approach

<!-- One paragraph. Not a play-by-play of the diff — explain the design decisions you made within the spec, and any choices the spec left to your judgment. -->

## Acceptance checklist (copy from the spec)

<!-- Copy the full "Acceptance checklist" section from your spec packet and mark each item as you complete it.
     Don't shorten or summarize — copy verbatim so the reviewer can see exactly which items you've addressed. -->

- [ ] All listed files created or modified.
- [ ] All listed tests present and passing.
- [ ] `ruff check .` passes.
- [ ] `black --check .` passes.
- [ ] `pytest` passes on Python 3.11, 3.12, 3.13.
- [ ] Delivery note `<packet-id>.delivery.md` written and committed.
- [ ] (If aliases packet) All translation entries pass `arabicpython.normalize.normalize_identifier()` round-trip.
- [ ] (If aliases packet) `examples/B<NN>_<short>.apy` example runs end-to-end.

## Delivery note checklist

- [ ] **Deviations from the spec** — every place I did something different, with reason. If "none", say "none."
- [ ] **Open questions for the planner** — anything I wasn't sure about. Empty is best.
- [ ] **Non-spec testing performed** — anything I tested manually that isn't in the test suite.
- [ ] **Phase A compat verified** — `pytest tests/test_phase_a_compat.py` passes (after B-002 merges; before then, confirm the seven `examples/` files still run).

## CI confirmation

- [ ] All 9 matrix cells passing (Linux/macOS/Windows × Python 3.11/3.12/3.13).

If any cell is failing, **explain why below** and tag the planner — do not mark this PR ready for review.

## Phase A compatibility statement

- [ ] This PR does not change `dictionaries/ar-v1.md`. (Required per ADR 0008.B.0.)
- [ ] This PR does not change any file under `examples/` or `apps/`. (Required per ADR 0008.B.3.)
- [ ] If this PR changes an internal API in `arabicpython/`, the change is documented in the delivery note's "Deviations" section.

If any of the above is unchecked, this PR cannot merge until a superseding ADR is accepted.

---

*Reviewers: see [CONTRIBUTING.md §8](../CONTRIBUTING.md#8--review-sla-and-what-to-expect) for the review process. Tests are the contract — focus review on whether tests cover the spec's requirements, not on code style.*
