# tests/aliases/test_requests.py
# B-014: Arabic aliases for requests

import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"

requests = pytest.importorskip("requests", reason="requests not installed")


@pytest.fixture(scope="module")
def طلبات():
    from arabicpython.aliases._finder import AliasFinder
    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("طلبات", None, None)
    assert spec is not None, "AliasFinder did not find 'طلبات'"
    return spec.loader.create_module(spec)


class TestHttpVerbs:
    def test_get(self, طلبات):
        assert طلبات.احصل is requests.get

    def test_post(self, طلبات):
        assert طلبات.نشر is requests.post

    def test_put(self, طلبات):
        assert طلبات.ضع is requests.put

    def test_delete(self, طلبات):
        assert طلبات.احذف is requests.delete

    def test_patch(self, طلبات):
        assert طلبات.عدل is requests.patch

    def test_head(self, طلبات):
        assert طلبات.راس is requests.head

    def test_options(self, طلبات):
        assert طلبات.خيارات is requests.options

    def test_request(self, طلبات):
        assert طلبات.اطلب is requests.request


class TestClasses:
    def test_session(self, طلبات):
        assert طلبات.جلسه is requests.Session

    def test_response(self, طلبات):
        assert طلبات.استجابه is requests.Response

    def test_request_class(self, طلبات):
        assert طلبات.طلب is requests.Request


class TestExceptions:
    def test_connection_error(self, طلبات):
        assert طلبات.خطا_اتصال is requests.ConnectionError

    def test_timeout(self, طلبات):
        assert طلبات.خطا_مهله is requests.Timeout

    def test_http_error(self, طلبات):
        assert طلبات.خطا_بروتوكول is requests.HTTPError

    def test_request_exception(self, طلبات):
        assert طلبات.خطا_طلب is requests.RequestException

    def test_too_many_redirects(self, طلبات):
        assert طلبات.خطا_كثير_تحويلات is requests.TooManyRedirects


class TestUtilities:
    def test_codes(self, طلبات):
        assert طلبات.رموز_الحاله is requests.codes

    def test_utils(self, طلبات):
        assert طلبات.ادوات is requests.utils

    def test_adapters(self, طلبات):
        assert طلبات.محولات is requests.adapters


class TestTomlMeta:
    def test_toml_parseable(self):
        import tomllib
        p = ALIASES_DIR / "requests.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert data["meta"]["python_module"] == "requests"
        assert data["meta"]["arabic_name"] == "طلبات"

    def test_entry_count(self):
        import tomllib
        p = ALIASES_DIR / "requests.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert len(data["entries"]) >= 20
