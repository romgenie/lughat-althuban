# tests/aliases/test_django.py
# B-012 third-party aliases — django web framework tests
#
# Django requires `settings.configure(...)` + `django.setup()` before its
# submodules can be imported.  This is done at module-load time, before any
# `from django.X import Y` line, so the proxy's submodule resolution works.

import pathlib

import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
        ],
    )
    django.setup()

import pytest  # noqa: E402

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def دجانغو():
    """Return a ModuleProxy wrapping `django`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("دجانغو", None, None)
    assert spec is not None, "AliasFinder did not find 'دجانغو'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestDjangoUrls:
    def test_path_alias(self, دجانغو):
        from django.urls import path

        assert دجانغو.مسار_رابط is path

    def test_re_path_alias(self, دجانغو):
        from django.urls import re_path

        assert دجانغو.مسار_تعبيري is re_path

    def test_include_alias(self, دجانغو):
        from django.urls import include

        assert دجانغو.ضمن_مسارات is include

    def test_reverse_alias(self, دجانغو):
        from django.urls import reverse

        assert دجانغو.اعكس_رابط is reverse

    def test_reverse_lazy_alias(self, دجانغو):
        from django.urls import reverse_lazy

        assert دجانغو.اعكس_رابط_كسلان is reverse_lazy


class TestDjangoHttp:
    def test_http_response_alias(self, دجانغو):
        from django.http import HttpResponse

        assert دجانغو.استجابه_http is HttpResponse

    def test_http_response_redirect_alias(self, دجانغو):
        from django.http import HttpResponseRedirect

        assert دجانغو.استجابه_تحويل is HttpResponseRedirect

    def test_http_response_not_found_alias(self, دجانغو):
        from django.http import HttpResponseNotFound

        assert دجانغو.استجابه_غير_موجود is HttpResponseNotFound

    def test_json_response_alias(self, دجانغو):
        from django.http import JsonResponse

        assert دجانغو.استجابه_json is JsonResponse

    def test_file_response_alias(self, دجانغو):
        from django.http import FileResponse

        assert دجانغو.استجابه_ملف is FileResponse

    def test_http404_alias(self, دجانغو):
        from django.http import Http404

        assert دجانغو.خطا_404 is Http404

    def test_streaming_http_response_alias(self, دجانغو):
        from django.http import StreamingHttpResponse

        assert دجانغو.استجابه_بث is StreamingHttpResponse


class TestDjangoShortcuts:
    def test_render_alias(self, دجانغو):
        from django.shortcuts import render

        assert دجانغو.اعرض_قالب is render

    def test_redirect_alias(self, دجانغو):
        from django.shortcuts import redirect

        assert دجانغو.اعد_توجيه is redirect

    def test_get_object_or_404_alias(self, دجانغو):
        from django.shortcuts import get_object_or_404

        assert دجانغو.اجلب_او_404 is get_object_or_404

    def test_get_list_or_404_alias(self, دجانغو):
        from django.shortcuts import get_list_or_404

        assert دجانغو.اجلب_قائمه_او_404 is get_list_or_404


class TestDjangoViews:
    def test_view_alias(self, دجانغو):
        from django.views import View

        assert دجانغو.صنف_عرض is View

    def test_list_view_alias(self, دجانغو):
        from django.views.generic import ListView

        assert دجانغو.عرض_قائمه is ListView

    def test_detail_view_alias(self, دجانغو):
        from django.views.generic import DetailView

        assert دجانغو.عرض_تفاصيل is DetailView

    def test_create_view_alias(self, دجانغو):
        from django.views.generic import CreateView

        assert دجانغو.عرض_انشاء is CreateView

    def test_update_view_alias(self, دجانغو):
        from django.views.generic import UpdateView

        assert دجانغو.عرض_تحديث is UpdateView

    def test_delete_view_alias(self, دجانغو):
        from django.views.generic import DeleteView

        assert دجانغو.عرض_حذف is DeleteView

    def test_form_view_alias(self, دجانغو):
        from django.views.generic import FormView

        assert دجانغو.عرض_نموذج is FormView

    def test_template_view_alias(self, دجانغو):
        from django.views.generic import TemplateView

        assert دجانغو.عرض_قالب is TemplateView

    def test_redirect_view_alias(self, دجانغو):
        from django.views.generic import RedirectView

        assert دجانغو.عرض_تحويل is RedirectView


class TestDjangoModels:
    def test_model_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.نموذج is models.Model

    def test_manager_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.مدير_نموذج is models.Manager

    def test_queryset_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.مجموعه_استعلام is models.QuerySet

    def test_charfield_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.حقل_نصي is models.CharField

    def test_textfield_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.حقل_نص_طويل is models.TextField

    def test_integerfield_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.حقل_عددي is models.IntegerField

    def test_floatfield_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.حقل_عشري is models.FloatField

    def test_booleanfield_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.حقل_منطقي is models.BooleanField

    def test_datefield_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.حقل_تاريخ is models.DateField

    def test_datetimefield_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.حقل_تاريخ_وقت is models.DateTimeField

    def test_timefield_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.حقل_وقت is models.TimeField

    def test_emailfield_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.حقل_بريد is models.EmailField

    def test_urlfield_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.حقل_رابط is models.URLField

    def test_slugfield_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.حقل_عنوان is models.SlugField

    def test_uuidfield_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.حقل_معرف_فريد is models.UUIDField

    def test_filefield_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.حقل_ملف is models.FileField

    def test_imagefield_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.حقل_صوره is models.ImageField

    def test_foreignkey_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.مفتاح_خارجي is models.ForeignKey

    def test_one_to_one_field_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.حقل_واحد_لواحد is models.OneToOneField

    def test_many_to_many_field_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.حقل_متعدد is models.ManyToManyField

    def test_cascade_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.تتالي is models.CASCADE

    def test_protect_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.احم is models.PROTECT

    def test_set_null_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.اضبط_فارغ is models.SET_NULL

    def test_do_nothing_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.لا_تفعل is models.DO_NOTHING

    def test_q_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.كائن_استعلام is models.Q

    def test_f_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.حقل_تعبير is models.F

    def test_value_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.قيمه_حرفيه is models.Value

    def test_expression_wrapper_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.تعبير_مغلف is models.ExpressionWrapper

    def test_count_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.عد_صفوف is models.Count

    def test_sum_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.مجموع_حقل is models.Sum

    def test_avg_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.متوسط_حقل is models.Avg

    def test_max_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.اعلي_حقل is models.Max

    def test_min_alias(self, دجانغو):
        from django.db import models

        assert دجانغو.ادني_حقل is models.Min


class TestDjangoForms:
    def test_form_alias(self, دجانغو):
        from django import forms

        assert دجانغو.نموذج_اساسي is forms.Form

    def test_modelform_alias(self, دجانغو):
        from django import forms

        assert دجانغو.نموذج_بيانات is forms.ModelForm

    def test_form_charfield_alias(self, دجانغو):
        from django import forms

        assert دجانغو.حقل_نموذج_نصي is forms.CharField

    def test_form_integerfield_alias(self, دجانغو):
        from django import forms

        assert دجانغو.حقل_نموذج_عددي is forms.IntegerField

    def test_form_emailfield_alias(self, دجانغو):
        from django import forms

        assert دجانغو.حقل_نموذج_بريد is forms.EmailField

    def test_form_choicefield_alias(self, دجانغو):
        from django import forms

        assert دجانغو.حقل_نموذج_خيار is forms.ChoiceField

    def test_form_multiple_choicefield_alias(self, دجانغو):
        from django import forms

        assert دجانغو.حقل_نموذج_خيارات is forms.MultipleChoiceField

    def test_form_booleanfield_alias(self, دجانغو):
        from django import forms

        assert دجانغو.حقل_نموذج_منطقي is forms.BooleanField

    def test_form_datefield_alias(self, دجانغو):
        from django import forms

        assert دجانغو.حقل_نموذج_تاريخ is forms.DateField

    def test_form_filefield_alias(self, دجانغو):
        from django import forms

        assert دجانغو.حقل_نموذج_ملف is forms.FileField


class TestDjangoSettingsApps:
    def test_settings_alias(self, دجانغو):
        from django.conf import settings as real_settings

        assert دجانغو.اعدادات is real_settings

    def test_app_config_alias(self, دجانغو):
        from django.apps import AppConfig

        assert دجانغو.اعداد_تطبيق is AppConfig


class TestDjangoExceptions:
    def test_object_does_not_exist_alias(self, دجانغو):
        from django.core.exceptions import ObjectDoesNotExist

        assert دجانغو.كائن_غير_موجود is ObjectDoesNotExist

    def test_multiple_objects_returned_alias(self, دجانغو):
        from django.core.exceptions import MultipleObjectsReturned

        assert دجانغو.تعدد_نتائج is MultipleObjectsReturned

    def test_validation_error_alias(self, دجانغو):
        from django.core.exceptions import ValidationError

        assert دجانغو.خطا_تحقق is ValidationError

    def test_permission_denied_alias(self, دجانغو):
        from django.core.exceptions import PermissionDenied

        assert دجانغو.ممنوع_صلاحيه is PermissionDenied

    def test_improperly_configured_alias(self, دجانغو):
        from django.core.exceptions import ImproperlyConfigured

        assert دجانغو.اعداد_خاطئ is ImproperlyConfigured


class TestDjangoSignals:
    def test_pre_save_alias(self, دجانغو):
        from django.db.models.signals import pre_save

        assert دجانغو.قبل_حفظ is pre_save

    def test_post_save_alias(self, دجانغو):
        from django.db.models.signals import post_save

        assert دجانغو.بعد_حفظ is post_save

    def test_pre_delete_alias(self, دجانغو):
        from django.db.models.signals import pre_delete

        assert دجانغو.قبل_حذف is pre_delete

    def test_post_delete_alias(self, دجانغو):
        from django.db.models.signals import post_delete

        assert دجانغو.بعد_حذف is post_delete


class TestDjangoWsgi:
    def test_wsgi_handler_alias(self, دجانغو):
        from django.core.handlers.wsgi import WSGIHandler

        assert دجانغو.معالج_wsgi is WSGIHandler

    def test_get_wsgi_application_alias(self, دجانغو):
        from django.core.wsgi import get_wsgi_application

        assert دجانغو.اجلب_تطبيق_wsgi is get_wsgi_application


class TestDjangoFunctional:
    """End-to-end smoke tests that build small artifacts via the Arabic aliases."""

    def test_path_builds_url_pattern(self, دجانغو):
        def view(request):
            return None

        pattern = دجانغو.مسار_رابط("hello/", view, name="hello")
        assert pattern.name == "hello"

    def test_http_response_body(self, دجانغو):
        resp = دجانغو.استجابه_http("hello")
        assert resp.status_code == 200
        assert resp.content == b"hello"

    def test_json_response_body(self, دجانغو):
        resp = دجانغو.استجابه_json({"k": 1})
        assert resp.status_code == 200
        assert resp["Content-Type"].startswith("application/json")

    def test_q_object_combination(self, دجانغو):
        q = دجانغو.كائن_استعلام(name="a") | دجانغو.كائن_استعلام(name="b")
        assert q.connector == "OR"

    def test_validation_error_raisable(self, دجانغو):
        with pytest.raises(دجانغو.خطا_تحقق):
            raise دجانغو.خطا_تحقق("bad")

    def test_settings_object_is_lazy(self, دجانغو):
        # Should be the same lazy settings object Django uses everywhere.
        from django.conf import settings as real_settings

        assert دجانغو.اعدادات is real_settings
        assert real_settings.configured  # we configured it at module load

    def test_charfield_accepts_max_length(self, دجانغو):
        f = دجانغو.حقل_نصي(max_length=50)
        assert f.max_length == 50

    def test_foreignkey_on_delete_cascade(self, دجانغو):
        # Building the field with the Arabic CASCADE alias must not raise.
        from django.db import models

        f = دجانغو.مفتاح_خارجي("self", on_delete=دجانغو.تتالي)
        assert f.remote_field.on_delete is models.CASCADE
