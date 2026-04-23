# tests/aliases/test_pathlib.py
# B-030 stdlib aliases — pathlib module tests
#
# pathlib exposes only 7 module-level names; all other entries use dotted
# paths (e.g., "Path.exists") and resolve to *unbound* methods.
# Tests call unbound methods with an explicit Path instance:
#   مسار_مكتبه.موجود(p)  ≡  pathlib.Path.exists(p)

import pathlib
import sys

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def مسار_مكتبه():
    """Return a ModuleProxy wrapping `pathlib` via the real pathlib.toml mapping."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("مسار_مكتبه", None, None)
    assert spec is not None, "AliasFinder did not find 'مسار_مكتبه'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestPathlibProxy:
    def test_path_class_alias(self, مسار_مكتبه):
        """مسار maps to pathlib.Path (the class itself)."""
        assert مسار_مكتبه.مسار is pathlib.Path

    def test_exists_unbound(self, مسار_مكتبه, tmp_path):
        """موجود is an unbound method; calling it with a Path instance works."""
        p = pathlib.Path(tmp_path)
        assert مسار_مكتبه.موجود(p) is True
        missing = pathlib.Path(tmp_path / "no_such_file.txt")
        assert مسار_مكتبه.موجود(missing) is False

    def test_is_dir_unbound(self, مسار_مكتبه, tmp_path):
        """هل_دليل is an unbound method wrapping Path.is_dir."""
        assert مسار_مكتبه.هل_دليل(pathlib.Path(tmp_path)) is True
        f = tmp_path / "f.txt"
        f.touch()
        assert مسار_مكتبه.هل_دليل(f) is False

    def test_read_write_text_unbound(self, مسار_مكتبه, tmp_path):
        """اكتب_نص / اقرا_نص round-trip through unbound methods."""
        p = pathlib.Path(tmp_path / "hello.txt")
        مسار_مكتبه.اكتب_نص(p, "مرحبا", encoding="utf-8")
        content = مسار_مكتبه.اقرا_نص(p, encoding="utf-8")
        assert content == "مرحبا"

    def test_mkdir_unbound(self, مسار_مكتبه, tmp_path):
        """انشئ_دليلا wraps Path.mkdir; parents=True works."""
        new_dir = pathlib.Path(tmp_path / "a" / "b")
        مسار_مكتبه.انشئ_دليلا(new_dir, parents=True, exist_ok=True)
        assert new_dir.is_dir()

    @pytest.mark.skipif(sys.version_info < (3, 12), reason="Path.walk requires Python 3.12+")
    def test_walk_unbound(self, مسار_مكتبه, tmp_path):
        """سر wraps Path.walk (Python 3.12+); yields (root, dirs, files)."""
        (tmp_path / "sub").mkdir()
        (tmp_path / "sub" / "f.txt").touch()
        entries = list(مسار_مكتبه.سر(pathlib.Path(tmp_path)))
        roots = [str(e[0]) for e in entries]
        assert str(tmp_path) in roots

    def test_posixpath_class_alias(self, مسار_مكتبه):
        """مسار_بحت maps to pathlib.PurePath."""
        assert مسار_مكتبه.مسار_بحت is pathlib.PurePath
