import importlib
import pathlib
import sys

import pytest

from arabicpython.import_hook import ApyLoader, install, uninstall


@pytest.fixture(autouse=True)
def restore_import_state():
    """Snapshot sys.meta_path, sys.modules, sys.path before each test; restore after."""
    saved_meta_path = sys.meta_path[:]
    saved_modules = dict(sys.modules)
    saved_path = sys.path[:]
    try:
        yield
    finally:
        sys.meta_path[:] = saved_meta_path
        # Remove anything added during the test
        for name in list(sys.modules):
            if name not in saved_modules:
                del sys.modules[name]
        sys.path[:] = saved_path
        importlib.invalidate_caches()


@pytest.fixture
def fixtures_on_path():
    fdir = str(pathlib.Path(__file__).parent / "fixtures")
    sys.path.insert(0, fdir)
    yield fdir


# Install / uninstall (4)


def test_install_adds_finder_to_meta_path():
    from arabicpython.import_hook import ApyFinder

    install()
    assert any(isinstance(f, ApyFinder) for f in sys.meta_path)


def test_install_is_idempotent():
    from arabicpython.import_hook import ApyFinder

    install()
    install()
    finders = [f for f in sys.meta_path if isinstance(f, ApyFinder)]
    assert len(finders) == 1


def test_uninstall_removes_finder():
    from arabicpython.import_hook import ApyFinder

    install()
    uninstall()
    assert not any(isinstance(f, ApyFinder) for f in sys.meta_path)


def test_uninstall_is_idempotent():
    uninstall()
    uninstall()
    # Should not raise


# Basic imports — module discovery (5)


def test_import_standalone_apy(fixtures_on_path):
    install()
    import standalone  # noqa: F401

    # normalized قيمة -> قيمه
    assert standalone.قيمه == 42
    # normalized هات_القيمة -> هات_القيمه
    assert standalone.هات_القيمه() == 42


def test_import_apy_from_apy(fixtures_on_path):
    install()
    import importer  # noqa: F401

    # normalized هات_قيمة_مستوردة -> هات_قيمة_مستورده
    assert importer.هات_قيمة_مستورده() == 42


def test_import_apy_from_py(fixtures_on_path, tmp_path):
    install()
    py_file = tmp_path / "importer_py.py"
    # use normalized name in py source
    py_file.write_text("import standalone\nval = standalone.قيمه\n", encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    import importer_py  # noqa: F401

    assert importer_py.val == 42


def test_no_install_means_no_apy_imports(fixtures_on_path):
    uninstall()  # Ensure clean state if prior tests didn't clean up correctly
    with pytest.raises(ModuleNotFoundError):
        import standalone  # noqa: F401


def test_finder_returns_none_for_missing_module(fixtures_on_path):
    install()
    with pytest.raises(ModuleNotFoundError):
        import nonexistent_module_xyz  # noqa: F401


# Packages (4)


def test_import_apy_package(fixtures_on_path):
    install()
    import apkg  # noqa: F401

    assert hasattr(apkg, "__path__")
    assert apkg.قائمة_عناصر == [1, 2, 3]


def test_import_apy_submodule(fixtures_on_path):
    install()
    import apkg.sub  # noqa: F401

    assert "apkg" in sys.modules
    assert "apkg.sub" in sys.modules
    # normalized اسم_الوحدة -> اسم_الوحده
    assert apkg.sub.اسم_الوحده == "فرعية"


def test_from_apkg_import_sub(fixtures_on_path):
    install()
    from apkg import sub  # noqa: F401

    assert sub.اسم_الوحده == "فرعية"


def test_mixed_package_apy_submodule(fixtures_on_path):
    install()
    import mixed.leaf  # noqa: F401

    assert mixed.leaf.قيمة_الورقه == "ورقة"


# Module attributes (4)


def test_imported_module_has_correct_name(fixtures_on_path):
    install()
    import standalone  # noqa: F401

    assert standalone.__name__ == "standalone"


def test_imported_module_has_absolute_file(fixtures_on_path):
    install()
    import standalone  # noqa: F401

    assert pathlib.Path(standalone.__file__).is_absolute()
    assert standalone.__file__.endswith("standalone.apy")


def test_imported_package_has_path(fixtures_on_path):
    install()
    import apkg  # noqa: F401

    assert isinstance(apkg.__path__, list)
    assert any(p.endswith("apkg") for p in apkg.__path__)


def test_imported_module_loader_is_apy_loader(fixtures_on_path):
    install()
    import standalone  # noqa: F401

    from arabicpython.import_hook import ApyLoader

    assert isinstance(standalone.__loader__, ApyLoader)


# Relative imports (2)


def test_relative_import_in_apy_package(fixtures_on_path):
    install()
    import apkg  # noqa: F401

    assert hasattr(apkg, "sub")
    # normalized اسم_الوحدة -> اسم_الوحده
    assert apkg.sub.اسم_الوحده == "فرعية"


def test_relative_import_dotted(fixtures_on_path):
    # This is handled by apkg/__init__.apy which does 'import apkg.sub as sub'
    install()
    import apkg  # noqa: F401

    # normalized اسم_الوحدة -> اسم_الوحده
    assert apkg.sub.اسم_الوحده == "فرعية"


# Caching and reload (3)


def test_import_uses_sys_modules_cache(fixtures_on_path):
    install()
    import standalone  # noqa: F401
    import standalone as standalone2

    assert standalone is standalone2


def test_importlib_reload_re_executes(fixtures_on_path):
    install()
    import standalone

    original_source = pathlib.Path(standalone.__file__).read_text(encoding="utf-8")
    try:
        pathlib.Path(standalone.__file__).write_text("قيمه = 100\n", encoding="utf-8")
        importlib.reload(standalone)
        assert standalone.قيمه == 100
    finally:
        pathlib.Path(standalone.__file__).write_text(original_source, encoding="utf-8")


def test_no_pycache_for_apy(fixtures_on_path, tmp_path):
    apy_source = (pathlib.Path(fixtures_on_path) / "standalone.apy").read_text(encoding="utf-8")
    test_apy = tmp_path / "to_cache.apy"
    test_apy.write_text(apy_source, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    install()
    import to_cache

    assert to_cache.قيمه == 42
    pycache = tmp_path / "__pycache__"
    assert not pycache.exists()


# Error handling (5)


def test_apy_with_bidi_raises_syntax_error(tmp_path):
    bidi_file = tmp_path / "bidi.apy"
    bidi_file.write_text("\u202e", encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    install()
    with pytest.raises(SyntaxError) as exc:
        import bidi  # noqa: F401

    assert "bidi control" in str(exc.value)
    assert exc.value.filename == str(bidi_file)


def test_apy_with_translated_python_syntax_error(tmp_path):
    bad_file = tmp_path / "bad.apy"
    # 'إذا صحيح:' in Arabic will be 'if True:' which needs a body.
    bad_file.write_text("إذا صحيح:\n", encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    install()
    with pytest.raises(SyntaxError) as exc:
        import bad  # noqa: F401

    assert exc.value.filename == str(bad_file)


def test_apy_runtime_error_in_module_import(tmp_path):
    err_file = tmp_path / "runtime_err.apy"
    err_file.write_text("x = ١ / ٠\n", encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    install()
    with pytest.raises(ZeroDivisionError):
        import runtime_err  # noqa: F401


def test_unreadable_apy_raises_import_error(tmp_path, monkeypatch):
    install()
    vanished = tmp_path / "vanished.apy"
    vanished.write_text("pass\n", encoding="utf-8")
    sys.path.insert(0, str(tmp_path))

    import builtins

    original_open = builtins.open

    def mock_open(path, *args, **kwargs):
        if str(path) == str(vanished):
            raise FileNotFoundError()
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", mock_open)

    with pytest.raises(ImportError):
        import vanished  # noqa: F401


def test_non_utf8_apy_raises_import_error(tmp_path):
    bad_file = tmp_path / "latin1.apy"
    bad_file.write_bytes(b"\xe0\xe1\xe2")
    sys.path.insert(0, str(tmp_path))
    install()
    with pytest.raises(ImportError) as exc:
        import latin1  # noqa: F401

    assert "decode" in str(exc.value)


# Search order and edge cases (3)


def test_apy_wins_over_py_when_both_present(tmp_path):
    (tmp_path / "both.apy").write_text("marker = 'apy'\n", encoding="utf-8")
    (tmp_path / "both.py").write_text("marker = 'py'\n", encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    install()
    import both

    assert both.marker == "apy"


def test_apy_does_not_shadow_stdlib(tmp_path):
    install()
    import os

    assert "os" in sys.modules
    assert not hasattr(os, "__loader__") or not isinstance(os.__loader__, ApyLoader)


def test_get_source_returns_original_apy(fixtures_on_path):
    install()
    import standalone

    source = standalone.__loader__.get_source("standalone")
    assert "دالة" in source
    assert "قيمة" in source


# CLI integration (1)


def test_cli_installs_hook(tmp_path, capsys):
    from arabicpython import cli

    main_apy = tmp_path / "main_run.apy"
    helper_apy = tmp_path / "helper.apy"
    main_apy.write_text("import helper\nاطبع(helper.هات_تحية())\n", encoding="utf-8")
    helper_apy.write_text("دالة هات_تحية():\n    ارجع 'مرحبا'\n", encoding="utf-8")

    # We must add tmp_path to sys.path manually since CLI doesn't do it yet.
    sys.path.insert(0, str(tmp_path))

    ret = cli.main([str(main_apy)])
    assert ret == 0
    out, err = capsys.readouterr()
    assert "مرحبا" in out
