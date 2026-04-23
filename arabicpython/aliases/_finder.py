"""AliasFinder — sys.meta_path finder that resolves Arabic module names to ModuleProxy objects."""

from __future__ import annotations

import importlib
import importlib.abc
import importlib.machinery
import importlib.util
import types
from pathlib import Path

from arabicpython.aliases._loader import AliasMapping, AliasMappingError, load_mapping
from arabicpython.aliases._proxy import ModuleProxy


class AliasLoader(importlib.abc.Loader):
    """Loader that materialises a ModuleProxy for one registered Arabic alias."""

    def __init__(self, mapping: AliasMapping) -> None:
        self._mapping = mapping

    def create_module(self, spec: importlib.machinery.ModuleSpec) -> ModuleProxy:
        """Construct and return the proxy; no further exec_module work is needed."""
        real_module = importlib.import_module(self._mapping.python_module)
        return ModuleProxy(
            real_module,
            self._mapping.entries,
            arabic_name=self._mapping.arabic_name,
        )

    def exec_module(self, module: types.ModuleType) -> None:  # noqa: ARG002
        """No-op: the proxy is fully initialised in create_module."""


class AliasFinder(importlib.abc.MetaPathFinder):
    """Resolves Arabic module names to ModuleProxy objects.

    Registered on ``sys.meta_path`` *after* the Phase A ``.apy`` finder so that:

    1. Local ``.apy`` modules still resolve first.
    2. Python stdlib / third-party modules resolve next (standard machinery).
    3. This finder resolves Arabic-named aliases last.
    4. An unknown name still raises ``ModuleNotFoundError`` correctly.

    The finder loads every ``*.toml`` file found in *mappings_dir*
    (defaults to the ``arabicpython/aliases/`` package directory).

    Thread safety
    -------------
    ``find_spec`` is thread-safe during steady-state import.
    ``reload_mappings`` is *not* thread-safe; call it only during development.
    """

    def __init__(self, mappings_dir: Path | None = None) -> None:
        if mappings_dir is None:
            mappings_dir = Path(__file__).parent
        self._mappings_dir: Path = mappings_dir
        self._arabic_to_mapping: dict[str, AliasMapping] = {}
        self._load_all_mappings()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_all_mappings(self) -> None:
        """(Re-)read every ``*.toml`` in *mappings_dir* and build the lookup table."""
        loaded: dict[str, AliasMapping] = {}
        for toml_file in sorted(self._mappings_dir.glob("*.toml")):
            try:
                mapping = load_mapping(toml_file)
                loaded[mapping.arabic_name] = mapping
            except AliasMappingError:
                # Don't crash the import system if one TOML is broken at startup.
                # The broken file is simply ignored; its error surfaces in tests
                # when load_mapping() is called directly.
                pass
        self._arabic_to_mapping = loaded

    # ------------------------------------------------------------------
    # MetaPathFinder protocol
    # ------------------------------------------------------------------

    def find_spec(
        self,
        fullname: str,
        path: object = None,  # noqa: ARG002
        target: types.ModuleType | None = None,  # noqa: ARG002
    ) -> importlib.machinery.ModuleSpec | None:
        """Return a ModuleSpec for *fullname* if it is a registered Arabic alias, else None."""
        if fullname not in self._arabic_to_mapping:
            return None
        mapping = self._arabic_to_mapping[fullname]
        loader = AliasLoader(mapping)
        return importlib.util.spec_from_loader(fullname, loader)

    # ------------------------------------------------------------------
    # Development helper
    # ------------------------------------------------------------------

    def reload_mappings(self) -> None:
        """Re-read all TOML files from *mappings_dir*.

        Intended for development / REPL use only. Already-imported proxy
        objects are *not* invalidated by this call.
        """
        self._load_all_mappings()
