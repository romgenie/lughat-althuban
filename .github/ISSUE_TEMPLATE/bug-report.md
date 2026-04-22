---
name: Bug report
about: Report unexpected behavior in `.apy` programs, the CLI, the REPL, or imports
title: "Bug: <one-line summary>"
labels: ["bug"]
assignees: []
---

## Minimal `.apy` source that reproduces the issue

```python
# Paste the smallest .apy program that triggers the bug.
# Ideally under 20 lines.
```

If the bug only appears via the CLI, paste the exact command:

```bash
ثعبان ...
```

## Expected behavior

<!-- What did you expect to happen? -->

## Actual behavior

<!-- What actually happened? Paste the full traceback if there is one (Arabic or English). -->

```
<paste output here>
```

## Environment

- **Python version:** <!-- output of `python --version` -->
- **OS:** <!-- e.g. Windows 11, Ubuntu 24.04, macOS 15.4 -->
- **`ثعبان` version:** <!-- output of `ثعبان --version` -->
- **Install method:** <!-- pip install -e . / pip install from git / other -->

## Have you checked the known issues?

- [ ] The Phase A "known limitations" section of [README.md](../../README.md) does not list this issue.
- [ ] The bug is reproducible (it's not a one-off flake).
- [ ] If the bug involves Arabic identifiers, it does NOT involve harakat (shadda, damma, etc.) — those are a known Python 3.11 tokenizer issue documented in the Phase A delivery notes.

## Anything else

<!-- Workarounds you tried, suspicions about cause, related issues, etc. -->
