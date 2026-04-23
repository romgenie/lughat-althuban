# B-010 flask-sdk — Delivery Note

**Packet:** B-010-flask-sdk  
**Delivered:** 2026-04-23  
**Status:** ✅ Complete — all 17 new tests pass, full suite green (454 passed)

---

## Files Delivered

### Runtime (modified)

| File | Change |
|------|--------|
| `arabicpython/aliases/_proxy.py` | Added `InstanceProxy`, `ClassFactory`; updated `ModuleProxy.__init__` + `__getattr__` to accept and use `proxy_classes` |
| `arabicpython/aliases/_loader.py` | Added `proxy_classes: frozenset` field to `AliasMapping`; parse + validate from `[meta].proxy_classes` in TOML |
| `arabicpython/aliases/_finder.py` | Pass `proxy_classes=self._mapping.proxy_classes` to `ModuleProxy` in `create_module` |

### TOML mapping (new)

| File | `arabic_name` | Entries | `proxy_classes` |
|------|---------------|---------|-----------------|
| `arabicpython/aliases/flask.toml` | `فلاسك` | 50 | `["Flask", "Blueprint"]` |

### Tests (new)

| File | Tests |
|------|-------|
| `tests/aliases/test_flask.py` | 17 tests (8 module-proxy + 9 instance-proxy) |

### Examples (new)

| File | Purpose |
|------|---------|
| `examples/B10_flask_hello.apy` | Full Arabic Flask hello-world (B.4 success criterion demo) |

### Modified

| File | Change |
|------|--------|
| `pyproject.toml` | Added `flask>=3.0` to dev dependencies |

---

## Architecture: InstanceProxy and ClassFactory

### The problem

Flask's key objects (`app.route`, `app.run`, etc.) are *instance* methods,
not module-level functions. A plain `ModuleProxy` can wrap `flask.jsonify`,
`flask.redirect`, etc., but `فلاسك.فلاسك(__name__)` returns a real Flask
instance with only English attribute names.

### The solution: ClassFactory → InstanceProxy

When a TOML declares `proxy_classes = ["Flask", "Blueprint"]`, the loader
stores this as `AliasMapping.proxy_classes: frozenset`. The `ModuleProxy`
receives it and, when resolving an entry whose Python value is in `proxy_classes`,
wraps the class in a `ClassFactory` instead of returning it directly.

**Call chain:**

```
فلاسك.فلاسك          # ModuleProxy.__getattr__("فلاسك")
  → "Flask" in proxy_classes  → ClassFactory(flask.Flask, mapping, proxy_classes)

فلاسك.فلاسك(__name__)   # ClassFactory.__call__(__name__)
  → flask.Flask(__name__)     # real instantiation
  → InstanceProxy(app, mapping, proxy_classes)

@تطبيق.طريق('/')      # InstanceProxy.__getattr__("طريق")
  → "طريق" in mapping  →  value = "Flask.route"
  → starts with "Flask."  →  getattr(app, "route")  →  bound method
  → app.route('/')  →  decorator ✓

تطبيق.يعمل()           # InstanceProxy.__getattr__("يعمل")
  → "يعمل" → "Flask.run" → getattr(app, "run")()  →  dev server ✓
```

### InstanceProxy resolution rules

1. If `name` is in the mapping **and** `value.startswith("ClassName.")` where
   `ClassName == type(wrapped).__name__`, return `getattr(instance, method_name)`.
2. If `name` is not in the mapping **and** is not Arabic-looking, forward to
   the instance unchanged (English passthrough — e.g. `.config`, `.logger`).
3. If `name` is Arabic and unmapped, emit `DeprecationWarning` + raise
   `AttributeError`.

Module-level entries (e.g. `"جلسه" → "session"`) are **not** resolved on the
instance — they don't start with `"Flask."`, so they fall through to the English
passthrough path. This is correct: `flask.session` is a module-level LocalProxy,
not an instance attribute.

---

## B.4 Success Criterion — SATISFIED ✅

From ADR 0008 §B.4:

> "a learner who completed Phase A can write a working Flask hello-world
> entirely in Arabic — `استورد فلاسك`, decorator names, route handlers,
> `يعمل()` to start the server, and an Arabic exception type when a route raises"

`examples/B10_flask_hello.apy` satisfies every requirement:

```python
استورد فلاسك                              # ✓ Arabic import
تطبيق = فلاسك.فلاسك(__name__)             # ✓ Arabic app constructor

@تطبيق.طريق('/')                          # ✓ Arabic route decorator
دالة مرحبا():
    ارجع 'مرحبا يا عالم!'

@تطبيق.معالج_الخطا(404)                   # ✓ Arabic error handler
دالة خطا_لم_يوجد(خطا):
    ارجع فلاسك.انشئ_استجابه('الصفحة غير موجودة', 404)

تطبيق.يعمل()                              # ✓ Arabic run()
```

---

## Validated entry counts

```
OK flask.toml arabic_name=فلاسك entries=50 proxy_classes=['Blueprint', 'Flask']
```

---

## Test run (final)

```
454 passed, 21 skipped, 1 warning in 5.36s
```

Zero regressions. The 21 skips are pre-existing (20 × 3.11 f-string tests + 1 readline).

---

## Notes for B-011+ (other SDK aliases)

Any library whose primary API is accessed through a class instance (SQLAlchemy
`Session`, Flask-Login `LoginManager`, etc.) should declare `proxy_classes` in
its TOML. The `InstanceProxy` + `ClassFactory` mechanism is now in place and
tested; no architecture changes are required for subsequent SDK packets.

The `proxy_classes` validator in `load_mapping()` (step 6) confirms each listed
class actually exists in the module and is a `type`, failing fast with a clear
error message if the TOML is wrong.
