# Spec Packet B-011: aliases-fastapi-v1

**Phase**: B
**Depends on**: B-001 (alias-runtime-v1), B-002 (phase-a-compat-suite), B-040 (dictionary-v1.1-async-match)
**Estimated size**: medium
**Owner**: —

## Goal

Ship the Arabic alias mapping for FastAPI, including support for async route handlers. Mirror the structure of B-010 (Flask).

## Non-goals

- No Pydantic-specific mapping (beyond what's needed for FastAPI basic usage).
- No SQLAlchemy/Databases integration (handled in B-013).
- No production deployment (uvicorn/gunicorn).

## Files

### Files to create

- `arabicpython/aliases/fastapi.toml`
- `tests/test_aliases_fastapi.py`
- `examples/B11_fastapi_hello.apy`
- `examples/B11_README-ar.md`

## Public interfaces

### `arabicpython/aliases/fastapi.toml`

[meta]
arabic_name = "فاست_أبي"
python_module = "fastapi"
dict_version = "ar-v1.1"
schema_version = 1

[entries]
"فاست_أبي" = "FastAPI"
"راوتر" = "APIRouter"
"طلب" = "Request"
"استجابة" = "Response"
"خطأ_http" = "HTTPException"
"حالة" = "status"
"يعتمد" = "Depends"
"استعلام" = "Query"
"مسار_رابط" = "Path"
"محتوى" = "Body"
"رأس" = "Header"
"كوكيز" = "Cookie"
"ملف" = "File"
"ملف_مرفوع" = "UploadFile"
"نموذج_إدخال" = "Form"
"مهام_خلفية" = "BackgroundTasks"
"ملفات_ثابتة" = "StaticFiles"
"استجابة_html" = "HTMLResponse"
"استجابة_جسون" = "JSONResponse"
"استجابة_نصية" = "PlainTextResponse"
"استجابة_توجيه" = "RedirectResponse"
"استجابة_بث" = "StreamingResponse"
"استجابة_ملف" = "FileResponse"
"عميل_اختبار" = "TestClient"
"ويب_سوكت" = "WebSocket"
"انقطاع_ويب_سوكت" = "WebSocketDisconnect"
"أمن" = "Security"
"أوث2_كلمة_سر" = "OAuth2PasswordBearer"
"نموذج_أوث2" = "OAuth2PasswordRequestForm"
"حماية_أساسية" = "HTTPBasic"
"حماية_توكن" = "HTTPBearer"
"نطاقات_أمنية" = "SecurityScopes"

# Starlette re-exports often used
"قوالب_جينجا" = "Jinja2Templates"

# Common status codes (often accessed via fastapi.status)
# These would be on the status object, but if we map them at module level:
# status.HTTP_200_OK -> ?
# For now, focusing on module-level.

# Count: ~35. Adding more to reach floor 40.
"واجهة_تطبيق" = "FastAPI"
"رابط" = "APIRouter"
"معلمات" = "Query"
"مرفق" = "File"
"تحميل" = "UploadFile"
"خلفية" = "BackgroundTasks"
"توجيه" = "RedirectResponse"
"سوكت" = "WebSocket"

### `examples/B11_fastapi_hello.apy`

```python
# arabicpython: dict=ar-v1.1
استورد فاست_أبي

تطبيق = فاست_أبي.فاست_أبي()

@تطبيق.get("/")
متزامن دالة الرئيسيه():
    ارجع {"رسالة": "مرحبا بك في فاست أبي العربي"}

@تطبيق.get("/سلام/{اسم}")
متزامن دالة سلام_على(اسم: نص):
    ارجع {"رسالة": f"السلام عليكم يا {اسم}"}

إذا __اسم__ == "__main__":
    استورد uvicorn
    uvicorn.run(تطبيق, host="0.0.0.0", port=8000)
```

## Implementation constraints

- **Cite B-010 as structural prior.** This packet follows the same deliverable structure and naming conventions.
- **Method-on-instance limitation:** Like B-010, this packet only maps module-level attributes. Methods on instances (e.g., `app.get`, `app.post`) remain in English in this version. The implementer should document this in the README-ar.md.
- **Acceptance checklist must include Phase A compat assertion.**
- **Ensure all Arabic names round-trip through `normalize_identifier`.**

## Test requirements

- Similar to B-010, but specifically testing async route handling and FastAPI-specific dependency injection (`Depends`).

## Acceptance checklist

- [ ] `arabicpython/aliases/fastapi.toml` shipped with at least 40 entries.
- [ ] All integration tests pass.
- [ ] `examples/B11_fastapi_hello.apy` runs end-to-end.
- [ ] `examples/B11_README-ar.md` written.
- [ ] Phase A compat assertion: `tests/test_phase_a_compat.py` still passes.
