"""apython — Arabic-keyword Python dialect.

Transpiler that executes ``.apy`` source files by translating Arabic
keywords to their Python equivalents at the tokenize layer, then handing
the result to the standard CPython compiler. The public API installs an
import hook for ``.apy`` modules, runs an interactive REPL, and rewrites
tracebacks so errors point back at the original Arabic source.

Phase B adds library aliases: Arabic module names that transparently proxy
third-party and stdlib modules via ``arabicpython.aliases``.
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
from arabicpython.aliases import install as install_aliases  # noqa: E402
from arabicpython.aliases import uninstall as uninstall_aliases
