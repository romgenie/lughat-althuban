"""B-061: Arabic cookbook — code-block execution tests.

Asserts that:
1. ``docs/cookbook-ar.md`` exists and is well-formed UTF-8 Markdown.
2. ``docs/cookbook-ar-glossary.md`` exists.
3. Every fenced ``apy`` / ``arabicpython`` code block in the cookbook runs
   under the apython CLI to a clean exit, unless explicitly tagged with
   ``<!-- not-runnable: snippet -->``.
"""

from __future__ import annotations

import pathlib
import re

import pytest

from tests.test_phase_a_compat import run_apy_program

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
COOKBOOK_AR = PROJECT_ROOT / "docs" / "cookbook-ar.md"
GLOSSARY = PROJECT_ROOT / "docs" / "cookbook-ar-glossary.md"


def _code_blocks(path: pathlib.Path) -> list[tuple[int, str, str]]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    blocks: list[tuple[int, str, str]] = []
    i = 0
    while i < len(lines):
        m = re.match(r"^```(\S+)\s*$", lines[i])
        if m and m.group(1) in ("apy", "arabicpython"):
            marker = ""
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
            blocks.append((start + 1, marker, "\n".join(lines[start:k])))
            i = k + 1
            continue
        i += 1
    return blocks


class TestStructure:
    def test_cookbook_exists(self):
        assert COOKBOOK_AR.exists(), f"missing: {COOKBOOK_AR}"

    def test_cookbook_is_utf8(self):
        COOKBOOK_AR.read_text(encoding="utf-8")

    def test_cookbook_starts_with_h1(self):
        first = COOKBOOK_AR.read_text(encoding="utf-8").lstrip()
        assert first.startswith("# ")

    def test_glossary_exists(self):
        assert GLOSSARY.exists(), f"missing: {GLOSSARY}"


_BLOCKS = _code_blocks(COOKBOOK_AR)


@pytest.mark.parametrize(
    "lineno,marker,code",
    _BLOCKS,
    ids=[f"recipe-line-{b[0]}" for b in _BLOCKS] if _BLOCKS else [],
)
def test_cookbook_block_runs(tmp_path, lineno, marker, code):
    if "not-runnable" in marker:
        pytest.skip(f"snippet block at line {lineno}: {marker}")

    apy_file = tmp_path / f"recipe_line_{lineno}.apy"
    apy_file.write_text(code, encoding="utf-8")

    rc, out, err = run_apy_program(apy_file, timeout=10.0)
    expected_error = "expected-error" in marker
    if expected_error:
        assert rc != 0
    else:
        assert rc == 0, (
            f"recipe at line {lineno} failed (rc={rc}).\n"
            f"--- code ---\n{code}\n--- stderr ---\n{err}"
        )
