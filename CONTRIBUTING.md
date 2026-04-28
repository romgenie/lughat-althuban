<div dir="rtl">

# دليل المساهمة في لغة الثعبان

نرحب بجميع المساهمين الشغوفين بتطوير مجتمع البرمجة العربي. كل العمل والنقاشات هنا بالعربية والإنجليزية كليهما.

---

## فهرس الأقسام

1. [ما الذي يحتاجه المشروع؟](#ما-الذي-يحتاجه-المشروع)
2. [سير عمل حزمة التنفيذ](#سير-عمل-حزمة-التنفيذ)
3. [إضافة وحدة مكتبة جديدة — TOML](#إضافة-وحدة-مكتبة-جديدة)
4. [قواعد التسمية العربية](#قواعد-التسمية-العربية)
5. [قواعد التطبيع (normalize_identifier)](#قواعد-التطبيع)
6. [قائمة التحقق من الاتساق المتقاطع](#قائمة-التحقق-من-الاتساق-المتقاطع)
7. [متطلبات الاختبارات](#متطلبات-الاختبارات)
8. [إصلاح الأخطاء](#إصلاح-الأخطاء)
9. [قواعد الالتزام بالمستودع](#قواعد-الالتزام-بالمستودع)
10. [مراجعة الترجمة العربية](#مراجعة-الترجمة-العربية)

---

## ما الذي يحتاجه المشروع؟

| الدور | الوصف |
|-------|--------|
| **مبرمجون** | كتابة حزم تنفيذية (TOMLs + اختبارات + أمثلة) |
| **لغويون ومترجمون** | اختيار المصطلحات العربية الدقيقة ومراجعة القاموس |
| **مراجعون** | مراجعة طلبات السحب والتأكد من الاتساق |
| **كتّاب الوثائق** | تحسين التوثيق العربي والأمثلة التعليمية |

---

## سير عمل حزمة التنفيذ

كل وحدة عمل في المشروع هي **حزمة تنفيذية** (Spec Packet) بالشكل التالي:

```
specs/B-NNN-اسم-الحزمة.md        ← المواصفة (يكتبها المخطط)
specs/B-NNN-اسم-الحزمة.delivery.md  ← ملاحظات التسليم (يكتبها المنفذ)
```

**خطوات المساهم:**

1. **اختر حزمة** من [`ROADMAP-PHASE-B.md`](ROADMAP-PHASE-B.md) التي لم تُنجز بعد.
2. **اقرأ المواصفة** بعناية — كل مطلب مكتوب بتفصيل.
3. **أنشئ فرعاً** باسم `B-NNN/اسم-الحزمة`.
4. **نفذ المتطلبات** — كود + اختبارات + مثال `.apy`.
5. **شغّل الاختبارات** كاملة: `pytest tests/ -x -q`.
6. **اكتب ملاحظات التسليم** في `specs/B-NNN-*.delivery.md`.
7. **ارفع طلب سحب** (Pull Request).

---

## إضافة وحدة مكتبة جديدة

لإضافة مكتبة Python بأسماء عربية، تحتاج إلى **ثلاثة ملفات**:

### 1. ملف TOML في `arabicpython/aliases/`

```toml
# arabicpython/aliases/mylib.toml

[meta]
arabic_name    = "اسم_عربي"        # الاسم المستعار لاستيراد المكتبة
python_module  = "mylib"           # اسم حزمة Python
dict_version   = "ar-v1"
schema_version = 1
maintainer     = "اسمك"

[entries]
"اسم_عربي_1"  = "PythonName1"
"اسم_عربي_2"  = "PythonName2"
"اسم_عربي_3"  = "submodule.Name3"    # للوصول إلى submodules
```

### 2. ملف الاختبار في `tests/aliases/test_mylib.py`

```python
# tests/aliases/test_mylib.py
import pathlib
import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"
mylib = pytest.importorskip("mylib", reason="mylib not installed")

@pytest.fixture(scope="module")
def اسم_عربي():
    from arabicpython.aliases._finder import AliasFinder
    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("اسم_عربي", None, None)
    assert spec is not None
    return spec.loader.create_module(spec)

class TestMyLibAliasesExist:
    def test_something(self, اسم_عربي):
        assert اسم_عربي.اسم_عربي_1 is mylib.PythonName1

class TestMyLibTomlMeta:
    def test_toml_parseable(self):
        import tomllib
        p = ALIASES_DIR / "mylib.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert data["meta"]["python_module"] == "mylib"
        assert data["meta"]["arabic_name"] == "اسم_عربي"

    def test_entry_count(self):
        import tomllib
        p = ALIASES_DIR / "mylib.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert len(data["entries"]) >= 5
```

### 3. مثال توضيحي في `examples/`

```python
# examples/BNNN_mylib_demo.apy
استورد اسم_عربي

# ... مثال يُظهر الوظائف الأساسية للمكتبة
```

---

## قواعد التسمية العربية

**المبادئ الأساسية:**

1. **الفصحى المعاصرة** — لا عامية، لا لهجات.
2. **المصطلحات الحاسوبية المعتمدة** — إن وُجد مصطلح متعارف عليه في الأدبيات العربية (مثل "مسار" لـ Path، "نص" لـ String) يُفضَّل على الترجمة الحرفية.
3. **الإيجاز** — تجنب الأسماء الطويلة جداً (أكثر من 3 كلمات).
4. **الشرطة السفلية** `_` للفصل بين كلمات الاسم المركب.
5. **بدون حركات** — لا تشكيل، لا كشيدة.

**قائمة مصطلحات ثابتة (لا تغيّرها):**

| المفهوم | الاسم العربي المعتمد |
|---------|---------------------|
| list | قائمه |
| dict | قاموس |
| tuple | مجموعه |
| set | مجموعه_غير_مرتبه |
| string | نص |
| integer | عدد_صحيح |
| float | عدد_عشري |
| function | دالة |
| class | صنف |
| module | وحدة |
| path | مسار |
| error/exception | خطا |
| import | استورد (**كلمة مفتاحية**، ليست اسماً) |

---

## قواعد التطبيع

كل مفتاح TOML يمر عبر `normalize_identifier()` تلقائياً. القواعد:

| التحويل | مثال |
|---------|------|
| `أ / إ / آ → ا` | `إطار → اطار` |
| `ة → ه` (في النهاية) | `قائمة → قائمه` |
| `ى → ي` (في النهاية) | `مجرى → مجري` |

**⚠️ مهم:** عند اختبار المفاتيح، استخدم الشكل المُطبَّع في كود Python (مثل `اطبع` وليس `أطبع`).

---

## قائمة التحقق من الاتساق المتقاطع

**قبل رفع طلب السحب**، تحقق من عدم التصادم مع الوحدات الموجودة:

```python
# تحقق سريع من التصادم
python -c "
from arabicpython.aliases._finder import AliasFinder
import pathlib
finder = AliasFinder(mappings_dir=pathlib.Path('arabicpython/aliases'))
# ... مقارنة المفاتيح
"
```

أو شغّل اختبارات الاتساق المتقاطع:

```bash
pytest tests/aliases/test_stdlib_B057_B058_B059_cross_consistency.py -v
```

**قواعد التعارض:**
- إذا تعارض اسم مع وحدة stdlib، أضف لاحقة توضيحية (مثل `علمي_` أو `غير_متزامن_`).
- وثّق التعارض في تعليق أعلى ملف TOML.

---

## متطلبات الاختبارات

لا يُقبل أي طلب سحب بدون اختبارات تغطي التغييرات:

| المطلب | التفاصيل |
|--------|---------|
| **الكلمات المفتاحية العربية** | استخدم `دالة` لا `def`، `لكل` لا `for`، إلخ |
| **توافقية المرحلة أ** | `pytest tests/test_phase_a_compat.py` يجب أن ينجح |
| **اختبارات TOML** | تحقق من `meta.python_module` و `meta.arabic_name` وعدد الإدخالات |
| **اختبارات الوصول** | تحقق أن `proxy.اسم_عربي is lib.PythonName` |
| **الاتساق المتقاطع** | لا تصادم مع المفاتيح الموجودة |

تشغيل كامل الاختبارات:

```bash
pytest tests/ -x -q                     # توقف عند أول فشل
pytest tests/ -v --tb=short             # تفاصيل كاملة
pytest tests/aliases/ -v                # اختبارات الأسماء المستعارة فقط
```

---

## إصلاح الأخطاء

1. ابحث في القضايا (Issues) عن الخطأ.
2. أنشئ فرعاً: `fix/وصف-الخطأ`.
3. **اكتب اختباراً يُظهر الخطأ أولاً** (يجب أن يفشل قبل الإصلاح).
4. أصلح الخطأ وتحقق من نجاح جميع الاختبارات.
5. ارفع طلب السحب مع إشارة إلى رقم القضية.

---

## قواعد الالتزام بالمستودع

رسائل الالتزام يُفضَّل أن تكون بالعربية:

```
إضافة مرادفات وحدة seaborn (B-057)
إصلاح تصادم جبر_خطي مع numpy في scipy.toml
تحديث قائمة الاختبارات المستثناة في test_phase_a_compat
```

**القالب:**
```
[فعل] [ما تغيّر] [(رقم الحزمة إن وجد)]
```

أفعال مناسبة: `إضافة` / `إصلاح` / `تحديث` / `حذف` / `إعادة_هيكلة`

---

## مراجعة الترجمة العربية

- **الفصحى المعاصرة**: لا عامية، لا لهجات.
- **الوضوح أولاً**: المصطلح المتعارف عليه في الأدبيات الحاسوبية العربية يُفضَّل على الترجمة الحرفية الغريبة.
- **استشر المعجم**: يمكن استخدام [معجم السوار (KSAA)](https://siwar.ksaa.gov.sa) للبحث عن المصطلحات المعتمدة.
- **النقاش البناء**: ناقش الترجمات بأدب في تعليقات طلب السحب.

</div>

---

# Contributing to لغة الثعبان

Welcome! Contributions are accepted in Arabic or English.

---

## Quick reference

### Adding a new alias module

1. Create `arabicpython/aliases/mylib.toml` with `[meta]` and `[entries]` sections.
2. Create `tests/aliases/test_mylib.py` using `pytest.importorskip("mylib")`.
3. Add an example at `examples/BNNN_mylib_demo.apy`.
4. Run `pytest tests/ -x -q` — all 2510+ tests must pass.
5. Check cross-consistency: no Arabic key may appear in two different module TOMLs.

### Normalization rules (critical)

All TOML keys are normalized before lookup:
- `أ/إ/آ → ا`
- final `ة → ه`
- final `ى → ي`

Write your keys in normalized form (e.g., `قائمه` not `قائمة`).

### The `استورد` keyword

`استورد` is the Arabic `import` **keyword** (a verb: "import!"). Do **not** confuse it with `استيراد` (noun: "importation"). Demo files must use `استورد`.

### Cross-consistency checklist

- No duplicate Arabic key across all TOMLs.
- Collisions: add a disambiguating suffix (e.g., `_علمي` for scipy vs numpy, `_غير_متزامن` for async vs sync).
- Document every collision in the TOML file's comment header.

### Running the test suite

```bash
pytest tests/ -x -q                 # stop at first failure
pytest tests/aliases/ -v            # alias tests only
pytest tests/test_formatter.py -v   # formatter tests
pytest tests/test_linter.py -v      # linter tests
pytest tests/test_jupyter_kernel.py # kernel tests (ipykernel mocked)
```

### Commit message style

Prefer Arabic. Use the pattern: `[verb] [what changed] [(packet number)]`

Examples:
- `إضافة مرادفات وحدة aiohttp (B-059)`
- `إصلاح تصادم خطا_اتصال في requests/aiohttp`

---

## See also

- [`specs/0000-template.md`](specs/0000-template.md) — packet template
- [`specs/INDEX.md`](specs/INDEX.md) — packet ledger
- [`decisions/0004-normalization-policy.md`](decisions/0004-normalization-policy.md) — normalization rules
- [`ROADMAP-PHASE-B.md`](ROADMAP-PHASE-B.md) — open packets
- [`HANDOVER-LARGE-PACKETS.md`](HANDOVER-LARGE-PACKETS.md) — large/complex implementation packets
