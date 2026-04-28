"""arabicpython/formatter.py
B-055: Source formatter for .apy files.

Applies deterministic, opinionated formatting to Arabic Python source:
  - Normalise indentation to 4 spaces per level (tabs -> spaces)
  - Remove trailing whitespace on every line
  - Collapse 3+ consecutive blank lines to at most 2
  - Ensure exactly one trailing newline
  - Add a space after '#' in comments (skip shebangs and '##' headers)
  - Ensure a space after ',' when not inside a string literal
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_INDENT_RE = re.compile(r"^(\s*)")


def _normalise_indentation(lines: list[str]) -> list[str]:
    result = []
    for line in lines:
        m = _INDENT_RE.match(line)
        indent = m.group(1)
        rest = line[len(indent):]
        indent = indent.replace("\t", "    ")
        result.append(indent + rest)
    return result


def _remove_trailing_whitespace(lines: list[str]) -> list[str]:
    return [line.rstrip() for line in lines]


def _collapse_blank_lines(lines: list[str]) -> list[str]:
    """Allow at most 2 consecutive blank lines."""
    result: list[str] = []
    blank_run = 0
    for line in lines:
        if line == "":
            blank_run += 1
            if blank_run <= 2:
                result.append(line)
        else:
            blank_run = 0
            result.append(line)
    return result


def _find_comment_start(line: str) -> int | None:
    """Return index of the '#' starting a comment, or None."""
    in_single = False
    in_double = False
    i = 0
    while i < len(line):
        c = line[i]
        if c == "\\" and (in_single or in_double):
            i += 2
            continue
        if c == "'" and not in_double:
            in_single = not in_single
        elif c == '"' and not in_single:
            in_double = not in_double
        elif c == "#" and not in_single and not in_double:
            return i
        i += 1
    return None


def _fix_comment_space(line: str) -> str:
    """Ensure a space after '#' in comments (not shebangs or ## headers)."""
    idx = _find_comment_start(line)
    if idx is None:
        return line
    comment = line[idx:]
    if comment.startswith("#!") or comment.startswith("##"):
        return line
    if len(comment) > 1 and comment[1] != " ":
        line = line[:idx] + "# " + comment[1:]
    return line


def _ensure_comma_space(line: str) -> str:
    """Add a space after ',' when missing, unless inside a string."""
    result: list[str] = []
    in_single = False
    in_double = False
    i = 0
    while i < len(line):
        c = line[i]
        if c == "\\" and (in_single or in_double):
            result.append(c)
            if i + 1 < len(line):
                result.append(line[i + 1])
            i += 2
            continue
        if c == "'" and not in_double:
            in_single = not in_single
        elif c == '"' and not in_single:
            in_double = not in_double
        elif c == "," and not in_single and not in_double:
            result.append(c)
            if i + 1 < len(line) and line[i + 1] not in (" ", "\n", ")", "]", "}"):
                result.append(" ")
            i += 1
            continue
        result.append(c)
        i += 1
    return "".join(result)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def format_source(source: str) -> str:
    """Return a formatted version of *source* (.apy text)."""
    lines = source.splitlines()
    lines = _normalise_indentation(lines)
    lines = _remove_trailing_whitespace(lines)

    processed: list[str] = []
    triple_double = 0
    triple_single = 0
    for line in lines:
        triple_double += line.count('"""')
        triple_single += line.count("'''")
        in_triple = (triple_double % 2 != 0) or (triple_single % 2 != 0)
        if not in_triple:
            line = _fix_comment_space(line)
            line = _ensure_comma_space(line)
        processed.append(line)

    processed = _collapse_blank_lines(processed)
    result = "\n".join(processed)
    result = result.rstrip("\n") + "\n"
    return result


def format_file(path: Path, *, check: bool = False) -> bool:
    """Format *path* in-place.  Returns True if the file was (or would be) changed."""
    original = path.read_text(encoding="utf-8")
    formatted = format_source(original)
    if formatted == original:
        return False
    if not check:
        path.write_text(formatted, encoding="utf-8")
    return True


def main(argv: list[str] | None = None) -> int:
    """CLI entry point used by ``ثعبان نسّق``."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="ثعبان نسّق",
        description="Format .apy source files.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Don't write; exit 1 if any file would change.",
    )
    parser.add_argument("files", nargs="*", metavar="FILE")
    args = parser.parse_args(argv)

    if not args.files:
        src = sys.stdin.read()
        sys.stdout.write(format_source(src))
        return 0

    any_changed = False
    errors = 0
    for fname in args.files:
        p = Path(fname)
        if not p.exists():
            sys.stderr.write(f"ثعبان نسّق: {fname}: file not found\n")
            errors += 1
            continue
        changed = format_file(p, check=args.check)
        if changed:
            any_changed = True
            verb = "would reformat" if args.check else "reformatted"
            sys.stderr.write(f"{verb} {fname}\n")
        else:
            sys.stderr.write(f"{fname} already formatted\n")

    if errors:
        return 1
    if args.check and any_changed:
        return 1
    return 0
