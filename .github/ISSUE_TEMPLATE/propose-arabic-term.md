---
name: Propose an Arabic term
about: Suggest an Arabic translation for a Python symbol (library function, stdlib name, error message)
title: "Term: <python-symbol> → <proposed-arabic>"
labels: ["dictionary", "translation"]
assignees: []
---

## Python symbol

<!-- The exact symbol. Examples:
     - flask.Flask
     - flask.request.args
     - pandas.DataFrame.groupby
     - urllib.request.urlopen
     - exception: ValueError -->

## Which packet does this belong to?

<!-- Check ROADMAP-PHASE-B.md. Examples:
     - B-010 (Flask)
     - B-018 (pandas)
     - B-035 (stdlib network)
     - B-041 (traceback messages)
     - or "I'm not sure — please route this" -->

## Proposed canonical Arabic term

<!-- One term. The one you actually recommend. -->

## Two alternates considered

1. <!-- Alternate 1, with one-sentence reason it's worse than your proposal -->
2. <!-- Alternate 2, with one-sentence reason it's worse than your proposal -->

## Rationale (one sentence)

<!-- Why this term? Examples:
     - "Matches Hedy's Arabic translation of the same concept."
     - "MSA equivalent; shorter than the alternates."
     - "Avoids homograph with the existing dictionary entry for `request`." -->

## Curation rules check

- [ ] **Hedy precedent** — checked Hedy's Arabic translation if applicable
- [ ] **MSA over dialect** — proposal is Modern Standard Arabic
- [ ] **Shortest defensible** — no shorter MSA option that's equally clear
- [ ] **No homograph** — does not collide with an existing entry in `dictionaries/ar-v1.md` or any merged alias TOML
- [ ] **Round-trips through normalization** — `arabicpython.normalize.normalize_identifier(proposal) == proposal`. (If unsure, leave unchecked and ask.)

## Anything else

<!-- Optional. Linguistic context, references to dictionaries, examples of the term used elsewhere. -->
