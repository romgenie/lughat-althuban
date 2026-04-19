# Getting started with apython

This tutorial walks through the apython dialect from "hello world" to importing
your own modules. Every code sample is a real `.apy` file you can paste into a
buffer and run; most of them mirror the seven progressive demos in
[`examples/`](../examples/).

If you read Arabic comfortably and have written Python before, this tutorial
will take ~20 minutes. If you're new to programming, plan on an hour and run
every snippet — apython is meant to be typed, not just read.

## Contents

1. [Install](#1-install)
2. [Hello world](#2-hello-world)
3. [Variables and arithmetic](#3-variables-and-arithmetic)
4. [Control flow](#4-control-flow)
5. [Functions](#5-functions)
6. [Data structures](#6-data-structures)
7. [Classes](#7-classes)
8. [Imports](#8-imports)
9. [Reading error messages](#9-reading-error-messages)
10. [Where to go next](#10-where-to-go-next)

---

## 1. Install

apython requires Python 3.11 or newer. From the repository root:

```bash
git clone https://github.com/GalaxyRuler/apython
cd apython
pip install -e .
```

That installs the `apython` console script. Verify it:

```bash
apython --version
```

You now have four ways to run apython code, mirroring stock `python`:

```bash
apython script.apy [args...]    # run a file
apython -c 'اطبع("مرحبا")'      # run an inline string
apython - < script.apy          # read from stdin
apython                          # interactive REPL
```

Exit codes: `0` success, `1` runtime/translate error, `2` usage error.

---

## 2. Hello world

Save this as `hello.apy`:

```arabic
اطبع("مرحبا، يا عالم")
```

Run it:

```bash
$ apython hello.apy
مرحبا، يا عالم
```

That's it. `اطبع` is the Arabic name for Python's `print`. Every other built-in,
keyword, and exception type works the same way — apython is Python with the
identifier table translated, nothing more.

A complete table of every translated symbol lives in
[`dictionaries/ar-v1.md`](../dictionaries/ar-v1.md). You don't need to
memorize it; the examples below introduce keywords as they're needed.

---

## 3. Variables and arithmetic

Variable assignment is plain Python — apython only translates *built-in* names,
not your own. Pick any Arabic identifier you like:

```arabic
العمر = 25
السنوات_حتى_التقاعد = 65 - العمر
اطبع(f"باقي {السنوات_حتى_التقاعد} سنة")
```

Output:

```
باقي 40 سنة
```

A few things are happening here that are worth calling out:

- **Multi-word identifiers use `_`**, not space. Arabic conventionally separates
  compound terms with a space, but Python's tokenizer treats space as a
  boundary, so the dialect uses underscores. This rule is universal across
  apython.
- **f-strings work normally.** Interior expressions are pretokenized just like
  the rest of the source, so `f"{السنوات_حتى_التقاعد}"` resolves the variable
  exactly as you'd expect.
- **Arabic-Indic and Eastern-Arabic digits are auto-folded.** Writing
  `العمر = ٢٥` is identical to writing `العمر = 25`. Mixing digit systems
  inside one numeric literal (e.g. `١2`) is a `SyntaxError` — apython rejects
  it loudly rather than guess.
- **Arabic punctuation is auto-folded** outside string literals: `،` → `,`,
  `؛` → `;`, `؟` → `?`. So `جمع(أ، ب)` is identical to `جمع(أ, ب)`. Inside
  strings, every Arabic character is preserved verbatim.

See [`examples/02_arithmetic.apy`](../examples/02_arithmetic.apy).

---

## 4. Control flow

The control-flow keywords:

| Python | apython | Reads as |
|---|---|---|
| `if` | `إذا` | "if" |
| `else` | `وإلا` | "otherwise" |
| `elif` | `وإلا_إذا` | "and if otherwise" |
| `for` | `لكل` | "for each" |
| `while` | `طالما` | "as long as" |
| `in` | `في` | "in" |
| `break` | `اكسر` | "break" |
| `continue` | `استمر` | "continue" |
| `range` | `نطاق` | "range/span" |

A loop with a conditional inside:

```arabic
لكل عدد في نطاق(1, 6):
    إذا عدد % 2 == 0:
        اطبع(f"{عدد}: زوجي")
    وإلا:
        اطبع(f"{عدد}: فردي")
```

Output:

```
1: فردي
2: زوجي
3: فردي
4: زوجي
5: فردي
```

Indentation is significant exactly the way it is in Python — four spaces per
level by convention.

See [`examples/03_control_flow.apy`](../examples/03_control_flow.apy).

---

## 5. Functions

`def` is `دالة` (the MSA mathematical word for "function"). `return` is
`ارجع`. Default arguments work the standard way:

```arabic
دالة جمع(أ, ب=10):
    ارجع أ + ب

اطبع(جمع(5))         # 15
اطبع(جمع(5, 7))      # 12
```

Function names, parameter names, and local variables are all your choice —
apython does not translate them, so you can use any Arabic, English, or mixed
identifier that's a valid Python name.

A note on identifier normalization: apython folds certain Arabic character
variants to a single canonical form before lookup, so `قيمه` and `قيمة` (with
ta-marbuta) refer to the same name, as do `إذا` and `اذا` (with and without
hamza). This means the spelling you type is forgiving, but the *stored* name
is one canonical form. The full rules are in
[`decisions/0004-normalization-policy.md`](../decisions/0004-normalization-policy.md);
for day-to-day code you can ignore the details.

See [`examples/04_functions.apy`](../examples/04_functions.apy).

---

## 6. Data structures

Lists, dicts, tuples, and sets all work normally. Their *type names* are
translated (`قائمة`, `قاموس`, `صف`, `مجموعة`) but you rarely call those
constructors directly — most code uses literals:

```arabic
الفواكه = ["تفاح", "موز", "برتقال"]
الأسعار = {"تفاح": 3, "موز": 2, "برتقال": 4}

لكل فاكهة في الفواكه:
    اطبع(f"{فاكهة}: {الأسعار[فاكهة]} ريال")
```

Output:

```
تفاح: 3 ريال
موز: 2 ريال
برتقال: 4 ريال
```

Common methods have Arabic names: `.append → اضف`, `.pop → انتزع`,
`.keys → مفاتيح`, `.values → قيم`, `.items → عناصر`, `.get → احصل`.
The full method table is in section 6 of `ar-v1.md`.

See [`examples/05_data_structures.apy`](../examples/05_data_structures.apy).

---

## 7. Classes

`class` is `صنف`. The conventional `self` parameter is `الذات` ("the self").
Dunder methods like `__init__` are not translated — they keep their Python
spelling because they're protocol-defined names, not user-facing vocabulary.

```arabic
صنف نقطة:
    دالة __init__(الذات, س, ص):
        الذات.س = س
        الذات.ص = ص

    دالة المسافة_من_الأصل(الذات):
        ارجع (الذات.س ** 2 + الذات.ص ** 2) ** 0.5

نقطة_1 = نقطة(3, 4)
اطبع(نقطة_1.المسافة_من_الأصل())   # 5.0
```

Inheritance, `super()` (`الاصل()`), classmethods, and staticmethods all work
the same way they do in Python — translate the keyword, write the rest in
ordinary Python style.

See [`examples/06_classes.apy`](../examples/06_classes.apy).

---

## 8. Imports

apython installs a `sys.meta_path` import hook so `.apy` files import each
other transparently:

```arabic
# helper.apy
دالة مربع(عدد):
    ارجع عدد ** 2

دالة مكعب(عدد):
    ارجع عدد ** 3
```

```arabic
# main.apy
استورد helper كـ مساعد

اطبع(مساعد.مربع(5))   # 25
اطبع(مساعد.مكعب(3))   # 27
```

Run `apython main.apy` and the hook finds `helper.apy`, translates it, and
makes it importable.

The keywords here are `استورد` (`import`) and `كـ` (`as`). You can also import
specific names: `من helper استورد مربع` (`from helper import مربع`).

Standard-library modules (`math`, `json`, `os`, …) are imported by their
ordinary Python names — `استورد math`. Phase A only translates the *language*,
not the standard library. Library-name aliasing is the job of Phase B; see
[`decisions/0008-phase-b-charter.md`](../decisions/0008-phase-b-charter.md).

**Cross-language imports** work in both directions:

- A `.py` file can `import helper` to get an `.apy` module.
- An `.apy` file can `استورد json` to get a stdlib `.py` module.

One Phase A gotcha: `from . import x` inside a package `__init__.apy` doesn't
yet translate. Workaround: write `استورد pkg.sub كـ sub`. This is documented
in the project README's *Known limitations* section and slated for a future
fix-up packet.

See [`examples/07_imports.apy`](../examples/07_imports.apy).

---

## 9. Reading error messages

Uncaught exceptions print Arabic tracebacks:

```bash
$ apython -c '1 / 0'
تتبع_الأخطاء (المكدس الأحدث آخرا):
  ملف "<string>", سطر 1, في <الوحدة>
خطا_القسمه_على_صفر: القسمة على صفر
```

The structure is the same as a Python traceback, just with translated frame
labels:

| Python | apython |
|---|---|
| `Traceback (most recent call last):` | `تتبع_الأخطاء (المكدس الأحدث آخرا):` |
| `File "..."` | `ملف "..."` |
| `line N` | `سطر N` |
| `in <module>` | `في <الوحدة>` |

Exception type names are translated systematically. `ZeroDivisionError` becomes
`خطا_القسمه_على_صفر` ("error of division by zero"); `KeyError` becomes
`خطا_المفتاح`; `ValueError` becomes `خطا_القيمه`. The `خطا_` prefix mirrors
Python's `Error` suffix. A handful of exceptions whose Python names *don't* end
in `Error` keep that distinction in Arabic: `KeyboardInterrupt`,
`StopIteration`, `Warning`, `GeneratorExit`, `SystemExit` are *not* prefixed
with `خطا_`.

Full list of all 38 translated exception types is in
[`dictionaries/exceptions-ar-v1.md`](../dictionaries/exceptions-ar-v1.md).

When you `raise` your own exception, you can use either the Arabic or the
English class name — both resolve to the same object:

```arabic
حاول:
    ارفع خطا_القيمه("القيمة غير صالحة")
استثناء خطا_القيمه كـ خطأ:
    اطبع(f"التُقط: {خطأ}")
```

Output:

```
التُقط: القيمة غير صالحة
```

Around 30 of the most common interpreter messages are translated as well
(`division by zero`, `list index out of range`, `unsupported operand type(s)`).
Messages that don't have a translation pass through unchanged in English —
better an honest English message than a misleading Arabic one.

---

## 10. Where to go next

- **Run the examples.** [`examples/01_hello.apy`](../examples/01_hello.apy)
  through `07_imports.apy` are progressively richer demos. Each one is
  intentionally short; together they exercise every feature of the dialect.
- **Skim the dictionary.** [`dictionaries/ar-v1.md`](../dictionaries/ar-v1.md)
  is the canonical word list. You don't need to memorize it, but a 5-minute
  skim builds a useful mental map of what's covered.
- **Read the architecture ADR.** If you're curious *how* the translation
  happens at all,
  [`decisions/0001-architecture.md`](../decisions/0001-architecture.md)
  explains the source-to-source preprocessor design in one page.
- **Try the REPL.** Just run `apython` with no arguments. It accepts the same
  Arabic-keyword syntax as a script, with multi-line input via continuation
  prompts.
- **File issues for things that surprised you.** Phase A is feature-complete
  but the dictionary will continue to evolve in `ar-v2`. If a translation
  reads strangely, that's signal worth capturing.

apython is a learning dialect first and a production tool second (see
[`decisions/0007-scope.md`](../decisions/0007-scope.md) for the explicit
ordering). The shape of Phase B — including whether `استورد طلبات` will
eventually mean `import requests` — is sketched in
[`decisions/0008-phase-b-charter.md`](../decisions/0008-phase-b-charter.md).
