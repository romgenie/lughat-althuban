# Spec Packet B-014: aliases-requests-extras-v1

**Phase**: B
**Depends on**: B-001 (alias-runtime-v1), B-002 (phase-a-compat-suite)
**Estimated size**: small
**Owner**: —

## Goal

Ship the Arabic alias mapping for the advanced surface of the `requests` library (Sessions, Auth, Adapters) that was omitted from the initial Phase B mapping.

## Non-goals

- No new basic HTTP methods (already covered in B-001).

## Files

### Files to create

- `arabicpython/aliases/requests_extras.toml` (Note: these should eventually merge into `requests.toml` or be a separate mapping that re-exports `requests` with more surface)
- `tests/test_aliases_requests_extras.py`
- `examples/B14_requests_session_demo.apy`
- `examples/B14_README-ar.md`

## Public interfaces

### `arabicpython/aliases/requests_extras.toml`

[meta]
arabic_name = "طلبات_إضافية"
python_module = "requests"
dict_version = "ar-v1"
schema_version = 1

[entries]
"جلسة" = "Session"
"طلب" = "Request"
"طلب_مجهز" = "PreparedRequest"
"استجابة" = "Response"
"محول_http" = "adapters.HTTPAdapter"
"توثيق_أساسي" = "auth.HTTPBasicAuth"
"توثيق_ديجيست" = "auth.HTTPDigestAuth"
"أكواد" = "codes"
"كوكيز" = "cookies.RequestsCookieJar"
"هياكل" = "structures.CaseInsensitiveDict"

# Exceptions
"خطأ_اتصال" = "exceptions.ConnectionError"
"خطأ_http" = "exceptions.HTTPError"
"مهلة" = "exceptions.Timeout"
"تحويلات_كثيرة" = "exceptions.TooManyRedirects"
"خطأ_طلب" = "exceptions.RequestException"

# (Adding more to reach 20)
"محولات" = "adapters"
"توثيق" = "auth"
"استثناءات" = "exceptions"
"شهادات" = "certs"
"كوكيز_برق" = "cookies"

# Count: 20 entries.

### `examples/B14_requests_session_demo.apy`

```python
استورد طلبات_إضافية من requests

جلسة = طلبات_إضافية.جلسة()
استجابة = جلسة.get("https://httpbin.org/get")
اطبع(f"حالة الاستجابة: {استجابة.status_code}")

توثيق = طلبات_إضافية.توثيق_أساسي("مستخدم", "كلمة_سر")
استجابة_محمية = جلسة.get("https://httpbin.org/basic-auth/مستخدم/كلمة_سر", auth=توثيق)
اطبع(f"حالة الاستجابة المحمية: {استجابة_محمية.status_code}")
```

## Implementation constraints

- **Cite B-010 as structural prior.** This packet follows the same deliverable structure and naming conventions.
- **Method-on-instance limitation:** Like B-010, this packet only maps module-level attributes. Methods on instances (e.g., `session.get`, `response.json`) remain in English in this version.
- **Acceptance checklist must include Phase A compat assertion.**
- **Ensure all Arabic names round-trip through `normalize_identifier`.**

## Test requirements

- Verification of `Session` object behavior.
- Verification of authentication helpers.
- Verification of custom adapters.

## Acceptance checklist

- [ ] `arabicpython/aliases/requests_extras.toml` shipped with at least 20 entries.
- [ ] All integration tests pass.
- [ ] `examples/B14_requests_session_demo.apy` runs end-to-end.
- [ ] `examples/B14_README-ar.md` written.
- [ ] Phase A compat assertion: `tests/test_phase_a_compat.py` still passes.
