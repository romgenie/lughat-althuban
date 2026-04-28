# tests/test_jupyter_kernel.py
# B-054: Jupyter kernel structural tests
#
# Tests validate the kernel module without requiring a live Jupyter server
# or ipykernel installation.  The ArabicPythonKernel class is exercised via
# mocking when ipykernel is unavailable.

import importlib
import json
import sys
import types
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

KERNEL_PKG = Path(__file__).parent.parent / "arabicpython_kernel"


# ---------------------------------------------------------------------------
# Module structure
# ---------------------------------------------------------------------------


class TestPackageStructure:
    def test_init_exists(self):
        assert (KERNEL_PKG / "__init__.py").exists()

    def test_kernel_py_exists(self):
        assert (KERNEL_PKG / "kernel.py").exists()

    def test_main_py_exists(self):
        assert (KERNEL_PKG / "__main__.py").exists()

    def test_init_imports_kernel_class(self):
        # Should define ArabicPythonKernel (may fail if ipykernel absent)
        import arabicpython_kernel
        assert hasattr(arabicpython_kernel, "ArabicPythonKernel")

    def test_version_defined(self):
        import arabicpython_kernel
        assert hasattr(arabicpython_kernel, "__version__")


# ---------------------------------------------------------------------------
# kernel.py static attributes
# ---------------------------------------------------------------------------


class TestKernelAttributes:
    @pytest.fixture(autouse=True)
    def _stub_ipykernel(self, monkeypatch):
        """Provide a minimal stub so kernel.py can be re-imported."""
        stub_mod = types.ModuleType("ipykernel")
        stub_ipkernel = types.ModuleType("ipykernel.ipkernel")

        class _FakeKernel:
            execution_count = 0
            iopub_socket = None
            session = MagicMock()
            _parent_header = {}

            def __init__(self, **kwargs):
                pass

            def do_execute(self, *a, **kw):
                return {"status": "ok"}

            def do_complete(self, code, cursor_pos):
                return {"matches": [], "cursor_start": cursor_pos, "cursor_end": cursor_pos, "status": "ok"}

            def _topic(self, name):
                return name.encode()

        stub_ipkernel.IPythonKernel = _FakeKernel
        stub_mod.ipkernel = stub_ipkernel
        monkeypatch.setitem(sys.modules, "ipykernel", stub_mod)
        monkeypatch.setitem(sys.modules, "ipykernel.ipkernel", stub_ipkernel)

        # Re-import kernel module with stub in place
        if "arabicpython_kernel.kernel" in sys.modules:
            del sys.modules["arabicpython_kernel.kernel"]
        if "arabicpython_kernel" in sys.modules:
            del sys.modules["arabicpython_kernel"]

    def test_language_is_apy(self):
        from arabicpython_kernel.kernel import ArabicPythonKernel
        assert ArabicPythonKernel.language == "apy"

    def test_file_extension(self):
        from arabicpython_kernel.kernel import ArabicPythonKernel
        assert ArabicPythonKernel.language_info["file_extension"] == ".apy"

    def test_banner_contains_arabic(self):
        from arabicpython_kernel.kernel import ArabicPythonKernel
        assert "ثعبان" in ArabicPythonKernel.banner or "apython" in ArabicPythonKernel.banner

    def test_implementation_is_apython(self):
        from arabicpython_kernel.kernel import ArabicPythonKernel
        assert ArabicPythonKernel.implementation == "apython"


# ---------------------------------------------------------------------------
# Translation hook in do_execute
# ---------------------------------------------------------------------------


class TestDoExecuteTranslation:
    @pytest.fixture(autouse=True)
    def _stub_and_instance(self, monkeypatch):
        stub_mod = types.ModuleType("ipykernel")
        stub_ipkernel = types.ModuleType("ipykernel.ipkernel")

        class _FakeKernel:
            execution_count = 0
            iopub_socket = None
            session = MagicMock()
            _parent_header = {}
            last_code = None

            def __init__(self, **kwargs):
                pass

            def do_execute(self, code, silent, store_history=True,
                           user_expressions=None, allow_stdin=False, **kw):
                _FakeKernel.last_code = code
                return {"status": "ok", "execution_count": 1}

            def do_complete(self, code, cursor_pos):
                return {"matches": [], "cursor_start": cursor_pos, "cursor_end": cursor_pos, "status": "ok"}

            def _topic(self, name):
                return name.encode()

        stub_ipkernel.IPythonKernel = _FakeKernel
        monkeypatch.setitem(sys.modules, "ipykernel", stub_mod)
        monkeypatch.setitem(sys.modules, "ipykernel.ipkernel", stub_ipkernel)

        for k in list(sys.modules):
            if k.startswith("arabicpython_kernel"):
                del sys.modules[k]

        from arabicpython_kernel.kernel import ArabicPythonKernel
        self.kernel = ArabicPythonKernel.__new__(ArabicPythonKernel)
        _FakeKernel.__init__(self.kernel)
        self._FakeKernel = _FakeKernel

    def test_arabic_source_is_translated(self):
        # اطبع -> print
        result = self.kernel.do_execute("اطبع('مرحبا')", silent=False)
        assert result["status"] == "ok"
        translated = self._FakeKernel.last_code
        assert "print" in translated

    def test_translation_error_returns_error_status(self):
        # Force a translation error by patching translate
        with patch("arabicpython_kernel.kernel.translate", side_effect=SyntaxError("bad")):
            result = self.kernel.do_execute("!!!###", silent=False)
        assert result["status"] == "error"

    def test_pure_python_passes_through(self):
        result = self.kernel.do_execute("x = 1 + 1", silent=False)
        assert result["status"] == "ok"
        assert self._FakeKernel.last_code == "x = 1 + 1"


# ---------------------------------------------------------------------------
# Tab completion
# ---------------------------------------------------------------------------


class TestDoComplete:
    @pytest.fixture(autouse=True)
    def _stub_and_instance(self, monkeypatch):
        stub_mod = types.ModuleType("ipykernel")
        stub_ipkernel = types.ModuleType("ipykernel.ipkernel")

        class _FakeKernel:
            execution_count = 0

            def __init__(self, **kwargs):
                pass

            def do_complete(self, code, cursor_pos):
                return {
                    "matches": [],
                    "cursor_start": cursor_pos,
                    "cursor_end": cursor_pos,
                    "status": "ok",
                }

        stub_ipkernel.IPythonKernel = _FakeKernel
        monkeypatch.setitem(sys.modules, "ipykernel", stub_mod)
        monkeypatch.setitem(sys.modules, "ipykernel.ipkernel", stub_ipkernel)
        for k in list(sys.modules):
            if k.startswith("arabicpython_kernel"):
                del sys.modules[k]

        from arabicpython_kernel.kernel import ArabicPythonKernel
        self.kernel = ArabicPythonKernel.__new__(ArabicPythonKernel)
        _FakeKernel.__init__(self.kernel)

    def test_keyword_completion(self):
        code = "إذ"
        result = self.kernel.do_complete(code, len(code))
        assert any("إذا" in m for m in result["matches"])

    def test_empty_token_returns_parent_result(self):
        result = self.kernel.do_complete("", 0)
        assert "matches" in result


# ---------------------------------------------------------------------------
# __main__.py KERNEL_JSON
# ---------------------------------------------------------------------------


class TestKernelJson:
    def test_kernel_json_has_argv(self):
        import arabicpython_kernel.__main__ as m
        kj = m.KERNEL_JSON
        assert "argv" in kj
        assert "{connection_file}" in kj["argv"]

    def test_kernel_json_language_apy(self):
        import arabicpython_kernel.__main__ as m
        assert m.KERNEL_JSON["language"] == "apy"

    def test_kernel_json_display_name_arabic(self):
        import arabicpython_kernel.__main__ as m
        name = m.KERNEL_JSON["display_name"]
        assert "apython" in name or "ثعبان" in name
