<div dir="rtl">

# الأمثلة — لغة الثعبان

سبعة برامج تعليمية تصاعدية مكتوبة بالعربية. كل مثال مستقل وقابل للتشغيل مباشرة.

| الملف | ما يُوضّحه |
|-------|------------|
| [01_hello.apy](01_hello.apy) | `اطبع` والسلاسل النصية |
| [02_arithmetic.apy](02_arithmetic.apy) | المتغيرات والحساب والنصوص المُدرَجة |
| [03_control_flow.apy](03_control_flow.apy) | `لكل` / `في` / `نطاق`، `إذا` / `وإلا` |
| [04_functions.apy](04_functions.apy) | `دالة`، القيم الافتراضية، `ارجع` |
| [05_data_structures.apy](05_data_structures.apy) | القوائم والقواميس والتكرار |
| [06_classes.apy](06_classes.apy) | `صنف` مع `__init__` والتوابع |
| [07_imports.apy](07_imports.apy) + [helper.apy](helper.apy) | خطّاف الاستيراد `.apy` |

## تشغيل الأمثلة

```bash
ثعبان examples/01_hello.apy
ثعبان examples/07_imports.apy
```

للشرح الكامل لكل مثال بالعربية: [README-ar.md](README-ar.md)

</div>

---

# لغة الثعبان examples

Seven progressive `.apy` programs demonstrating Phase A's feature surface.

| File | Demonstrates |
|---|---|
| [01_hello.apy](01_hello.apy) | `print` (`اطبع`) and string literals |
| [02_arithmetic.apy](02_arithmetic.apy) | Variables, integer arithmetic, f-strings |
| [03_control_flow.apy](03_control_flow.apy) | `for`/`in`/`range`, `if`/`else`, modulo |
| [04_functions.apy](04_functions.apy) | `def`, default arguments, `return` |
| [05_data_structures.apy](05_data_structures.apy) | Lists, dicts, iteration |
| [06_classes.apy](06_classes.apy) | `class` with `__init__` and methods |
| [07_imports.apy](07_imports.apy) (+ [helper.apy](helper.apy)) | The `.apy` import hook in action |

## Running

From the repository root, after `pip install -e .`:

```bash
ثعبان examples/01_hello.apy
ثعبان examples/07_imports.apy   # imports examples/helper.apy via the hook
```

Or run the whole suite as a smoke test:

```bash
python -m pytest tests/test_examples.py
```

## Notes

- All examples are deterministic — no `input()`, randomness, or time-dependent calls.
- Every Arabic identifier is drawn from the canonical dictionary at [`dictionaries/ar-v1.md`](../dictionaries/ar-v1.md).
- For `07_imports.apy` to find `helper.apy`, the working directory must be `examples/` *or* `examples/` must be on `sys.path`. The smoke test handles this by running the example via `subprocess` with `cwd=examples/`.
