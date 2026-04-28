<div dir="rtl">

# ويكي لغة الثعبان — الدليل الشامل

مرحباً بك في الوثائق الكاملة للغة الثعبان. هذه الويكي تغطي كل ما تحتاجه من مرجع فني وأمثلة عملية.

---

## أقسام الويكي

| القسم | الوصف |
|-------|--------|
| [الكلمات المفتاحية](keywords.md) | كل كلمة مفتاحية عربية مع مكافئها في Python |
| [الدوال المدمجة](builtins.md) | دوال مثل اطبع، نوع، طول، مدى |
| [الاستثناءات](exceptions.md) | الأسماء العربية لكل استثناء قياسي |
| [وحدات المكتبة القياسية](stdlib-aliases.md) | 21 وحدة stdlib مع أمثلة |
| [مكتبات علمية وبيانات](science-aliases.md) | numpy، pandas، matplotlib، seaborn، scipy |
| [مكتبات الويب](web-aliases.md) | flask، requests، aiohttp، fastapi |
| [أدوات التطوير](tooling.md) | المنسّق، المدقّق، نواة Jupyter، VS Code |
| [قواعد التطبيع](normalization.md) | كيف تُوحَّد الهمزات وتاء المربوطة والألف المقصورة |
| [الأسئلة الشائعة](faq.md) | إجابات للأسئلة المتكررة |
| [معمارية المشروع](architecture.md) | كيف تعمل اللغة من الداخل |

---

## البداية السريعة

```bash
# التثبيت
git clone https://github.com/GalaxyRuler/lughat-althuban
cd lughat-althuban
pip install -e .

# أول برنامج
echo 'اطبع("مرحبا بالعالم!")' > مرحبا.apy
ثعبان مرحبا.apy
```

---

## مثال في 10 أسطر

```python
# برنامج_كامل.apy
استورد رياضيات
استورد عشوائيات

دالة العب_تخمين(الحد_الأعلى=100):
    الرقم_السري = عشوائيات.عدد_صحيح_عشوائي(1, الحد_الأعلى)
    اطبع(f"فكّر في رقم بين 1 و{الحد_الأعلى}...")
    
    بينما صحيح:
        تخمين = عدد_صحيح(ادخل("تخمينك: "))
        اذا تخمين == الرقم_السري:
            اطبع("أحسنت! 🎉")
            ارجع
        وإلا اذا تخمين < الرقم_السري:
            اطبع("أكبر!")
        وإلا:
            اطبع("أصغر!")

العب_تخمين()
```

</div>

---

# لغة الثعبان Wiki — Complete Reference

Welcome to the complete documentation for Arabic Python.

## Wiki sections

| Section | Description |
|---|---|
| [Keywords](keywords.md) | Every Arabic keyword with its Python equivalent |
| [Built-ins](builtins.md) | اطبع, نوع, طول, مدى and all other built-in functions |
| [Exceptions](exceptions.md) | Arabic names for all standard exceptions |
| [Stdlib aliases](stdlib-aliases.md) | 21 stdlib modules with usage examples |
| [Science & data aliases](science-aliases.md) | numpy, pandas, matplotlib, seaborn, scipy |
| [Web aliases](web-aliases.md) | flask, requests, aiohttp |
| [Tooling](tooling.md) | Formatter, linter, Jupyter kernel, VS Code |
| [Normalization](normalization.md) | How hamza, ta-marbuta, and alef-maqsura variants are folded |
| [FAQ](faq.md) | Answers to common questions |
| [Architecture](architecture.md) | How the dialect works internally |
