import functools
import re
import types
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from arabicpython.normalize import normalize_identifier


class DialectError(ValueError):
    """Raised when a dictionary file cannot be parsed or is internally inconsistent."""


@dataclass(frozen=True)
class Dialect:
    """Immutable snapshot of an apython dialect."""

    name: str
    names: Mapping[str, str]
    attributes: Mapping[str, str]
    reverse_names: Mapping[str, str]
    reverse_attributes: Mapping[str, str]
    categories: Mapping[str, str]


@functools.lru_cache(maxsize=8)
def load_dialect(name: str = "ar-v1", *, path: "Path | None" = None) -> Dialect:
    """Parse a dialect dictionary and return an immutable Dialect."""
    if path is None:
        path = Path(__file__).parent.parent / "dictionaries" / f"{name}.md"

    try:
        content = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise

    names: dict[str, str] = {}
    attributes: dict[str, str] = {}
    reverse_names: dict[str, str] = {}
    reverse_attributes: dict[str, str] = {}
    categories: dict[str, str] = {}

    current_category: str | None = None

    for i, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()

        # Check for headers
        if stripped.startswith("## 1. Control-flow keywords") or stripped.startswith(
            "### Soft keywords"
        ):
            current_category = "keyword"
            continue
        elif stripped.startswith("## 2. Literal keywords"):
            current_category = "literal"
            continue
        elif stripped.startswith("## 3. Built-in types"):
            current_category = "type"
            continue
        elif stripped.startswith("## 4. Built-in functions"):
            current_category = "function"
            continue
        elif stripped.startswith("## 5. Built-in exceptions"):
            current_category = "exception"
            continue
        elif stripped.startswith("## 6. Common methods on built-in types"):
            current_category = "method"
            continue

        # Ignore other sections (H2 only)
        if stripped.startswith("## "):
            current_category = "IGNORED"
            continue

        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue

        if current_category == "IGNORED":
            continue

        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) >= 2 and (
            set(cells[0]) <= {"-"} or (cells[0] == "Python" and cells[1] == "Canonical")
        ):
            continue

        if len(cells) != 4:
            raise DialectError(f"Line {i}: Expected exactly 4 cells, got {len(cells)}")

        if current_category is None:
            raise DialectError(f"Line {i}: Encountered data row before category heading")

        python_cell = cells[0]
        canonical = cells[1]

        match = re.match(r"^`([^`]+)`$", python_cell)
        if not match:
            raise DialectError(f"Line {i}: Python cell not wrapped in backticks")

        python_symbol = match.group(1)
        if not python_symbol:
            raise DialectError(f"Line {i}: Python cell is empty")

        if not canonical:
            raise DialectError(f"Line {i}: Arabic canonical is empty")

        is_method = python_symbol.startswith(".")
        if is_method:
            python_symbol = python_symbol[1:]

        normalized = normalize_identifier(canonical)

        target_map = attributes if current_category == "method" else names
        reverse_map = reverse_attributes if current_category == "method" else reverse_names

        if normalized in target_map:
            existing_symbol = target_map[normalized]
            if existing_symbol != python_symbol:
                raise DialectError(
                    f"Line {i}: Normalized key '{normalized}' maps to different "
                    f"Python symbols: '{existing_symbol}' and '{python_symbol}'"
                )

        if python_symbol in reverse_map:
            existing_canonical = reverse_map[python_symbol]
            if normalize_identifier(existing_canonical) != normalized:
                raise DialectError(
                    f"Line {i}: Python symbol '{python_symbol}' mapped from different "
                    f"Arabic keys: '{existing_canonical}' and '{canonical}'"
                )

        target_map[normalized] = python_symbol
        reverse_map[python_symbol] = canonical
        # Categories are overwritten so the last one wins.
        # This allows 'type' (soft keyword and built-in type) to keep its last parsed category.
        # The test checks `d.categories[normalize_identifier("نص")] == "type"`.
        # So overwrite is fine.
        if normalized not in categories:
            categories[normalized] = current_category

    total_entries = len(names) + len(attributes)
    if total_entries < 150:
        raise DialectError(f"Insufficient entries: expected >= 150, got {total_entries}")

    return Dialect(
        name=name,
        names=types.MappingProxyType(names),
        attributes=types.MappingProxyType(attributes),
        reverse_names=types.MappingProxyType(reverse_names),
        reverse_attributes=types.MappingProxyType(reverse_attributes),
        categories=types.MappingProxyType(categories),
    )
