"""TOML alias mapping loader and validator."""

from __future__ import annotations

import importlib
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from arabicpython.normalize import normalize_identifier

REQUIRED_META_FIELDS: frozenset[str] = frozenset(
    {"arabic_name", "python_module", "dict_version", "schema_version"}
)


class AliasMappingError(Exception):
    """Raised when a TOML alias mapping file is malformed or invalid."""


@dataclass(frozen=True)
class AliasMapping:
    """Validated, immutable representation of one alias mapping file."""

    arabic_name: str  # e.g. "طلبات" — the name users import
    python_module: str  # e.g. "requests" — the wrapped stdlib/third-party module
    dict_version: str  # e.g. "ar-v1" — tracks ADR 0003 dictionary versioning
    entries: dict[str, str]  # Arabic attribute → Python attribute name
    source_path: Path  # for error messages
    proxy_classes: frozenset  # class names whose *instances* get wrapped in InstanceProxy


def _resolve_dotted_attr(obj: Any, dotted_name: str) -> Any:
    """Resolve a potentially dotted attribute path, e.g. ``'adapters.HTTPAdapter'``."""
    result = obj
    for part in dotted_name.split("."):
        result = getattr(result, part)
    return result


def load_mapping(toml_path: Path) -> AliasMapping:
    """Parse and validate one alias TOML file.

    Parameters
    ----------
    toml_path:
        Absolute path to a ``*.toml`` alias mapping file.

    Returns
    -------
    AliasMapping
        A frozen dataclass containing the validated mapping.

    Raises
    ------
    AliasMappingError
        On any of: malformed TOML, missing required fields, duplicate Arabic
        keys (rejected by the TOML parser itself), duplicate Python values,
        Arabic keys that don't round-trip through ``normalize_identifier``,
        module not importable, or mapped Python attributes that don't exist.
    """
    # ------------------------------------------------------------------ #
    # 1. Parse TOML
    # ------------------------------------------------------------------ #
    try:
        raw: dict[str, Any] = tomllib.loads(toml_path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise AliasMappingError(f"{toml_path}: TOML parse error: {exc}") from exc

    # ------------------------------------------------------------------ #
    # 2. Validate [meta]
    # ------------------------------------------------------------------ #
    meta = raw.get("meta")
    if meta is None:
        raise AliasMappingError(f"{toml_path}: missing [meta] section")

    missing_fields = REQUIRED_META_FIELDS - set(meta.keys())
    if missing_fields:
        raise AliasMappingError(
            f"{toml_path}: [meta] is missing required fields: {sorted(missing_fields)}"
        )

    arabic_name: str = meta["arabic_name"]
    python_module: str = meta["python_module"]
    dict_version: str = meta["dict_version"]

    # Optional proxy_classes — class names whose instances get wrapped
    proxy_classes_raw = meta.get("proxy_classes", [])
    if not isinstance(proxy_classes_raw, list) or not all(
        isinstance(c, str) for c in proxy_classes_raw
    ):
        raise AliasMappingError(
            f"{toml_path}: [meta].proxy_classes must be a list of strings, "
            f"got {proxy_classes_raw!r}"
        )
    proxy_classes: frozenset = frozenset(proxy_classes_raw)

    # ------------------------------------------------------------------ #
    # 3. Validate [entries]
    # ------------------------------------------------------------------ #
    entries_raw = raw.get("entries")
    if entries_raw is None:
        raise AliasMappingError(f"{toml_path}: missing [entries] section")

    if not isinstance(entries_raw, dict):
        raise AliasMappingError(f"{toml_path}: [entries] must be a TOML table")

    # 3a. Arabic key normalization round-trip
    for arabic_key in entries_raw:
        normalized = normalize_identifier(arabic_key)
        if normalized != arabic_key:
            raise AliasMappingError(
                f"{toml_path}: Arabic key {arabic_key!r} does not round-trip through "
                f"normalize_identifier() — got {normalized!r}. "
                f"Store the normalized form as the key."
            )

    # 3b. No duplicate Python values (two Arabic synonyms → same Python name)
    seen_python: dict[str, str] = {}  # python_attr → first arabic_key that claimed it
    for arabic_key, python_attr in entries_raw.items():
        if python_attr in seen_python:
            raise AliasMappingError(
                f"{toml_path}: Python attribute {python_attr!r} is claimed by two Arabic "
                f"keys: {seen_python[python_attr]!r} and {arabic_key!r}. "
                f"Each Python name may appear at most once in the mapping."
            )
        seen_python[python_attr] = arabic_key

    # ------------------------------------------------------------------ #
    # 4. Import the target module
    # ------------------------------------------------------------------ #
    try:
        module = importlib.import_module(python_module)
    except ImportError as exc:
        raise AliasMappingError(
            f"{toml_path}: Python module {python_module!r} is not importable: {exc}"
        ) from exc

    # ------------------------------------------------------------------ #
    # 5. Verify all mapped Python attributes exist
    # ------------------------------------------------------------------ #
    for arabic_key, python_attr in entries_raw.items():
        try:
            _resolve_dotted_attr(module, python_attr)
        except AttributeError:
            raise AliasMappingError(
                f"{toml_path}: module {python_module!r} has no attribute {python_attr!r} "
                f"(mapped from Arabic key {arabic_key!r})"
            )

    # ------------------------------------------------------------------ #
    # 6. Verify proxy_classes entries are actual classes in the module
    # ------------------------------------------------------------------ #
    for cls_name in proxy_classes:
        cls = getattr(module, cls_name, None)
        if cls is None:
            raise AliasMappingError(
                f"{toml_path}: proxy_classes entry {cls_name!r} does not exist "
                f"in module {python_module!r}"
            )
        if not isinstance(cls, type):
            raise AliasMappingError(
                f"{toml_path}: proxy_classes entry {cls_name!r} is not a class "
                f"(got {type(cls).__name__!r})"
            )

    return AliasMapping(
        arabic_name=arabic_name,
        python_module=python_module,
        dict_version=dict_version,
        entries=dict(entries_raw),
        source_path=toml_path,
        proxy_classes=proxy_classes,
    )
