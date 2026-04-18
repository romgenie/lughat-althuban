"""Import hook for .apy files."""

import importlib.abc
import importlib.machinery
import importlib.util
import os
import sys
from collections.abc import Sequence

from arabicpython.translate import translate


class ApyFinder(importlib.abc.MetaPathFinder):
    """Locate `.apy` modules and packages on sys.path / parent __path__."""

    def find_spec(
        self,
        fullname: str,
        path: Sequence[str] | None,
        target: object | None = None,
    ) -> importlib.machinery.ModuleSpec | None:
        if path is None:
            path = sys.path

        name = fullname.split(".")[-1]

        for entry in path:
            # Check for package
            pkg_dir = os.path.join(entry, name)
            if os.path.isdir(pkg_dir):
                init_apy = os.path.join(pkg_dir, "__init__.apy")
                if os.path.isfile(init_apy):
                    loader = ApyLoader(fullname, init_apy, is_package=True)
                    return importlib.util.spec_from_file_location(
                        fullname, init_apy, loader=loader, submodule_search_locations=[pkg_dir]
                    )

            # Check for module
            apy_file = os.path.join(entry, f"{name}.apy")
            if os.path.isfile(apy_file):
                loader = ApyLoader(fullname, apy_file, is_package=False)
                return importlib.util.spec_from_file_location(fullname, apy_file, loader=loader)

        return None


class ApyLoader(importlib.abc.Loader):
    """Translate, compile, and exec a `.apy` module."""

    def __init__(self, fullname: str, path: str, *, is_package: bool = False) -> None:
        self.fullname = fullname
        self.path = path
        self._is_package = is_package

    def is_package(self, fullname: str) -> bool:
        """Return True if the module is a package."""
        return self._is_package

    def create_module(self, spec):
        return None  # use default module creation

    def exec_module(self, module) -> None:
        try:
            with open(self.path, encoding="utf-8") as f:
                source = f.read()
        except UnicodeDecodeError as e:
            raise ImportError(f"can't decode {self.path}: {e}") from e
        except FileNotFoundError as e:
            raise ImportError(f"file not found: {self.path}") from e

        try:
            translated = translate(source)
            code = compile(translated, self.path, "exec")
        except SyntaxError as e:
            if e.filename is None:
                e.filename = self.path
            raise
        exec(code, module.__dict__)

    def get_source(self, fullname: str) -> str:
        """Return the original .apy source (used by linecache / tracebacks)."""
        try:
            with open(self.path, encoding="utf-8") as f:
                return f.read()
        except (UnicodeDecodeError, FileNotFoundError) as e:
            raise ImportError(f"Could not get source for {fullname}: {e}") from e


def install() -> None:
    """Idempotent: insert ApyFinder at the FRONT of sys.meta_path if not already there."""
    for finder in sys.meta_path:
        if isinstance(finder, ApyFinder):
            return
    sys.meta_path.insert(0, ApyFinder())


def uninstall() -> None:
    """Idempotent: remove any ApyFinder instances from sys.meta_path."""
    sys.meta_path[:] = [f for f in sys.meta_path if not isinstance(f, ApyFinder)]
