# apython — Arabic Python

A Python dialect where keywords, built-ins, and exceptions are written in Arabic. `.apy` files are translated to standard Python at load time and executed by CPython — no interpreter fork.

**Status**: Phase A complete (2026-04-19). All four entry surfaces work: file, `-c`, stdin, REPL. `.apy` modules import each other. Uncaught exceptions print Arabic tracebacks.
**Phase B**: not yet chartered.
**License**: Apache-2.0.
**Repo**: private during pre-release.

## Quick example

```arabic
# hello.apy
دالة مرحبا(اسم):
    اطبع(f"مرحبا يا {اسم}")

لكل شخص في ["سارة", "أحمد", "ليلى"]:
    مرحبا(شخص)
```

```bash
$ apython hello.apy
مرحبا يا سارة
مرحبا يا أحمد
مرحبا يا ليلى
```

## Install

```bash
git clone https://github.com/GalaxyRuler/apython
cd apython
pip install -e .
```

Requires Python 3.11+. Installs the `apython` console script.

## Running code

Four entry surfaces, mirroring stock `python`:

```bash
apython script.apy [args...]    # run a file
apython -c 'اطبع("مرحبا")'      # run an inline string
apython - < script.apy          # read from stdin
apython                          # interactive REPL
```

`apython --help` and `apython --version` work as expected. Exit codes: `0` success, `1` runtime/translate error, `2` usage error.

## Importing `.apy` modules

The package installs a `sys.meta_path` import hook so `.apy` files can be imported like any Python module:

```arabic
# main.apy
استورد helper
helper.مرحبا("عالم")
```

```arabic
# helper.apy
دالة مرحبا(اسم):
    اطبع(f"مرحبا يا {اسم}")
```

```bash
$ apython main.apy
مرحبا يا عالم
```

Mixed `.py` / `.apy` packages work — Python files importing `.apy` modules see the translated, normalized identifier names (e.g., `helper.مرحبا` from Python uses the same form).

## Arabic tracebacks

Uncaught exceptions are printed with Arabic type names and translated messages:

```bash
$ apython -c '1 / 0'
تتبع_الأخطاء (المكدس الأحدث آخرا):
  ملف "<string>", سطر 1, في <الوحدة>
خطا_القسمه_على_صفر: القسمة على صفر
```

38 standard exception types and ~30 common interpreter messages are translated. Unmapped types and messages pass through unchanged.

## Public Python API

For embedding the dialect in other tools:

```python
from arabicpython import (
    install,                       # install the .apy import hook
    uninstall,
    run_repl,                      # start the interactive REPL
    install_excepthook,            # route uncaught exceptions through the translator
    uninstall_excepthook,
    format_translated_exception,   # format a (type, value, tb) triple as Arabic
)
```

## Project structure

```
apython/
├── decisions/        ADRs — architectural choices, immutable once accepted
├── dictionaries/     ar-v1.md (keywords/built-ins) + exceptions-ar-v1.md
├── specs/            Spec packets handed off to the implementer
├── arabicpython/     The transpiler package
├── tests/            pytest suite (316 tests as of Phase A wrap)
└── examples/         Runnable .apy programs (7 progressive demos)
```

## Architecture in one paragraph

Source goes through `pretokenize` (Arabic numerals → ASCII, punctuation aliasing, bidi-control rejection) → Python's `tokenize` → a NAME-rewriter that consults the canonical Arabic→Python dictionary → `untokenize` → `compile` → `exec`. No AST rewrite, no CPython fork. The same pipeline backs every entry surface (CLI, REPL, import hook). See [`decisions/0001-architecture.md`](decisions/0001-architecture.md) for the full rationale and [`decisions/0004-normalization-policy.md`](decisions/0004-normalization-policy.md) for how Arabic identifier variants (hamza, ta-marbuta, alef-maksura) are folded.

## Known limitations (Phase A)

- **`from . import x` in package `__init__.apy`** does not translate — the tokenizer sees `import` after the `.` and treats it as an attribute lookup. Workaround: `import pkg.sub as sub`. Fix deferred to a future "translate-fixups" packet.
- **Cross-language attribute access from `.py` to `.apy`** must use the ADR-0004-normalized identifier form (e.g., `module.قيمه`, not `module.قيمة`). This is correct per the normalization policy but is a real learner gotcha.
- **No async/await ergonomics testing yet.** The keywords translate; end-to-end async program coverage is not part of Phase A.

## Development model

Planner / implementer split:

- **Claude** (planner): writes ADRs, curates dictionaries, authors spec packets, reviews diffs.
- **Gemini CLI** (implementer): reads packets in `specs/NNNN-*.md`, writes code, runs tests, files PRs, writes a delivery note in `specs/NNNN-*.delivery.md`.

Every implementation unit is a spec packet. See [`specs/0000-template.md`](specs/0000-template.md) for the format and [`specs/INDEX.md`](specs/INDEX.md) for the packet ledger.

## Roadmap

| Phase | Content | Status |
|---|---|---|
| 0 | Design decisions (7 ADRs) | complete |
| A | Tokenize-based dialect: pretokenize, normalize, translate, CLI, import hook, REPL, Arabic tracebacks | complete |
| B | Production replacement — scope and entry conditions to be defined | not started |

## Acknowledgements

- **zhpy** (gasolin, 2014) — the tokenize-based Chinese Python dialect this project is architecturally modeled on.
- **Ramsey Nasser's قلب (Qalb)** — the critique this project takes seriously, and the reason Phase B is a distinct, deliberately-deferred phase rather than the default goal.
- **Hedy** — proof that gradual-syntax, multilingual Python-like education works at scale.
