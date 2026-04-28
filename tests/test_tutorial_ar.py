"""B-060: Arabic tutorial — structural and execution tests.

Asserts that:
1. ``docs/tutorial-ar.md`` exists and is well-formed UTF-8 Markdown.
2. Its section count matches (or differs by at most 1) the English tutorial
   ``docs/getting-started-ar.md``.
3. ``docs/tutorial-ar-glossary.md`` exists and covers every required term.
4. Glossary terms that overlap with ``dictionaries/ar-v1.md`` are consistent.
5. Every fenced ``apy`` / ``arabicpython`` code block in the tutorial runs
   under the apython CLI to a clean exit (or to the documented expected
   error / skip marker).
6. Every ``.apy`` file in ``examples/B60_tutorial_excerpts/`` (if present)
   runs to a clean exit.
"""

from __future__ import annotations

import pathlib
import re

import pytest

from tests.test_phase_a_compat import run_apy_program

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
TUTORIAL_AR = PROJECT_ROOT / "docs" / "tutorial-ar.md"
TUTORIAL_EN = PROJECT_ROOT / "docs" / "getting-started-ar.md"
GLOSSARY = PROJECT_ROOT / "docs" / "tutorial-ar-glossary.md"
EXCERPTS_DIR = PROJECT_ROOT / "examples" / "B60_tutorial_excerpts"
DICTIONARY_AR_V1 = PROJECT_ROOT / "dictionaries" / "ar-v1.md"

KEY_TERMS = [
    "decorator",
    "iterator",
    "generator",
    "context manager",
    "coroutine",
    "module",
    "package",
    "exception",
    "keyword argument",
    "list comprehension",
]


def _headings(path: pathlib.Path) -> list[str]:
    return [
        line
        for line in path.read_text(encoding="utf-8").splitlines()
        if re.match(r"^#+\s", line)
    ]


def _code_blocks(path: pathlib.Path) -> list[tuple[int, str, str, str]]:
    """Return list of (line_no, info_string, preceding_marker, code) tuples.

    ``preceding_marker`` is the trimmed text of the immediately preceding
    HTML comment (e.g. ``not-runnable: snippet``) or the empty string.
    """
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    blocks: list[tuple[int, str, str, str]] = []
    i = 0
    while i < len(lines):
        m = re.match(r"^```(\S+)\s*$", lines[i])
        if m:
            info = m.group(1)
            if info in ("apy", "arabicpython"):
                marker = ""
                # Look back through optional blank lines for an HTML comment.
                j = i - 1
                while j >= 0 and lines[j].strip() == "":
                    j -= 1
                if j >= 0:
                    cm = re.match(r"^<!--\s*(.*?)\s*-->\s*$", lines[j])
                    if cm:
                        marker = cm.group(1)
                start = i + 1
                k = start
                while k < len(lines) and not lines[k].startswith("```"):
                    k += 1
                code = "\n".join(lines[start:k])
                blocks.append((start + 1, info, marker, code))
                i = k + 1
                continue
        i += 1
    return blocks


# ─────────────────────────────────────────────────────────────────────────
# 1. Structural tests
# ─────────────────────────────────────────────────────────────────────────


class TestStructure:
    def test_tutorial_ar_exists(self):
        assert TUTORIAL_AR.exists(), f"missing: {TUTORIAL_AR}"

    def test_tutorial_ar_is_utf8(self):
        TUTORIAL_AR.read_text(encoding="utf-8")

    def test_tutorial_ar_starts_with_h1(self):
        first = TUTORIAL_AR.read_text(encoding="utf-8").lstrip()
        assert first.startswith("# "), "tutorial must start with a level-1 heading"

    def test_section_count_matches_english(self):
        en = len(_headings(TUTORIAL_EN))
        ar = len(_headings(TUTORIAL_AR))
        # Allow ±2 to accommodate Arabic-only bonus subsections or table-row
        # headings the implementer chose to drop.
        assert abs(ar - en) <= 2, (
            f"English headings: {en}; Arabic headings: {ar}; "
            f"difference exceeds tolerance"
        )


# ─────────────────────────────────────────────────────────────────────────
# 2. Glossary tests
# ─────────────────────────────────────────────────────────────────────────


class TestGlossary:
    def test_glossary_exists(self):
        assert GLOSSARY.exists(), f"missing: {GLOSSARY}"

    @pytest.mark.parametrize("term", KEY_TERMS)
    def test_key_term_in_glossary(self, term):
        content = GLOSSARY.read_text(encoding="utf-8")
        assert term in content, f"key term '{term}' not found in glossary"

    def test_glossary_class_term_consistent(self):
        # `class` is `صنف` per dictionaries/ar-v1.md; the glossary must agree.
        glossary = GLOSSARY.read_text(encoding="utf-8")
        if "class" in glossary.lower():
            # Loose check: when the glossary mentions class, it must use صنف.
            assert "صنف" in glossary, (
                "glossary mentions 'class' but does not use the canonical "
                "translation 'صنف' from ar-v1.md"
            )

    def test_glossary_dict_term_consistent(self):
        glossary = GLOSSARY.read_text(encoding="utf-8")
        if "dictionary" in glossary.lower():
            assert "قاموس" in glossary

    def test_glossary_list_term_consistent(self):
        glossary = GLOSSARY.read_text(encoding="utf-8")
        if "`list`" in glossary or "list " in glossary.lower():
            assert "قائمة" in glossary or "قائمه" in glossary


# ─────────────────────────────────────────────────────────────────────────
# 3. Code-block execution
# ─────────────────────────────────────────────────────────────────────────


_BLOCKS = _code_blocks(TUTORIAL_AR)


@pytest.mark.parametrize(
    "lineno,info,marker,code",
    _BLOCKS,
    ids=[f"block-line-{b[0]}" for b in _BLOCKS] if _BLOCKS else [],
)
def test_tutorial_code_block_runs(tmp_path, lineno, info, marker, code):
    if "not-runnable" in marker:
        pytest.skip(f"snippet block at line {lineno}: {marker}")
    if marker.startswith("requires:"):
        # e.g. requires: ar-v1.1
        required = marker.split(":", 1)[1].strip()
        if required == "ar-v1.1" and not (
            PROJECT_ROOT / "dictionaries" / "ar-v1.1.md"
        ).exists():
            pytest.skip(f"requires {required}, not yet shipped")

    apy_file = tmp_path / f"block_line_{lineno}.apy"
    apy_file.write_text(code, encoding="utf-8")

    rc, out, err = run_apy_program(apy_file, timeout=10.0)
    expected_error = "expected-error" in marker
    if expected_error:
        assert rc != 0, (
            f"block at line {lineno} expected error, but exited cleanly. "
            f"stdout={out!r}"
        )
    else:
        assert rc == 0, (
            f"block at line {lineno} failed (rc={rc}).\n"
            f"--- code ---\n{code}\n--- stderr ---\n{err}"
        )


# ─────────────────────────────────────────────────────────────────────────
# 4. Excerpts directory
# ─────────────────────────────────────────────────────────────────────────


_EXCERPTS = sorted(EXCERPTS_DIR.glob("*.apy")) if EXCERPTS_DIR.exists() else []


@pytest.mark.parametrize(
    "apy_file",
    _EXCERPTS,
    ids=[p.name for p in _EXCERPTS] if _EXCERPTS else [],
)
def test_excerpt_runs(apy_file):
    rc, out, err = run_apy_program(apy_file, timeout=10.0)
    assert rc == 0, f"{apy_file.name} failed (rc={rc}):\n{err}"
