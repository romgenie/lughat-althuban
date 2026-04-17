from __future__ import annotations

from pathlib import Path

from arabicpython.normalize import normalize_identifier

HARAKAT_BLOCK = "".join(chr(codepoint) for codepoint in range(0x064B, 0x0660))
SUPERSCRIPT_ALEF = "\u0670"
PRESENTATION_FORM_MEEM = "\ufee3"
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _dictionary_canonical_entries() -> list[str]:
    entries: list[str] = []
    for line in (
        (PROJECT_ROOT / "dictionaries" / "ar-v1.md").read_text(encoding="utf-8").splitlines()
    ):
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue

        cells = [cell.strip() for cell in stripped.split("|")[1:-1]]
        if len(cells) < 4:
            continue
        if cells[0] == "Python" or cells[1] == "Canonical":
            continue
        if all(set(cell) <= {"-"} for cell in cells):
            continue

        entries.append(cells[1])
    return entries


def test_empty_string() -> None:
    assert normalize_identifier("") == ""


def test_ascii_passthrough() -> None:
    assert normalize_identifier("hello_world") == "hello_world"


def test_ascii_numbers_passthrough() -> None:
    assert normalize_identifier("var123") == "var123"


def test_plain_arabic_passthrough() -> None:
    assert normalize_identifier("كتاب") == "كتاب"


def test_nfkc_presentation_form() -> None:
    assert normalize_identifier(PRESENTATION_FORM_MEEM) == "م"


def test_nfkc_applied_in_strict() -> None:
    assert normalize_identifier(PRESENTATION_FORM_MEEM, strict=True) == "م"


def test_tatweel_stripped() -> None:
    assert normalize_identifier("مـرحـبا") == "مرحبا"


def test_tatweel_at_edges() -> None:
    assert normalize_identifier("ـمرحباـ") == "مرحبا"


def test_only_tatweel() -> None:
    assert normalize_identifier("ـــ") == ""


def test_fatha_stripped() -> None:
    assert normalize_identifier("مَرحبا") == "مرحبا"


def test_kasra_stripped() -> None:
    assert normalize_identifier("مِرحبا") == "مرحبا"


def test_damma_stripped() -> None:
    assert normalize_identifier("مُرحبا") == "مرحبا"


def test_sukun_stripped() -> None:
    assert normalize_identifier("مْرحبا") == "مرحبا"


def test_shadda_stripped() -> None:
    assert normalize_identifier("مّرحبا") == "مرحبا"


def test_tanwin_stripped() -> None:
    assert normalize_identifier("مًٌٍرحبا") == "مرحبا"


def test_superscript_alef_stripped() -> None:
    assert normalize_identifier("رحمٰن") == "رحمن"


def test_all_harakat_combined() -> None:
    assert normalize_identifier("ب" + HARAKAT_BLOCK + SUPERSCRIPT_ALEF + "ت") == "بت"


def test_hamza_above_folded() -> None:
    assert normalize_identifier("أ") == "ا"


def test_hamza_below_folded() -> None:
    assert normalize_identifier("إ") == "ا"


def test_madda_folded() -> None:
    assert normalize_identifier("آ") == "ا"


def test_hamza_at_start() -> None:
    assert normalize_identifier("أحمد") == "احمد"


def test_hamza_at_middle() -> None:
    assert normalize_identifier("سأل") == "سال"


def test_hamza_at_end() -> None:
    assert normalize_identifier("بدأ") == "بدا"


def test_multiple_hamzas() -> None:
    assert normalize_identifier("أكدأ") == "اكدا"


def test_alef_maksura_final_folded() -> None:
    assert normalize_identifier("مشى") == "مشي"


def test_alef_maksura_not_final_preserved() -> None:
    assert normalize_identifier("ىa") == "ىa"


def test_alef_maksura_only() -> None:
    assert normalize_identifier("ى") == "ي"


def test_ta_marbuta_final_folded() -> None:
    assert normalize_identifier("شجرة") == "شجره"


def test_ta_marbuta_not_final_preserved() -> None:
    assert normalize_identifier("ةa") == "ةa"


def test_ta_marbuta_only() -> None:
    assert normalize_identifier("ة") == "ه"


def test_strict_mode_preserves_harakat() -> None:
    assert normalize_identifier("مَرحَبا", strict=True) == "مَرحَبا"


def test_strict_mode_preserves_tatweel() -> None:
    assert normalize_identifier("مـرحبا", strict=True) == "مـرحبا"


def test_strict_mode_preserves_hamza_variants() -> None:
    assert normalize_identifier("أحمد", strict=True) == "أحمد"


def test_strict_mode_still_applies_nfkc() -> None:
    assert normalize_identifier(PRESENTATION_FORM_MEEM, strict=True) == "م"


def test_idempotent_non_strict() -> None:
    samples = ["", "hello_world", "مَرحَبا", "مـرحـبا", "أحمد", "شجرة", "مشى", "خطا_قيمة"]
    for sample in samples:
        normalized = normalize_identifier(sample)
        assert normalize_identifier(normalized) == normalized


def test_idempotent_strict() -> None:
    samples = ["", "hello_world", "مَرحَبا", "مـرحـبا", "أحمد", "شجرة", "مشى", "خطا_قيمة"]
    for sample in samples:
        normalized = normalize_identifier(sample, strict=True)
        assert normalize_identifier(normalized, strict=True) == normalized


def test_tatweel_and_harakat_together() -> None:
    assert normalize_identifier("مَـرحَـبا") == "مرحبا"


def test_hamza_and_harakat_together() -> None:
    assert normalize_identifier("أَحمد") == "احمد"


def test_all_at_once() -> None:
    assert normalize_identifier(PRESENTATION_FORM_MEEM + "ـأَشجَرَة") == "ماشجره"


def test_dictionary_entries_idempotent() -> None:
    entries = _dictionary_canonical_entries()

    assert len(entries) >= 150

    for entry in entries:
        normalized = normalize_identifier(entry)
        assert normalize_identifier(normalized) == normalized


def test_latin_preserved() -> None:
    assert normalize_identifier("variableName") == "variableName"


def test_mixed_script_identifier() -> None:
    assert normalize_identifier("myمتغير") == "myمتغير"


def test_digits_passthrough() -> None:
    assert normalize_identifier("var_123") == "var_123"
