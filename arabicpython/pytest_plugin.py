"""
arabicpython/pytest_plugin.py
B-062: pytest plugin — discover and run .apy test files.

Arabic test file naming conventions:
  اختبار_*.apy   (Arabic prefix for "test")
  test_*.apy     (English prefix, also accepted)
  *_اختبار.apy   (Arabic suffix)
  *_test.apy     (English suffix)

Registration (pyproject.toml):
  [project.entry-points."pytest11"]
  apy = "arabicpython.pytest_plugin"
"""

from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
from pathlib import Path
from typing import Optional

import pytest

_ARABIC_PREFIXES = ("اختبار_",)
_ARABIC_SUFFIXES = ("_اختبار",)


# ── pytest hooks ─────────────────────────────────────────────────────────────

def pytest_configure(config: pytest.Config) -> None:
    """Install the arabicpython .apy import hook and alias finder at collection startup."""
    import arabicpython
    import arabicpython.aliases
    arabicpython.install()           # .apy file import hook
    arabicpython.aliases.install()   # Arabic module name aliases (رياضيات → math, etc.)


def pytest_collect_file(
    parent: pytest.Collector, file_path: Path
) -> Optional["ApyModule"]:
    """Return an ApyModule collector for .apy files that match test naming."""
    if file_path.suffix != ".apy":
        return None
    stem = file_path.stem
    is_test = (
        any(stem.startswith(p) for p in _ARABIC_PREFIXES)
        or any(stem.endswith(s) for s in _ARABIC_SUFFIXES)
        or stem.startswith("test_")
        or stem.endswith("_test")
    )
    if is_test:
        return ApyModule.from_parent(parent, path=file_path)
    return None


# ── collector ─────────────────────────────────────────────────────────────────

class ApyModule(pytest.Module):
    """
    pytest collector for a single .apy test file.

    Translates Arabic source → Python via arabicpython.translator.translate(),
    loads the resulting module into a temporary .py file, then delegates all
    item collection to the standard pytest.Module machinery.
    """

    def _getobj(self) -> object:
        """Translate the .apy file and load it as a Python module."""
        from arabicpython.translate import translate

        source = self.path.read_text(encoding="utf-8")
        try:
            python_source = translate(source)
        except Exception as exc:
            raise pytest.UsageError(
                f"arabicpython: failed to translate {self.path.name}: {exc}"
            ) from exc

        # Write translated source to a temp .py file for importlib
        fd, temp_path = tempfile.mkstemp(
            prefix=f"_apy_{self.path.stem}_", suffix=".py"
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(python_source)

            spec = importlib.util.spec_from_file_location(
                self.path.stem,
                temp_path,
                submodule_search_locations=[],
            )
            if spec is None or spec.loader is None:  # pragma: no cover
                raise pytest.UsageError(
                    f"arabicpython: could not create module spec for {self.path.name}"
                )

            module = importlib.util.module_from_spec(spec)
            # Point __file__ at the original .apy source — cleaner tracebacks
            module.__file__ = str(self.path)
            if module.__spec__ is not None:
                module.__spec__.origin = str(self.path)

            # Register before exec so intra-module imports resolve
            sys.modules.setdefault(self.path.stem, module)
            spec.loader.exec_module(module)  # type: ignore[union-attr]

        finally:
            try:
                os.unlink(temp_path)
            except OSError:
                pass

        return module
