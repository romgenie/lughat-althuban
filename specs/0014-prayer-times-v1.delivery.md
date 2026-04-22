# Delivery Note — Spec 0014: prayer-times-v1

**Status**: merged  
**Delivered by**: Gemini Pro  
**CI fixes**: Claude  
**Merged**: 2026-04-22

## What was built

A prayer time calculator written entirely in apython using the Umm al-Qura method:

- `apps/prayer_times/المدن.apy` — dictionary of 15 major Arab cities with coordinates and timezone; lookup function `ابحث_عن_مدينه` with exact and partial matching
- `apps/prayer_times/الحساب.apy` — class `حاسبة_الصلاه` implementing full spherical astronomy (Julian Day, solar declination, equation of time, hour angles, Asr shadow formula, Isha = Maghrib + 90 min)
- `apps/prayer_times/الرئيسي.apy` — CLI entry point with box-drawing Unicode table, Arabic-Indic digits, "الصلاة القادمة" next-prayer row, city-name and date arguments
- `tests/test_prayer_times.py` — 10 tests (all passing); prayer times for Riyadh 2026-04-21 verified within ±2 min of reference sources

All identifiers in `.apy` source are pure Arabic. `اجلب_صفة` (getattr) was used to access stdlib `math` and `datetime` without English identifiers in source.

## CI fixes required after Gemini delivery

**Ruff lint** (`tests/test_prayer_times.py`):
- Removed unused imports (`sys`, `os`, `subprocess`, `datetime`)
- Sorted import blocks (I001: `pytest` before `arabicpython` since arabicpython is first-party)
- Added `# noqa: E402, I001` to Arabic module imports that follow `arabicpython.install()`

No Python 3.11 tokenizer issues in prayer times source — Gemini used `هـ` (tatweel U+0640) but no damma/shadda in identifiers.
