<div dir="rtl">

# أدوات التطوير — Tooling Guide

---

## 1. المنسّق (Formatter) — `ثعبان نسّق`

ينسّق ملفات `.apy` تلقائياً دون تغيير المعنى.

### الاستخدام

```bash
ثعبان نسّق ملف.apy          # تنسيق في مكانه
ثعبان نسّق --فحص ملف.apy    # فحص فقط دون تغيير (exit 1 إذا يحتاج تنسيقاً)
ثعبان نسّق *.apy             # تنسيق عدة ملفات
```

### ما يُصلحه المنسّق

| المشكلة | قبل | بعد |
|---------|-----|-----|
| تعليق بدون مسافة | `#تعليق` | `# تعليق` |
| فاصلة بدون مسافة | `أ,ب,ج` | `أ, ب, ج` |
| تبويب (tab) | `→اطبع(...)` | `    اطبع(...)` |
| أسطر فارغة زائدة | (أكثر من 2) | (2 كحد أقصى) |
| مسافات في نهاية السطر | `اطبع(س)   ` | `اطبع(س)` |

### واجهة برمجية

```python
from arabicpython.formatter import format_source, format_file

# تنسيق نص
نص_منسّق = format_source("""
دالة حساب(س,ص):
    ارجع س+ص
""")

# تنسيق ملف
تغيّر = format_file(pathlib.Path("ملف.apy"))
```

---

## 2. المدقّق (Linter) — `ثعبان راجع`

يفحص ملفات `.apy` ويُبلّغ عن تحذيرات وأخطاء.

### الاستخدام

```bash
ثعبان راجع ملف.apy           # فحص ملف
ثعبان راجع *.apy              # فحص عدة ملفات
ثعبان راجع --json ملف.apy    # إخراج JSON للأدوات
```

### رموز التشخيص

| الرمز | النوع | الوصف |
|-------|-------|--------|
| `W001` | تحذير | السطر أطول من 99 حرف |
| `W002` | تحذير | مسافة في نهاية السطر |
| `W003` | تحذير | تبويب (tab) بدلاً من مسافات |
| `W004` | تحذير | معرّف يخلط العربية والإنجليزية |
| `E001` | خطأ | كلمة مفتاحية ar-v1 في ملف ar-v2 |
| `I001` | معلومة | لا تعليق أو docstring في أول 10 أسطر |

### واجهة برمجية

```python
from arabicpython.linter import lint_source, Diagnostic

تشخيصات = lint_source("""
دالة  f(س,ص):
    ارجع س+ص
""")
لكل تشخيص في تشخيصات:
    اطبع(f"{تشخيص.code}: {تشخيص.message} (سطر {تشخيص.line})")
```

---

## 3. نواة Jupyter — `apython kernel`

تتيح تشغيل ملفات `.apy` كـ notebooks في Jupyter.

### التثبيت

```bash
pip install -e ".[kernel]"
python -m arabicpython_kernel install
```

### الاستخدام

```bash
jupyter notebook    # اختر kernel "apython (لغة الثعبان)"
jupyter lab         # نفس الشيء
```

في الـ notebook يمكنك كتابة كود عربي مباشرة:

```python
# خلية في notebook
استورد جداول_بيانات كـ جب
استورد رسوم_احصائيه كـ رسم

بيانات = جب.إطار_بيانات({"س": [1,2,3,4], "ص": [2,4,6,8]})
رسم.خط_بياني(data=بيانات, x="س", y="ص")
```

---

## 4. امتداد VS Code

يوفر تلوين الصياغة لملفات `.apy`.

### التثبيت

```bash
cd editors/vscode
vsce package        # يُنشئ ملف .vsix
code --install-extension arabic-python-*.vsix
```

أو افتح مجلد `editors/vscode/` كـ workspace في VS Code وشغّل F5.

### الميزات

- تلوين الكلمات المفتاحية العربية
- تلوين الأرقام والسلاسل النصية والتعليقات
- دعم الـ snippets (قريباً)

</div>

---

# Tooling Guide (English)

## Formatter (`ثعبان نسّق`)

Auto-formats `.apy` files without changing behavior.

```bash
ثعبان نسّق file.apy          # format in place
ثعبان نسّق --فحص file.apy    # check only, exit 1 if changes needed
```

Fixes: comment spacing (`#x` → `# x`), comma spacing (`a,b` → `a, b`), tabs → 4 spaces, trailing whitespace, max 2 consecutive blank lines.

## Linter (`ثعبان راجع`)

Reports diagnostics: W001 (line too long), W002 (trailing whitespace), W003 (tab indent), W004 (mixed Arabic/Latin identifier), E001 (wrong dialect keyword), I001 (no intro comment).

```bash
ثعبان راجع file.apy
```

## Jupyter Kernel

```bash
pip install -e ".[kernel]"
python -m arabicpython_kernel install
jupyter notebook   # choose "apython" kernel
```

## VS Code Extension

Install from `editors/vscode/`. Provides syntax highlighting for `.apy` files.
