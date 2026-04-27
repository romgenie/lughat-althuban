"""apython CLI runner."""

import argparse
import contextlib
import os
import re
import sys
import types

from arabicpython import __version__
from arabicpython.translate import translate

# Regex for the per-file dictionary directive.
# Matches: # arabicpython: dict=<version>   (in any of the first 5 lines)
_DIRECTIVE_RE = re.compile(r"#\s*arabicpython\s*:\s*dict\s*=\s*(\S+)")


def _parse_file_directive(source: str) -> "str | None":
    """Return the dict version named by the first per-file directive, or None.

    Scans only the first five lines so a shebang on line 1 doesn't block it.
    """
    for line in source.splitlines()[:5]:
        m = _DIRECTIVE_RE.search(line)
        if m:
            return m.group(1)
    return None


def _configure_utf8_streams() -> None:
    # Default Windows stdout codec is cp1252; can't encode Arabic. Reconfigure
    # to UTF-8 so print(...) of Arabic strings doesn't raise UnicodeEncodeError.
    for stream in (sys.stdout, sys.stderr):
        if stream is not None and hasattr(stream, "reconfigure"):
            with contextlib.suppress(AttributeError, OSError, ValueError):
                stream.reconfigure(encoding="utf-8")


def main(argv: "list[str] | None" = None) -> int:
    """apython CLI entry point.

    Args:
        argv: command-line arguments NOT including program name. If None,
            defaults to sys.argv[1:].

    Returns:
        Exit code: 0 on success, 1 on translate/compile/runtime errors,
        2 on usage errors (mirrors argparse convention).
    """
    from arabicpython.aliases import install as install_aliases
    from arabicpython.import_hook import install
    from arabicpython.tracebacks import install_excepthook, print_translated_exception

    _configure_utf8_streams()
    install()
    install_aliases()
    install_excepthook()

    if argv is None:
        argv = sys.argv[1:]

    # ── Subcommand dispatch ───────────────────────────────────────────────────
    # `ثعبان اختبر [pytest-args]` — Arabic test runner (B-051).
    if argv and argv[0] == "اختبر":
        from arabicpython.test_runner import run_tests

        return run_tests(argv[1:])

    parser = argparse.ArgumentParser(
        prog="ثعبان",
        usage="ثعبان [-h] [--version] [--dict VERSION] [-c CODE] [FILE] [args ...]",
        description="لغة الثعبان — Arabic Python runner.",
        add_help=False,
    )
    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("--version", action="version", version=f"ثعبان {__version__}")
    parser.add_argument(
        "--dict",
        dest="dict_version",
        metavar="VERSION",
        default=None,
        help="dictionary version to use (e.g. ar-v1.1, ar-v2). "
        "Overrides any per-file '# arabicpython: dict=' directive.",
    )
    parser.add_argument("-c", dest="code", metavar="CODE")
    parser.add_argument("file", nargs="?", metavar="FILE")
    parser.add_argument("args", nargs=argparse.REMAINDER)

    # Use parse_known_args to avoid argparse exiting on its own for -h/--help
    # so we can control the exit code and output if needed, but the spec says
    # "argparse default" for usage errors (exit 2).
    # Actually, the spec says main returns int and tests check it.

    try:
        args = parser.parse_args(argv)
    except SystemExit as e:
        return e.code

    if args.help:
        parser.print_help()
        return 0

    source: str
    original_path: str
    forwarded_args: list[str]
    prog_name: str

    if args.code is not None:
        source = args.code
        original_path = "<string>"
        prog_name = "-c"
        # If -c is used, the first positional (args.file) is actually part of args
        forwarded_args = []
        if args.file:
            forwarded_args.append(args.file)
        if args.args:
            forwarded_args.extend(args.args)
    elif args.file is not None:
        forwarded_args = args.args if args.args else []
        if args.file == "-":
            try:
                source = sys.stdin.read()
            except UnicodeDecodeError as e:
                sys.stderr.write(f"ثعبان:can't read from stdin: {e}\n")
                return 1
            original_path = "<stdin>"
            prog_name = "-"
        else:
            file_path = args.file
            prog_name = file_path
            if os.path.isdir(file_path):
                sys.stderr.write(
                    f"ثعبان:can't open file '{file_path}': [Errno 21] Is a directory\n"
                )
                return 1
            try:
                # Absolute path for __file__ and error reporting
                original_path = os.path.abspath(file_path)
                with open(file_path, encoding="utf-8") as f:
                    source = f.read()
            except FileNotFoundError:
                sys.stderr.write(
                    f"ثعبان:can't open file '{file_path}': [Errno 2] No such file or directory\n"
                )
                return 1
            except PermissionError as e:
                sys.stderr.write(f"ثعبان:can't open file '{file_path}': {e}\n")
                return 1
            except UnicodeDecodeError as e:
                sys.stderr.write(
                    f"ثعبان:can't open file '{file_path}': invalid UTF-8 encoding ({e})\n"
                )
                return 1
            except Exception as e:
                sys.stderr.write(f"ثعبان:can't open file '{file_path}': {e}\n")
                return 1
    else:
        # No FILE, no -c, no '-': drop into the REPL.
        from arabicpython.repl import run_repl

        return run_repl()

    # Resolve the dictionary version: --dict flag > per-file directive > default.
    # If the file has a directive and the flag is also given, they must agree;
    # a mismatch is a hard error so ambiguity surfaces early.
    file_directive = _parse_file_directive(source)
    cli_dict = args.dict_version  # may be None if flag not given

    if cli_dict is not None and file_directive is not None and cli_dict != file_directive:
        sys.stderr.write(
            f"ثعبان: dictionary version conflict — "
            f"--dict specifies '{cli_dict}' but the file directive says '{file_directive}'. "
            f"Remove one or make them agree.\n"
        )
        return 1

    effective_dict = cli_dict if cli_dict is not None else file_directive  # None → use default

    # Step 1 & 2 & 3: translate
    try:
        translated = translate(source, dict_version=effective_dict)
    except SyntaxError:
        print_translated_exception(*sys.exc_info())
        return 1
    except FileNotFoundError as e:
        sys.stderr.write(f"ثعبان: unknown dictionary version: {e}\n")
        return 1
    except Exception:
        print_translated_exception(*sys.exc_info())
        return 1

    # Step 4: compile
    try:
        code_obj = compile(translated, original_path, "exec")
    except SyntaxError:
        print_translated_exception(*sys.exc_info())
        return 1
    except Exception:
        print_translated_exception(*sys.exc_info())
        return 1

    # Step 5: execute
    mod = types.ModuleType("__main__")
    mod.__file__ = original_path
    mod.__loader__ = None
    mod.__package__ = None
    mod.__spec__ = None
    # builtins must be available
    mod.__dict__["__builtins__"] = __import__("builtins")

    old_main = sys.modules.get("__main__")
    sys.modules["__main__"] = mod

    old_argv = sys.argv
    sys.argv = [prog_name] + forwarded_args

    try:
        exec(code_obj, mod.__dict__)
    except SystemExit as e:
        # SystemExit.code can be None, int, or any object
        if e.code is None:
            return 0
        if isinstance(e.code, int):
            return e.code
        sys.stderr.write(str(e.code) + "\n")
        return 1
    except KeyboardInterrupt:
        sys.stderr.write("KeyboardInterrupt\n")
        return 130
    except Exception:
        print_translated_exception(*sys.exc_info())
        return 1
    finally:
        sys.argv = old_argv
        if old_main:
            sys.modules["__main__"] = old_main
        else:
            del sys.modules["__main__"]

    return 0


if __name__ == "__main__":
    sys.exit(main())
