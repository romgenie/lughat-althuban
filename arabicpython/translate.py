"""Translate apython source to Python source."""

import io
import sys
import tokenize
from typing import TYPE_CHECKING

from arabicpython._fstring_311 import rewrite_fstring_literal
from arabicpython.dialect import load_dialect
from arabicpython.normalize import normalize_identifier
from arabicpython.pretokenize import pretokenize

if TYPE_CHECKING:
    from arabicpython.dialect import Dialect


def translate(source: str, *, dialect: "Dialect | None" = None) -> str:
    """Translate apython source to Python source.

    Pipeline:
      1. pretokenize(source) — fold Arabic digits/punctuation, reject bidi
         outside strings (raises SyntaxError on bidi or mixed-digit literals).
      2. tokenize.tokenize on the result, treated as UTF-8 bytes.
      3. Walk the token stream. For each NAME token:
         - If the previous non-whitespace, non-comment token is OP('.'),
           look up normalize_identifier(name) in dialect.attributes.
         - Otherwise, look up normalize_identifier(name) in dialect.names.
         - On hit, replace the token's string with the dictionary's Python
           symbol (e.g., 'إذا' → 'if', 'قراءة' → 'read').
         - On miss, replace with normalize_identifier(name) — collapses
           harakat/hamza variants per ADR 0004 so equivalent spellings refer
           to the same Python identifier.
         - ASCII-only NAME tokens that are unchanged by normalize_identifier
           pass through untouched.
      4. untokenize and return the result as a str.

    Args:
        source: the .apy source text.
        dialect: optional Dialect to use; defaults to load_dialect("ar-v1").

    Returns:
        Python source text suitable for compile(src, path, "exec").

    Raises:
        SyntaxError: propagated from pretokenize (bidi, mixed digits) or
            from tokenize (e.g., unclosed string literal).
        DialectError: propagated from load_dialect on first call when no
            explicit dialect is provided.
    """
    if dialect is None:
        dialect = load_dialect("ar-v1")

    # Step 1: pretokenize
    intermediate = pretokenize(source)

    # Step 2: tokenize
    try:
        tokens_gen = tokenize.tokenize(io.BytesIO(intermediate.encode("utf-8")).readline)
        tokens = list(tokens_gen)
    except tokenize.TokenError as e:
        msg, loc = e.args
        raise SyntaxError(msg, ("<string>", loc[0], loc[1], "", loc[0], loc[1])) from e

    for tok in tokens:
        if tok.type == tokenize.ERRORTOKEN:
            raise SyntaxError(
                f"tokenization error near {tok.string!r}",
                ("<string>", tok.start[0], tok.start[1], tok.line, tok.start[0], tok.start[1]),
            )

    # Step 3: NAME rewrite
    new_tokens = []
    # Track last significant token to check for attribute context
    last_significant_type = None
    last_significant_string = None

    for tok in tokens:
        is_significant = tok.type not in (
            tokenize.NL,
            tokenize.NEWLINE,
            tokenize.INDENT,
            tokenize.DEDENT,
            tokenize.COMMENT,
            tokenize.ENCODING,
            tokenize.ENDMARKER,
        )

        if tok.type == tokenize.NAME:
            is_attr = last_significant_type == tokenize.OP and last_significant_string == "."
            key = normalize_identifier(tok.string)

            if is_attr and key in dialect.attributes:
                new_string = dialect.attributes[key]
            elif not is_attr and key in dialect.names:
                new_string = dialect.names[key]
            else:
                new_string = key

            if new_string == tok.string:
                new_tokens.append(tok)
            else:
                new_tokens.append(
                    tokenize.TokenInfo(tokenize.NAME, new_string, tok.start, tok.end, tok.line)
                )
        elif tok.type == tokenize.STRING and sys.version_info < (3, 12):
            # TODO(phase-b-drop-311): delete this branch and rewrite_fstring_literal
            # when 3.11 support is dropped.
            new_literal = rewrite_fstring_literal(tok.string, dialect)
            if new_literal == tok.string:
                new_tokens.append(tok)
            else:
                new_tokens.append(
                    tokenize.TokenInfo(tokenize.STRING, new_literal, tok.start, tok.end, tok.line)
                )
        else:
            new_tokens.append(tok)

        if is_significant:
            last_significant_type = tok.type
            last_significant_string = tok.string

    # Step 4: untokenize
    try:
        result_bytes = tokenize.untokenize(new_tokens)
    except tokenize.TokenError as e:
        msg, loc = e.args
        raise SyntaxError(msg, ("<string>", loc[0], loc[1], "", loc[0], loc[1])) from e

    result_str = result_bytes.decode("utf-8") if isinstance(result_bytes, bytes) else result_bytes

    # Strip BOM if present
    if result_str.startswith("\ufeff"):
        result_str = result_str[1:]

    return result_str
