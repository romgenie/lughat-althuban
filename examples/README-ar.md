<div dir="rtl">

# أمثلة apython

سبعة برامج `.apy` تصاعدية تستعرض ميزات Phase A.

| الملف | ما يستعرضه |
|---|---|
| `01_hello.apy` | `print` (`اطبع`) والثوابت النصية |
| `02_arithmetic.apy` | المتغيرات، والحساب الصحيح، و `f-strings` |
| `03_control_flow.apy` | `for`/`in`/`range` ، `if`/`else` ، وباقي القسمة |
| `04_functions.apy` | `def` ، والوسائط الافتراضية، و `return` |
| `05_data_structures.apy` | القوائم، والقواميس، والتكرار |
| `06_classes.apy` | `class` مع `__init__` والتوابع |
| `07_imports.apy` (+ `helper.apy`) | خطّاف استيراد `.apy` قيد العمل |

## التشغيل

من جذر المستودع، بعد تنفيذ `pip install -e .`:

```bash
apython examples/01_hello.apy
apython examples/07_imports.apy   # يستورد examples/helper.apy عبر الخطّاف
```

أو شغّل المجموعة كاملة كاختبار شامل:

```bash
python -m pytest tests/test_examples.py
```

## ملاحظات

- جميع الأمثلة حتمية النتائج — لا توجد استدعاءات لـ `input()` أو عشوائية أو تعتمد على الوقت.
- كل معرّف عربي مستمد من القاموس القياسي في [`dictionaries/ar-v1.md`](../dictionaries/ar-v1.md).
- لكي يعثر `07_imports.apy` على `helper.apy` ، يجب أن يكون دليل العمل هو `examples/` أو يجب أن يكون `examples/` في `sys.path`. يتعامل اختبار الدخان مع هذا عن طريق تشغيل المثال عبر `subprocess` مع جعل `cwd=examples/`.

</div>
