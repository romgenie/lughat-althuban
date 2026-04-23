# tests/aliases/test_sys.py
# B-030 stdlib aliases — sys module tests

import pathlib
import sys

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def نظام():
    """Return a ModuleProxy wrapping `sys` via the real sys.toml mapping."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("نظام", None, None)
    assert spec is not None, "AliasFinder did not find 'نظام'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestSysProxy:
    def test_argv_alias(self, نظام):
        """الوسائط maps to sys.argv (the same list object)."""
        assert نظام.الوسائط is sys.argv

    def test_path_alias(self, نظام):
        """مسارات_الاستيراد maps to sys.path (the same list object)."""
        assert نظام.مسارات_الاستيراد is sys.path

    def test_version_alias(self, نظام):
        """الاصدار maps to sys.version (a non-empty string)."""
        v = نظام.الاصدار
        assert isinstance(v, str)
        assert len(v) > 0

    def test_platform_alias(self, نظام):
        """المنصه maps to sys.platform."""
        assert نظام.المنصه == sys.platform

    def test_getrecursionlimit_alias(self, نظام):
        """حد_العوديه maps to sys.getrecursionlimit; returns a positive int."""
        limit = نظام.حد_العوديه()
        assert isinstance(limit, int)
        assert limit > 0

    def test_stdout_alias(self, نظام):
        """معيار_الاخراج maps to sys.stdout."""
        assert نظام.معيار_الاخراج is sys.stdout
