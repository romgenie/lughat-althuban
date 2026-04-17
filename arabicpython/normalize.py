"""Identifier normalization for Arabic Python."""

from __future__ import annotations

import unicodedata

TATWEEL = "\u0640"
SUPERSCRIPT_ALEF = "\u0670"
ALEF_MAKSURA = "\u0649"
YEH = "\u064a"
TA_MARBUTA = "\u0629"
HEH = "\u0647"

HARAKAT = frozenset(chr(codepoint) for codepoint in range(0x064B, 0x0660)) | frozenset(
    {SUPERSCRIPT_ALEF}
)
HAMZA_FOLD_TRANSLATION = str.maketrans(
    {
        "\u0622": "\u0627",  # ALEF WITH MADDA ABOVE -> ALEF
        "\u0623": "\u0627",  # ALEF WITH HAMZA ABOVE -> ALEF
        "\u0625": "\u0627",  # ALEF WITH HAMZA BELOW -> ALEF
    }
)


def normalize_identifier(s: str, *, strict: bool = False) -> str:
    """Normalize an Arabic (or mixed-script) identifier to canonical form."""
    normalized = unicodedata.normalize("NFKC", s)
    if strict:
        return normalized

    stripped = "".join(ch for ch in normalized if ch != TATWEEL and ch not in HARAKAT)
    folded = stripped.translate(HAMZA_FOLD_TRANSLATION)

    if not folded:
        return folded
    if folded[-1] == ALEF_MAKSURA:
        return folded[:-1] + YEH
    if folded[-1] == TA_MARBUTA:
        return folded[:-1] + HEH
    return folded
