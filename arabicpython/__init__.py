"""apython — Arabic Python dialect.

This package is a placeholder during Phase 0. Real implementation lands
starting with Packet 1.1.
"""

__version__ = "0.0.1"

from arabicpython.import_hook import install as install  # noqa: E402
from arabicpython.import_hook import uninstall as uninstall
from arabicpython.repl import run_repl as run_repl  # noqa: E402
from arabicpython.tracebacks import (
    format_translated_exception as format_translated_exception,
)  # noqa: E402
from arabicpython.tracebacks import (
    install_excepthook as install_excepthook,
)
from arabicpython.tracebacks import (
    uninstall_excepthook as uninstall_excepthook,
)
