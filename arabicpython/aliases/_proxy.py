"""ModuleProxy — transparent wrapper forwarding attribute access through an Arabic→Python mapping.

Architecture
------------
Three public classes are defined here:

ModuleProxy
    Wraps a Python *module*. Created by AliasFinder; the object a user
    receives after ``استورد فلاسك``. Arabic keys are looked up in the
    mapping dict; unrecognised Arabic raises AttributeError + DeprecationWarning;
    ASCII names fall through to the underlying module.

ClassFactory
    Wraps a Python *class* that appears in the mapping's ``proxy_classes`` list.
    When called (``فلاسك.فلاسك(__name__)``), it instantiates the class and
    wraps the result in an InstanceProxy, so Arabic method names work on the
    resulting object.

InstanceProxy
    Wraps a Python *object instance* (e.g. a live Flask app). Resolves
    ``Class.method``-style mapping entries against the real instance:
    ``"طريق" → "Flask.route"`` becomes ``getattr(app, "route")`` (bound).
    Falls through to English for unmapped names; warns + raises for unmapped
    Arabic names that don't correspond to any bound method.
"""

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


# ---------------------------------------------------------------------------
# InstanceProxy
# ---------------------------------------------------------------------------


class InstanceProxy:
    """Wraps a live Python object instance with an Arabic→Python name mapping.

    Only resolves entries of the form ``"ClassName.method"`` where
    *ClassName* matches the actual class of the wrapped instance. This
    prevents module-level entries (e.g. ``"جلسه" → "session"``) from
    accidentally being looked up on the wrong object.

    Calling ``تطبيق.طريق('/')`` (where ``تطبيق`` is a proxied Flask app):
      1. Looks up ``"طريق"`` in the mapping → ``"Flask.route"``
      2. Sees ``"Flask."`` prefix matches ``type(app).__name__ == "Flask"``
      3. Returns ``getattr(app, "route")`` — the bound method

    English names (e.g. ``.config``, ``.logger``) pass through unchanged.
    """

    __slots__ = ("_wrapped", "_mapping", "_proxy_classes")

    def __init__(
        self,
        obj: Any,
        mapping: types.MappingProxyType,
        proxy_classes: frozenset,
    ) -> None:
        object.__setattr__(self, "_wrapped", obj)
        object.__setattr__(self, "_mapping", mapping)
        object.__setattr__(self, "_proxy_classes", proxy_classes)

    def __getattr__(self, name: str) -> Any:
        obj: Any = object.__getattribute__(self, "_wrapped")
        mapping: types.MappingProxyType = object.__getattribute__(self, "_mapping")
        proxy_classes: frozenset = object.__getattribute__(self, "_proxy_classes")

        class_name = type(obj).__name__  # e.g. "Flask"
        prefix = class_name + "."

        if name in mapping:
            python_value: str = mapping[name]
            # Only handle entries prefixed with this instance's class name
            if python_value.startswith(prefix):
                method_name = python_value[len(prefix):]  # e.g. "route"
                result = getattr(obj, method_name)
                # If the result is itself a proxy class, wrap it too
                if isinstance(result, type) and python_value in proxy_classes:
                    return ClassFactory(result, mapping, proxy_classes=proxy_classes)
                return result
            # Entry exists but is for a different class or is module-level;
            # fall through to English passthrough below.

        # English passthrough — works for unmapped English names
        if not _is_arabic_looking(name):
            return getattr(obj, name)

        # Unmapped Arabic name: warn and raise
        warnings.warn(
            f"'{name}' is not in the curated instance mapping for "
            f"'{class_name}'. "
            f"Use dir(...) to list available Arabic names.",
            DeprecationWarning,
            stacklevel=2,
        )
        raise AttributeError(
            f"'{class_name}' proxy has no Arabic attribute '{name}'. "
            f"Use dir(...) to list available Arabic names."
        )

    def __repr__(self) -> str:
        obj: Any = object.__getattribute__(self, "_wrapped")
        return f"<arabic-instance-proxy of {type(obj).__name__}>"

    def __dir__(self) -> list[str]:
        obj: Any = object.__getattribute__(self, "_wrapped")
        mapping: types.MappingProxyType = object.__getattribute__(self, "_mapping")
        class_name = type(obj).__name__
        prefix = class_name + "."
        instance_arabic = [k for k, v in mapping.items() if v.startswith(prefix)]
        english_pass = [n for n in dir(obj) if not _is_arabic_looking(n)]
        return sorted(set(instance_arabic + english_pass))


# ---------------------------------------------------------------------------
# ClassFactory
# ---------------------------------------------------------------------------


class ClassFactory:
    """Wraps a Python class so that calling it returns an InstanceProxy.

    When ``فلاسك.فلاسك`` is accessed on a ModuleProxy, it returns a
    ClassFactory wrapping ``flask.Flask``. Calling the factory
    (``فلاسك.فلاسك(__name__)``) creates a real Flask app and wraps it in
    an InstanceProxy, enabling Arabic method access on the result.
    """

    __slots__ = ("_cls", "_mapping", "_proxy_classes")

    def __init__(
        self,
        cls: type,
        mapping: types.MappingProxyType,
        *,
        proxy_classes: frozenset,
    ) -> None:
        object.__setattr__(self, "_cls", cls)
        object.__setattr__(self, "_mapping", mapping)
        object.__setattr__(self, "_proxy_classes", proxy_classes)

    def __call__(self, *args: Any, **kwargs: Any) -> InstanceProxy:
        cls: type = object.__getattribute__(self, "_cls")
        mapping: types.MappingProxyType = object.__getattribute__(self, "_mapping")
        proxy_classes: frozenset = object.__getattribute__(self, "_proxy_classes")
        instance = cls(*args, **kwargs)
        return InstanceProxy(instance, mapping, proxy_classes)

    def __repr__(self) -> str:
        cls: type = object.__getattribute__(self, "_cls")
        return f"<arabic-class-factory for {cls.__name__}>"

    @property
    def __class__(self):  # type: ignore[override]
        """Return the wrapped class so isinstance checks work."""
        return object.__getattribute__(self, "_cls")


# ---------------------------------------------------------------------------
# ModuleProxy
# ---------------------------------------------------------------------------


class ModuleProxy:
    """Transparent wrapper around a Python module with an Arabic→Python name mapping.

    Created by AliasFinder; not intended for direct instantiation by user code.

    Invariants
    ----------
    - ``self._wrapped`` is the underlying Python module object.
    - ``self._mapping`` is an immutable dict of Arabic → Python attribute names.
    - Attribute lookup first checks ``self._mapping``; on a hit it forwards to
      ``getattr(self._wrapped, mapping[name])`` (dotted paths resolved left-to-right).
    - If the resolved name is in ``self._proxy_classes``, a :class:`ClassFactory`
      is returned so that instantiation yields an :class:`InstanceProxy`.
    - An unmapped *Arabic* name emits DeprecationWarning then raises AttributeError
      with guidance text.
    - An unmapped *ASCII* name falls through to the wrapped module unchanged.

    Examples
    --------
    >>> import sys
    >>> proxy = ModuleProxy(sys, {"وسائط": "argv"}, arabic_name="نظام", proxy_classes=frozenset())
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
        proxy_classes: frozenset = frozenset(),
    ) -> None:
        object.__setattr__(self, "_wrapped", wrapped)
        object.__setattr__(self, "_mapping", types.MappingProxyType(dict(mapping)))
        object.__setattr__(self, "_arabic_name", arabic_name)
        object.__setattr__(self, "_proxy_classes", proxy_classes)

    # ------------------------------------------------------------------
    # Attribute access
    # ------------------------------------------------------------------

    def __getattr__(self, name: str) -> Any:
        mapping: types.MappingProxyType[str, str] = object.__getattribute__(self, "_mapping")
        wrapped: types.ModuleType = object.__getattribute__(self, "_wrapped")
        arabic_name: str = object.__getattribute__(self, "_arabic_name")
        proxy_classes: frozenset = object.__getattribute__(self, "_proxy_classes")

        if name in mapping:
            python_attr = mapping[name]
            # Support dotted paths such as "adapters.HTTPAdapter" or "Flask.route"
            if "." in python_attr:
                result: Any = wrapped
                for part in python_attr.split("."):
                    result = getattr(result, part)
            else:
                result = getattr(wrapped, python_attr)

            # If this is a proxy class, wrap it in a ClassFactory
            if isinstance(result, type) and python_attr in proxy_classes:
                return ClassFactory(result, mapping, proxy_classes=proxy_classes)

            return result

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
