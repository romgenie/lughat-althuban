"""apython CLI runner."""

import argparse
import os
import sys
import traceback
import types

from arabicpython import __version__
from arabicpython.translate import translate


def main(argv: "list[str] | None" = None) -> int:
    """apython CLI entry point.

    Args:
        argv: command-line arguments NOT including program name. If None,
            defaults to sys.argv[1:].

    Returns:
        Exit code: 0 on success, 1 on translate/compile/runtime errors,
        2 on usage errors (mirrors argparse convention).
    """
    from arabicpython.import_hook import install

    install()

    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="apython",
        usage="apython [-h] [--version] [-c CODE] [FILE] [args ...]",
        description="Arabic Python runner.",
        add_help=False,
    )
    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("--version", action="version", version=f"apython {__version__}")
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
                sys.stderr.write(f"apython: can't read from stdin: {e}\n")
                return 1
            original_path = "<stdin>"
            prog_name = "-"
        else:
            file_path = args.file
            prog_name = file_path
            if os.path.isdir(file_path):
                sys.stderr.write(
                    f"apython: can't open file '{file_path}': [Errno 21] Is a directory\n"
                )
                return 1
            try:
                # Absolute path for __file__ and error reporting
                original_path = os.path.abspath(file_path)
                with open(file_path, encoding="utf-8") as f:
                    source = f.read()
            except FileNotFoundError:
                sys.stderr.write(
                    f"apython: can't open file '{file_path}': [Errno 2] No such file or directory\n"
                )
                return 1
            except PermissionError as e:
                sys.stderr.write(f"apython: can't open file '{file_path}': {e}\n")
                return 1
            except UnicodeDecodeError as e:
                sys.stderr.write(
                    f"apython: can't open file '{file_path}': invalid UTF-8 encoding ({e})\n"
                )
                return 1
            except Exception as e:
                sys.stderr.write(f"apython: can't open file '{file_path}': {e}\n")
                return 1
    else:
        parser.print_usage(sys.stderr)
        return 2

    # Step 1 & 2 & 3: translate
    try:
        translated = translate(source)
    except SyntaxError as e:
        # Format: File "{path}", line L: {msg}
        loc = ""
        if e.lineno is not None:
            loc = f'File "{original_path}", line {e.lineno}: '
        sys.stderr.write(f"{loc}{e.msg}\n")
        return 1
    except Exception:
        traceback.print_exc()
        return 1

    # Step 4: compile
    try:
        code_obj = compile(translated, original_path, "exec")
    except SyntaxError:
        traceback.print_exc()
        return 1
    except Exception:
        traceback.print_exc()
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
        traceback.print_exc()
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
