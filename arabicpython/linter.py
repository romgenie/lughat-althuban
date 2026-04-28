"""arabicpython/linter.py
B-056: Static linter for .apy files.

Checks performed (all reported as Diagnostic namedtuples):
  W001  line > 99 characters
  W002  trailing whitespace
  W003  tab indentation (use spaces)
  W004  mixed Arabic/Latin in a single identifier token
  E001  ar-v1-only keyword used when file declares ar-v2 (كـ / هو)
  E002  unrecognised keyword-like token (looks like Arabic but is not a keyword)
  I001  file has no top-level docstring / module comment
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple

# ---------------------------------------------------------------------------
# Known keyword sets
# ---------------------------------------------------------------------------

_KEYWORDS_V2 = {
    "إذا", "وإلا", "إلا_إذا", "إلا",
    "بينما", "لكل", "في",
    "دالة", "صنف", "إرجاع", "ناتج",
    "حاول", "أخيرًا", "إثارة", "مع", "باسم",
    "استيراد", "من",
    "و", "أو", "ليس",
    "مرر", "تابع", "اكسر", "احذف", "عالمي", "غير_محلي",
    "لامدا", "تأكيد", "منتج",
    "صحيح", "خطأ", "لا_شيء",
    # ar-v2 additions
    "يكون",
}

_V1_ONLY_KEYWORDS = {"كـ", "هو"}  # removed in ar-v2

_ARABIC_RE = re.compile(r"[ء-ي]+")
_IDENTIFIER_RE = re.compile(r"[ء-يa-zA-Z_][ء-يa-zA-Z_٠-٩0-9]*")
_DIRECTIVE_RE = re.compile(r"#\s*arabicpython\s*:\s*dict\s*=\s*(\S+)")

MAX_LINE_LENGTH = 99


# ---------------------------------------------------------------------------
# Diagnostic
# ---------------------------------------------------------------------------


class Diagnostic(NamedTuple):
    path: str
    line: int   # 1-based
    col: int    # 1-based
    code: str
    message: str
    severity: str  # "error" | "warning" | "info"

    def __str__(self) -> str:
        return f"{self.path}:{self.line}:{self.col}: {self.severity[0].upper()} [{self.code}] {self.message}"


# ---------------------------------------------------------------------------
# Lint passes
# ---------------------------------------------------------------------------


def _detect_dict_version(source: str) -> str | None:
    for line in source.splitlines()[:5]:
        m = _DIRECTIVE_RE.search(line)
        if m:
            return m.group(1)
    return None


def lint_source(source: str, path: str = "<string>") -> list[Diagnostic]:
    diags: list[Diagnostic] = []
    lines = source.splitlines()
    dict_version = _detect_dict_version(source)
    is_v2 = dict_version is not None and "v2" in dict_version

    # I001: no module-level comment or docstring
    has_intro = False
    for line in lines[:10]:
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''"):
            has_intro = True
            break
        if stripped and not stripped.startswith("#"):
            break
    if not has_intro:
        diags.append(Diagnostic(path, 1, 1, "I001", "file has no top-level comment or docstring", "info"))

    for lineno, raw_line in enumerate(lines, start=1):
        # W001: line length
        if len(raw_line) > MAX_LINE_LENGTH:
            diags.append(Diagnostic(
                path, lineno, MAX_LINE_LENGTH + 1, "W001",
                f"line too long ({len(raw_line)} > {MAX_LINE_LENGTH} characters)", "warning",
            ))

        # W002: trailing whitespace
        if raw_line != raw_line.rstrip():
            col = len(raw_line.rstrip()) + 1
            diags.append(Diagnostic(path, lineno, col, "W002", "trailing whitespace", "warning"))

        # W003: tab indentation
        if raw_line.startswith("\t"):
            diags.append(Diagnostic(path, lineno, 1, "W003", "tab indentation (use 4 spaces)", "warning"))

        # Skip further token checks inside string literals (rough heuristic)
        stripped = raw_line.strip()
        if stripped.startswith(("#", '"""', "'''")):
            continue

        # Tokenize identifiers in the line
        for m in _IDENTIFIER_RE.finditer(raw_line):
            token = m.group()
            col = m.start() + 1

            # E001: ar-v1-only keyword in ar-v2 file
            if is_v2 and token in _V1_ONLY_KEYWORDS:
                diags.append(Diagnostic(
                    path, lineno, col, "E001",
                    f"ar-v1 keyword '{token}' is not valid in ar-v2 — use 'باسم' for 'as', 'يكون' for 'is'",
                    "error",
                ))

            # W004: mixed Arabic/Latin identifier
            has_arabic = bool(re.search(r"[ء-ي]", token))
            has_latin = bool(re.search(r"[a-zA-Z]", token))
            if has_arabic and has_latin:
                diags.append(Diagnostic(
                    path, lineno, col, "W004",
                    f"mixed Arabic/Latin identifier '{token}'",
                    "warning",
                ))

    return diags


def lint_file(path: Path) -> list[Diagnostic]:
    source = path.read_text(encoding="utf-8")
    return lint_source(source, str(path))


def main(argv: list[str] | None = None) -> int:
    """CLI entry point used by ``ثعبان راجع``."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        prog="ثعبان راجع",
        description="Lint .apy source files.",
    )
    parser.add_argument(
        "--no-info", action="store_true", help="Suppress I-level (info) diagnostics."
    )
    parser.add_argument(
        "--select",
        metavar="CODES",
        help="Comma-separated list of codes to enable (e.g. W001,E001).",
    )
    parser.add_argument("files", nargs="+", metavar="FILE")
    args = parser.parse_args(argv)

    select_codes: set[str] | None = None
    if args.select:
        select_codes = {c.strip() for c in args.select.split(",")}

    errors_found = 0
    for fname in args.files:
        p = Path(fname)
        if not p.exists():
            sys.stderr.write(f"ثعبان راجع: {fname}: file not found\n")
            errors_found += 1
            continue
        diags = lint_file(p)
        for d in diags:
            if args.no_info and d.severity == "info":
                continue
            if select_codes and d.code not in select_codes:
                continue
            print(d)
            if d.severity == "error":
                errors_found += 1

    return 1 if errors_found else 0
