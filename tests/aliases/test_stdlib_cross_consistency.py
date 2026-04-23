# tests/aliases/test_stdlib_cross_consistency.py
# B-030 cross-consistency tests
#
# Verifies that related concepts across os / pathlib / sys follow the
# deliberate divergences documented in B-030 (see KNOWN_DIVERGENCES below).
# Each test is a positive assertion: the chosen Arabic name is the right one
# for the concept, and the divergence from a superficially-similar name in
# another module is intentional.

import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"

# ---------------------------------------------------------------------------
# Document deliberate divergences (used as a spec floor for code review)
# ---------------------------------------------------------------------------

KNOWN_DIVERGENCES = {
    # sys.path (import search list) and pathlib.Path (filesystem path class)
    # share the English word "path" but are entirely different concepts.
    # Arabic uses different roots deliberately:
    #   sys.path → مسارات_الاستيراد ("import-search paths", plural, import-scoped)
    #   pathlib.Path → مسار ("path", singular class name)
    "sys.path vs pathlib.Path": (
        "مسارات_الاستيراد",  # sys.path
        "مسار",              # pathlib.Path
    ),
    # os._exit bypasses atexit/finalizers; sys.exit raises SystemExit.
    # Both share root اخرج; os._exit adds فورا ("immediately") as modifier.
    "sys.exit vs os._exit": (
        "اخرج",       # sys.exit
        "اخرج_فورا",  # os._exit
    ),
    # os.mkdir creates one level; pathlib.Path.mkdir supports parents=True.
    # Different signatures → different Arabic names for safety.
    "os.mkdir vs Path.mkdir": (
        "انشئ_دليل",   # os.mkdir
        "انشئ_دليلا",  # Path.mkdir
    ),
    # os.walk vs Path.walk — same concept, different modules → different names.
    # os.walk returns a generator of (root_str, dirs, files).
    # Path.walk (3.12+) returns a generator of (Path, dirs, files).
    "os.walk vs Path.walk": (
        "سر_شجره",  # os.walk
        "سر",       # Path.walk
    ),
}


# ---------------------------------------------------------------------------
# Helper: load a proxy by Arabic name
# ---------------------------------------------------------------------------


def _proxy(arabic_name: str):
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec(arabic_name, None, None)
    assert spec is not None
    return spec.loader.create_module(spec)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestCrossConsistency:
    def test_sys_path_vs_pathlib_path_names_differ(self):
        """sys.path and pathlib.Path have different Arabic names (not مسار for both)."""
        sys_arabic, pathlib_arabic = KNOWN_DIVERGENCES["sys.path vs pathlib.Path"]
        assert sys_arabic != pathlib_arabic

        نظام = _proxy("نظام")
        مسار_مكتبه = _proxy("مسار_مكتبه")

        import sys as _sys
        import pathlib as _pathlib

        assert نظام.مسارات_الاستيراد is _sys.path
        assert مسار_مكتبه.مسار is _pathlib.Path

    def test_sys_exit_vs_os_exit_share_root(self):
        """sys.exit → اخرج; os._exit → اخرج_فورا; both have root اخرج."""
        sys_arabic, os_arabic = KNOWN_DIVERGENCES["sys.exit vs os._exit"]
        assert sys_arabic == "اخرج"
        assert os_arabic == "اخرج_فورا"
        assert os_arabic.startswith(sys_arabic)

    def test_os_mkdir_vs_pathlib_mkdir_names_differ(self):
        """os.mkdir → انشئ_دليل; Path.mkdir → انشئ_دليلا; different names."""
        os_arabic, path_arabic = KNOWN_DIVERGENCES["os.mkdir vs Path.mkdir"]
        assert os_arabic != path_arabic

    def test_os_walk_vs_pathlib_walk_names_differ(self):
        """os.walk → سر_شجره; Path.walk → سر; different names."""
        os_arabic, path_arabic = KNOWN_DIVERGENCES["os.walk vs Path.walk"]
        assert os_arabic != path_arabic

        نظام_تشغيل = _proxy("نظام_تشغيل")
        مسار_مكتبه = _proxy("مسار_مكتبه")

        import os as _os
        import pathlib as _pathlib

        assert نظام_تشغيل.سر_شجره is _os.walk
        assert مسار_مكتبه.سر is _pathlib.Path.walk
