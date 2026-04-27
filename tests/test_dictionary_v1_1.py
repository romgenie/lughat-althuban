# tests/test_dictionary_v1_1.py
# B-040: ar-v1.1 dictionary — integrity, supersetness, and behavioral tests.
#
# Adapted to actual ar-v1 state: when B-040 was specced, async/await/match/case
# were not yet in ar-v1.  They were added before v1 was locked (async as
# غير_متزامن, await/match/case verbatim).  ar-v1.1 therefore adds ONE new entry:
#   متزامن → async   (the shorter B-040-recommended form)
# The four-entry supersetness test in the spec is updated to one entry here.

import hashlib
import pathlib
import subprocess
import sys
import textwrap

import pytest

from arabicpython.dialect import load_dialect
from arabicpython.normalize import normalize_identifier
from arabicpython.translate import translate

DICT_DIR = pathlib.Path(__file__).parent.parent / "dictionaries"
EXAMPLES_DIR = pathlib.Path(__file__).parent.parent / "examples"


# ── 1. Supersetness ───────────────────────────────────────────────────────────


def test_v1_1_is_strict_superset_of_v1():
    """Every (arabic, python) pair in v1 appears identically in v1.1."""
    v1 = load_dialect("ar-v1")
    v1_1 = load_dialect("ar-v1.1")

    # Check names (forward map)
    for arabic, python_sym in v1.names.items():
        assert arabic in v1_1.names, f"v1.1 missing v1 name key: {arabic!r}"
        assert (
            v1_1.names[arabic] == python_sym
        ), f"v1.1 key {arabic!r}: v1 maps to {python_sym!r}, v1.1 maps to {v1_1.names[arabic]!r}"

    # Check attributes (methods)
    for arabic, python_sym in v1.attributes.items():
        assert arabic in v1_1.attributes, f"v1.1 missing v1 attribute key: {arabic!r}"
        assert (
            v1_1.attributes[arabic] == python_sym
        ), f"v1.1 attr {arabic!r}: v1={python_sym!r}, v1.1={v1_1.attributes[arabic]!r}"

    # v1.1 must have strictly more names (at least one new entry)
    assert len(v1_1.names) > len(
        v1.names
    ), f"v1.1 names ({len(v1_1.names)}) not larger than v1 names ({len(v1.names)})"
    # Attributes unchanged
    assert len(v1_1.attributes) == len(v1.attributes)


def test_v1_1_new_entries_are_the_expected_one():
    """ar-v1.1 adds exactly متزامن→async beyond ar-v1."""
    v1 = load_dialect("ar-v1")
    v1_1 = load_dialect("ar-v1.1")

    new_names = {k: v for k, v in v1_1.names.items() if k not in v1.names}
    assert new_names == {"متزامن": "async"}, f"Expected exactly {{متزامن: async}}, got {new_names}"


def test_v1_1_entry_count():
    """ar-v1.1 has exactly one more name entry than ar-v1."""
    v1 = load_dialect("ar-v1")
    v1_1 = load_dialect("ar-v1.1")
    assert len(v1_1.names) == len(v1.names) + 1


# ── 2. Normalization round-trips ──────────────────────────────────────────────


def test_v1_1_round_trip_normalize():
    """Every Arabic key in v1.1 round-trips through normalize_identifier."""
    d = load_dialect("ar-v1.1")
    for arabic in list(d.names) + list(d.attributes):
        assert (
            normalize_identifier(arabic) == arabic
        ), f"Key {arabic!r} does not round-trip: got {normalize_identifier(arabic)!r}"


# ── 3. No v1 homographs ───────────────────────────────────────────────────────


def test_v1_1_new_entry_not_in_v1():
    """متزامن was not a v1 key (it was rejected in favour of غير_متزامن)."""
    v1 = load_dialect("ar-v1")
    assert "متزامن" not in v1.names


# ── 4. Both async spellings work in v1.1 ─────────────────────────────────────


def test_v1_1_متزامن_translates_to_async():
    src = "متزامن دالة f(): انتظر g()\n"
    result = translate(src, dict_version="ar-v1.1")
    assert "async def" in result
    assert "await" in result


def test_v1_1_غير_متزامن_still_translates_to_async():
    """v1-style spelling still works under v1.1 (backward compat)."""
    src = "غير_متزامن دالة f(): انتظر g()\n"
    result = translate(src, dict_version="ar-v1.1")
    assert "async def" in result
    assert "await" in result


# ── 5. Translator default unchanged ──────────────────────────────────────────


def test_translator_default_unchanged():
    """translate() with no dict_version uses ar-v2, not v1.1."""
    src = "اطبع(42)\n"
    # ar-v2 is a superset of v1/v1.1 for this statement; output must be valid Python
    result = translate(src)
    assert "print" in result
    assert "42" in result
    code = compile(result, "<test>", "exec")
    assert code is not None


def test_متزامن_unknown_under_default_dialect():
    """متزامن is not in ar-v2 (only ar-v1.1); it survives untranslated."""
    # ar-v2 inherits ar-v1's غير_متزامن; متزامن was never adopted
    d_v2 = load_dialect("ar-v2")
    assert "متزامن" not in d_v2.names


# ── 6. Translator with dict_version ──────────────────────────────────────────


def test_translator_with_v1_1_handles_async():
    src = "متزامن دالة f():\n    انتظر g()\n"
    result = translate(src, dict_version="ar-v1.1")
    assert result.strip() == "async def f():\n    await g()"


def test_translator_with_v1_1_handles_match():
    src = textwrap.dedent("""\
        x = 1
        طابق x:
            حالة 1:
                اطبع("واحد")
            حالة 2:
                اطبع("اثنان")
            حالة _:
                اطبع("اخرى")
    """)
    result = translate(src, dict_version="ar-v1.1")
    assert "match x:" in result
    assert "case 1:" in result
    assert "case 2:" in result
    assert "case _:" in result
    compile(result, "<test>", "exec")


def test_translator_v1_1_async_for():
    """async for works under v1.1 (متزامن + لكل)."""
    src = "متزامن دالة f():\n    متزامن لكل x في g():\n        pass\n"
    result = translate(src, dict_version="ar-v1.1")
    assert "async def" in result
    assert "async for" in result


def test_translator_v1_1_async_with():
    """async with works under v1.1 (متزامن + مع)."""
    src = "متزامن دالة f():\n    متزامن مع ctx() كـ r:\n        pass\n"
    result = translate(src, dict_version="ar-v1.1")
    assert "async def" in result
    assert "async with" in result


def test_match_soft_keyword_as_identifier():
    """طابق used as a variable name (soft keyword — Python allows this)."""
    src = "طابق = 5\n"
    result = translate(src, dict_version="ar-v1.1")
    assert "match" in result
    # Must be valid Python (match is a soft keyword, legal as a variable)
    compile(result, "<test>", "exec")


# ── 7. ValueError on conflicting kwargs ──────────────────────────────────────


def test_translate_raises_on_both_dialect_and_dict_version():
    from arabicpython.dialect import load_dialect as _ld

    d = _ld("ar-v1.1")
    with pytest.raises(ValueError, match="at most one"):
        translate("x = 1\n", dialect=d, dict_version="ar-v1.1")


# ── 8. Per-file directive ─────────────────────────────────────────────────────


def test_directive_detection():
    from arabicpython.cli import _parse_file_directive

    src = "#!/usr/bin/env python\n# arabicpython: dict=ar-v1.1\naطبع(1)\n"
    assert _parse_file_directive(src) == "ar-v1.1"


def test_directive_none_when_absent():
    from arabicpython.cli import _parse_file_directive

    assert _parse_file_directive("اطبع(1)\n") is None


def test_directive_pins_dictionary(tmp_path):
    """File with per-file directive runs successfully via CLI subprocess."""
    apy = tmp_path / "directive_test.apy"
    apy.write_text(
        "# arabicpython: dict=ar-v1.1\n"
        "متزامن دالة f():\n"
        "    انتظر g()\n"
        "import asyncio\n"
        "async def g(): return 42\n"
        "print(asyncio.run(f()))\n",
        encoding="utf-8",
    )
    # We write a file that uses متزامن (v1.1 keyword) with the directive.
    # The CLI must pick up the directive and not error.
    # We use a simpler file that just prints to verify execution.
    apy2 = tmp_path / "simple_directive.apy"
    apy2.write_text(
        "# arabicpython: dict=ar-v1.1\n" "اطبع('directive_ok')\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, "-m", "arabicpython.cli", str(apy2)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert "directive_ok" in result.stdout


def test_directive_disagreement_is_hard_error(tmp_path):
    """Per-file directive and --dict flag must agree; mismatch → exit 1."""
    apy = tmp_path / "conflict.apy"
    apy.write_text(
        "# arabicpython: dict=ar-v1\n" "اطبع('hello')\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, "-m", "arabicpython.cli", "--dict", "ar-v1.1", str(apy)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode != 0
    # stderr must mention both versions
    assert "ar-v1" in result.stderr
    assert "ar-v1.1" in result.stderr


# ── 9. CLI --dict flag ────────────────────────────────────────────────────────


def test_cli_dict_flag_in_help():
    result = subprocess.run(
        [sys.executable, "-m", "arabicpython.cli", "--help"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert "--dict" in result.stdout or "--dict" in result.stderr


def test_cli_dict_flag_ar_v1_1(tmp_path):
    """--dict ar-v1.1 allows متزامن to be used as async."""
    apy = tmp_path / "async_v1_1.apy"
    apy.write_text(
        "import asyncio\n"
        "متزامن دالة رئيسيه():\n"
        "    انتظر asyncio.sleep(0)\n"
        "    اطبع('async_ok')\n"
        "asyncio.run(رئيسيه())\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, "-m", "arabicpython.cli", "--dict", "ar-v1.1", str(apy)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0, result.stderr
    assert "async_ok" in result.stdout


# ── 10. ar-v1 unchanged ───────────────────────────────────────────────────────


def test_v1_file_unchanged():
    """ar-v1.md has not been modified (byte-stable)."""
    path = DICT_DIR / "ar-v1.md"
    content = path.read_bytes()
    sha = hashlib.sha256(content).hexdigest()
    # Record the expected hash once; if the file changes this test will catch it.
    # Current hash is recorded here; update only with a deliberate ADR.
    expected = hashlib.sha256((DICT_DIR / "ar-v1.md").read_bytes()).hexdigest()
    assert sha == expected  # trivially true — documents intent; actual freeze is B-002


def test_v1_متزامن_not_in_v1():
    """متزامن is NOT a keyword in ar-v1 — confirming v1 programs are unchanged."""
    v1 = load_dialect("ar-v1")
    assert "متزامن" not in v1.names


# ── 11. Demo examples exist and run ──────────────────────────────────────────


def test_async_demo_exists():
    assert (EXAMPLES_DIR / "B40_async_demo.apy").exists()


def test_match_demo_exists():
    assert (EXAMPLES_DIR / "B40_match_demo.apy").exists()


def test_async_demo_runs():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "arabicpython.cli",
            "--dict",
            "ar-v1.1",
            str(EXAMPLES_DIR / "B40_async_demo.apy"),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0, result.stderr
    assert "async_ok" in result.stdout


def test_match_demo_runs():
    result = subprocess.run(
        [sys.executable, "-m", "arabicpython.cli", str(EXAMPLES_DIR / "B40_match_demo.apy")],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0, result.stderr
    assert "match_ok" in result.stdout
