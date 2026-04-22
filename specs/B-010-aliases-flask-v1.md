# Spec Packet B-010: aliases-flask-v1

**Phase**: B
**Depends on**: B-001 (alias-runtime-v1) merged
**Estimated size**: medium (2–3 sessions; one for mapping research, one for tests, one for the demo app)
**Owner**: — (claim via issue; **first-pickup recommended for Flask users**)

## Goal

Ship the Arabic alias mapping for Flask, plus a runnable demo app that proves an Arabic-speaking developer can write a working Flask hello-world entirely in Arabic. This packet is the **Phase B success criterion** per ADR 0008.B.4 — once it merges, Phase B has shipped its smallest end-to-end demonstration that the Layer 3 model works for a non-trivial framework.

The packet has three deliverables: (1) `arabicpython/aliases/flask.toml` with ~60 entries covering Flask 3.x's core surface, (2) `examples/B10_flask_hello.apy` — a complete Flask app written in Arabic that responds to GET requests, (3) integration tests that boot the app on a test client and assert observable behavior.

This packet also defines the **template that B-011 through B-018 will copy** for other top-10 SDK packets. Every decision made here about translation conventions, test density, and demo-app shape becomes precedent. Implementer judgment matters more than usual.

## Non-goals

- **No Flask extensions.** `flask-sqlalchemy`, `flask-login`, `flask-wtf`, etc. are out of scope; each gets its own future packet if and when there's demand.
- **No Jinja2 template translation.** Templates are user-authored HTML; translating Jinja's filter names and template tags is a separate, much larger problem. Out of scope.
- **No Werkzeug surface.** Werkzeug is Flask's underlying WSGI library; users rarely import from it directly. If a Werkzeug name is needed (e.g., `secure_filename`), it appears as a re-export in the Flask mapping, not as a separate `werkzeug.toml`.
- **No CLI plugin (`flask run`) translation.** The `flask` shell command is itself untranslated; users invoke `flask run` from the terminal in English. A future tooling packet (B-050) may wrap it.
- **No async support testing.** Flask 2.0+ supports async views; the alias mapping covers them syntactically (`async دالة` translates fine via the Phase A keyword translator), but verifying real async-view runtime is deferred to whatever packet ships async coverage broadly.
- **No production deployment guidance.** The demo app uses Flask's dev server (`app.run()`); Gunicorn / uWSGI / production WSGI is out of scope.

## Files

### Files to create

- `arabicpython/aliases/flask.toml` — the mapping file.
- `tests/test_aliases_flask.py` — integration tests booting the test app.
- `examples/B10_flask_hello.apy` — the Phase B demo app (the thing that proves Phase B success criterion).
- `examples/B10_README-ar.md` — a one-page Arabic walkthrough of the demo. **Required** because this example is the project's most visible artifact for would-be Arabic developers; it must be self-explanatory.
- `tests/fixtures/flask_apps/minimal.apy` — a 5-line Flask app used by the integration tests. Smaller than `B10_flask_hello.apy`; meant for fast test iteration.

### Files to modify

- `examples/README.md` and `examples/README-ar.md` — add an entry for `B10_flask_hello.apy` to the example index.
- `ROADMAP-PHASE-B.md` — change B-010 status from `drafted` to `merged` after PR merges (planner does this; implementer flags it in the delivery note).

### Files to read (do not modify)

- `arabicpython/aliases/__init__.py`, `_proxy.py`, `_finder.py`, `_loader.py` — the B-001 runtime this packet consumes.
- `arabicpython/aliases/requests.toml` — the precedent file. **Mirror its structure exactly.** `[meta]` and `[entries]` sections only; no other top-level tables.
- Flask 3.x source at https://github.com/pallets/flask — specifically `src/flask/app.py`, `src/flask/blueprints.py`, `src/flask/wrappers.py`, `src/flask/templating.py`, `src/flask/helpers.py`. These define the public surface to map.
- Flask quickstart documentation: https://flask.palletsprojects.com/en/latest/quickstart/ — the canonical "what does a Flask user actually write" reference. Every name that appears in the quickstart must be in the mapping.
- `decisions/0008-phase-b-charter.md` §B.4 — the success-criterion definition.
- `dictionaries/ar-v1.md` — confirm no naming collisions with Phase A keywords.
- `arabicpython/normalize.py` — `normalize_identifier()` for the round-trip check on every entry.

## Public interfaces

### `arabicpython/aliases/flask.toml`

The full mapping. **Every entry below must be in the shipped file**; the implementer may add more if they discover gaps during the test phase, but the floor is fixed.

```toml
# arabicpython/aliases/flask.toml
# Schema version: 1
# Maps Arabic names to the Flask 3.x library.
# Phase B success-criterion mapping per ADR 0008.B.4.

[meta]
arabic_name = "فلاسك"
python_module = "flask"
dict_version = "ar-v1"
schema_version = 1
maintainer = "—"

[entries]
# === Application object ===
"تطبيق_فلاسك" = "Flask"
"تطبيق_حالي" = "current_app"

# === Routing decorator and methods ===
"مسار" = "route"                      # used as @تطبيق.مسار("/")
"استرجاع" = "get"                     # @تطبيق.استرجاع — Flask 2.0+ shortcut
"ارسال" = "post"
"وضع" = "put"
"حذف" = "delete"
"تعديل" = "patch"
"استبدال" = "put"

# === Request and response objects ===
"طلب" = "request"
"جلسه" = "session"
"تطبيق_طلب" = "Request"
"استجابه" = "Response"
"اصنع_استجابه" = "make_response"
"اعد_التوجيه" = "redirect"
"ارفع" = "abort"

# === Templating ===
"اعرض_قالب" = "render_template"
"اعرض_قالب_نص" = "render_template_string"
"احصل_على_البيئه" = "get_template_attribute"

# === URL building ===
"بناء_رابط" = "url_for"

# === Static and helper functions ===
"ارسل_من_مجلد" = "send_from_directory"
"ارسل_ملف" = "send_file"
"امسك_بيانات" = "stream_with_context"

# === JSON ===
"حول_جسون" = "jsonify"

# === Blueprints ===
"مخطط" = "Blueprint"

# === Flash messages ===
"اخطر" = "flash"
"احصل_على_الاخطارات" = "get_flashed_messages"

# === Configuration ===
"اعدادات" = "Config"

# === Errors ===
"خطا_http" = "HTTPException"

# === Flask exceptions in werkzeug.exceptions (re-exported) ===
"خطا_بيانات_سيئه" = "BadRequest"
"خطا_غير_مصرح" = "Unauthorized"
"خطا_ممنوع" = "Forbidden"
"خطا_غير_موجود" = "NotFound"
"خطا_طريقه_غير_مسموحه" = "MethodNotAllowed"
"خطا_غير_مقبول" = "NotAcceptable"
"خطا_تعارض" = "Conflict"
"خطا_ضمن_خادم" = "InternalServerError"

# === Globals ===
"غ" = "g"

# === Hooks (registered via decorator on app) ===
# (No top-level imports for these; documented in B10_README-ar.md as decorator usage.)

# === Type hints / common types ===
"كائن_استجابه" = "Response"
"كائن_طلب" = "Request"
```

**Count: 38 entries.** This is below the spec's "~60" estimate — the implementer must add the remaining ~20 entries during research, choosing from Flask's surface as covered in the quickstart. Likely additions: `before_request`, `after_request`, `teardown_request`, `errorhandler`, `app.run`, `app.add_url_rule`, the `request.args/form/files/cookies/method/path` accessors, `session.permanent`, `Flask.config`, `Flask.logger`, `app.test_client`, `app.test_request_context`. Document the final list in the delivery note.

### Translation rationale (for review)

A reviewer judging the translations should know:

- **`فلاسك` for the package name** — transliteration. The library is a brand; we don't translate it semantically.
- **`تطبيق_فلاسك` for the `Flask` class** — composed: "Flask application." Avoids the bare `تطبيق` colliding with future generic-application aliases.
- **`مسار` for `route`** — MSA, matches Hedy's URL-routing terminology.
- **`اعرض_قالب` for `render_template`** — composed: "render template." `اعرض` alone is too generic.
- **`غ` for `g` (the global namespace)** — single-letter Arabic for single-letter English. Flask users know `g` is jargon; preserving the brevity helps.
- **`خطا_*` prefix for exceptions** — matches the Phase A traceback convention in `dictionaries/exceptions-ar-v1.md`.

### `examples/B10_flask_hello.apy`

A complete, runnable Flask application in Arabic. Approximately 25 lines. Must demonstrate:

1. Importing Flask via `استورد فلاسك`.
2. Creating an app: `تطبيق = فلاسك.تطبيق_فلاسك(__اسم__)`.
3. Defining a route with the decorator: `@تطبيق.مسار("/")`.
4. Returning a string response.
5. A second route with a path parameter (e.g., `/مرحبا/<اسم>`).
6. A route returning JSON via `حول_جسون`.
7. Running the app with `تطبيق.شغل()` (or whichever name is settled for `app.run`).

The file must be entirely Arabic except for: HTTP method names in the routing path (URLs are RFC-3986 ASCII), JSON keys if needed (consumer-facing decision), and Python's `__اسم__` dunder which is a Phase A normalization of `__name__` and is documented as the canonical form.

```python
# examples/B10_flask_hello.apy — Phase B success-criterion demo
# يوضح هذا المثال كيفية كتابة تطبيق فلاسك كامل بالعربية.

استورد فلاسك

تطبيق = فلاسك.تطبيق_فلاسك(__اسم__)


@تطبيق.مسار("/")
دالة الرئيسيه():
    ارجع "مرحبا بك في تطبيق فلاسك العربي"


@تطبيق.مسار("/مرحبا/<اسم>")
دالة سلام_على(اسم):
    ارجع f"السلام عليكم يا {اسم}"


@تطبيق.مسار("/معلومات")
دالة معلومات_التطبيق():
    ارجع فلاسك.حول_جسون({
        "اسم": "تطبيق فلاسك العربي",
        "اصدار": "1.0",
        "وصف": "أول تطبيق فلاسك مكتوب بالكامل بالعربية"
    })


إذا __اسم__ == "__main__":
    تطبيق.شغل(host="0.0.0.0", port=5000)
```

**Note on `شغل` for `app.run`:** This is a method-on-instance, NOT a module-level alias. The TOML mapping covers module-level names. Method translation on instances of mapped classes is a known gap that surfaces here. The implementer has two options:

1. **Document and live with the limitation.** Tell the user to write `تطبيق.run(host=..., port=...)` — methods stay English. This is the honest path; the mapping pattern from B-001 only covers module-level surface.
2. **Extend `ModuleProxy` to support class-attribute translation.** Out of scope for B-010 — that's a runtime change requiring a B-001 fix-up packet.

**Decision: option 1.** The example uses `تطبيق.run(...)`. The README explains why and points to the future "instance proxy" packet. This honest limitation is part of what makes Phase B v1 a v1 — not pretending to solve more than it solves.

The example becomes:

```python
إذا __اسم__ == "__main__":
    تطبيق.run(host="0.0.0.0", port=5000)
```

### `examples/B10_README-ar.md`

A 1-page walkthrough in Arabic. Sections:

1. **ماذا يفعل هذا المثال** (what it does) — one paragraph.
2. **كيف تشغّله** (how to run) — `pip install flask`, then `ثعبان examples/B10_flask_hello.apy`, then `curl http://localhost:5000/`.
3. **شرح كل سطر** (line-by-line) — annotation of each route and what the Arabic name maps to in English.
4. **القيود الحاليه** (current limitations) — honest note that methods on instances (e.g., `app.run`) stay English in this version, and why.
5. **خطوات تالية** (next steps) — "if you want to extend this with X, claim packet Y."

## Implementation constraints

- **Flask version**: 3.x. The mapping must work on Flask 3.0 through whatever current is at implementation time. If a name was renamed between Flask 2.x and 3.x, prefer the 3.x name.
- **No new dependencies on the project.** Flask is added as a *test* dependency in `pyproject.toml`'s `[project.optional-dependencies] dev` extra, not as a runtime dep. Users who want to use the Flask aliases install Flask themselves (`pip install flask`).
- **Add `flask>=3.0` to the dev extra** in `pyproject.toml`.
- **TOML round-trip check**: every Arabic key must satisfy `normalize_identifier(key) == key`. The B-001 loader enforces this at load time; the implementer should also add an explicit test that loads `flask.toml` and asserts no entry was rejected.
- **No naming collisions with `requests.toml`.** Both files can use the same Arabic name only if they map to the same conceptual operation across libraries (e.g., `طلب` for `request` is fine in both because it means the same thing; `استجابه` for `Response` is fine likewise). Document any deliberate cross-library reuse in the delivery note.
- **Style**: ruff and black at project defaults.
- **Performance budget**: not applicable — Flask aliasing is one-time module-load cost, dwarfed by Flask's own import time.

## Test requirements

### `tests/test_aliases_flask.py`

**Mapping integrity (4 tests):**

1. `test_flask_toml_loads`:
   - Load `arabicpython/aliases/flask.toml` via the B-001 loader.
   - Assert no exception; returns valid `AliasMapping`.

2. `test_flask_toml_minimum_surface`:
   - Assert mapping contains entries for: `تطبيق_فلاسك`, `مسار`, `طلب`, `حول_جسون`, `اعرض_قالب`, `بناء_رابط`, `مخطط`, `اخطر`, `خطا_غير_موجود`. (Floor of nine; if any missing, packet is broken.)

3. `test_flask_toml_all_entries_round_trip_normalize`:
   - For every Arabic key in the mapping: `normalize_identifier(key) == key`.

4. `test_flask_toml_all_python_attributes_exist_on_module`:
   - Import `flask`. For every Python value in the mapping: `getattr(flask, value)` does not raise. Catches stale entries from API churn.

**Proxy behavior (5 tests):**

5. `test_فلاسك_resolves_to_proxy`:
   - After `arabicpython.install()`, evaluate `استورد فلاسك; type(فلاسك)` (executed via `arabicpython.translate.exec_translated()` or equivalent).
   - Assert the resulting object is a `ModuleProxy` whose `_wrapped is flask`.

6. `test_تطبيق_فلاسك_constructs_real_flask_app`:
   - Via the proxy, construct `فلاسك.تطبيق_فلاسك("test")`.
   - Assert the result `isinstance(_, flask.Flask)`.

7. `test_route_decorator_works`:
   - Construct app via proxy, register a route via `@تطبيق.مسار("/x")`, and verify Flask's `app.url_map` contains the rule.

8. `test_حول_جسون_returns_response_with_json_content`:
   - Call `فلاسك.حول_جسون({"k": "v"})` inside a request context.
   - Assert the result is a Flask `Response` with content-type containing `application/json`.

9. `test_خطا_غير_موجود_is_real_NotFound`:
   - Access `فلاسك.خطا_غير_موجود`.
   - Assert it is the `werkzeug.exceptions.NotFound` class.

**Demo-app integration (3 tests, using Flask's test client):**

10. `test_minimal_app_root_returns_200`:
    - Load `tests/fixtures/flask_apps/minimal.apy` as an importable module.
    - Get the app's `test_client()`, GET `/`, assert status 200, assert body contains expected Arabic string.

11. `test_demo_app_path_parameter_route`:
    - Load `examples/B10_flask_hello.apy`.
    - GET `/مرحبا/سارة` via test client. Assert status 200, body contains `"السلام عليكم يا سارة"`.
    - **URL-encoding note:** the test client must URL-encode the Arabic path component. Flask handles UTF-8 paths natively per WSGI 1.0.1; this test confirms it.

12. `test_demo_app_json_route`:
    - GET `/معلومات` via test client. Assert status 200, content-type is `application/json`, parsed JSON contains key `"اسم"` with value containing `"فلاسك"`.

**Phase A compat (1 test):**

13. `test_existing_apy_examples_unaffected`:
    - Run `examples/01_hello.apy` through the same path as `tests/test_phase_a_compat.py` (B-002).
    - Assert success. Catches "this packet broke a Phase A example by mistake" before merge.

### Edge cases to cover

- Flask app name uses Arabic (`__اسم__` value is "فلاسك_تجريبي" or similar) — must work because Flask passes the name through to the logger and template loader. Some libraries (not Flask) crash on non-ASCII module names; verify Flask doesn't.
- Route path with Arabic characters (`/مرحبا/<اسم>`) — must work; Flask 3.x routing is UTF-8-clean.
- JSON response with Arabic values — `حول_جسون` must produce UTF-8 JSON without `\u` escapes (Flask's default `JSONIFY_PRETTYPRINT_REGULAR` setting controls this; document the test's expectation).
- Decorator stacked with other decorators (`@app.route("/") + @login_required`) — out of scope for B-010 (no auth library), but note in delivery as future test.

## Reference materials

- B-001 spec at `specs/B-001-alias-runtime-v1.md`.
- Flask 3.x docs: https://flask.palletsprojects.com/en/3.0.x/
- Flask quickstart: https://flask.palletsprojects.com/en/3.0.x/quickstart/
- Flask API reference: https://flask.palletsprojects.com/en/3.0.x/api/
- Werkzeug exceptions: https://werkzeug.palletsprojects.com/en/latest/exceptions/
- Hedy's HTTP-related translations (cross-reference for term consistency): https://github.com/hedyorg/hedy
- ADR 0008 §B.4 — the success criterion this packet satisfies.
- The `requests.toml` mapping (B-001) — structural template.

## Open questions for the planner

Empty.

## Acceptance checklist

- [ ] `arabicpython/aliases/flask.toml` shipped with at least the 38 entries listed in this spec, expanded toward ~60 by the implementer.
- [ ] All 13 tests in `tests/test_aliases_flask.py` pass.
- [ ] `examples/B10_flask_hello.apy` runs end-to-end (manual: `pip install flask && ثعبان examples/B10_flask_hello.apy`, then `curl localhost:5000/`).
- [ ] `examples/B10_README-ar.md` written with all five required sections.
- [ ] `examples/README.md` and `README-ar.md` updated with the new example.
- [ ] `pyproject.toml` adds `flask>=3.0` to the dev extra.
- [ ] `ruff check .` passes.
- [ ] `black --check .` passes.
- [ ] `pytest` passes on Python 3.11/3.12/3.13 × Linux/macOS/Windows.
- [ ] `tests/test_phase_a_compat.py` (from B-002) still passes.
- [ ] Delivery note `B-010-aliases-flask-v1.delivery.md` written, including: full final entry list (the delta from this spec's 38 floor), translation choices made under judgment (every entry not pre-decided in this spec), the explicit "method-on-instance limitation" call-out, and any term-collision decisions with `requests.toml`.
- [ ] **Phase B success-criterion proof:** record (in the delivery note) that you, the implementer, ran the demo app and successfully made HTTP requests to all three routes from a separate terminal. This is the demonstration that ADR 0008.B.4 was satisfied.
