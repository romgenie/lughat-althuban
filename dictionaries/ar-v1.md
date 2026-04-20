# Arabic dialect dictionary — ar-v1.0

**Status**: locked (ar-v1.0)
**Locked**: 2026-04-19 per ADR 0008 § B.0 (Phase B charter freezes ar-v1)
**Supersedes**: none
**Governance**: changes to existing entries require a new ADR (see ADR 0003). The dictionary is now frozen for the lifetime of Phase A; subsequent dictionary versions (`ar-v2`, etc.) require a superseding ADR per ADR 0008 § B.0.

---

## Reading this file

- **Python**: the Python symbol this entry translates.
- **Canonical**: the single Arabic word or underscored phrase the dialect accepts in v1.
- **Alternates considered**: other Arabic words that are defensible; documented for transparency, **not accepted at runtime**.
- **Rationale**: why this canonical was chosen.

Every canonical entry is shown in its **natural visible form** — the spelling a learner would type and that appears in IDE tooltips and error messages. The ADR 0004 normalizer folds hamza variants (`أ`/`إ`/`آ` → `ا`), ta-marbuta (`ة` → `ه`), harakat, and tatweel on both the dictionary entry and the user's identifier at lookup time, so `خطأ` and `خطا` resolve to the same key at runtime. Where a rationale note references the stored (normalized) form, it is marked explicitly.

Multi-word translations use underscore `_` rather than space, because Python tokenizes space as a token boundary. Dotted method names are written with a leading `.` in this file for clarity but are stored without the dot in the machine-readable dictionary.

---

## 1. Control-flow keywords

| Python | Canonical | Alternates | Rationale |
|---|---|---|---|
| `and` | و | — | MSA conjunction "and". |
| `as` | كـ | باسم | Arabic prefix meaning "as"; natural in `import X as Y`. |
| `assert` | أكد | تحقق | MSA "affirm/assert". |
| `async` | غير_متزامن | لاتزامني | MSA "non-synchronous"; composed for clarity. |
| `await` | انتظر | — | MSA "wait". |
| `break` | اكسر | توقف، اقطع | MSA direct cognate; matches the "break out of loop" metaphor. |
| `class` | صنف | فئة، طبقة | Matches Hedy; MSA for "kind/category" is more established in CS translation than alternatives. |
| `continue` | استمر | تابع، واصل | MSA "continue". |
| `def` | دالة | عرف، تعريف | MSA mathematical standard for "function"; Hedy uses this. |
| `del` | احذف | امسح | MSA "delete". |
| `elif` | وإلا_إذا | وإذا | Composed from else + if; matches natural Arabic construction. |
| `else` | وإلا | والا | MSA "otherwise"; Hedy uses this. |
| `except` | استثناء | التقط | MSA noun form of "exception"; reads naturally in `try/except`. |
| `finally` | أخيرا | نهاية | MSA "at last / finally". |
| `for` | لكل | من_أجل | "For each" idiom in MSA; concise. |
| `from` | من | — | MSA preposition "from". |
| `global` | عام | عالمي | MSA "public/general"; avoid عالمي which means "global as in worldwide". |
| `if` | إذا | لو، إذا | MSA conditional "if". |
| `import` | استورد | اجلب، ادرج | MSA "import". |
| `in` | في | — | MSA preposition "in". |
| `is` | هو | يكون | MSA copula "is/he". |
| `lambda` | لامدا | دالة_مجهولة | Transliteration; standard in Arabic mathematics for lambda. |
| `nonlocal` | غير_محلي | — | Composed MSA. |
| `not` | ليس | لا | MSA negation; ليس reads as a formal "not". |
| `or` | أو | — | MSA disjunction "or". |
| `pass` | مرر | تجاوز | MSA "pass through". |
| `raise` | ارفع | اطلق | MSA "raise"; matches Python's metaphor. |
| `return` | ارجع | أرجع، اعد | MSA "return/go back"; without hamza variants for normalizer idempotency. |
| `try` | حاول | جرب | MSA "try/attempt". |
| `while` | طالما | بينما | MSA "as long as". |
| `with` | مع | — | MSA "with". |
| `yield` | سلم | انتج | MSA "hand over"; semantically closer to generator `yield` than "produce". |

### Soft keywords

| Python | Canonical | Alternates | Rationale |
|---|---|---|---|
| `match` | طابق | — | MSA "match/compare". |
| `case` | حالة | — | MSA "case". |
| `type` | نوع | — | MSA "type"; shared with built-in `type()`. |
| `_` | _ | — | Underscore is universal; no translation. |

## 2. Literal keywords

| Python | Canonical | Alternates | Rationale |
|---|---|---|---|
| `False` | خطأ | باطل، كاذب | Semantic literal "incorrect"; Hedy uses صحيح/خطأ pair. Shown in visible form `خطأ`; normalizer folds final hamza to give stored key `خطا` per ADR 0004. |
| `None` | لاشيء | عدم، فراغ | Literal "nothing"; closest to `None` semantically. |
| `True` | صحيح | حق | Semantic literal "correct"; Hedy uses. |

## 3. Built-in types

| Python | Canonical | Alternates | Rationale |
|---|---|---|---|
| `bool` | منطقي | — | MSA "logical/boolean". |
| `bytearray` | مصفوفة_بايتات | — | Composed: "array of bytes". |
| `bytes` | بايتات | ثنائيات | Transliteration; standard in Arabic technical writing. |
| `complex` | عدد_مركب | — | MSA "complex number" (mathematical). |
| `dict` | قاموس | — | MSA "dictionary". |
| `float` | عدد_عشري | عشري | MSA "decimal number". |
| `frozenset` | مجموعة_ثابتة | — | Composed: "frozen set". |
| `int` | عدد_صحيح | صحيح | MSA "integer"; avoids collision with True literal. |
| `list` | قائمة | — | MSA "list". |
| `object` | كائن | شيء | MSA "object"; established in Arabic OOP translation. |
| `range` | نطاق | مدى | MSA "range/span". |
| `set` | مجموعة | — | MSA "set" (mathematical usage). |
| `str` | نص | سلسلة، سلسلة_نصية | MSA "text"; simpler than "string" and widely used. |
| `tuple` | صف | ثنائية، طقم | MSA "row/series"; matches ordered-tuple concept. |
| `type` | نوع | — | See soft keywords. |

## 4. Built-in functions

| Python | Canonical | Alternates | Rationale |
|---|---|---|---|
| `abs` | مطلق | — | MSA "absolute". |
| `all` | كل | — | MSA "all". |
| `any` | أي | — | MSA "any"; normalizer folds hamza to give stored key `اي` per ADR 0004. |
| `ascii` | أيسكي | — | Transliteration. |
| `bin` | ثنائي | — | MSA "binary". |
| `breakpoint` | نقطة_توقف | — | Composed: "stopping point"; matches the debugger metaphor. |
| `callable` | قابل_للاستدعاء | — | MSA "callable". |
| `chr` | رمز | حرف | MSA "symbol"; `.ord` counterpart is قيمة_رمز. |
| `classmethod` | تابع_صنف | — | Composed: "method of class". |
| `compile` | ترجم | جمع | MSA "translate/compile". |
| `delattr` | احذف_صفة | — | Composed: "delete attribute". |
| `dir` | محتويات | — | MSA "contents"; reads naturally for object inspection. |
| `divmod` | قسمة_باقي | — | Composed: "division and remainder". |
| `enumerate` | رقم | عدد، عدد_متسلسل | MSA "number"; short and clear. |
| `eval` | قيم | — | MSA "evaluate". |
| `exec` | نفذ | — | MSA "execute". |
| `filter` | فلتر | صف | Transliteration; `صف` would collide with `tuple`. See collision audit. |
| `format` | نسق | — | MSA "format". |
| `getattr` | اجلب_صفة | — | Composed: "fetch attribute". |
| `globals` | متغيرات_عامة | عامات | Composed for clarity. |
| `hasattr` | يملك_صفة | — | Composed: "owns attribute". |
| `hash` | بصمة | تجزئة | MSA "fingerprint/signature"; semantic. |
| `help` | مساعدة | ساعد | MSA "help". |
| `hex` | ست_عشري | — | MSA "hexadecimal". |
| `id` | معرف | — | MSA "identifier". |
| `input` | ادخل | اقرا | MSA "enter"; reads as an imperative. |
| `isinstance` | من_نوع | — | Composed: "is of type". |
| `issubclass` | صنف_فرعي | — | MSA "subclass". |
| `iter` | كرر | — | MSA "iterate". |
| `len` | طول | — | MSA "length". |
| `locals` | متغيرات_محلية | محلات | Composed for clarity. |
| `map` | طبق | — | MSA "apply"; closer to functional map than alternatives. |
| `max` | الأكبر | أكبر | MSA "maximum". |
| `min` | الأصغر | أصغر | MSA "minimum". |
| `next` | التالي | — | MSA "next". |
| `oct` | ثماني | — | MSA "octal". |
| `open` | افتح | — | MSA "open". |
| `ord` | قيمة_رمز | — | Composed: "value of symbol"; pairs with chr. |
| `pow` | أس | — | MSA "power/exponent" (short mathematical form). |
| `print` | اطبع | — | MSA "print"; Hedy uses. |
| `property` | خاصية | — | MSA "property/attribute". |
| `repr` | تمثيل | — | MSA "representation". |
| `reversed` | معكوس | — | MSA "reversed". |
| `round` | قرب | دور | MSA "approximate". |
| `setattr` | عين_صفة | — | Composed: "set attribute". |
| `slice` | شريحة | — | MSA "slice". |
| `sorted` | مرتب | — | MSA "sorted". |
| `staticmethod` | تابع_ثابت | — | Composed: "static method". |
| `sum` | مجموع | — | MSA "sum". |
| `super` | الأصل | الأب | MSA "origin/parent"; matches OOP inheritance metaphor. |
| `vars` | متغيرات | — | MSA "variables". |
| `zip` | ازدوج | دمج | MSA "pair up". |

Type-constructor duplicates (also function and type, but listed once above): `bool`, `bytearray`, `bytes`, `complex`, `dict`, `float`, `frozenset`, `int`, `list`, `object`, `range`, `set`, `str`, `tuple`, `type`.

## 5. Built-in exceptions

| Python | Canonical | Alternates | Rationale |
|---|---|---|---|
| `ArithmeticError` | خطأ_حسابي | — | Composed. |
| `AssertionError` | خطأ_تأكيد | — | Composed. |
| `AttributeError` | خطأ_صفة | — | Composed. |
| `BaseException` | استثناء_أساسي | — | Composed. |
| `ConnectionError` | خطأ_اتصال | — | Composed. |
| `EOFError` | خطأ_نهاية_ملف | — | Composed. |
| `Exception` | استثناء_عام | استثناء | "general exception"; `استثناء` alone collides with the `except` keyword (same name in MSA). Parallels `BaseException` → `استثناء_أساسي`. |
| `FileExistsError` | خطأ_ملف_موجود | — | Composed. |
| `FileNotFoundError` | خطأ_ملف_مفقود | — | Composed. |
| `FloatingPointError` | خطأ_عشري | — | Composed. |
| `GeneratorExit` | خروج_مولد | — | Composed. |
| `ImportError` | خطأ_استيراد | — | Composed. |
| `IndentationError` | خطأ_إزاحة | — | Composed. |
| `IndexError` | خطأ_فهرس | — | Composed. |
| `IOError` | خطأ_إدخال_إخراج | — | Composed. |
| `KeyboardInterrupt` | مقاطعة | — | MSA "interruption"; simplest form. |
| `KeyError` | خطأ_مفتاح | — | Composed. |
| `LookupError` | خطأ_بحث | — | Composed. |
| `MemoryError` | خطأ_ذاكرة | — | Composed. |
| `ModuleNotFoundError` | خطأ_وحدة_مفقودة | — | Composed. |
| `NameError` | خطأ_اسم | — | Composed. |
| `NotImplementedError` | خطأ_غير_منفذ | — | Composed. |
| `OSError` | خطأ_نظام | — | Composed. |
| `OverflowError` | خطأ_فائض | — | Composed. |
| `PermissionError` | خطأ_صلاحية | — | Composed. |
| `RecursionError` | خطأ_تكرار_ذاتي | — | Composed. |
| `RuntimeError` | خطأ_تشغيل | — | Composed. |
| `StopIteration` | انتهاء_التكرار | — | Composed. |
| `SyntaxError` | خطأ_صياغة | — | Composed. |
| `SystemError` | خطأ_نظام_داخلي | — | Composed. |
| `SystemExit` | خروج_نظام | — | Composed. |
| `TabError` | خطأ_جدولة | — | Composed. |
| `TimeoutError` | خطأ_انتهاء_وقت | — | Composed. |
| `TypeError` | خطأ_نوع | — | Composed. |
| `UnicodeDecodeError` | خطأ_فك_يونيكود | — | Composed. |
| `UnicodeEncodeError` | خطأ_ترميز_يونيكود | — | Composed. |
| `UnicodeError` | خطأ_يونيكود | — | Composed. |
| `ValueError` | خطأ_قيمة | — | Composed. |
| `Warning` | تحذير | — | MSA "warning". |
| `ZeroDivisionError` | خطأ_قسمة_صفر | — | Composed. |

## 6. Common methods on built-in types

Methods are stored without the leading dot in the machine-readable dictionary. The translation happens at the token level; the dot before a method call is a separate `OP` token and is preserved.

### String methods

| Python | Canonical | Alternates | Rationale |
|---|---|---|---|
| `.count` | عد | — | MSA "count". |
| `.decode` | فك_رمز | — | Composed: "decode". |
| `.encode` | رمز_بايتات | رمز | Composed; `رمز` alone would collide with `chr`. See collision audit. |
| `.endswith` | ينتهي_بـ | — | Composed: "ends with". |
| `.find` | ابحث | — | MSA "find/search". |
| `.format` | نسق | — | Same as built-in `format`. |
| `.join` | اجمع | — | MSA "join/collect". |
| `.lower` | صغير | — | MSA "small/lowercase". |
| `.replace` | استبدل | — | MSA "replace". |
| `.split` | قسم | — | MSA "split/divide". |
| `.startswith` | يبدأ_بـ | — | Composed: "starts with". |
| `.capitalize` | كبر_الأول | — | Composed: "capitalize the first (letter)". |
| `.center` | توسط | — | MSA "be in the center"; pads to center the string. |
| `.ljust` | ضبط_يسار | — | Composed: "left-align". |
| `.rjust` | ضبط_يمين | — | Composed: "right-align". |
| `.strip` | جرد | نظف | MSA "strip". |
| `.swapcase` | عكس_الحالة | — | Composed: "reverse/swap case". |
| `.title` | عنوان | — | MSA "title/heading"; title-cases every word. |
| `.upper` | كبير | — | MSA "big/uppercase". |
| `.zfill` | مل_بأصفار | — | Composed: "fill with zeros". |

### List methods

| Python | Canonical | Alternates | Rationale |
|---|---|---|---|
| `.append` | اضف | الحق | MSA "add". |
| `.extend` | مدد | — | MSA "extend". |
| `.index` | موقع | — | MSA "position". |
| `.insert` | ادرج | — | MSA "insert". |
| `.pop` | انتزع | — | MSA "extract". |
| `.remove` | ازل | — | MSA "remove". |
| `.reverse` | اعكس | — | MSA "reverse" (imperative). |
| `.sort` | رتب | — | MSA "arrange/sort". |

### Dict methods

| Python | Canonical | Alternates | Rationale |
|---|---|---|---|
| `.get` | اجلب | — | MSA "fetch". |
| `.items` | عناصر | — | MSA "items/elements". |
| `.keys` | مفاتيح | — | MSA "keys". |
| `.pop` | انتزع | — | Same Python name as list `.pop`; the existing `انتزع → pop` mapping covers dicts automatically. No new entry needed — documented here for completeness. |
| `.popitem` | انتزع_زوج | — | Composed: "extract a pair" (dict items are key-value pairs). |
| `.setdefault` | عين_افتراضي | — | Composed. |
| `.update` | حدث | — | MSA "update". |
| `.values` | قيم_القاموس | قيم | Composed; `قيم` alone would collide with `eval`. See collision audit. |

### Set methods

`.remove`, `.clear`, and `.copy` already work on sets via the list and generic method mappings above (same Python names, same Arabic translations).

| Python | Canonical | Alternates | Rationale |
|---|---|---|---|
| `.add` | ضم | — | MSA "include/incorporate"; distinct from `اضف` (list `.append`) to avoid attribute collision. |
| `.difference` | فرق | — | MSA mathematical "difference" (A minus B). |
| `.discard` | أسقط | — | MSA "drop/set aside"; like `.remove` but no error if element absent. |
| `.intersection` | تقاطع | — | MSA mathematical "intersection". |
| `.union` | اتحاد | — | MSA mathematical "union". |

### Generic methods (on multiple types)

| Python | Canonical | Alternates | Rationale |
|---|---|---|---|
| `.clear` | امسح | — | MSA "clear/erase". |
| `.copy` | انسخ | — | MSA "copy". |

---

## Collision audit

The following canonicals appear in more than one section and must resolve to the same English symbol at runtime:

| Arabic | Maps to (Python) | Notes |
|---|---|---|
| نسق | `format` (function and `.format` method) | Same target — safe. |
| رمز | `chr` (function) and `.encode` (method) | **Conflict**. Since both are NAME tokens, the token-level rewrite cannot distinguish them. Resolution: `chr` keeps رمز; `.encode` uses رمّز (with shadda). But shadda is stripped by normalizer. **Decision**: rename `.encode` to `رمز_بايتات` in v1. Documented here; will verify during Packet 1.2. |
| قيم | `eval` (function) and `.values` (method) | **Conflict**. Resolution: `eval` keeps قيم; `.values` renamed to `قيم_القاموس`. Applied below. |
| اجلب | `.get` (method) and `getattr` (function) | `getattr` uses اجلب_صفة already; `.get` uses اجلب. Safe. |
| عين_صفة | `setattr` (function) only | Safe. |
| نوع | `type` (function/soft-keyword) | Intentional merge. |
| صف | `tuple` (type) and `filter` (function) | **Conflict**. Resolution: `filter` renamed to `فلتر`. Applied below. |

### Resolutions applied

The three collisions above are resolved **inline in the tables** — `filter`, `.encode`, and `.values` now use their resolved canonicals (`فلتر`, `رمز_بايتات`, `قيم_القاموس`) in their respective sections. The rejected forms (`صف`, `رمز`, `قيم`) are listed as alternates for the audit trail.

The loader reads only the tables; this audit section is historical documentation.

---

## Counts

These match what `dialect.load_dialect("ar-v1")` reports at runtime
(`names: 145, attributes: 42, total: 187`).

- Hard keywords: 32 (Python 3.13's `keyword.kwlist` minus `True`/`False`/`None`, which live in *Literals* below)
- Soft keywords: 4 (`match`, `case`, `type`, `_`)
- Literals: 3 (`True`, `False`, `None`)
- Built-in types: 15
- Built-in functions: 52 (unique; excludes type-constructor duplicates; includes `breakpoint` added in v1.1)
- Built-in exceptions: 40
- Subtotal (names): **145** — sums to 146 by section, minus 1 for the `type` soft-keyword / `type` built-in-type dedup (both map to `نوع`, stored once in `dialect.names`)
- Methods (attributes): 42 (29 original + 7 new string methods + 5 new set methods + 1 new dict method)
- **Total entries: 187**

*Note: dict `.pop` is not counted as a new attribute — it resolves via the existing `انتزع → pop` mapping shared with list `.pop`.*

## Known omissions

- `yield from` — compound keyword, needs multi-token handling.
- `async for`, `async with` — compounds.
- `pattern matching` class patterns — limited use in beginner code.
- `aiter`, `anext` — async iterator builtins (3.10+); deferred to Phase B.
- Dunder methods (`__init__`, `__str__`, etc.) — Phase B aliasing concern.
- `self`, `cls` — naming conventions, not syntax.
- Stdlib module-level functions (`os.path.join`, `math.sqrt`, etc.) — Phase B.
- Set methods `.issubset`, `.issuperset`, `.symmetric_difference` — advanced; deferred to ar-v2.
- String methods `.encode`, `.format_map`, `.maketrans`, `.translate` — advanced; deferred to ar-v2.

## References

- Hedy Arabic translations (source for many canonical choices): https://hedy.org/
- Python 3.13 `keyword.kwlist`: https://docs.python.org/3/library/keyword.html
- Python Built-in Functions: https://docs.python.org/3/library/functions.html
- Python Built-in Exceptions: https://docs.python.org/3/library/exceptions.html
- ADR 0003 (governance), ADR 0004 (normalization).
