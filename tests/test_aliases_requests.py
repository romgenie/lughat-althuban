"""Integration tests for B-001: Arabic alias mapping for the `requests` library.

These tests verify that ``requests.toml`` is correctly parsed and that the
ModuleProxy surfaces the right Python objects under their Arabic names.

Skipped automatically when `requests` is not installed (e.g. in a minimal
CI environment).  No actual HTTP calls are made; every assertion is local.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

requests = pytest.importorskip(
    "requests", reason="requests not installed — skipping integration tests"
)

from arabicpython.aliases import AliasFinder, ModuleProxy  # noqa: E402

# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

ALIASES_DIR = Path(__file__).parent.parent / "arabicpython" / "aliases"


@pytest.fixture()
def requests_finder() -> AliasFinder:
    """An AliasFinder pointed at the real arabicpython/aliases/ directory."""
    return AliasFinder(mappings_dir=ALIASES_DIR)


@pytest.fixture()
def طلبات(requests_finder: AliasFinder) -> ModuleProxy:
    """The Arabic proxy for the `requests` module, loaded from requests.toml."""
    spec = requests_finder.find_spec("طلبات")
    assert spec is not None, "requests.toml must register 'طلبات'"
    assert spec.loader is not None
    proxy = spec.loader.create_module(spec)
    return proxy


@pytest.fixture()
def clean_meta_path():
    original = list(sys.meta_path)
    yield
    sys.meta_path[:] = original


# ─────────────────────────────────────────────────────────────────────────────
# Integration tests — 7
# ─────────────────────────────────────────────────────────────────────────────


def test_requests_toml_registers_arabic_name(requests_finder: AliasFinder) -> None:
    """requests.toml must register the Arabic alias 'طلبات' in the finder."""
    assert "طلبات" in requests_finder._arabic_to_mapping
    mapping = requests_finder._arabic_to_mapping["طلبات"]
    assert mapping.python_module == "requests"


def test_requests_get_maps_to_requests_get(طلبات: ModuleProxy) -> None:
    """Arabic 'احصل' must resolve to the same object as requests.get."""
    assert طلبات.احصل is requests.get


def test_requests_post_maps_to_requests_post(طلبات: ModuleProxy) -> None:
    """Arabic 'نشر' must resolve to the same object as requests.post."""
    assert طلبات.نشر is requests.post


def test_requests_session_class(طلبات: ModuleProxy) -> None:
    """Arabic 'جلسه' must resolve to requests.Session."""
    assert طلبات.جلسه is requests.Session


def test_requests_dotted_path_http_adapter(طلبات: ModuleProxy) -> None:
    """'محول_http' uses a dotted path 'adapters.HTTPAdapter'; must resolve correctly."""
    import requests.adapters  # ensure sub-module is loaded

    assert طلبات.محول_http is requests.adapters.HTTPAdapter


def test_requests_connection_error_exception(طلبات: ModuleProxy) -> None:
    """Arabic 'خطا_اتصال' must resolve to requests.ConnectionError."""
    assert طلبات.خطا_اتصال is requests.ConnectionError


def test_requests_proxy_dir_and_repr(طلبات: ModuleProxy) -> None:
    """dir(proxy) must contain Arabic keys; repr must mention 'requests' and 'طلبات'."""
    d = dir(طلبات)
    assert "احصل" in d
    assert "نشر" in d
    assert "جلسه" in d

    r = repr(طلبات)
    assert "requests" in r
    assert "طلبات" in r


# ─────────────────────────────────────────────────────────────────────────────
# B-014 extras — auth, exceptions, structures
# ─────────────────────────────────────────────────────────────────────────────


class TestB014Auth:
    def test_auth_base(self, طلبات):
        import requests.auth

        assert طلبات.مصادقه_قاعده is requests.auth.AuthBase

    def test_http_proxy_auth(self, طلبات):
        import requests.auth

        assert طلبات.مصادقه_وكيل is requests.auth.HTTPProxyAuth

    def test_custom_auth_subclass(self, طلبات):
        """AuthBase is actually usable as a base class."""

        class MyAuth(طلبات.مصادقه_قاعده):
            def __call__(self, r):
                return r

        import requests

        s = requests.Session()
        s.auth = MyAuth()
        assert isinstance(s.auth, طلبات.مصادقه_قاعده)


class TestB014Exceptions:
    def test_proxy_error(self, طلبات):
        import requests.exceptions

        assert طلبات.خطا_وكيل is requests.exceptions.ProxyError

    def test_chunked_encoding_error(self, طلبات):
        import requests.exceptions

        assert طلبات.خطا_ترميز_مقطع is requests.exceptions.ChunkedEncodingError

    def test_content_decoding_error(self, طلبات):
        import requests.exceptions

        assert طلبات.خطا_فك_محتوي is requests.exceptions.ContentDecodingError

    def test_retry_error(self, طلبات):
        import requests.exceptions

        assert طلبات.خطا_اعاده_محاوله is requests.exceptions.RetryError

    def test_stream_consumed_error(self, طلبات):
        import requests.exceptions

        assert طلبات.خطا_بث_مستهلك is requests.exceptions.StreamConsumedError

    def test_invalid_schema_error(self, طلبات):
        import requests.exceptions

        assert طلبات.خطا_المخطط is requests.exceptions.InvalidSchema

    def test_json_decode_error(self, طلبات):
        import requests.exceptions

        assert طلبات.خطا_json is requests.exceptions.JSONDecodeError

    def test_invalid_proxy_url_error(self, طلبات):
        import requests.exceptions

        assert طلبات.خطا_رابط_وكيل is requests.exceptions.InvalidProxyURL

    def test_cookie_conflict_error(self, طلبات):
        import requests.cookies

        assert طلبات.خطا_كوكيز is requests.cookies.CookieConflictError

    def test_unwindable_body_error(self, طلبات):
        import requests.exceptions

        assert طلبات.خطا_جسم is requests.exceptions.UnrewindableBodyError

    def test_exception_hierarchy(self, طلبات):
        """ChunkedEncodingError, ContentDecodingError, RetryError all inherit RequestException."""
        assert issubclass(طلبات.خطا_ترميز_مقطع, طلبات.خطا_طلب)
        assert issubclass(طلبات.خطا_فك_محتوي, طلبات.خطا_طلب)
        assert issubclass(طلبات.خطا_اعاده_محاوله, طلبات.خطا_طلب)


class TestB014Structures:
    def test_case_insensitive_dict(self, طلبات):
        import requests.structures

        assert طلبات.قاموس_غير_حساس is requests.structures.CaseInsensitiveDict

    def test_lookup_dict(self, طلبات):
        import requests.structures

        assert طلبات.قاموس_بحث is requests.structures.LookupDict

    def test_requests_cookie_jar(self, طلبات):
        import requests.cookies

        assert طلبات.وعاء_كوكيز is requests.cookies.RequestsCookieJar

    def test_case_insensitive_dict_functional(self, طلبات):
        """CaseInsensitiveDict should treat keys case-insensitively."""
        headers = طلبات.قاموس_غير_حساس({"Content-Type": "application/json"})
        assert headers["content-type"] == "application/json"
        assert headers["CONTENT-TYPE"] == "application/json"


class TestB014SessionFactory:
    def test_session_factory_function(self, طلبات):
        import requests

        assert طلبات.انشئ_جلسه is requests.session

    def test_session_factory_creates_session(self, طلبات):
        import requests

        s = طلبات.انشئ_جلسه()
        assert isinstance(s, requests.Session)
        s.close()
