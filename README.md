<div dir="rtl">

# لغة الثعبان — بايثون بالعربية

[![الاختبارات](https://img.shields.io/badge/اختبارات-2510_نجاح-brightgreen)](tests/)
[![بايثون](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)
[![الرخصة](https://img.shields.io/badge/رخصة-Apache--2.0-orange)](LICENSE)

لهجة برمجية تكتب فيها **الكلمات المفتاحية والدوال المدمجة والاستثناءات والمكتبات** بالعربية الكاملة. ملفات `.apy` تُترجم إلى بايثون القياسي في وقت التحميل وتُنفَّذ بواسطة CPython — دون تشعيب للمترجم ودون تعديل على اللغة.

---

## مثال متكامل — تحليل بيانات بالعربية الكاملة

```python
# تحليل_مبيعات.apy
استورد جداول_بيانات  كـ  جب        # pandas
استورد حسابات_عددية كـ  عد        # numpy
استورد رسوم_احصائيه كـ  رسم       # seaborn
استورد رياضيات

بيانات = جب.قراءة_جيسون("مبيعات.json")
متوسط  = عد.متوسط(بيانات["الإيرادات"])
اطبع(f"متوسط الإيرادات: {رياضيات.تقريب(متوسط, 2)}")

رسم.ضبط_موضوع("darkgrid")
مخطط = رسم.خط_بياني(بيانات=بيانات, x="الشهر", y="الإيرادات")
مخطط.figure.savefig("تقرير_المبيعات.png")
اطبع("✓ تم حفظ التقرير")
```

```bash
$ ثعبان تحليل_مبيعات.apy
متوسط الإيرادات: 48750.32
✓ تم حفظ التقرير
```

---

## التثبيت

يتطلب Python 3.11 أو أحدث:

```bash
git clone https://github.com/GalaxyRuler/lughat-althuban
cd lughat-althuban
pip install -e .
```

للتطوير مع جميع المكتبات المدعومة:

```bash
pip install -e ".[dev]"
```

---

## طرق التشغيل

```bash
ثعبان ملف.apy              # تشغيل ملف
ثعبان -c 'اطبع("مرحبا")'   # تنفيذ سطر مباشرةً
ثعبان - < ملف.apy          # قراءة من المدخل القياسي
ثعبان                       # البيئة التفاعلية REPL
ثعبان نسّق ملف.apy          # تنسيق الملف تلقائياً
ثعبان راجع ملف.apy          # فحص الجودة وإظهار التحذيرات
```

---

## الحالة الراهنة

| البند | القيمة |
|-------|--------|
| الاختبارات | 🟢 **2510 نجاح** — 45 تجاوز (مكتبات اختيارية) |
| وحدات قياسية عربية | 21 وحدة من stdlib |
| مكتبات علمية وبيانات | numpy، pandas، matplotlib، seaborn، scipy، scikit-learn |
| مكتبات ويب وشبكات | flask، requests، aiohttp، fastapi |
| تعلم آلي | pytorch |
| أدوات | مُنسِّق، مُدقِّق، نواة Jupyter |
| بيئات CI | Ubuntu، macOS، Windows / Python 3.11–3.13 |

---

## رسائل الخطأ بالعربية

```bash
$ ثعبان -c '1 / 0'
تتبع_الأخطاء (المكدس الأحدث آخرا):
  ملف "<string>", سطر 1, في <الوحدة>
خطا_القسمه_على_صفر: القسمة على صفر
```

38 نوع استثناء قياسي و~30 رسالة مترجمة. الأنواع غير المعروفة تمر كما هي.

---

## الوثائق بالعربية

| الوثيقة | الوصف |
|---------|--------|
| [دليل البدء الشامل](docs/ar/getting-started.md) | من "مرحبا بالعالم" إلى الاستيراد — خطوة بخطوة |
| [دليل البدء الموسَّع](docs/tutorial-ar.md) | الموازي العربي للدليل الإنجليزي مع مسرد المصطلحات (B-060) |
| [كتاب الوصفات العربي](docs/cookbook-ar.md) | عشر وصفات قصيرة قائمة بذاتها مع مسرد مصطلحات (B-061) |
| [نظرة عامة على المشروع](docs/ar/README.md) | المعمارية، هيكل المشروع، خارطة الطريق |
| [مرجع المكتبة القياسية](docs/ar/stdlib-reference.md) | جميع الوحدات القياسية العربية مع أمثلة |
| [ويكي المشروع](docs/wiki/index.md) | دليل شامل: الكلمات المفتاحية، المكتبات، الأدوات، الأسئلة الشائعة |
| [سجل التغييرات](CHANGELOG.md) | ما الذي تغيّر في كل إصدار |
| [خارطة الطريق](ROADMAP-PHASE-B.md) | الحزم القادمة وحالتها |

---

## المرحلة (ب): مكتملة إلى حدٍّ بعيد

المرحلة (أ) اكتملت. المرحلة (ب) أضافت منظومة متكاملة:

- **نظام الأسماء المستعارة**: 40+ وحدة مع أسماء عربية
- **طبقة الأدوات**: منسّق + مدقّق + نواة Jupyter + امتداد VS Code
- **التوسعية**: إضافة مكتبة جديدة يعني كتابة ملف TOML واحد

- **خارطة الطريق:** [`ROADMAP-PHASE-B.md`](ROADMAP-PHASE-B.md)
- **دليل المساهمة:** [`CONTRIBUTING.md`](CONTRIBUTING.md)
- **حزمة جيدة للبدء:** [`specs/B-002-phase-a-compat-suite.md`](specs/B-002-phase-a-compat-suite.md)

</div>

---

# لغة الثعبان — Arabic Python

A Python dialect where **keywords, built-ins, exceptions, and popular libraries** are written in Arabic. `.apy` files are translated to standard Python at load time and executed by CPython — no interpreter fork, no language modification.

**Status (2026-04-28)**: Phase A complete. Phase B substantially complete — **2,510 tests passing** across Python 3.11–3.13 on Ubuntu/macOS/Windows. 40+ alias modules shipped. Full tooling layer (formatter, linter, Jupyter kernel, VS Code extension).

**License**: Apache-2.0.

---

## Full example — data analysis entirely in Arabic

```python
# sales_analysis.apy
استورد جداول_بيانات  كـ  جب        # pandas
استورد حسابات_عددية كـ  عد        # numpy
استورد رسوم_احصائيه كـ  رسم       # seaborn
استورد رياضيات

data = جب.قراءة_جيسون("sales.json")
avg  = عد.متوسط(data["revenue"])
اطبع(f"Average revenue: {رياضيات.تقريب(avg, 2)}")

رسم.ضبط_موضوع("darkgrid")
chart = رسم.خط_بياني(data=data, x="month", y="revenue")
chart.figure.savefig("report.png")
```

---

## Install

```bash
git clone https://github.com/GalaxyRuler/lughat-althuban
cd lughat-althuban
pip install -e .
```

Requires Python 3.11+. Installs the `ثعبان` console script.

For all optional library aliases:

```bash
pip install -e ".[dev]"
```

---

## Running code

```bash
ثعبان script.apy [args...]    # run a file
ثعبان -c 'اطبع("مرحبا")'      # run an inline string
ثعبان - < script.apy          # read from stdin
ثعبان                          # interactive REPL
ثعبان نسّق script.apy          # auto-format a file
ثعبان راجع script.apy          # lint and report diagnostics
```

`ثعبان --help` and `ثعبان --version` work as expected. Exit codes: `0` success, `1` runtime/translate error, `2` usage error.

---

## Importing `.apy` modules

```python
# main.apy
استورد helper
helper.مرحبا("عالم")
```

```python
# helper.apy
دالة مرحبا(اسم):
    اطبع(f"مرحبا يا {اسم}")
```

Mixed `.py` / `.apy` packages work — Python files importing `.apy` modules see the translated, normalized identifier names.

---

## Arabic tracebacks

```bash
$ ثعبان -c '1 / 0'
تتبع_الأخطاء (المكدس الأحدث آخرا):
  ملف "<string>", سطر 1, في <الوحدة>
خطا_القسمه_على_صفر: القسمة على صفر
```

38 standard exception types and ~30 common interpreter messages translated.

---

## Arabic alias modules

Import Python's standard library and popular packages using Arabic names:

### Standard library (21 modules)

| Arabic name | Python module | Arabic name | Python module |
|---|---|---|---|
| `نظام_تشغيل` | `os` | `رياضيات` | `math` |
| `مسار_مكتبه` | `pathlib` | `احصاء` | `statistics` |
| `نظام` | `sys` | `عشوائيات` | `random` |
| `مجموعات` | `collections` | `تسجيل` | `logging` |
| `ادوات_تكرار` | `itertools` | `اتزامن` | `asyncio` |
| `ادوات_داليه` | `functools` | `هاشلب` | `hashlib` |
| `مكتبة_تاريخ` | `datetime` | `مجاري` | `io` |
| `وقت_نظام` | `time` | `مدير_سياق` | `contextlib` |
| `روزنامه` | `calendar` | `قاعدة_بيانات` | `sqlite3` |
| `جيسون` | `json` | `تعابير_نمطيه` | `re` |
| `ملفات_csv` | `csv` | | |

### Science & data (6 packages)

| Arabic name | Python package |
|---|---|
| `حسابات_عددية` | `numpy` |
| `جداول_بيانات` | `pandas` |
| `رسوم_بيانيه` | `matplotlib` |
| `رسوم_احصائيه` | `seaborn` |
| `علوم_حسابيه` | `scipy` |
| `تعلم_آلي` | `scikit-learn` |

### Web & async (4 packages)

| Arabic name | Python package |
|---|---|
| `قارورة` | `flask` |
| `طلبات` | `requests` |
| `طلبات_غير_متزامنه` | `aiohttp` |
| `واجهه_برمجيه` | `fastapi` |

### Machine learning (1 package)

| Arabic name | Python package |
|---|---|
| `مشعل` | `torch` |

---

## Tooling layer (Phase B)

| Tool | Command | Description |
|---|---|---|
| **Formatter** | `ثعبان نسّق file.apy` | Auto-format: indentation, spacing, comment style |
| **Linter** | `ثعبان راجع file.apy` | Diagnostics: W001-W004, E001, I001 |
| **Jupyter kernel** | `pip install -e ".[kernel]"` | Run `.apy` notebooks in Jupyter |
| **VS Code extension** | `editors/vscode/` | Syntax highlighting for `.apy` files |

---

## Public Python API

```python
from arabicpython import (
    install,                       # install the .apy import hook
    uninstall,
    run_repl,                      # start the interactive REPL
    install_excepthook,            # route uncaught exceptions through the translator
    uninstall_excepthook,
    format_translated_exception,   # format a (type, value, tb) triple as Arabic
)
from arabicpython.formatter import format_source, format_file
from arabicpython.linter import lint_source, Diagnostic
```

---

## Project structure

```
lughat-althuban/
├── arabicpython/              The transpiler package
│   ├── aliases/               TOML alias mappings (40+ modules)
│   ├── formatter.py           Auto-formatter
│   └── linter.py              Linter / diagnostic engine
├── arabicpython_kernel/       Jupyter kernel package
├── editors/vscode/            VS Code extension
├── tools/                     Grammar generator and dev utilities
├── decisions/                 ADRs — architectural decisions
├── dictionaries/              ar-v1 keyword/built-in reference
├── specs/                     Spec packets for implementation
├── tests/                     pytest suite (2510 passing, 45 skipped)
├── examples/                  Runnable .apy programs
├── docs/
│   ├── ar/                    Arabic documentation
│   └── wiki/                  Full reference wiki
└── apps/                      Showcase applications
```

---

## Architecture

Source goes through `pretokenize` (Arabic numerals → ASCII, punctuation aliasing, bidi-control rejection) → Python's `tokenize` → a NAME-rewriter consulting the canonical Arabic→Python dictionary → `untokenize` → `compile` → `exec`. No AST rewrite, no CPython fork. The same pipeline backs every entry surface (CLI, REPL, import hook).

Key decisions: [`decisions/0001-architecture.md`](decisions/0001-architecture.md) | [`decisions/0004-normalization-policy.md`](decisions/0004-normalization-policy.md)

**Normalization rules**: `أ/إ/آ → ا`, final `ة → ه`, final `ى → ي`. All TOML keys must survive `normalize_identifier()`.

---

## Development model

- **Planner (Claude)**: writes ADRs, curates dictionaries, authors spec packets, reviews diffs.
- **Implementer**: reads packets in `specs/NNNN-*.md`, writes code, runs tests.

Every implementation unit is a self-contained spec packet. See [`specs/0000-template.md`](specs/0000-template.md) and [`specs/INDEX.md`](specs/INDEX.md).

---

## Known limitations

- **`from . import x` in package `__init__.apy`** — workaround: `import pkg.sub as sub`.
- **Cross-language attribute access from `.py` to `.apy`** must use the ADR-0004-normalized identifier form (e.g., `module.قيمه`, not `module.قيمة`).

---

## Roadmap

| Phase | Content | Status |
|---|---|---|
| 0 | Design decisions (8 ADRs) | ✅ complete |
| A | Core dialect: pretokenize, normalize, translate, CLI, REPL, import hook, tracebacks | ✅ complete |
| B | Ecosystem: 40+ alias modules, formatter, linter, Jupyter kernel, VS Code, tutorial, cookbook | 🟡 **substantially complete — contributors welcome** |
| C | Advanced: package manager integration, LSP server, web playground | 📋 planned |

See [`ROADMAP-PHASE-B.md`](ROADMAP-PHASE-B.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## Acknowledgements

- **zhpy** (gasolin, 2014) — the tokenize-based Chinese Python dialect this project is architecturally modeled on.
- **Ramsey Nasser's قلب (Qalb)** — the critique this project takes seriously.
- **Hedy** — proof that gradual-syntax, multilingual Python-like education works at scale.
- **Siwar / KSAA** — Arabic lexicon API used for terminology research.
