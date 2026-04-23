"""Integration tests for B-001: Arabic alias mapping for the `requests` library.

These tests verify that ``requests.toml`` is correctly parsed and that the
ModuleProxy surfaces the right Python objects under their Arabic names.

Skipped automatically when `requests` is not installed (e.g. in a minimal
CI environment).  No actual HTTP calls are made; every assertion is local.
"""

from __future__ import annotations

import sys
import types
from pathlib import Path

import pytest

requests = pytest.importorskip("requests", reason="requests not installed — skipping integration tests")

from arabicpython.aliases import AliasFinder, ModuleProxy, install, uninstall  # noqa: E402


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
