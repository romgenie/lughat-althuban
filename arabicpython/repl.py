"""Arabic Python REPL."""

import atexit
import code as _code_module
import contextlib
import os
import sys
from typing import Any

from arabicpython import __version__
from arabicpython.translate import translate


class ArabicConsole(_code_module.InteractiveConsole):
    """An InteractiveConsole that translates Arabic source before compiling."""

    def __init__(
        self,
        locals: "dict[str, Any] | None" = None,
        filename: str = "<stdin>",
    ) -> None:
        super().__init__(locals=locals, filename=filename)

    def runsource(
        self,
        source: str,
        filename: str = "<stdin>",
        symbol: str = "single",
    ) -> bool:
        """Translate, then compile-or-defer-or-error.

        Returns:
            True  → input is incomplete; caller should request another line.
            False → input was processed (executed OR errored). Caller resets the buffer.
        """
        try:
            translated = translate(source)
        except SyntaxError as e:
            # Distinguish "incomplete input" from "real translate-time error".
            if _is_incomplete_marker(e):
                return True
            self._write_translate_error(e, filename)
            return False
        except Exception:
            # Should not happen in translate but handle gracefully
            self.showtraceback()
            return False

        return super().runsource(translated, filename, symbol)

    def _write_translate_error(self, e: SyntaxError, filename: str) -> None:
        """Print a one-line, traceback-free error to self.write."""
        self.write(f'  File "{filename}", line {e.lineno or 1}\n')
        self.write(f"    {e.msg}\n")

    def showtraceback(self) -> None:
        from arabicpython.tracebacks import print_translated_exception

        exc_type, exc_value, exc_tb = sys.exc_info()
        # Trim the top frame which is the InteractiveConsole's exec call;
        # we only want frames inside user code. Match what the parent's
        # showtraceback does — it strips its own frame.
        if exc_tb is not None:
            exc_tb = exc_tb.tb_next
        print_translated_exception(exc_type, exc_value, exc_tb, file=self)


def _is_incomplete_marker(e: SyntaxError) -> bool:
    """Check if a SyntaxError msg indicates incomplete input."""
    msg = e.msg or ""
    # Standard tokenize.TokenError messages converted to SyntaxError in translate.py
    # and standard Python compiler messages for incomplete input.
    incomplete_msgs = (
        "EOF in multi-line statement",
        "EOF in multi-line string",
        "unexpected EOF while parsing",
        "unterminated string literal",
        "unterminated triple-quoted string literal",
    )
    return any(m in msg for m in incomplete_msgs)


def run_repl(
    *,
    banner: "str | None" = None,
    exit_msg: "str | None" = None,
) -> int:
    """Start an interactive Arabic Python session.

    Sets up readline (if available) for history and tab completion, prints the
    banner, runs the InteractiveConsole loop until EOF, returns 0.

    Args:
        banner: override the default startup banner (mostly for tests).
        exit_msg: override the default exit message (mostly for tests).

    Returns:
        0 on clean exit (EOF or sys.exit(0)).
        Other ints if the user calls sys.exit(N).
    """
    history_path = _setup_readline()

    if banner is None:
        banner = (
            f"apython {__version__} — Arabic Python REPL\n"
            f"Python {sys.version.split()[0]} on {sys.platform}\n"
            f'Type "help()", "exit()", or press Ctrl-D to quit.\n'
        )
    if exit_msg is None:
        exit_msg = ""

    sys.ps1 = os.environ.get("APYTHON_PS1", getattr(sys, "ps1", ">>> "))
    sys.ps2 = os.environ.get("APYTHON_PS2", getattr(sys, "ps2", "... "))

    console = ArabicConsole()
    try:
        console.interact(banner=banner, exitmsg=exit_msg)
    except SystemExit as e:
        if e.code is None:
            return 0
        if isinstance(e.code, int):
            return e.code
        sys.stderr.write(str(e.code) + "\n")
        return 1
    finally:
        if history_path is not None:
            _save_history(history_path)
    return 0


def _setup_readline() -> "str | None":
    """Best-effort readline setup. Never raises.

    Returns the resolved history file path if readline is available, else None.
    The caller is responsible for invoking _save_history(path) on shutdown so
    that history is written even when the process exits via the normal
    interpreter-shutdown path (atexit handlers do not fire between pytest cases).
    The atexit registration is kept as a fallback for crashes.
    """
    try:
        import readline
        import rlcompleter  # noqa: F401
    except ImportError:
        return None

    history_path = os.path.expanduser("~/.apython_history")
    with contextlib.suppress(OSError, FileNotFoundError):
        readline.read_history_file(history_path)

    readline.set_history_length(1000)
    atexit.register(_save_history, history_path)

    readline.parse_and_bind("tab: complete")
    return history_path


def _save_history(path: str) -> None:
    try:
        import readline

        readline.write_history_file(path)
    except Exception:
        pass
