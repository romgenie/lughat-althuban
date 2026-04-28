# tests/aliases/test_aiohttp.py
# B-059: Arabic aliases for aiohttp

import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"

aiohttp = pytest.importorskip("aiohttp", reason="aiohttp not installed")


@pytest.fixture(scope="module")
def طلبات_غير_متزامنه():
    from arabicpython.aliases._finder import AliasFinder
    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("طلبات_غير_متزامنه", None, None)
    assert spec is not None, "AliasFinder did not find 'طلبات_غير_متزامنه'"
    proxy = spec.loader.create_module(spec)
    return proxy


class TestAiohttpAliasesExist:
    def test_client_session(self, طلبات_غير_متزامنه):
        assert طلبات_غير_متزامنه.جلسه_غير_متزامنه is aiohttp.ClientSession

    def test_client_error(self, طلبات_غير_متزامنه):
        assert طلبات_غير_متزامنه.خطا_عميل is aiohttp.ClientError

    def test_client_response_error(self, طلبات_غير_متزامنه):
        assert طلبات_غير_متزامنه.خطا_استجابه is aiohttp.ClientResponseError

    def test_client_connection_error(self, طلبات_غير_متزامنه):
        assert طلبات_غير_متزامنه.خطا_اتصال_غير_متزامن is aiohttp.ClientConnectionError

    def test_client_timeout(self, طلبات_غير_متزامنه):
        assert طلبات_غير_متزامنه.مهله_عميل is aiohttp.ClientTimeout

    def test_tcp_connector(self, طلبات_غير_متزامنه):
        assert طلبات_غير_متزامنه.اعدادات_اتصال is aiohttp.TCPConnector

    def test_basic_auth(self, طلبات_غير_متزامنه):
        assert طلبات_غير_متزامنه.ترميز_عنوان is aiohttp.BasicAuth

    def test_form_data(self, طلبات_غير_متزامنه):
        assert طلبات_غير_متزامنه.بيانات_متعدده is aiohttp.FormData

    def test_stream_reader(self, طلبات_غير_متزامنه):
        assert طلبات_غير_متزامنه.قارئ_مجري is aiohttp.StreamReader


class TestAiohttpTomlMeta:
    def test_toml_parseable(self):
        import tomllib
        p = ALIASES_DIR / "aiohttp.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert data["meta"]["python_module"] == "aiohttp"
        assert data["meta"]["arabic_name"] == "طلبات_غير_متزامنه"

    def test_entry_count(self):
        import tomllib
        p = ALIASES_DIR / "aiohttp.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert len(data["entries"]) >= 8
