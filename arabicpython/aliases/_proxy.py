"""ModuleProxy — transparent wrapper forwarding attribute access through an Arabic→Python mapping."""

from __future__ import annotations

import types
import warnings
from typing import Any

# Unicode ranges covering Arabic script variants
_ARABIC_RANGES: tuple[tuple[str, str], ...] = (
    ("\u0600", "\u06FF"),  # Arabic
    ("\u0750", "\u077F"),  # Arabic Supplement
    ("\u08A0", "\u08FF"),  # Arabic Extended-A
    ("\uFB50", "\uFDFF"),  # Arabic Presentation Forms-A
    ("\uFE70", "\uFEFF"),  # Arabic Presentation Forms-B
)


def _is_arabic_looking(name: str) -> bool:
    """Return True if *name* contains at least one Arabic-script character."""
    return any(lo <= ch <= hi for ch in name for lo, hi in _ARABIC_RANGES)


class ModuleProxy:
    """Transparent wrapper around a Python module with an Arabic→Python name mapping.

    Created by AliasFinder; not intended for direct instantiation by user code.

    Invariants
    ----------
    - ``self._wrapped`` is the underlying Python module object.
    - ``self._mapping`` is an immutable dict of Arabic → Python attribute names.
    - Attribute lookup first checks ``self._mapping``; on a hit it forwards to
      ``getattr(self._wrapped, mapping[name])`` (dotted paths resolved left-to-right).
    - An unmapped *Arabic* name emits DeprecationWarning then raises AttributeError
      with guidance text.
    - An unmapped *ASCII* name falls through to the wrapped module unchanged.

    Examples
    --------
    >>> import sys
    >>> proxy = ModuleProxy(sys, {"وسائط": "argv"}, arabic_name="نظام")
    >>> proxy.وسائط is sys.argv
    True
    >>> proxy.argv is sys.argv     # English fallthrough
    True
    """

    def __init__(
        self,
        wrapped: types.ModuleType,
        mapping: dict[str, str],
        *,
        arabic_name: str,
    ) -> None:
        object.__setattr__(self, "_wrapped", wrapped)
        object.__setattr__(self, "_mapping", types.MappingProxyType(dict(mapping)))
        object.__setattr__(self, "_arabic_name", arabic_name)

    # ------------------------------------------------------------------
    # Attribute access
    # ------------------------------------------------------------------

    def __getattr__(self, name: str) -> Any:
        mapping: types.MappingProxyType[str, str] = object.__getattribute__(self, "_mapping")
        wrapped: types.ModuleType = object.__getattribute__(self, "_wrapped")
        arabic_name: str = object.__getattribute__(self, "_arabic_name")

        if name in mapping:
            python_attr = mapping[name]
            # Support dotted paths such as "adapters.HTTPAdapter"
            if "." in python_attr:
                result: Any = wrapped
                for part in python_attr.split("."):
                    result = getattr(result, part)
                return result
            return getattr(wrapped, python_attr)

        if _is_arabic_looking(name):
            warnings.warn(
                f"'{name}' is not in the curated mapping for '{arabic_name}'. "
                f"Use dir({arabic_name}) to list available Arabic names.",
                DeprecationWarning,
                stacklevel=2,
            )
            raise AttributeError(
                f"'{arabic_name}' has no attribute '{name}'. "
                f"'{name}' is not in the curated mapping. "
                f"Use dir({arabic_name}) to list available Arabic names."
            )

        # ASCII / non-Arabic name: forward unchanged to the wrapped module
        return getattr(wrapped, name)

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def __dir__(self) -> list[str]:
        """Return Arabic names from the mapping *plus* English names from the wrapped module."""
        mapping: types.MappingProxyType[str, str] = object.__getattribute__(self, "_mapping")
        wrapped: types.ModuleType = object.__getattribute__(self, "_wrapped")
        return sorted(set(list(mapping.keys()) + dir(wrapped)))

    def __repr__(self) -> str:
        wrapped: types.ModuleType = object.__getattribute__(self, "_wrapped")
        arabic_name: str = object.__getattribute__(self, "_arabic_name")
        return f"<arabic-proxy of {wrapped.__name__} via {arabic_name}>"

    # ------------------------------------------------------------------
    # isinstance / type reflexivity
    # ------------------------------------------------------------------

    @property
    def __class__(self):  # type: ignore[override]
        """Return the wrapped module's class so ``isinstance(proxy, ModuleType)`` works."""
        wrapped: types.ModuleType = object.__getattribute__(self, "_wrapped")
        return wrapped.__class__
