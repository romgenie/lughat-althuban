"""Pre-process Arabic Python source for Python's tokenizer."""

import unicodedata

_BIDI_CONTROLS = frozenset("\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069")
_ASCII_DIGITS = frozenset("0123456789")
_ARABIC_INDIC_DIGITS = frozenset("٠١٢٣٤٥٦٧٨٩")
_EASTERN_ARABIC_INDIC_DIGITS = frozenset("۰۱۲۳۴۵۶۷۸۹")
_ALL_DIGITS = _ASCII_DIGITS | _ARABIC_INDIC_DIGITS | _EASTERN_ARABIC_INDIC_DIGITS

_PUNCTUATION_TRANSLATE = str.maketrans(
    {
        "٠": "0",
        "١": "1",
        "٢": "2",
        "٣": "3",
        "٤": "4",
        "٥": "5",
        "٦": "6",
        "٧": "7",
        "٨": "8",
        "٩": "9",
        "۰": "0",
        "۱": "1",
        "۲": "2",
        "۳": "3",
        "۴": "4",
        "۵": "5",
        "۶": "6",
        "۷": "7",
        "۸": "8",
        "۹": "9",
        "،": ",",
        "؛": ";",
        "؟": "?",
    }
)


def pretokenize(source: str) -> str:
    """Pre-process Arabic Python source for Python's tokenizer.

    Performs three transformations during a single left-to-right walk:

    1. Outside string literals: replace U+0660-U+0669 (Arabic-Indic digits)
       and U+06F0-U+06F9 (Eastern Arabic-Indic digits) with the corresponding
       ASCII digits 0-9.
    2. Outside string literals: replace U+060C (،) with U+002C (,),
       U+061B (؛) with U+003B (;), U+061F (؟) with U+003F (?).
    3. Outside string literals: raise SyntaxError if any of U+202A-U+202E or
       U+2066-U+2069 (bidi control characters) is encountered. Inside string
       literals these pass through unchanged.

    Single-line and multi-line string literals (', ", ''', \"\"\") and string
    prefixes (r, b, u, f, and case-insensitive combinations) are recognized.
    String contents are preserved byte-for-byte.

    Comments (# ... newline) are NOT string literals: substitutions apply and
    bidi controls are rejected (per ADR 0006: comments are an attack vector,
    not a safe haven).

    A run of consecutive digit characters that mixes digit systems (e.g.,
    `١2` mixing Arabic-Indic and ASCII) raises SyntaxError. Pure-system runs
    are folded to ASCII; pure-ASCII runs pass through unchanged.

    Args:
        source: the .apy source text.

    Returns:
        Source text with the substitutions applied.

    Raises:
        SyntaxError: with the exact format from ADR 0006 for bidi controls,
            or a clear message naming the offending characters and line/column
            for mixed-digit literals.
    """
    state = "DEFAULT"
    out = []
    line = 1
    col = 0
    i = 0
    n = len(source)

    escape_next = False

    while i < n:
        ch = source[i]

        if escape_next:
            out.append(ch)
            escape_next = False
            if ch == "\n":
                line += 1
                col = 0
            else:
                col += 1
            i += 1
            continue

        if state == "DEFAULT":
            if ch in _BIDI_CONTROLS:
                name = unicodedata.name(ch, "UNKNOWN")
                code = f"U+{ord(ch):04X}"
                raise SyntaxError(
                    f"bidi control character {code} ({name}) is not allowed outside "
                    f"string literals at line {line}, column {col}. "
                    f"See https://trojansource.codes for why."
                )

            if ch == "#":
                state = "COMMENT"
                out.append(ch)
                col += 1
                i += 1
                continue

            if ch in ("'", '"'):
                if source[i : i + 3] == "'''":
                    state = "STRING_TSQ"
                    out.append("'''")
                    col += 3
                    i += 3
                    continue
                elif source[i : i + 3] == '"""':
                    state = "STRING_TDQ"
                    out.append('"""')
                    col += 3
                    i += 3
                    continue
                else:
                    state = "STRING_SQ" if ch == "'" else "STRING_DQ"
                    out.append(ch)
                    col += 1
                    i += 1
                    continue

            if ch in _ALL_DIGITS:
                start_i = i
                while i < n and source[i] in _ALL_DIGITS:
                    i += 1
                run = source[start_i:i]
                sys_names = []
                if any(c in _ASCII_DIGITS for c in run):
                    sys_names.append("ASCII")
                if any(c in _ARABIC_INDIC_DIGITS for c in run):
                    sys_names.append("Arabic-Indic")
                if any(c in _EASTERN_ARABIC_INDIC_DIGITS for c in run):
                    sys_names.append("Eastern Arabic-Indic")

                if len(sys_names) > 1:
                    if len(sys_names) == 2:
                        sys_str = f"{sys_names[0]} and {sys_names[1]}"
                    else:
                        sys_str = "ASCII, Arabic-Indic, and Eastern Arabic-Indic"
                    raise SyntaxError(
                        f"mixed digit systems in numeric literal at line {line}, column {col} "
                        f"— found {sys_str} digits in '{run}'. Use one system per literal."
                    )

                translated = run.translate(_PUNCTUATION_TRANSLATE)
                out.append(translated)
                col += len(run)
                continue

            # Normal char
            out.append(ch.translate(_PUNCTUATION_TRANSLATE))
            if ch == "\n":
                line += 1
                col = 0
            else:
                col += 1
            i += 1
            continue

        elif state == "COMMENT":
            if ch in _BIDI_CONTROLS:
                name = unicodedata.name(ch, "UNKNOWN")
                code = f"U+{ord(ch):04X}"
                raise SyntaxError(
                    f"bidi control character {code} ({name}) is not allowed outside "
                    f"string literals at line {line}, column {col}. "
                    f"See https://trojansource.codes for why."
                )
            out.append(ch.translate(_PUNCTUATION_TRANSLATE))
            if ch == "\n":
                state = "DEFAULT"
                line += 1
                col = 0
            else:
                col += 1
            i += 1
            continue

        elif state.startswith("STRING_"):
            out.append(ch)
            if ch == "\\":
                escape_next = True
                col += 1
                i += 1
                continue

            if state == "STRING_SQ" and ch == "'" or state == "STRING_DQ" and ch == '"':
                state = "DEFAULT"
            elif state == "STRING_TSQ" and ch == "'":
                if source[i : i + 3] == "'''":
                    out.append("''")
                    col += 3
                    i += 3
                    state = "DEFAULT"
                    continue
            elif state == "STRING_TDQ" and ch == '"' and source[i : i + 3] == '"""':
                out.append('""')
                col += 3
                i += 3
                state = "DEFAULT"
                continue

            if ch == "\n":
                line += 1
                col = 0
            else:
                col += 1
            i += 1

    return "".join(out)
