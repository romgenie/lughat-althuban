# Spec Packet B-012: aliases-django-core-v1

**Phase**: B
**Depends on**: B-001 (alias-runtime-v1), B-002 (phase-a-compat-suite)
**Estimated size**: large
**Owner**: —

## Goal

Ship the Arabic alias mapping for Django's core surface: `urls`, `views`, `models`, and `forms`. This is a large mapping (Floor 80) covering the most common parts of the Django framework.

## Non-goals

- No Django REST Framework (DRF) mapping.
- No specialized contrib apps (except basic auth/admin).
- No complex template tag translation (as per B-010).

## Files

### Files to create

- `arabicpython/aliases/django.toml`
- `tests/test_aliases_django.py`
- `examples/B12_django_hello.apy`
- `examples/B12_README-ar.md`

## Public interfaces

### `arabicpython/aliases/django.toml`

[meta]
arabic_name = "ديانغو"
python_module = "django"
dict_version = "ar-v1"
schema_version = 1

[entries]
# === URLs ===
"مسار" = "urls.path"
"مسار_ريجيكس" = "urls.re_path"
"تضمين" = "urls.include"
"عكس" = "urls.reverse"
"عكس_متأخر" = "urls.reverse_lazy"

# === HTTP ===
"استجابة_http" = "http.HttpResponse"
"استجابة_جسون" = "http.JsonResponse"
"استجابة_توجيه" = "http.HttpResponseRedirect"
"خطأ_404" = "http.Http404"
"خطأ_ممنوع" = "http.HttpResponseForbidden"
"طلب_http" = "http.HttpRequest"

# === Shortcuts ===
"عرض" = "shortcuts.render"
"توجيه" = "shortcuts.redirect"
"احصل_أو_404" = "shortcuts.get_object_or_404"
"احصل_قائمة_أو_404" = "shortcuts.get_list_or_404"

# === Models ===
"نموذج" = "db.models.Model"
"مدير" = "db.models.Manager"
"استعلام" = "db.models.Q"
"تعبيرات" = "db.models.F"
"حقل_نصي" = "db.models.CharField"
"حقل_نص_طويل" = "db.models.TextField"
"حقل_رقمي" = "db.models.IntegerField"
"حقل_تاريخ" = "db.models.DateField"
"حقل_وقت" = "db.models.DateTimeField"
"حقل_رابط" = "db.models.URLField"
"حقل_بريد" = "db.models.EmailField"
"حقل_منطقي" = "db.models.BooleanField"
"حقل_أرقام_عشرية" = "db.models.DecimalField"
"حقل_ملف" = "db.models.FileField"
"حقل_صورة" = "db.models.ImageField"
"مفتاح_أجنبي" = "db.models.ForeignKey"
"علاقة_متعدد_لمتعدد" = "db.models.ManyToManyField"
"علاقة_واحد_لواحد" = "db.models.OneToOneField"

# === Aggregates ===
"مجموع" = "db.models.Sum"
"متوسط" = "db.models.Avg"
"عدد" = "db.models.Count"
"أدنى" = "db.models.Min"
"أقصى" = "db.models.Max"

# === Views ===
"مشهد_عام" = "views.View"
"مشهد_قائمة" = "views.generic.ListView"
"مشهد_تفاصيل" = "views.generic.DetailView"
"مشهد_إنشاء" = "views.generic.CreateView"
"مشهد_تعديل" = "views.generic.UpdateView"
"مشهد_حذف" = "views.generic.DeleteView"
"مشهد_قالب" = "views.generic.TemplateView"

# === Forms ===
"استمارة" = "forms.Form"
"استمارة_نموذج" = "forms.ModelForm"
"حقل_استمارة_نص" = "forms.CharField"
"حقل_استمارة_رقم" = "forms.IntegerField"
"حقل_استمارة_خيار" = "forms.ChoiceField"
"حقل_استمارة_منطقي" = "forms.BooleanField"

# === Auth ===
"احصل_على_المستخدم" = "contrib.auth.get_user"
"توثيق" = "contrib.auth.authenticate"
"دخول" = "contrib.auth.login"
"خروج" = "contrib.auth.logout"

# === Admin ===
"مسؤول_النموذج" = "contrib.admin.ModelAdmin"
"موقع_المسؤول" = "contrib.admin.site"

# === Core ===
"خطأ_تحقق" = "core.exceptions.ValidationError"
"كائن_غير_موجود" = "core.exceptions.ObjectDoesNotExist"

# (Adding more to reach 80)
"إعدادات" = "conf.settings"
"إشارة" = "dispatch.Signal"
"استقبال_إشارة" = "dispatch.receiver"
"رسائل" = "contrib.messages"
"أضف_رسالة" = "contrib.messages.add_message"
"نجاح" = "contrib.messages.SUCCESS"
"تحذير" = "contrib.messages.WARNING"
"خطأ" = "contrib.messages.ERROR"
"معلومات" = "contrib.messages.INFO"
"استعلام_قاعدة" = "db.connection"
"تنفيذ_خام" = "db.models.expressions.RawSQL"
"فرز" = "db.models.OrderBy"
"تجميع" = "db.models.Aggregate"
"ربط_خارجي" = "db.models.OuterRef"
"استعلام_فرعي" = "db.models.Subquery"
"حقل_اختيار" = "db.models.SlugField"
"حقل_إحداثيات" = "db.models.FloatField"
"حقل_ip" = "db.models.GenericIPAddressField"
"حقل_uuid" = "db.models.UUIDField"
"حقل_جسون" = "db.models.JSONField"
"حقل_وقت_تلقائي" = "db.models.TimeField"

# Count: ~75. Final implementation must reach 80.

### `examples/B12_django_hello.apy`

```python
استورد ديانغو
من ديانغو.مسار استورد مسار
من ديانغو.استجابة_http استورد استجابة_http

دالة الرئيسيه(طلب):
    ارجع استجابة_http("مرحبا بك في ديانغو العربي")

قائمة_المسارات = [
    مسار("", الرئيسيه),
]
```

## Implementation constraints

- **Cite B-010 as structural prior.** This packet follows the same deliverable structure and naming conventions.
- **Method-on-instance limitation:** Like B-010, this packet only maps module-level attributes. Methods on instances (e.g., `Model.objects.filter`, `QuerySet.all`) remain in English in this version.
- **Acceptance checklist must include Phase A compat assertion.**
- **Ensure all Arabic names round-trip through `normalize_identifier`.**

## Test requirements

- Verification of ORM operations (creating models, querying).
- Verification of routing and view execution.
- Verification of form validation.

## Acceptance checklist

- [ ] `arabicpython/aliases/django.toml` shipped with at least 80 entries.
- [ ] All integration tests pass.
- [ ] `examples/B12_django_hello.apy` runs end-to-end.
- [ ] `examples/B12_README-ar.md` written.
- [ ] Phase A compat assertion: `tests/test_phase_a_compat.py` still passes.
