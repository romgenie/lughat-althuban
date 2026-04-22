# Delivery Note for 0013 (search-engine-v1)

- Created 6 Arabic text documents in `apps/search_engine/docs/`.
- Implemented `normalizer.apy` with text folding rules.
- Implemented `indexer.apy` to read `.txt` files and build inverted index.
- Implemented `ranker.apy` with TF-IDF calculation and snippet extraction, using bubble sort (`ترتيب_تنازلي`) internally.
- Implemented `cli.apy` with both interactive and single query modes, using Arabic-Indic digits conversion.
- Used `getattr` via `اجلب_صفة` to access standard Python library functions since English identifiers are disallowed in `.apy` code.
- Added 10 tests in `tests/test_search_engine.py` using `arabicpython` import hooks.
- All identifiers in `.apy` code are purely Arabic.
- Formatted `tests/test_search_engine.py` with `black`.
