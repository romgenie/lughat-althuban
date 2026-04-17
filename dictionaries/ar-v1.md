# Arabic dialect dictionary — ar-v1.0

**Status**: draft (Packet 0001)
**Locked**: pending review
**Supersedes**: none
**Governance**: changes to existing entries require a new ADR (see ADR 0003).

---

## Reading this file

- **Python**: the Python symbol this entry translates.
- **Canonical**: the single Arabic word or underscored phrase the dialect accepts in v1.
- **Alternates considered**: other Arabic words that are defensible; documented for transparency, **not accepted at runtime**.
- **Rationale**: why this canonical was chosen.

Every canonical entry is written in a form that is idempotent under the ADR 0004 normalizer (no harakat, no tatweel, no hamza variants that fold). Loading code applies the normalizer once on the way in and once on each identifier at lookup time.

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
| `if` | إذا | لو، اذا | MSA conditional "if". |
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
| `False` | خطا | باطل، كاذب | Semantic literal "incorrect"; Hedy uses صحيح/خطأ pair. Hamza in خطأ folds to ا per ADR 0004, stored as خطا. |
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
| `any` | اي | — | MSA "any" (stored without hamza per normalizer). |
| `ascii` | ايسكي | — | Transliteration. |
| `bin` | ثنائي | — | MSA "binary". |
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
| `filter` | صف | فلتر | MSA "filter/refine". |
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
| `max` | الاكبر | اكبر | MSA "maximum". |
| `min` | الاصغر | اصغر | MSA "minimum". |
| `next` | التالي | — | MSA "next". |
| `oct` | ثماني | — | MSA "octal". |
| `open` | افتح | — | MSA "open". |
| `ord` | قيمة_رمز | — | Composed: "value of symbol"; pairs with chr. |
| `pow` | اس | — | MSA "power/exponent" (short mathematical form). |
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
| `super` | الاصل | الاب | MSA "origin/parent"; matches OOP inheritance metaphor. |
| `vars` | متغيرات | — | MSA "variables". |
| `zip` | ازدوج | دمج | MSA "pair up". |

Type-constructor duplicates (also function and type, but listed once above): `bool`, `bytearray`, `bytes`, `complex`, `dict`, `float`, `frozenset`, `int`, `list`, `object`, `range`, `set`, `str`, `tuple`, `type`.

## 5. Built-in exceptions

| Python | Canonical | Alternates | Rationale |
|---|---|---|---|
| `ArithmeticError` | خطا_حسابي | — | Composed. |
| `AssertionError` | خطا_تاكيد | — | Composed (tashkeel stripped per normalizer). |
| `AttributeError` | خطا_صفة | — | Composed. |
| `BaseException` | استثناء_اساسي | — | Composed. |
| `ConnectionError` | خطا_اتصال | — | Composed. |
| `EOFError` | خطا_نهاية_ملف | — | Composed. |
| `Exception` | استثناء | — | MSA "exception". |
| `FileExistsError` | خطا_ملف_موجود | — | Composed. |
| `FileNotFoundError` | خطا_ملف_مفقود | — | Composed. |
| `FloatingPointError` | خطا_عشري | — | Composed. |
| `GeneratorExit` | خروج_مولد | — | Composed. |
| `ImportError` | خطا_استيراد | — | Composed. |
| `IndentationError` | خطا_ازاحة | — | Composed. |
| `IndexError` | خطا_فهرس | — | Composed. |
| `IOError` | خطا_ادخال_اخراج | — | Composed. |
| `KeyboardInterrupt` | مقاطعة | — | MSA "interruption"; simplest form. |
| `KeyError` | خطا_مفتاح | — | Composed. |
| `LookupError` | خطا_بحث | — | Composed. |
| `MemoryError` | خطا_ذاكرة | — | Composed. |
| `ModuleNotFoundError` | خطا_وحدة_مفقودة | — | Composed. |
| `NameError` | خطا_اسم | — | Composed. |
| `NotImplementedError` | خطا_غير_منفذ | — | Composed. |
| `OSError` | خطا_نظام | — | Composed. |
| `OverflowError` | خطا_فائض | — | Composed. |
| `PermissionError` | خطا_صلاحية | — | Composed. |
| `RecursionError` | خطا_تكرار_ذاتي | — | Composed. |
| `RuntimeError` | خطا_تشغيل | — | Composed. |
| `StopIteration` | انتهاء_التكرار | — | Composed. |
| `SyntaxError` | خطا_صياغة | — | Composed. |
| `SystemError` | خطا_نظام_داخلي | — | Composed. |
| `SystemExit` | خروج_نظام | — | Composed. |
| `TabError` | خطا_جدولة | — | Composed. |
| `TimeoutError` | خطا_انتهاء_وقت | — | Composed. |
| `TypeError` | خطا_نوع | — | Composed. |
| `UnicodeDecodeError` | خطا_فك_يونيكود | — | Composed. |
| `UnicodeEncodeError` | خطا_ترميز_يونيكود | — | Composed. |
| `UnicodeError` | خطا_يونيكود | — | Composed. |
| `ValueError` | خطا_قيمة | — | Composed. |
| `Warning` | تحذير | — | MSA "warning". |
| `ZeroDivisionError` | خطا_قسمة_صفر | — | Composed. |

## 6. Common methods on built-in types

Methods are stored without the leading dot in the machine-readable dictionary. The translation happens at the token level; the dot before a method call is a separate `OP` token and is preserved.

### String methods

| Python | Canonical | Alternates | Rationale |
|---|---|---|---|
| `.count` | عد | — | MSA "count". |
| `.decode` | فك_رمز | — | Composed: "decode". |
| `.encode` | رمز | — | MSA "encode"; collision with `chr`'s رمز is fine — both are token-level NAME lookups. |
| `.endswith` | ينتهي_بـ | — | Composed: "ends with". |
| `.find` | ابحث | — | MSA "find/search". |
| `.format` | نسق | — | Same as built-in `format`. |
| `.join` | اجمع | — | MSA "join/collect". |
| `.lower` | صغير | — | MSA "small/lowercase". |
| `.replace` | استبدل | — | MSA "replace". |
| `.split` | قسم | — | MSA "split/divide". |
| `.startswith` | يبدا_بـ | — | Composed: "starts with". |
| `.strip` | جرد | نظف | MSA "strip". |
| `.upper` | كبير | — | MSA "big/uppercase". |

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
| `.setdefault` | عين_افتراضي | — | Composed. |
| `.update` | حدث | — | MSA "update". |
| `.values` | قيم | — | MSA "values". |

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

- `.encode` → `رمز_بايتات` (was رمز)
- `.values` → `قيم_القاموس` (was قيم)
- `filter` → `فلتر` (was صف)

These three renames supersede the entries above. When this file is consumed by Packet 1.2, the resolved names are used.

---

## Counts

- Keywords: 36 hard + 4 soft = 40
- Literals: 3 (in keywords section above)
- Built-in types: 15
- Built-in functions: 51 (unique; excludes type-constructor duplicates)
- Built-in exceptions: 40
- Methods: 29
- **Total entries: 175**

## Known omissions (v1.1 and later)

- `yield from` — compound keyword, needs multi-token handling.
- `async for`, `async with` — compounds.
- `pattern matching` class patterns — limited use in beginner code.
- Dunder methods (`__init__`, `__str__`, etc.) — Phase B aliasing concern.
- `self`, `cls` — naming conventions, not syntax.
- Stdlib module-level functions (`os.path.join`, `math.sqrt`, etc.) — Phase B.

## References

- Hedy Arabic translations (source for many canonical choices): https://hedy.org/
- Python 3.13 `keyword.kwlist`: https://docs.python.org/3/library/keyword.html
- Python Built-in Functions: https://docs.python.org/3/library/functions.html
- Python Built-in Exceptions: https://docs.python.org/3/library/exceptions.html
- ADR 0003 (governance), ADR 0004 (normalization).
