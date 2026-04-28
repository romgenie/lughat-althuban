<div dir="rtl">

# معمارية المشروع — Architecture

---

## نظرة عامة

لغة الثعبان تعمل عبر **خط أنابيب الترجمة** (translation pipeline) الذي يُحوّل ملفات `.apy` إلى Python قياسي في وقت التحميل، ثم يُنفّذها CPython. لا يوجد مترجم مستقل، ولا تشعيب لكود CPython.

```
ملف .apy
    │
    ▼
┌─────────────────────────────────────────────────────┐
│                  خط أنابيب الترجمة                  │
│                                                     │
│  1. pretokenize()    ← أرقام عربية، ترقيم، bidi     │
│       │                                             │
│  2. tokenize()       ← Python tokenizer             │
│       │                                             │
│  3. NAME rewriter    ← قاموس عربي→Python            │
│       │                                             │
│  4. untokenize()     ← إعادة تجميع الكود            │
│       │                                             │
│  5. compile()        ← Python bytecode              │
│       │                                             │
│  6. exec()           ← CPython ينفذ                 │
└─────────────────────────────────────────────────────┘
```

---

## مراحل خط الأنابيب

### 1. pretokenize — المعالجة المسبقة

**الملف**: `arabicpython/pretokenizer.py`

يُعالج النص قبل إرساله لـ tokenizer Python:

- **الأرقام العربية**: `١٢٣` → `123`
- **علامات الترقيم**: `،` → `,`  /  `؛` → `;`
- **رموز التحكم الثنائي (bidi)**: رفض U+200F و U+200E وغيرها
- **تحقق من الترميز**: يجب أن يكون UTF-8

### 2. tokenize — الرمزنة

يستخدم `tokenize.tokenize()` المدمج في Python. هذا يضمن أن كل قواعد Python في المزامنة السطرية والمسافات البادئة تعمل بشكل صحيح.

### 3. NAME rewriter — إعادة كتابة الأسماء

**القلب الأساسي للمشروع.**

لكل رمز من نوع `NAME` في تدفق الرموز:

1. طبّق `normalize_identifier()` على الرمز.
2. ابحث في القاموس الأساسي (ar-v1 / ar-v2).
3. إذا وُجد: استبدله بمكافئه Python.
4. إذا لم يوجد: اتركه كما هو (يمكن أن يكون معرّفاً مخصصاً).

### 4. untokenize — إعادة التجميع

`tokenize.untokenize()` يُعيد تجميع الرموز في نص Python قانوني.

### 5–6. compile + exec

Python القياسي. لا شيء خاص هنا.

---

## نقاط الدخول

| الواجهة | الملف | الوصف |
|---------|-------|--------|
| CLI | `arabicpython/cli.py` | `ثعبان script.apy` |
| REPL | `arabicpython/repl.py` | `ثعبان` (تفاعلي) |
| خطاف الاستيراد | `arabicpython/importer.py` | `استورد وحدة_apy` |
| API عام | `arabicpython/__init__.py` | `install()` / `uninstall()` |
| المنسّق | `arabicpython/formatter.py` | `ثعبان نسّق` |
| المدقّق | `arabicpython/linter.py` | `ثعبان راجع` |

---

## نظام الأسماء المستعارة (Alias System)

```
arabicpython/aliases/
    ├── _finder.py    ← AliasFinder: sys.meta_path hook
    ├── _loader.py    ← AliasLoader: creates ModuleProxy
    ├── _proxy.py     ← ModuleProxy: lazy attribute access
    ├── numpy.toml    ← "حسابات_عددية" → numpy
    ├── pandas.toml   ← "جداول_بيانات" → pandas
    └── ...           ← (40+ ملف TOML)
```

**كيف يعمل الاستيراد؟**

```python
استورد جداول_بيانات كـ جب
```

1. Python يستدعي `AliasFinder.find_spec("جداول_بيانات", ...)`
2. AliasFinder يبحث في ملفات TOML عن `arabic_name == "جداول_بيانات"`
3. يجد `pandas.toml` → يُعيد `ModuleSpec`
4. `AliasLoader.create_module()` يُنشئ `ModuleProxy(pandas)`
5. `جب.إطار_بيانات` → `pandas.DataFrame`

---

## قرارات المعمارية الرئيسية (ADRs)

| القرار | الملف |
|--------|-------|
| اختيار tokenize بدلاً من AST | `decisions/0001-architecture.md` |
| سياسة التطبيع | `decisions/0004-normalization-policy.md` |
| تصميم نظام الأسماء المستعارة | `decisions/0005-alias-runtime.md` |

---

## هيكل الأدلة الكاملة

```
lughat-althuban/
├── arabicpython/
│   ├── __init__.py         # install/uninstall/run_repl
│   ├── cli.py              # نقطة دخول CLI
│   ├── repl.py             # REPL التفاعلي
│   ├── translator.py       # خط أنابيب الترجمة الرئيسي
│   ├── pretokenizer.py     # المعالجة المسبقة
│   ├── normalizer.py       # normalize_identifier()
│   ├── dictionary.py       # تحميل قاموس ar-v1/ar-v2
│   ├── importer.py         # خطاف استيراد .apy
│   ├── excepthook.py       # ترجمة رسائل الأخطاء
│   ├── formatter.py        # المنسّق التلقائي
│   ├── linter.py           # المدقّق
│   └── aliases/            # 40+ ملف TOML + runtime
├── arabicpython_kernel/    # نواة Jupyter
├── editors/vscode/         # امتداد VS Code
├── dictionaries/           # ar-v1.md (مصدر القاموس)
├── decisions/              # 8 ADRs
├── specs/                  # حزم التنفيذ
└── tests/                  # pytest (2510 اختبار)
```

</div>

---

# Architecture (English)

## Pipeline

```
.apy source
    │
    ▼  pretokenize()   — Arabic numerals, punctuation, bidi rejection
    ▼  tokenize()      — Python's tokenizer
    ▼  NAME rewriter   — Arabic→Python dictionary lookup (with normalize_identifier)
    ▼  untokenize()    — Reassemble token stream
    ▼  compile()       — Python bytecode
    ▼  exec()          — CPython
```

No AST rewrite. No CPython fork. The same pipeline serves CLI, REPL, and the import hook.

## Alias system

`AliasFinder` (a `sys.meta_path` hook) intercepts `import جداول_بيانات`, finds `pandas.toml` where `arabic_name == "جداول_بيانات"`, and returns a `ModuleProxy(pandas)` whose attribute `إطار_بيانات` resolves to `pandas.DataFrame`.

## Key ADRs

- `decisions/0001-architecture.md` — why tokenize not AST
- `decisions/0004-normalization-policy.md` — hamza/ta-marbuta/alef-maqsura folding
- `decisions/0005-alias-runtime.md` — TOML-driven alias design
