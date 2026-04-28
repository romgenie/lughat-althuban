<div dir="rtl">

# تطبيقات لغة الثعبان — Showcase Apps

هذا المجلد يحتوي على تطبيقات متكاملة تُظهر الحد الأقصى من التعبيرية العربية في البرمجة. كل برنامج يستخدم عدة مكتبات عربية معاً ويُمثّل حالة استخدام حقيقية.

---

| التطبيق | المكتبات | الوصف |
|---------|---------|--------|
| [تحليل_اخبار.apy](تحليل_اخبار.apy) | pandas، numpy، matplotlib، re، json | تحليل نصي وإحصائي لمجموعة أخبار |
| [خادم_ويب.apy](خادم_ويب.apy) | flask، sqlite3، datetime، hashlib | REST API كامل بالعربية |
| [حاسبة_علمية.apy](حاسبة_علمية.apy) | numpy، scipy، math، statistics | حاسبة علمية مع تحليل إحصائي وحل معادلات |
| [مدير_مهام.apy](مدير_مهام.apy) | sqlite3، datetime، json | تطبيق إدارة مهام من سطر الأوامر |

---

## التشغيل

```bash
# تحليل الأخبار
pip install pandas numpy matplotlib
ثعبان apps/تحليل_اخبار.apy

# الخادم (يبدأ على المنفذ 5000)
pip install flask
ثعبان apps/خادم_ويب.apy

# الحاسبة العلمية
pip install numpy scipy
ثعبان apps/حاسبة_علمية.apy

# مدير المهام (لا يحتاج مكتبات إضافية)
ثعبان apps/مدير_مهام.apy
```

أو ثبّت كل شيء دفعة واحدة:

```bash
pip install -e ".[dev]"
```

---

## الهدف من هذه التطبيقات

توضّح هذه التطبيقات إمكانية كتابة برامج Python **حقيقية وكاملة** باستخدام العربية فقط — من السطر الأول إلى آخر سطر، دون الحاجة لمعرفة أي كلمة إنجليزية.

</div>

---

# لغة الثعبان Showcase Apps

These applications demonstrate writing complete, real-world Python programs entirely in Arabic — every keyword, every library call, every identifier.

## Apps

| App | Libraries | Description |
|---|---|---|
| [تحليل_اخبار.apy](تحليل_اخبار.apy) | pandas, numpy, matplotlib, re, json | Text/statistical analysis of news articles |
| [خادم_ويب.apy](خادم_ويب.apy) | flask, sqlite3, datetime, hashlib | Full REST API in Arabic |
| [حاسبة_علمية.apy](حاسبة_علمية.apy) | numpy, scipy, math, statistics | Scientific calculator with equation solving |
| [مدير_مهام.apy](مدير_مهام.apy) | sqlite3, datetime, json | CLI task manager with SQLite persistence |

## Run

```bash
pip install -e ".[dev]"           # install all optional dependencies
ثعبان apps/حاسبة_علمية.apy       # scientific calculator
ثعبان apps/مدير_مهام.apy         # task manager demo
ثعبان apps/خادم_ويب.apy          # web server (port 5000)
```
