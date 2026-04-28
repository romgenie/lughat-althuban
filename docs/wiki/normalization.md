<div dir="rtl">

# قواعد التطبيع — Normalization Rules

**المرجع الرسمي**: [`decisions/0004-normalization-policy.md`](../../decisions/0004-normalization-policy.md)

---

## لماذا التطبيع؟

العربية تُكتب بأشكال متعددة للحرف الواحد. مثلاً "أ" و"إ" و"آ" و"ا" كلها صور للألف، لكنها نقاط Unicode مختلفة. بدون تطبيع، المطوّر الذي يكتب `أطبع` لن يتعرف عليها المترجم الذي توقع `اطبع`.

لغة الثعبان تُطبّع **كل المعرّفات** قبل البحث في القاموس، لذا كل الصيغ التالية تعمل:

```python
اطبع("مرحبا")   # ✅ الشكل المُوحَّد
أطبع("مرحبا")   # ✅ يعمل (الهمزة فوق تُطبَّع)
إطبع("مرحبا")   # ✅ يعمل (الهمزة تحت تُطبَّع)
```

---

## قواعد التطبيع الثلاث

### القاعدة 1: صور الألف

```
أ  →  ا    (الهمزة فوق)
إ  →  ا    (الهمزة تحت)
آ  →  ا    (المد)
ٱ  →  ا    (الوصل)
```

**مثال**: `إطار` → `اطار` / `آليه` → `اليه`

### القاعدة 2: تاء المربوطة في النهاية

```
ة  →  ه    (في نهاية الكلمة فقط)
```

**مثال**: `قائمة` → `قائمه` / `مجموعة` → `مجموعه`

> **ملاحظة**: القاعدة تنطبق على نهاية الكلمة فقط. `قاعدة_بيانات` → `قاعده_بيانات` (كل كلمة تُطبَّع على حدة).

### القاعدة 3: الألف المقصورة في النهاية

```
ى  →  ي    (في نهاية الكلمة فقط)
```

**مثال**: `مجرى` → `مجري` / `منحنى` → `منحني`

---

## التطبيع في مفاتيح TOML

**يجب أن تكون مفاتيح TOML مُطبَّعة مسبقاً.** النظام يُطبّعها عند القراءة، لكن كتابتها مُطبَّعة يجعل القراءة أوضح ويمنع الالتباس.

```toml
# ✅ صحيح — مفاتيح مطبّعة
[entries]
"قائمه"     = "list"
"قاموس"     = "dict"
"اطبع"      = "print"

# ❌ يعمل لكن غير مُفضَّل — مفاتيح غير مطبّعة
[entries]
"قائمة"     = "list"    # ة ستُطبَّع تلقائياً لكن غير موصى به
```

---

## استخدام دالة التطبيع في الكود

```python
from arabicpython.normalizer import normalize_identifier

normalize_identifier("قائمة")    # → "قائمه"
normalize_identifier("أطبع")     # → "اطبع"
normalize_identifier("مجرى")     # → "مجري"
normalize_identifier("إطار")     # → "اطار"
```

---

## قائمة التحقق للمساهمين

قبل إضافة مفتاح TOML جديد:

- [ ] الألف بدون همزة (`ا` لا `أ/إ/آ`)
- [ ] تاء مربوطة في النهاية مُحوَّلة إلى هاء (`ه` لا `ة`)
- [ ] ألف مقصورة في النهاية مُحوَّلة إلى ياء (`ي` لا `ى`)
- [ ] بدون تشكيل (حركات)
- [ ] بدون كشيدة (تطويل)
- [ ] الشرطة السفلية `_` للفصل بين الكلمات

</div>

---

# Normalization Rules (English)

Arabic has multiple Unicode code points for the same letter. The normalization pipeline folds all variants so that `أطبع`, `إطبع`, and `اطبع` all resolve to the same identifier.

## Rules

| Transformation | Input → Output |
|---|---|
| Hamza forms → bare alef | `أ/إ/آ/ٱ → ا` |
| Final ta-marbuta → ha | `ة → ه` (word-final only) |
| Final alef-maqsura → ya | `ى → ي` (word-final only) |

## Programmatic use

```python
from arabicpython.normalizer import normalize_identifier

normalize_identifier("قائمة")   # → "قائمه"
normalize_identifier("أطبع")    # → "اطبع"
normalize_identifier("مجرى")    # → "مجري"
```

## TOML keys

Write keys in normalized form. The system normalizes on read, but pre-normalized keys are clearer.
