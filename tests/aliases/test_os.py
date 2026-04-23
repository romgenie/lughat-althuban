# tests/aliases/test_os.py
# B-030 stdlib aliases — os module tests
#
# All tests import نظام_تشغيل through the AliasFinder using the real
# arabicpython/aliases/os.toml file. No mocking; if the TOML is wrong these
# fail, which is the point.

import os
import pathlib
import sys

import pytest

# ---------------------------------------------------------------------------
# Fixture: obtain the proxy via the real finder + loader
# ---------------------------------------------------------------------------

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def نظام_تشغيل():
    """Return a ModuleProxy wrapping `os` via the real os.toml mapping."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("نظام_تشغيل", None, None)
    assert spec is not None, "AliasFinder did not find 'نظام_تشغيل'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestOsProxy:
    def test_getcwd_alias(self, نظام_تشغيل):
        """الدليل_الحالي maps to os.getcwd and returns a non-empty string."""
        result = نظام_تشغيل.الدليل_الحالي()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_listdir_alias(self, نظام_تشغيل, tmp_path):
        """اسرد_الدليل maps to os.listdir and lists directory contents."""
        (tmp_path / "a.txt").touch()
        (tmp_path / "b.txt").touch()
        entries = نظام_تشغيل.اسرد_الدليل(str(tmp_path))
        assert set(entries) == {"a.txt", "b.txt"}

    def test_mkdir_rmdir_aliases(self, نظام_تشغيل, tmp_path):
        """انشئ_دليل / احذف_دليل map to os.mkdir / os.rmdir."""
        new_dir = tmp_path / "test_subdir"
        نظام_تشغيل.انشئ_دليل(str(new_dir))
        assert new_dir.is_dir()
        نظام_تشغيل.احذف_دليل(str(new_dir))
        assert not new_dir.exists()

    def test_environ_alias(self, نظام_تشغيل):
        """متغيرات_البيئه maps to os.environ (a live mapping)."""
        env = نظام_تشغيل.متغيرات_البيئه
        assert env is os.environ

    def test_sep_alias(self, نظام_تشغيل):
        """فاصل_المسار maps to os.sep (a string constant)."""
        assert نظام_تشغيل.فاصل_المسار == os.sep

    def test_walk_alias(self, نظام_تشغيل, tmp_path):
        """سر_شجره maps to os.walk; yields (root, dirs, files) tuples."""
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "f.txt").touch()
        entries = list(نظام_تشغيل.سر_شجره(str(tmp_path)))
        # Should yield at least the root and the sub directory
        roots = [e[0] for e in entries]
        assert str(tmp_path) in roots
