# Delivery Note — Spec 0013: search-engine-v1

**Status**: merged  
**Delivered by**: Gemini Pro  
**CI fixes**: Claude  
**Merged**: 2026-04-22

## What was built

A fully-functional Arabic full-text search engine written entirely in apython:

- `apps/search_engine/normalizer.apy` — Arabic text normalization (strip harakat, fold hamza/alef-maksura/ta-marbuta)
- `apps/search_engine/indexer.apy` — class `فهرس` with inverted index and TF-IDF support
- `apps/search_engine/ranker.apy` — class `باحث` with TF-IDF scoring and snippet extraction
- `apps/search_engine/cli.apy` — interactive and single-query CLI modes
- `apps/search_engine/docs/` — 6 Arabic text documents (الخوارزمي, بيت_الحكمة, اللغة_العربية, علم_الفلك, ابن_سينا, ابن_بطوطة)
- `tests/test_search_engine.py` — 10 tests (all passing)

## CI fixes required after Gemini delivery

**Ruff lint** (`tests/test_search_engine.py`):
- Removed unused imports (`os`, `pytest`)
- Sorted import blocks (I001)
- Added `# noqa: E402` to Arabic module imports that follow `arabicpython.install()`

**Python 3.11 tokenizer compatibility**:
- Python 3.11's `tokenize` module produces `ERRORTOKEN` for Arabic harakat diacritics
  (shadda ّ U+0651, damma ُ U+064F) used in identifiers, even though
  `str.isidentifier()` returns True. This regression was fixed upstream in Python 3.12.
- Renamed affected identifiers in `.apy` source files:
  - `طبّع` → `طبع` (normalizer function, all three modules)
  - `مطبّعة` → `مطبعة` (local variable)
  - `كلمات_مطبّعة` → `كلمات_مطبعة` (list variable)
  - `_رمّز` → `_رمز` (private method)
  - `نص_معلّم` → `نص_معلم` (annotated-text variable)
  - `مُقرب` → `مقرب` (rounded-value variable in cli.apy)
- The apython ADR 0004 normalizer strips harakat at runtime anyway, so the
  public API is unchanged — this is a source-level spelling change only.

## Note for future .apy files

Avoid harakat (U+064B–U+065F) in identifiers to stay compatible with Python 3.11.
The tatweel `ـ` (U+0640) is fine; it is accepted by Python 3.11's tokenizer.
