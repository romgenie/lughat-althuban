<div dir="rtl">

# الأمثلة — لغة الثعبان

برامج تعليمية تصاعدية وأمثلة للمرحلتين (أ) و(ب). كل مثال مستقل وقابل للتشغيل مباشرة.

## المرحلة أ — الأساسيات

| الملف | ما يُوضّحه |
|-------|------------|
| [01_hello.apy](01_hello.apy) | `اطبع` والسلاسل النصية |
| [02_arithmetic.apy](02_arithmetic.apy) | المتغيرات والحساب والنصوص المُدرَجة |
| [03_control_flow.apy](03_control_flow.apy) | `لكل` / `في` / `مدى`، `اذا` / `وإلا` |
| [04_functions.apy](04_functions.apy) | `دالة`، القيم الافتراضية، `ارجع` |
| [05_data_structures.apy](05_data_structures.apy) | القوائم والقواميس والتكرار |
| [06_classes.apy](06_classes.apy) | `صنف` مع `__init__` والتوابع |
| [07_imports.apy](07_imports.apy) + [helper.apy](helper.apy) | خطّاف الاستيراد `.apy` |

## المرحلة ب — المكتبات والأدوات

| الملف | ما يُوضّحه |
|-------|------------|
| [B30_filesystem_walk.apy](B30_filesystem_walk.apy) | نظام_تشغيل، مسار_مكتبه |
| [B31_functional_data.apy](B31_functional_data.apy) | ادوات_داليه، ادوات_تكرار |
| [B32_datetime_math.apy](B32_datetime_math.apy) | مكتبة_تاريخ، وقت_نظام |
| [B33_data_storage.apy](B33_data_storage.apy) | جيسون، ملفات_csv، قاعدة_بيانات |
| [B34_text_processing.apy](B34_text_processing.apy) | تعابير_نمطيه |
| [B35_numerics.apy](B35_numerics.apy) | رياضيات، احصاء، عشوائيات |
| [B36_logging_demo.apy](B36_logging_demo.apy) | تسجيل |
| [B37_async_demo.apy](B37_async_demo.apy) | اتزامن، `غير_متزامن`/`انتظر` |
| [B38_utilities_demo.apy](B38_utilities_demo.apy) | هاشلب، مجاري، مدير_سياق |
| [B55_formatter_demo.apy](B55_formatter_demo.apy) | المنسّق التلقائي |
| [B56_linter_demo.apy](B56_linter_demo.apy) | المدقّق |
| [B57_seaborn_demo.apy](B57_seaborn_demo.apy) | رسوم_احصائيه (seaborn) |
| [B58_scipy_demo.apy](B58_scipy_demo.apy) | علوم_حسابيه (scipy) |
| [B59_aiohttp_demo.apy](B59_aiohttp_demo.apy) | طلبات_غير_متزامنه (aiohttp) |

## تطبيقات متكاملة (مجلد apps/)

| الملف | الوصف |
|-------|--------|
| [تحليل_اخبار.apy](../apps/تحليل_اخبار.apy) | تحليل نصي + pandas + matplotlib |
| [خادم_ويب.apy](../apps/خادم_ويب.apy) | REST API كامل بـ Flask |
| [حاسبة_علمية.apy](../apps/حاسبة_علمية.apy) | numpy + scipy + match/case |
| [مدير_مهام.apy](../apps/مدير_مهام.apy) | SQLite + OOP + context managers |

## تشغيل الأمثلة

```bash
ثعبان examples/01_hello.apy
ثعبان examples/B37_async_demo.apy
ثعبان apps/حاسبة_علمية.apy
```

للشرح الكامل لكل مثال بالعربية: [README-ar.md](README-ar.md)

</div>

---

# لغة الثعبان examples

Progressive `.apy` programs demonstrating the full feature surface of Phase A and Phase B.

## Phase A — Core language (01–07)

| File | Demonstrates |
|---|---|
| [01_hello.apy](01_hello.apy) | `print` (`اطبع`) and string literals |
| [02_arithmetic.apy](02_arithmetic.apy) | Variables, integer arithmetic, f-strings |
| [03_control_flow.apy](03_control_flow.apy) | `for`/`in`/`range`, `if`/`else`, modulo |
| [04_functions.apy](04_functions.apy) | `def`, default arguments, `return` |
| [05_data_structures.apy](05_data_structures.apy) | Lists, dicts, iteration |
| [06_classes.apy](06_classes.apy) | `class` with `__init__` and methods |
| [07_imports.apy](07_imports.apy) (+ [helper.apy](helper.apy)) | The `.apy` import hook in action |

## Phase B — Library aliases and tooling (B30–B59)

| File | Demonstrates |
|---|---|
| [B30_filesystem_walk.apy](B30_filesystem_walk.apy) | `نظام_تشغيل` (os), `مسار_مكتبه` (pathlib) |
| [B31_functional_data.apy](B31_functional_data.apy) | `ادوات_داليه` (functools), `ادوات_تكرار` (itertools) |
| [B32_datetime_math.apy](B32_datetime_math.apy) | `مكتبة_تاريخ` (datetime), `وقت_نظام` (time) |
| [B33_data_storage.apy](B33_data_storage.apy) | `جيسون` (json), `ملفات_csv` (csv), `قاعدة_بيانات` (sqlite3) |
| [B34_text_processing.apy](B34_text_processing.apy) | `تعابير_نمطيه` (re) |
| [B35_numerics.apy](B35_numerics.apy) | `رياضيات` (math), `احصاء` (statistics), `عشوائيات` (random) |
| [B36_logging_demo.apy](B36_logging_demo.apy) | `تسجيل` (logging) |
| [B37_async_demo.apy](B37_async_demo.apy) | `اتزامن` (asyncio), `غير_متزامن`/`انتظر` keywords |
| [B38_utilities_demo.apy](B38_utilities_demo.apy) | `هاشلب` (hashlib), `مجاري` (io), `مدير_سياق` (contextlib) |
| [B55_formatter_demo.apy](B55_formatter_demo.apy) | Auto-formatter (`ثعبان نسّق`) |
| [B56_linter_demo.apy](B56_linter_demo.apy) | Linter (`ثعبان راجع`) |
| [B57_seaborn_demo.apy](B57_seaborn_demo.apy) | `رسوم_احصائيه` (seaborn) |
| [B58_scipy_demo.apy](B58_scipy_demo.apy) | `علوم_حسابيه` (scipy) |
| [B59_aiohttp_demo.apy](B59_aiohttp_demo.apy) | `طلبات_غير_متزامنه` (aiohttp) |

## Showcase apps (`apps/`)

| File | Description |
|---|---|
| [تحليل_اخبار.apy](../apps/تحليل_اخبار.apy) | News analysis — pandas + numpy + matplotlib + re + json |
| [خادم_ويب.apy](../apps/خادم_ويب.apy) | Full REST API — Flask + sqlite3 + datetime + hashlib |
| [حاسبة_علمية.apy](../apps/حاسبة_علمية.apy) | Scientific calculator — numpy + scipy + match/case |
| [مدير_مهام.apy](../apps/مدير_مهام.apy) | Task manager CLI — sqlite3 + OOP + context managers |

## Running

```bash
ثعبان examples/01_hello.apy
ثعبان examples/B37_async_demo.apy
ثعبان apps/حاسبة_علمية.apy

# Smoke test (all Phase A examples):
python -m pytest tests/test_examples.py
```

## Notes

- Phase A examples (01–07) are deterministic — no randomness or time-dependent calls.
- Every Arabic keyword comes from the canonical dictionary at [`dictionaries/ar-v1.md`](../dictionaries/ar-v1.md).
- Phase B examples require their respective libraries (`pip install -e ".[dev]"`).
- Showcase apps in `apps/` demonstrate maximum Arabic expressiveness — they serve as the project's "what's possible" reference.
