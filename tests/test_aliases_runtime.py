"""Unit tests for B-001 alias runtime: ModuleProxy, AliasFinder, and load_mapping.

Test groups
-----------
ModuleProxy (10 tests):  proxy attribute routing, dir, repr, isinstance
AliasFinder  (8 tests):  TOML loading, find_spec, install/uninstall lifecycle
Loader       (7 tests):  load_mapping validation paths, AliasMapping frozen
"""

from __future__ import annotations

import importlib
import sys
import tempfile
import types
import warnings
from pathlib import Path

import pytest

from arabicpython.aliases import (
    AliasFinder,
    AliasMappingError,
    ModuleProxy,
    install,
    load_mapping,
    uninstall,
)

# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "aliases"


@pytest.fixture()
def sys_proxy() -> ModuleProxy:
    """A ModuleProxy wrapping `sys` with a two-entry mapping."""
    return ModuleProxy(sys, {"وسائط": "argv", "مسارات": "path"}, arabic_name="نظام")


@pytest.fixture()
def clean_meta_path():
    """Restore sys.meta_path to its original state after each test."""
    original = list(sys.meta_path)
    yield
    sys.meta_path[:] = original


@pytest.fixture()
def temp_mappings_dir(tmp_path: Path) -> Path:
    """A temporary directory pre-populated with a valid minimal TOML."""
    toml_content = """\
[meta]
arabic_name   = "نظام"
python_module = "sys"
dict_version  = "ar-v1"
schema_version = 1
maintainer    = "—"

[entries]
"وسائط" = "argv"
"مسارات" = "path"
"""
    (tmp_path / "sys_test.toml").write_text(toml_content, encoding="utf-8")
    return tmp_path


# ─────────────────────────────────────────────────────────────────────────────
# ModuleProxy — 10 tests
# ─────────────────────────────────────────────────────────────────────────────


def test_proxy_mapped_arabic_returns_correct_attribute(sys_proxy: ModuleProxy) -> None:
    """Arabic key in mapping should return the corresponding Python attribute value."""
    assert sys_proxy.وسائط is sys.argv


def test_proxy_second_mapped_arabic_key(sys_proxy: ModuleProxy) -> None:
    """A second Arabic key should also resolve correctly."""
    assert sys_proxy.مسارات is sys.path


def test_proxy_english_fallthrough(sys_proxy: ModuleProxy) -> None:
    """An unmapped ASCII name should fall through to the wrapped module unchanged."""
    assert sys_proxy.version is sys.version


def test_proxy_dotted_path_resolution() -> None:
    """An entry with a dotted path like 'adapters.HTTPAdapter' is resolved step-by-step."""
    import os
    # Use os.path.sep as the dotted target — a real stdlib dotted attribute
    proxy = ModuleProxy(os, {"فاصل": "path.sep"}, arabic_name="نظام_الملفات")
    assert proxy.فاصل == os.path.sep


def test_proxy_unmapped_arabic_raises_attribute_error(sys_proxy: ModuleProxy) -> None:
    """An unmapped Arabic name must raise AttributeError."""
    with pytest.raises(AttributeError, match="مجهول"):
        _ = sys_proxy.مجهول


def test_proxy_unmapped_arabic_emits_deprecation_warning(sys_proxy: ModuleProxy) -> None:
    """An unmapped Arabic name must emit DeprecationWarning before raising."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with pytest.raises(AttributeError):
            _ = sys_proxy.مجهول
    assert len(caught) == 1
    assert issubclass(caught[0].category, DeprecationWarning)
    assert "مجهول" in str(caught[0].message)


def test_proxy_dir_contains_arabic_keys(sys_proxy: ModuleProxy) -> None:
    """dir() on the proxy should include Arabic keys from the mapping."""
    d = dir(sys_proxy)
    assert "وسائط" in d
    assert "مسارات" in d


def test_proxy_dir_contains_wrapped_module_attrs(sys_proxy: ModuleProxy) -> None:
    """dir() on the proxy should also include English attrs from the wrapped module."""
    d = dir(sys_proxy)
    assert "version" in d
    assert "argv" in d


def test_proxy_repr(sys_proxy: ModuleProxy) -> None:
    """repr() should mention the wrapped module name and the Arabic name."""
    r = repr(sys_proxy)
    assert "sys" in r
    assert "نظام" in r


def test_proxy_isinstance_module_type(sys_proxy: ModuleProxy) -> None:
    """isinstance(proxy, types.ModuleType) must return True (reflexivity via __class__)."""
    assert isinstance(sys_proxy, types.ModuleType)


# ─────────────────────────────────────────────────────────────────────────────
# AliasFinder — 8 tests
# ─────────────────────────────────────────────────────────────────────────────


def test_finder_loads_toml_from_custom_dir(temp_mappings_dir: Path) -> None:
    """AliasFinder should discover and load the TOML file from the given directory."""
    finder = AliasFinder(mappings_dir=temp_mappings_dir)
    # "نظام" is the arabic_name in the fixture
    assert "نظام" in finder._arabic_to_mapping


def test_finder_find_spec_returns_spec_for_known_name(temp_mappings_dir: Path) -> None:
    """find_spec should return a ModuleSpec when the fullname is a registered Arabic alias."""
    finder = AliasFinder(mappings_dir=temp_mappings_dir)
    spec = finder.find_spec("نظام")
    assert spec is not None
    assert spec.name == "نظام"


def test_finder_find_spec_returns_none_for_unknown_name(temp_mappings_dir: Path) -> None:
    """find_spec should return None for a name not in the mapping table."""
    finder = AliasFinder(mappings_dir=temp_mappings_dir)
    assert finder.find_spec("requests") is None
    assert finder.find_spec("مجهول_تمام") is None


def test_finder_reload_mappings_picks_up_new_file(temp_mappings_dir: Path) -> None:
    """reload_mappings() should make a newly added TOML visible."""
    finder = AliasFinder(mappings_dir=temp_mappings_dir)
    assert "مجلد" not in finder._arabic_to_mapping

    new_toml = """\
[meta]
arabic_name   = "مجلد"
python_module = "os"
dict_version  = "ar-v1"
schema_version = 1
maintainer    = "—"

[entries]
"ربط" = "getcwd"
"""
    (temp_mappings_dir / "os_test.toml").write_text(new_toml, encoding="utf-8")
    finder.reload_mappings()
    assert "مجلد" in finder._arabic_to_mapping


def test_install_appends_finder_to_meta_path(clean_meta_path) -> None:
    """install() should add exactly one AliasFinder to sys.meta_path."""
    uninstall()  # ensure clean state
    before = len(sys.meta_path)
    install()
    finders = [f for f in sys.meta_path if isinstance(f, AliasFinder)]
    assert len(finders) == 1
    assert len(sys.meta_path) == before + 1


def test_install_is_idempotent(clean_meta_path) -> None:
    """Calling install() twice should not add a second AliasFinder."""
    uninstall()
    install()
    install()  # second call — must be a no-op
    finders = [f for f in sys.meta_path if isinstance(f, AliasFinder)]
    assert len(finders) == 1


def test_uninstall_removes_finder(clean_meta_path) -> None:
    """uninstall() should remove all AliasFinder instances from sys.meta_path."""
    install()
    uninstall()
    finders = [f for f in sys.meta_path if isinstance(f, AliasFinder)]
    assert finders == []


def test_finder_silently_skips_broken_toml(tmp_path: Path) -> None:
    """AliasFinder must not raise if a TOML in its directory is malformed."""
    (tmp_path / "broken.toml").write_text("NOT VALID TOML [\x00", encoding="utf-8")
    # Should not raise — broken file is silently ignored
    finder = AliasFinder(mappings_dir=tmp_path)
    assert finder._arabic_to_mapping == {}


# ─────────────────────────────────────────────────────────────────────────────
# Loader / load_mapping — 7 tests
# ─────────────────────────────────────────────────────────────────────────────


def test_loader_parses_valid_minimal() -> None:
    """load_mapping on valid_minimal.toml should return a well-formed AliasMapping."""
    path = FIXTURES_DIR / "valid_minimal.toml"
    mapping = load_mapping(path)
    assert mapping.arabic_name == "نظام"
    assert mapping.python_module == "sys"
    assert mapping.dict_version == "ar-v1"
    assert mapping.entries["وسائط"] == "argv"
    assert mapping.entries["مسارات"] == "path"
    assert mapping.source_path == path


def test_loader_error_missing_module() -> None:
    """load_mapping on missing_module.toml must raise AliasMappingError mentioning 'not importable'."""
    path = FIXTURES_DIR / "missing_module.toml"
    with pytest.raises(AliasMappingError, match="not importable"):
        load_mapping(path)


def test_loader_error_duplicate_python_value() -> None:
    """load_mapping on duplicate_arabic.toml must raise AliasMappingError listing both Arabic keys."""
    path = FIXTURES_DIR / "duplicate_arabic.toml"
    with pytest.raises(AliasMappingError, match="argv"):
        load_mapping(path)
    # Error message should name both conflicting Arabic keys
    with pytest.raises(AliasMappingError) as exc_info:
        load_mapping(path)
    msg = str(exc_info.value)
    assert "وسائط" in msg or "معطيات" in msg


def test_loader_error_bad_normalization() -> None:
    """load_mapping on bad_normalization.toml must raise AliasMappingError about normalize_identifier."""
    path = FIXTURES_DIR / "bad_normalization.toml"
    with pytest.raises(AliasMappingError, match="normalize_identifier"):
        load_mapping(path)


def test_loader_error_missing_meta_section(tmp_path: Path) -> None:
    """A TOML missing the [meta] section entirely must raise AliasMappingError."""
    toml = """\
[entries]
"وسائط" = "argv"
"""
    p = tmp_path / "no_meta.toml"
    p.write_text(toml, encoding="utf-8")
    with pytest.raises(AliasMappingError, match="meta"):
        load_mapping(p)


def test_loader_error_missing_entries_section(tmp_path: Path) -> None:
    """A TOML missing the [entries] section entirely must raise AliasMappingError."""
    toml = """\
[meta]
arabic_name   = "نظام"
python_module = "sys"
dict_version  = "ar-v1"
schema_version = 1
maintainer    = "—"
"""
    p = tmp_path / "no_entries.toml"
    p.write_text(toml, encoding="utf-8")
    with pytest.raises(AliasMappingError, match="entries"):
        load_mapping(p)


def test_loader_alias_mapping_is_frozen() -> None:
    """AliasMapping must be a frozen dataclass — mutation must raise FrozenInstanceError."""
    from dataclasses import FrozenInstanceError

    path = FIXTURES_DIR / "valid_minimal.toml"
    mapping = load_mapping(path)
    with pytest.raises(FrozenInstanceError):
        mapping.arabic_name = "تجربة"  # type: ignore[misc]
