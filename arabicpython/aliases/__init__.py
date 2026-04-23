"""arabicpython.aliases — Phase B library alias runtime.

Provides Arabic-named access to third-party and stdlib modules via a
``sys.meta_path`` finder that wraps matching imports in ``ModuleProxy``.

Quick start
-----------
After ``arabicpython.install()`` (which calls ``install_aliases()`` by default),
an ``.apy`` program can write::

    استورد طلبات          # import requests as طلبات
    استجابه = طلبات.احصل("https://example.com")

Public API
----------
install()
    Register ``AliasFinder`` on ``sys.meta_path``. Idempotent.
uninstall()
    Remove ``AliasFinder`` from ``sys.meta_path``. Idempotent.
load_mapping(path)
    Parse and validate one ``.toml`` alias file. Returns ``AliasMapping``.
ModuleProxy
    The wrapper class (created by the finder; not for direct use).
AliasFinder
    The ``sys.meta_path`` finder.
AliasMapping
    Frozen dataclass returned by ``load_mapping``.
AliasMappingError
    Exception raised for invalid mapping files.
"""

from __future__ import annotations

import sys

from arabicpython.aliases._finder import AliasFinder
from arabicpython.aliases._loader import AliasMapping, AliasMappingError, load_mapping
from arabicpython.aliases._proxy import ModuleProxy

__all__ = [
    "install",
    "uninstall",
    "ModuleProxy",
    "AliasFinder",
    "AliasMapping",
    "AliasMappingError",
    "load_mapping",
]


def install() -> None:
    """Register ``AliasFinder`` on ``sys.meta_path``.

    Idempotent — safe to call multiple times. The finder is appended *after*
    any already-registered finders so that ``.apy`` modules and ordinary Python
    modules take precedence.

    Should be called *after* ``arabicpython.install()`` to ensure the Phase A
    ``.apy`` finder is already registered at a higher-priority slot.
    """
    for finder in sys.meta_path:
        if isinstance(finder, AliasFinder):
            return
    sys.meta_path.append(AliasFinder())


def uninstall() -> None:
    """Remove ``AliasFinder`` from ``sys.meta_path``.

    Idempotent — safe to call even when the finder is not registered.
    Already-imported proxy objects remain usable after this call.
    """
    sys.meta_path[:] = [f for f in sys.meta_path if not isinstance(f, AliasFinder)]
