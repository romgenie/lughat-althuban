"""F-string interior rewriter for Python 3.11."""

import io
import tokenize
from typing import TYPE_CHECKING

from arabicpython.normalize import normalize_identifier

if TYPE_CHECKING:
    from arabicpython.dialect import Dialect


def rewrite_fstring_literal(literal: str, dialect: "Dialect", *, strict: bool = False) -> str:
    """Rewrite identifiers inside an f-string literal's expression regions."""
    prefix, quote, body = _split_literal(literal)
    if "f" not in prefix.lower():
        return literal

    new_body = []
    i = 0
    n = len(body)
    while i < n:
        if body[i] == "{":
            if i + 1 < n and body[i + 1] == "{":
                new_body.append("{{")
                i += 2
                continue
            # Start of expression region
            expr_start = i + 1
            i += 1
            depth = 0
            expr_end = -1

            # Markers found at depth 0

            while i < n:
                ch = body[i]
                if ch in "([{":
                    depth += 1
                    i += 1
                elif ch in ")]}":
                    if depth == 0:
                        if ch == "}":
                            # End of whole region
                            if expr_end == -1:
                                expr_end = i
                            i + 1

                            expr_src = body[expr_start:expr_end]
                            rewritten_expr = _rewrite_expression_source(
                                expr_src, dialect, strict=strict
                            )

                            # The part from expr_end to i is conversion/format_spec
                            tail = body[expr_end:i]
                            # Format spec may contain nested expressions
                            if ":" in tail:
                                colon_idx = tail.find(":")
                                head = tail[: colon_idx + 1]
                                spec = tail[colon_idx + 1 :]
                                # Recursively rewrite the spec.
                                # We treat the spec as a "body" of an f-string.
                                rewritten_spec = _rewrite_fstring_body(spec, dialect, strict=strict)
                                tail = head + rewritten_spec

                            new_body.append("{" + rewritten_expr + tail + "}")
                            i += 1
                            break
                        else:
                            # Unbalanced ) or ]
                            raise SyntaxError(f"f-string: unmatched '{ch}'")
                    else:
                        depth -= 1
                        i += 1
                elif depth == 0 and expr_end == -1:
                    if ch == "=" and (i + 1 == n or body[i + 1] != "="):
                        expr_end = i + 1  # Include = in expr_src? No, spec says:
                        # "the literal x before the = is part of the expression;
                        # the trailing = is not."
                        # But wait, if I exclude =, I need to add it back.
                        expr_end = i
                        i += 1
                    elif ch == "!":
                        expr_end = i
                        # Skip conversion marker !r, !s, !a
                        i += 1
                        if i < n and body[i] in "rsa":
                            i += 1
                        else:
                            # Not a valid conversion marker? Let it be.
                            pass
                    elif ch == ":":
                        expr_end = i
                        # Resume loop to find closing } for format spec
                        i += 1
                    elif ch == "\\":
                        raise SyntaxError("f-string expression part cannot include a backslash")
                    else:
                        i += 1
                elif ch == "\\":
                    # Backslash anywhere in 3.11 f-string expression is bad
                    raise SyntaxError("f-string expression part cannot include a backslash")
                else:
                    i += 1
            else:
                if i == n:
                    raise SyntaxError("f-string: expected '}' before end of f-string")
        elif body[i] == "}":
            if i + 1 < n and body[i + 1] == "}":
                new_body.append("}}")
                i += 2
                continue
            raise SyntaxError("f-string: single '}' in f-string literal")
        else:
            new_body.append(body[i])
            i += 1

    return prefix + quote + "".join(new_body) + quote


def _split_literal(literal: str) -> tuple[str, str, str]:
    """Split literal into (prefix, quote, body)."""
    # Find first quote
    first_quote_idx = -1
    for i, ch in enumerate(literal):
        if ch in ("'", '"'):
            first_quote_idx = i
            break
    if first_quote_idx == -1:
        return "", "", literal

    prefix = literal[:first_quote_idx]
    rest = literal[first_quote_idx:]

    if rest.startswith('"""') or rest.startswith("'''"):
        quote = rest[:3]
        body = rest[3:-3]
    else:
        quote = rest[0]
        body = rest[1:-1]

    return prefix, quote, body


def _rewrite_fstring_body(body: str, dialect: "Dialect", *, strict: bool) -> str:
    """Helper for recursive format spec rewriting. Does not handle outer quotes."""
    new_body = []
    i = 0
    n = len(body)
    while i < n:
        if body[i] == "{":
            if i + 1 < n and body[i + 1] == "{":
                new_body.append("{{")
                i += 2
                continue
            expr_start = i + 1
            i += 1
            depth = 0
            expr_end = -1
            while i < n:
                ch = body[i]
                if ch in "([{":
                    depth += 1
                    i += 1
                elif ch in ")]}":
                    if depth == 0:
                        if ch == "}":
                            if expr_end == -1:
                                expr_end = i
                            expr_src = body[expr_start:expr_end]
                            rewritten_expr = _rewrite_expression_source(
                                expr_src, dialect, strict=strict
                            )
                            tail = body[expr_end:i]
                            if ":" in tail:
                                colon_idx = tail.find(":")
                                tail = tail[: colon_idx + 1] + _rewrite_fstring_body(
                                    tail[colon_idx + 1 :], dialect, strict=strict
                                )
                            new_body.append("{" + rewritten_expr + tail + "}")
                            i += 1
                            break
                        depth -= 1
                        i += 1
                    else:
                        depth -= 1
                        i += 1
                elif depth == 0 and expr_end == -1:
                    if ch in "!=":  # conversion or self-doc
                        expr_end = i
                        i += 1
                        if ch == "!" and i < n and body[i] in "rsa":
                            i += 1
                    elif ch == ":":
                        expr_end = i
                        i += 1
                    else:
                        i += 1
                else:
                    i += 1
            else:
                raise SyntaxError("f-string: expected '}'")
        elif body[i] == "}":
            if i + 1 < n and body[i + 1] == "}":
                new_body.append("}}")
                i += 2
                continue
            raise SyntaxError("f-string: single '}'")
        else:
            new_body.append(body[i])
            i += 1
    return "".join(new_body)


def _rewrite_expression_source(expr_src: str, dialect: "Dialect", *, strict: bool) -> str:
    """Rewrite NAMEs in a Python expression string."""
    if not expr_src.strip():
        return expr_src

    # Wrap in dummy assignment to ensure it's a valid tokenizable statement
    wrapped = "_ = (" + expr_src + ")\n"
    try:
        tokens = list(tokenize.tokenize(io.BytesIO(wrapped.encode("utf-8")).readline))
    except (tokenize.TokenError, SyntaxError) as e:
        raise SyntaxError(f"f-string: invalid expression '{expr_src}'") from e

    new_tokens = []
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
            # Check if this is the dummy variable we added
            if tok.string == "_" and tok.start == (1, 0):
                new_tokens.append(tok)
            else:
                is_attr = last_significant_type == tokenize.OP and last_significant_string == "."
                key = normalize_identifier(tok.string, strict=strict)

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
        else:
            new_tokens.append(tok)

        if is_significant:
            last_significant_type = tok.type
            last_significant_string = tok.string

    try:
        result_bytes = tokenize.untokenize(new_tokens)
    except Exception as e:
        raise SyntaxError(f"f-string: untokenize failed for '{expr_src}'") from e

    result_str = result_bytes.decode("utf-8") if isinstance(result_bytes, bytes) else result_bytes

    # Strip BOM if present
    if result_str.startswith("\ufeff"):
        result_str = result_str[1:]

    # Strip wrapper: "_ = (" and ")\n"
    # untokenize might add spaces.
    # We find the first "(" and the last ")".
    start_paren = result_str.find("(")
    end_paren = result_str.rfind(")")
    return result_str[start_paren + 1 : end_paren]
