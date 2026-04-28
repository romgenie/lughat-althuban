<div dir="rtl">

# الأسئلة الشائعة — FAQ

---

## سؤال: هل لغة الثعبان لغة مستقلة؟

**لا.** هي لهجة (dialect) فوق Python القياسي. الملفات `.apy` تُترجَم إلى Python في وقت التحميل وتُنفَّذ بواسطة CPython. لا يوجد مترجم مستقل، ولا تشعيب للكود المصدري.

---

## سؤال: ماذا أستخدم للاستيراد — `استورد` أم `استيراد`؟

**`استورد`** دائماً. هي الكلمة المفتاحية (فعل أمر). `استيراد` مصدر بمعنى "عملية الاستيراد" وليست كلمة مفتاحية.

```python
استورد رياضيات          # ✅ صحيح
استيراد رياضيات         # ❌ خطأ - لن يعمل
```

---

## سؤال: لماذا مفتاحي `قائمة` لا يعمل وأكتبه `قائمه`؟

بسبب قاعدة التطبيع: **تاء المربوطة في نهاية الكلمة تُحوَّل إلى هاء**. لذا يجب كتابة:

| الشكل المكتوب في الكود | الشكل الذي يُرفض |
|------------------------|-----------------|
| `قائمه` | `قائمة` |
| `اطبع` | `أطبع` |
| `مجموعه` | `مجموعة` |

القاعدة: `ة → ه`، `أ/إ/آ → ا`، `ى → ي` (في النهاية).

---

## سؤال: هل يمكن خلط `.apy` و `.py` في نفس المشروع؟

**نعم.** ملفات `.py` و `.apy` يمكن أن تستورد بعضها. الشرط الوحيد هو أن يكون كود Python الذي يستورد ملف `.apy` قد فعّل خطاف الاستيراد (`arabicpython.install()`).

---

## سؤال: هل الأداء مختلف عن Python العادي؟

**لا يُذكر.** الترجمة تحدث مرة واحدة عند التحميل. بعد ذلك ينفّذ Python bytecode عادي. لا overhead في وقت التشغيل.

---

## سؤال: كيف أضيف مكتبة جديدة بأسماء عربية؟

انظر [قسم إضافة وحدة جديدة](../../CONTRIBUTING.md) في دليل المساهمة. باختصار:

1. أنشئ `arabicpython/aliases/mylib.toml`
2. أنشئ `tests/aliases/test_mylib.py`
3. أضف مثالاً في `examples/`

---

## سؤال: ما الفرق بين `ذات` و `self`؟

`ذات` هو الاسم العربي لـ `self`. يمكن استخدامهما بالتبادل في الكود، لكن الاتفاق في المشروع هو استخدام `ذات`.

```python
صنف مستطيل:
    دالة __init__(ذات, عرض, طول):
        ذات.عرض = عرض
        ذات.طول = طول
    
    دالة المساحة(ذات):
        ارجع ذات.عرض * ذات.طول
```

---

## سؤال: هل يعمل مع Jupyter Notebook؟

**نعم** بعد تثبيت النواة:

```bash
pip install -e ".[kernel]"
python -m arabicpython_kernel install
jupyter notebook   # اختر kernel "apython"
```

---

## سؤال: هل يعمل مع VS Code؟

**نعم.** ثبّت الامتداد من مجلد `editors/vscode/` للحصول على:

- تلوين الصياغة (Syntax highlighting) لملفات `.apy`
- التعرف على الكلمات المفتاحية العربية
- ترميز الألوان الصحيح

---

## سؤال: أين أجد مرجع الكلمات المفتاحية كاملاً؟

- [`docs/wiki/keywords.md`](keywords.md) — كل كلمة مفتاحية مع أمثلة
- [`dictionaries/ar-v1.md`](../../dictionaries/ar-v1.md) — القاموس الرسمي الكامل

</div>

---

# FAQ (English)

**Q: Is this a standalone language?**  
No. It's a dialect over standard Python. `.apy` files are translated at load time and run by CPython.

**Q: `استورد` or `استيراد` for import?**  
Always `استورد` (verb = "import!"). `استيراد` is a noun and is not a keyword.

**Q: Why does `قائمة` not work — I have to write `قائمه`?**  
Normalization: final `ة → ه`, `أ/إ/آ → ا`, final `ى → ي`. Write all keys in normalized form.

**Q: Can I mix `.apy` and `.py` files?**  
Yes, as long as the import hook (`arabicpython.install()`) is active.

**Q: Is there a performance penalty?**  
Negligible. Translation happens once at load time; afterwards it's standard Python bytecode.

**Q: Does it work with Jupyter?**  
Yes. `pip install -e ".[kernel]"` then `python -m arabicpython_kernel install`.

**Q: Does it work with VS Code?**  
Yes. Install the extension from `editors/vscode/` for syntax highlighting.
