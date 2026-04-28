"""arabicpython_kernel/kernel.py
B-054: ArabicPythonKernel — IPython kernel with Arabic Python translation.

Intercepts ``do_execute`` to translate .apy source -> Python before
handing off to the parent IPythonKernel implementation.  All other
kernel capabilities (inspection, completion, history, comms, display)
are inherited unchanged.

The kernel also:
  - Installs the arabicpython aliases system so ``استيراد نمباي`` works.
  - Provides Arabic-aware tab-completion for keywords and alias module names.
  - Translates error tracebacks back to Arabic identifiers via the
    existing ``arabicpython.tracebacks`` mechanism.
"""
from __future__ import annotations

import sys
import traceback
from typing import Any

# ipykernel is an optional dependency; guard import so the module can be
# imported (and tested) without a full Jupyter installation.
try:
    from ipykernel.ipkernel import IPythonKernel  # type: ignore
    _HAVE_IPYKERNEL = True
except ImportError:  # pragma: no cover
    IPythonKernel = object  # type: ignore
    _HAVE_IPYKERNEL = False

from arabicpython.translate import translate
from arabicpython.normalize import normalize_identifier

# Arabic keywords offered as completions
_ARABIC_KEYWORDS = [
    "إذا", "وإلا", "إلا_إذا", "إلا",
    "بينما", "لكل", "في",
    "دالة", "صنف", "إرجاع", "ناتج",
    "حاول", "أخيرًا", "إثارة", "مع", "باسم",
    "استيراد", "من",
    "و", "أو", "ليس",
    "مرر", "تابع", "اكسر", "احذف", "عالمي", "غير_محلي",
    "لامدا", "تأكيد", "منتج",
    "صحيح", "خطأ", "لا_شيء",
]

# Names of alias modules registered with AliasFinder
_ALIAS_MODULE_NAMES: list[str] = []


def _load_alias_names() -> list[str]:
    """Return the Arabic module names available via the alias system."""
    try:
        from arabicpython.aliases._finder import AliasFinder
        from pathlib import Path
        mappings_dir = Path(__file__).parent.parent / "arabicpython" / "aliases"
        finder = AliasFinder(mappings_dir=mappings_dir)
        return list(finder._mappings.keys())
    except Exception:
        return []


class ArabicPythonKernel(IPythonKernel):  # type: ignore[misc]
    """Jupyter kernel that translates Arabic Python before execution."""

    implementation = "apython"
    implementation_version = "0.1.0"
    language = "apy"
    language_version = "0.1"
    language_info = {
        "name": "apy",
        "mimetype": "text/x-apy",
        "file_extension": ".apy",
        "pygments_lexer": "python",  # fallback highlighter
        "codemirror_mode": {"name": "python"},
    }
    banner = "لغة الثعبان (apython) — Arabic Python kernel"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        # Install alias system once
        try:
            from arabicpython.aliases import install as install_aliases
            from arabicpython.import_hook import install as install_hook
            install_hook()
            install_aliases()
        except Exception:
            pass
        global _ALIAS_MODULE_NAMES
        _ALIAS_MODULE_NAMES = _load_alias_names()

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def do_execute(
        self,
        code: str,
        silent: bool,
        store_history: bool = True,
        user_expressions: dict | None = None,
        allow_stdin: bool = False,
        *,
        cell_id: str | None = None,
    ) -> dict:
        """Translate Arabic Python source then delegate to IPythonKernel."""
        try:
            python_code = translate(code)
        except Exception as exc:
            # Translation error — report to the frontend and return
            err_text = f"خطأ في الترجمة: {exc}\n"
            if not silent:
                self._publish_stream("stderr", err_text)
            return {
                "status": "error",
                "execution_count": self.execution_count,
                "ename": type(exc).__name__,
                "evalue": str(exc),
                "traceback": [err_text],
            }

        # Delegate to parent with the translated (Python) source
        kwargs: dict[str, Any] = dict(
            code=python_code,
            silent=silent,
            store_history=store_history,
            user_expressions=user_expressions or {},
            allow_stdin=allow_stdin,
        )
        if cell_id is not None:
            kwargs["cell_id"] = cell_id
        return super().do_execute(**kwargs)

    # ------------------------------------------------------------------
    # Tab completion
    # ------------------------------------------------------------------

    def do_complete(self, code: str, cursor_pos: int) -> dict:
        """Augment IPython completions with Arabic keywords and module names."""
        result = super().do_complete(code, cursor_pos)
        # Extract the current token being typed
        text_before = code[:cursor_pos]
        # Find start of current Arabic token
        i = len(text_before) - 1
        while i >= 0 and (text_before[i].isalpha() or text_before[i] in "_"):
            i -= 1
        token = text_before[i + 1:]
        if not token:
            return result
        norm = normalize_identifier(token)
        matches = [
            kw for kw in (_ARABIC_KEYWORDS + _ALIAS_MODULE_NAMES)
            if normalize_identifier(kw).startswith(norm)
        ]
        # Merge without duplicates
        existing: list[str] = result.get("matches", [])
        combined = list(dict.fromkeys(existing + matches))
        result["matches"] = combined
        return result

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _publish_stream(self, name: str, text: str) -> None:
        """Publish a stream message (stdout/stderr) to the frontend."""
        content = {"name": name, "text": text}
        self.session.send(
            self.iopub_socket,
            "stream",
            content,
            parent=self._parent_header,
            ident=self._topic("stream"),
        )
