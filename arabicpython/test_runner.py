"""B-051: Arabic test runner — `ثعبان اختبر`.

Maps Arabic CLI flags to pytest equivalents and invokes pytest.main().
Designed to be called from arabicpython.cli when the first argument is `اختبر`.

Arabic flag reference
---------------------
--مطول              -v            verbose output
--هادئ              -q            quiet output
--توقف_اول          -x            stop on first failure
--بلا_رأس           --no-header   suppress pytest header
--اسم=<expr>        -k <expr>     keyword filter
--علامه=<expr>      -m <expr>     marker filter
--تقرير=<نوع>       --tb=<type>   traceback style (short/long/line/no)
--غطاء              --cov         coverage (requires pytest-cov)
--غطاء=<مسار>       --cov=<path>  coverage for a specific path
--بلا_تحذيرات       -p no:warnings suppress warnings plugin
--منفذ=<n>          -n <n>        parallel workers (requires pytest-xdist)

All unrecognised arguments are forwarded verbatim to pytest.
"""

from __future__ import annotations

import sys

# ── Arabic flag → pytest arg mapping ──────────────────────────────────────────

_FLAG_MAP: dict[str, str] = {
    "--مطول": "-v",
    "--هادئ": "-q",
    "--توقف_اول": "-x",
    "--بلا_رأس": "--no-header",
    "--بلا_تحذيرات": "-p no:warnings",
}

_PREFIX_MAP: list[tuple[str, str]] = [
    ("--اسم=", "-k "),
    ("--علامه=", "-m "),
    ("--تقرير=", "--tb="),
    ("--غطاء=", "--cov="),
    ("--منفذ=", "-n "),
]

# Bare --غطاء without a value maps to --cov (covers the whole project)
_FLAG_MAP["--غطاء"] = "--cov"


def _translate_args(arabic_args: list[str]) -> list[str]:
    """Translate Arabic pytest flags in *arabic_args* to their pytest equivalents.

    Unknown arguments (including plain paths like ``tests/``) are forwarded
    verbatim.  Returns a flat list of strings suitable for pytest.main().
    """
    pytest_args: list[str] = []
    for arg in arabic_args:
        if arg in _FLAG_MAP:
            # May expand to multiple words (e.g. "-p no:warnings")
            pytest_args.extend(_FLAG_MAP[arg].split())
            continue

        matched = False
        for arabic_prefix, pytest_prefix in _PREFIX_MAP:
            if arg.startswith(arabic_prefix):
                value = arg[len(arabic_prefix) :]
                if " " in pytest_prefix:
                    # e.g. "-k " → ["-k", value]
                    pytest_args.extend(pytest_prefix.split() + [value])
                else:
                    # e.g. "--tb=" → ["--tb=value"]
                    pytest_args.append(pytest_prefix + value)
                matched = True
                break

        if not matched:
            pytest_args.append(arg)

    return pytest_args


def run_tests(args: list[str]) -> int:
    """Entry point called by `ثعبان اختبر [args...]`.

    *args* is everything after the ``اختبر`` token.
    Returns an integer exit code (0 = all passed, non-zero = failure / error).
    """
    try:
        import pytest
    except ImportError:
        sys.stderr.write("ثعبان اختبر: pytest غير مثبت. " "ثبّته بالأمر: pip install pytest\n")
        return 1

    pytest_args = _translate_args(args)
    return pytest.main(pytest_args)
