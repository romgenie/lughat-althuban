# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Tooling & third-party aliases (B-053 through B-059)

Test suite: **2386 passing, 21 skipped**.

#### B-059 — aiohttp (`طلبات_غير_متزامنه`)

22 entries covering `ClientSession` (`جلسه_غير_متزامنه`), `ClientTimeout` (`مهله_عميل`),
`TCPConnector`, `BasicAuth`, `FormData`, `StreamReader`, web-server helpers
(`web.Application`, `web.run_app`, `web.Response`, `web.json_response`),
`WebSocketResponse`, and all client error/exception classes.
Demo: `examples/B59_aiohttp_demo.apy`.

#### B-058 — scipy (`علوم_حسابيه`)

17 entries mapping scipy's major submodule namespaces: `احصاء_متقدم` (stats),
`تحسين` (optimize), `تكامل` (integrate), `جبر_خطي` (linalg), `استيفاء`
(interpolate), `تحويل_فوريه` (fft), `معالجه_اشارات` (signal), `مصفوفات_مبعثره`
(sparse), `هندسه_فضائيه` (spatial), `دالات_خاصه` (special), `ثوابت` (constants).
Demo: `examples/B58_scipy_demo.apy`.

#### B-057 — seaborn (`رسوم_احصائيه`)

38 entries: full coverage of relational (`خط_بياني`, `مخطط_نقاط`), distribution
(`توزيع_بيانات`, `كثافه_احتماليه`, `توزيع_تراكمي`), categorical (`مخطط_شريطي`,
`مخطط_صندوقي`, `مخطط_كمان`, `مخطط_سرب`), matrix (`خريطه_حراره`), multi-plot grids,
theming (`ضبط_موضوع`, `احضر_لوحه`), and dataset helpers (`حمل_بيانات`).
Demo: `examples/B57_seaborn_demo.apy`.

#### B-056 — Linter (`ثعبان راجع`)

`arabicpython/linter.py` — static analysis for `.apy` files.
Codes: W001 (line length), W002 (trailing whitespace), W003 (tab indent),
W004 (mixed Arabic/Latin identifier), E001 (ar-v1 keyword in ar-v2 file),
I001 (no module intro). CLI: `ثعبان راجع [--select CODES] [--no-info] FILE…`.
23 tests. Demo: `examples/B56_linter_demo.apy`.

#### B-055 — Formatter (`ثعبان نسّق`)

`arabicpython/formatter.py` — deterministic source formatter for `.apy` files.
Fixes: tab→space indentation, trailing whitespace, blank-line collapse (≤2),
comment spacing (`#comment` → `# comment`), comma spacing.
CLI: `ثعبان نسّق [--check] FILE…`. Idempotent. 22 tests.
Demo: `examples/B55_formatter_demo.apy`.

#### B-054 — Jupyter Kernel

`arabicpython_kernel/` package — `ArabicPythonKernel` extends `IPythonKernel`.
Translates Arabic Python in `do_execute` before execution; Arabic tab-completion
for keywords and alias module names; `__main__.py` installer
(`python -m arabicpython_kernel install`). Optional dep group: `pip install apython[kernel]`.
17 structural tests (no live Jupyter required). Language: `apy`, extension: `.apy`.

#### B-053 — VSCode Extension

`editors/vscode/` — full VSCode language extension for `.apy` files.
Ships: `package.json` (language contribution, grammar, LSP config),
`extension.js` (LanguageClient wrapping `ثعبان خادم`, status-bar item),
`language-config.json` (brackets, Arabic wordPattern, indentation rules),
`syntaxes/apy.tmLanguage.json` (TextMate grammar — 12 repository rules,
500+ Arabic keywords/builtins). Generator: `tools/generate_vscode_grammar.py`.
51 structural tests.

### Phase B — stdlib aliases (B-030 through B-038)

All modules import via Arabic names and expose curated Arabic attribute aliases.
Every batch ships with a TOML mapping, test file, cross-consistency test (no
Arabic key collisions with earlier batches), demo `.apy` file, and snapshot.
CI matrix: ubuntu / macOS / windows × Python 3.11 / 3.12 / 3.13 — **1093 passing**.

#### B-038 — hashlib (`هاشلب`), io (`مجاري`), contextlib (`مدير_سياق`)

- **هاشلب**: 17 entries — `شا256`, `مد5`, `بليك_ب/ص`, `خوارزميات_مضمونه`, `مشتق_مفتاح`, `هاش_ملف`, SHA-3 family.
- **مجاري**: 16 entries — `تيار_نص` (StringIO), `تيار_بايت` (BytesIO), Buffered*/TextIOWrapper, IOBase hierarchy, `ابحث_بدايه/حاليه/نهايه` (SEEK_*).
- **مدير_سياق**: 11 entries — `مدير_سياق_داله` (contextmanager), `اكتم` (suppress), `سياق_فارغ` (nullcontext), ExitStack, redirect_stdout/stderr.

#### B-037 — asyncio (`اتزامن`)

46 entries: `شغل` (run), `تريث` (sleep — uses `تريث` not `نمه` to avoid collision with `وقت_نظام`), `اجمع_مهام` (gather), `انتظر`/`انتظر_من_اجل`, Task/Future/TaskGroup, Lock/Queue/Semaphore/Barrier, `مهله` (timeout), coroutine checks, event-loop helpers.

Note: `حلقه_احداث` maps to `AbstractEventLoop` (not `EventLoop` which is Python 3.13-only).

#### B-036 — logging (`تسجيل`)

41 entries: level constants (`مستوى_تصحيح`/`مستوى_خطا`/…), logger functions, `احضر_مسجل` (getLogger), Handler/Formatter (`منسق_سجل`)/Filter class aliases, StreamHandler/FileHandler/NullHandler.

#### B-035 — math (`رياضيات`), statistics (`احصاء`), random (`عشوائيات`)

- **رياضيات**: 41 entries — `باي`, `جذر`, `مصنوعيه` (factorial), `قاسم_مشترك` (gcd), trig functions (جيب/جيب_تمام/ظل), `توليفه`/`تباديل_عدد` (comb/perm).
- **احصاء**: 21 entries — `وسط` (mean), `وسيط` (median), `منوال` (mode), `انحراف` (stdev), `توزيع_طبيعي` (NormalDist).
- **عشوائيات**: 21 entries — `عشوائي` (random), `عدد_عشوائي` (randint), `اختر` (choice), `خلط` (shuffle), `ابذر` (seed). Uses `بايتات_عشوائيه_عدد` for `randbytes` (avoids collision with `os.urandom`).

#### B-034 — re (`تعابير_نمطيه`), string (`نصوص`), textwrap (`تنسيق_نص`)

- **تعابير_نمطيه**: 33 entries — `رجم` (compile), `طابق` (match), `ابحث` (search), `عوض` (sub — uses `عوض` not `استبدل` to avoid dialect `.replace` collision), `خطا_نمط` maps to `re.error` (not `PatternError` which is Python 3.13-only), Pattern/Match unbound methods.
- **نصوص**: 14 entries — Template/Formatter class aliases, `بديل_امن` (safe_substitute).
- **تنسيق_نص**: 8 entries — `التف` (wrap), `امل` (fill), `اختصر` (shorten), TextWrapper class.

#### B-033 — json (`جيسون`), csv (`ملفات_csv`), sqlite3 (`قاعدة_بيانات`)

- **جيسون**: 10 entries — `نص` (dumps), `من_نص` (loads), `حفظ`/`تحميل` (dump/load), JSONEncoder/Decoder unbound `رمز`/`فكك`.
- **ملفات_csv**: 17 entries — `قارئ`/`كاتب` (reader/writer), DictReader/DictWriter with `اكتب_سطر`/`اكتب_راس`, QUOTE_* constants.
- **قاعدة_بيانات**: 23 entries — `اتصل` (connect), Connection/Cursor/Row, `نفذ`/`نفذ_عديد`/`ثبت`/`تراجع`/`اغلق`, `اجلب_واحد`/`اجلب_الكل`.

#### B-032 — datetime (`مكتبة_تاريخ`), time (`وقت_نظام`), calendar (`روزنامه`)

#### B-031 — collections (`مجموعات`), itertools (`ادوات_تكرار`), functools (`ادوات_داليه`)

#### B-030 — os (`نظام_تشغيل`), pathlib (`مسار_مكتبه`), sys (`نظام`)

### SDK aliases

- **قارورة** (flask): ~60 entries covering Flask app, routes, request/response, blueprints, error handlers.
- **طلبات** (requests): core HTTP surface — `اجلب`/`ارسل`/`رفع`/`حذف`, Session, Response aliases.

## [0.1.1] — 2026-04-20 — Dictionary rendering + coverage pass

Post-release doc and dictionary improvements. No code changes.

### Changed — dictionaries

- **ar-v1.md rendering convention**: all canonical entries now shown in natural
  visible (pre-normalizer) form. The ADR 0004 normalizer folds on lookup so
  runtime behaviour is unchanged; this is documentation-only. 45 entries
  corrected — primarily `خطا_*` → `خطأ_*` exception names, `اي` → `أي`,
  `الاكبر` → `الأكبر`, `يبدا_بـ` → `يبدأ_بـ`, and similar hamza restorations.

### Added — dictionaries (Category C, no ADR required per ADR 0003)

- `breakpoint` → `نقطة_توقف` (built-in function)
- 7 string methods: `.title عنوان`, `.capitalize كبر_الأول`,
  `.swapcase عكس_الحالة`, `.zfill مل_بأصفار`, `.center توسط`,
  `.ljust ضبط_يسار`, `.rjust ضبط_يمين`
- 5 set methods: `.add ضم`, `.discard أسقط`, `.union اتحاد`,
  `.intersection تقاطع`, `.difference فرق`
  (`.remove` / `.clear` / `.copy` already worked via existing mappings)
- 1 dict method: `.popitem → انتزع_زوج`
  (`.pop` was already covered via the shared `انتزع → pop` mapping)
- `aiter` / `anext` documented as deferred to Phase B in Known omissions

**Updated counts**: 173 → 187 entries (names 144→145, attributes 29→42).

### Added — tests

- 15 new tests in `test_dialect.py` covering all v1.1 additions.
- Count assertions updated to ≥ 187 total / ≥ 42 attributes.
- **Test suite: 351 passing, 21 intentionally skipped.**

## [0.1.0] — 2026-04-19 — Phase A complete

First feature-complete release of the Arabic-keyword Python dialect. Source-to-source preprocessor on top of CPython 3.11+; no fork.

### Added — language pipeline

- **Pretokenize layer** (`arabicpython/pretokenize.py`): Arabic-Indic + Eastern-Arabic digit folding, Arabic punctuation aliasing (`،`/`؛`/`؟`), 12-codepoint bidi-control rejection per UAX #9.
- **Identifier normalization** (`arabicpython/normalize.py`): hamza folding, ta-marbuta→ha, harakat stripping, tatweel removal. Idempotent; `قيمه` and `قيمة` resolve to the same name.
- **Dialect loader** (`arabicpython/dialect.py`): parses `dictionaries/ar-v1.md` directly at load time into frozen name/attribute mappings. 173 entries at Phase A ship (expanded to 187 in v0.1.1).
- **Translate layer** (`arabicpython/translate.py`): tokenize → name-rewrite → untokenize. Includes a Python-3.11-specific f-string-interior rewriter (Packet 0011) that's bypassed on 3.12+ where PEP 701 changed f-string tokenization.
- **`.apy` import hook** (`arabicpython/importer.py`): `sys.meta_path` finder so `.apy` files import each other and `.py` modules transparently in both directions.
- **Interactive REPL** (`arabicpython/repl.py`): multi-line Arabic input with continuation prompts; readline-aware where available.
- **Arabic tracebacks** (`arabicpython/excepthook.py`): 38 exception types and ~30 common interpreter messages translated; unmapped messages pass through.
- **CLI** (`arabicpython/cli.py`): four entry surfaces (file, `-c`, stdin, REPL) mirroring `python`. UTF-8 stdout/stderr forced on Windows.

### Added — content

- **Dictionaries**: `ar-v1.md` (canonical word list, locked at v1.0) and `exceptions-ar-v1.md` (exception subclass hierarchy + interpreter-message translations).
- **Examples**: 7 progressive `.apy` programs covering hello, arithmetic, control flow, functions, data structures, classes, and cross-module imports.
- **Tutorial**: `docs/getting-started-ar.md` covering the eight ADR-0007 ship topics.

### Added — design (ADRs)

- **0001** Architecture: source-to-source preprocessor.
- **0002** File extension: `.apy`.
- **0003** Keyword dictionary governance.
- **0004** Identifier normalization policy.
- **0005** Arabic numerals and punctuation in source.
- **0006** Bidi control character policy *(superseded by 0009 — reject-list portion only)*.
- **0007** Scope: learning dialect first, production replacement second.
- **0008** Phase B charter (freeze ar-v1, module-proxy meta-path finder, B-001 first packet, funding-gate unlocks, 24-month sunset default).
- **0009** Bidi control marks extension (12 codepoints per UAX #9 §7).

### Added — process

- 11 spec packets (0001–0011) tracked in `specs/INDEX.md`, each with paired delivery notes.
- CI matrix: ubuntu / macos / windows × Python 3.11 / 3.12 / 3.13.
- Test suite: 336 passing, 21 intentionally skipped (3.11-specific paths on 3.12+; readline-unavailable on Windows).

### Known limitations (deferred fixups)

- `from . import x` inside `__init__.apy` does not translate; workaround `import pkg.sub as sub`.
- Cross-language attribute access from `.py` to `.apy` requires the ADR-0004-normalized form (e.g., `module.قيمه`, not `module.قيمة`).
- No end-to-end async/await program coverage; keywords translate but real async programs are not exercised by the suite.

## Phase 0 — Design decisions

Initial scaffolding period (pre-Phase A):

- Project scaffolding: README, LICENSE (Apache-2.0), `pyproject.toml`, CI workflow.
- ADRs 0001–0007 establishing architecture, file extension, dictionary governance, normalization policy, numerals/punctuation, bidi policy, and scope.
- Spec packet template for planner→implementer handoff.
