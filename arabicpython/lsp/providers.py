"""B-052: LSP feature providers — pure, testable, no I/O.

Each provider function takes plain data (source text, position, dialect) and
returns plain data (strings, dicts).  The server loop in server.py calls these
and wraps the results in JSON-RPC responses.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from arabicpython.dialect import Dialect  # noqa: F401

# ── Helpers ───────────────────────────────────────────────────────────────────

# Arabic word boundary: sequence of Arabic letters, digits, combining marks,
# underscores, and tatweel — same character classes the pre-tokeniser accepts.
_ARABIC_WORD_RE = re.compile(r"[؀-ۿݐ-ݿ\w]+")

# Map dialect category codes to human-readable Arabic labels
_CATEGORY_LABEL: dict[str, str] = {
    "keyword": "كلمة مفتاحية",
    "literal": "قيمة حرفية",
    "type": "نوع مدمج",
    "builtin_func": "دالة مدمجة",
    "builtin_exc": "استثناء مدمج",
    "builtin_const": "ثابت مدمج",
    "attribute": "خاصية",
    "dunder": "خاصية خاصة",
}

# LSP CompletionItemKind constants
_KIND_KEYWORD = 14
_KIND_FUNCTION = 3
_KIND_CLASS = 7
_KIND_CONSTANT = 21
_KIND_FIELD = 5

_CATEGORY_KIND: dict[str, int] = {
    "keyword": _KIND_KEYWORD,
    "literal": _KIND_CONSTANT,
    "type": _KIND_CLASS,
    "builtin_func": _KIND_FUNCTION,
    "builtin_exc": _KIND_CLASS,
    "builtin_const": _KIND_CONSTANT,
    "attribute": _KIND_FIELD,
    "dunder": _KIND_FIELD,
}


def _word_at(source: str, line: int, character: int) -> str | None:
    """Return the Arabic word token at (line, character) in *source*, or None.

    *line* and *character* are 0-based LSP positions.
    """
    lines = source.splitlines()
    if line >= len(lines):
        return None
    row = lines[line]
    if character > len(row):
        return None
    for m in _ARABIC_WORD_RE.finditer(row):
        if m.start() <= character < m.end():
            return m.group()
    return None


# ── Hover provider ────────────────────────────────────────────────────────────


def get_hover(source: str, line: int, character: int, dialect: Dialect) -> str | None:
    """Return a Markdown hover string for the word at (line, character).

    Returns None if the position is not over a known Arabic word.
    """
    from arabicpython.normalize import normalize_identifier

    word = _word_at(source, line, character)
    if word is None:
        return None

    key = normalize_identifier(word)

    python_name = dialect.names.get(key)
    if python_name is None:
        # Not a keyword/builtin — could still be a user identifier.
        # Return a neutral hover showing the normalised form.
        if key != word:
            return f"**{word}** → `{key}` *(معرّف مستخدم)*"
        return None

    category = dialect.categories.get(key, "")
    label = _CATEGORY_LABEL.get(category, category)
    lines_md: list[str] = [f"**{word}** → `{python_name}`"]
    if label:
        lines_md.append(f"*{label}*")
    return "\n\n".join(lines_md)


# ── Diagnostics provider ──────────────────────────────────────────────────────


def get_diagnostics(source: str, uri: str) -> list[dict]:
    """Translate *source* and compile it; return LSP diagnostic objects for errors.

    Returns an empty list when the source is valid.
    Each diagnostic dict follows the LSP ``Diagnostic`` shape:
    ``{range, severity, source, message}``.
    """
    from arabicpython.translate import translate

    # Severity 1 = Error, 2 = Warning
    def _make(line: int, col: int, end_line: int, end_col: int, msg: str) -> dict:
        return {
            "range": {
                "start": {"line": line, "character": col},
                "end": {"line": end_line, "character": end_col},
            },
            "severity": 1,
            "source": "ثعبان",
            "message": msg,
        }

    try:
        translated = translate(source)
    except SyntaxError as e:
        ln = max((e.lineno or 1) - 1, 0)
        col = max((e.offset or 1) - 1, 0)
        end_col = col + max(e.end_offset - e.offset, 1) if e.end_offset else col + 1
        from arabicpython.tracebacks import translate_exception_message

        msg = translate_exception_message(e.msg)
        return [_make(ln, col, ln, end_col, msg)]
    except Exception as e:  # pretokenize errors etc.
        return [_make(0, 0, 0, 1, str(e))]

    # Try to compile the translated source too
    try:
        compile(translated, uri, "exec")
    except SyntaxError as e:
        ln = max((e.lineno or 1) - 1, 0)
        col = max((e.offset or 1) - 1, 0)
        end_col = col + max(e.end_offset - e.offset, 1) if e.end_offset else col + 1
        from arabicpython.tracebacks import translate_exception_message

        msg = translate_exception_message(e.msg)
        return [_make(ln, col, ln, end_col, msg)]

    return []


# ── Completion provider ───────────────────────────────────────────────────────


def get_completions(source: str, line: int, character: int, dialect: Dialect) -> list[dict]:
    """Return LSP completion items for all known Arabic names.

    Filters by the word prefix already typed at (line, character).
    """
    from arabicpython.normalize import normalize_identifier

    # Find the word fragment before the cursor
    lines = source.splitlines()
    prefix = ""
    if line < len(lines):
        row = lines[line]
        col = min(character, len(row))
        # Walk left collecting Arabic/identifier characters
        i = col
        while i > 0 and (_ARABIC_WORD_RE.match(row[i - 1]) or row[i - 1] == "_"):
            i -= 1
        prefix = normalize_identifier(row[i:col])

    items: list[dict] = []
    for arabic, python_name in dialect.names.items():
        if prefix and not arabic.startswith(prefix):
            continue
        category = dialect.categories.get(arabic, "")
        kind = _CATEGORY_KIND.get(category, _KIND_KEYWORD)
        items.append(
            {
                "label": arabic,
                "kind": kind,
                "detail": python_name,
                "documentation": {
                    "kind": "markdown",
                    "value": f"**{arabic}** → `{python_name}`",
                },
                "insertText": arabic,
            }
        )

    # Sort: keywords first, then alphabetically
    items.sort(key=lambda x: (0 if x.get("kind") == _KIND_KEYWORD else 1, x["label"]))
    return items
