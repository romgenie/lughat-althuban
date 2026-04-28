# Hand-Over Document — Large Open Packets
*Prepared 2026-04-28. Current test suite: 2510 passing, 45 skipped.*

This document is a self-contained brief for a contributor picking up one of
the two large open packets (B-060 and B-061). Everything needed to start is
here; no further questions to the planner are required.

---

## Project overview (30-second version)

**apython** is an Arabic-keyword Python dialect. You write `.apy` files using
Arabic keywords, built-in names, and imported library aliases; the runtime
translates them to Python and executes them. The project ships:

- A CLI (`ثعبان`), REPL, import hook, and traceback translator.
- 40 alias TOML files covering stdlib + top third-party libs (numpy, pandas,
  Flask, Django, SQLAlchemy, seaborn, scipy, aiohttp, …).
- An LSP server (`ثعبان خادم`), VSCode extension, Jupyter kernel.
- A formatter (`ثعبان نسّق`) and linter (`ثعبان راجع`).

**Dictionary**: `dictionaries/ar-v2.md` is the active keyword table.
The entry format is `| python_keyword | arabic_keyword | notes |`.

**Alias modules**: `arabicpython/aliases/*.toml`. Each TOML maps an Arabic
module name (e.g. `نمباي`) to a Python module (`numpy`) and lists Arabic
attribute aliases.

**Running `.apy` files**: `ثعبان file.apy` or  
`python -c "from arabicpython.translate import translate; exec(translate(open('f.apy').read()))"`

**Tests**: `pytest` from the repo root. The suite runs in ~3 min on Windows.

---

## Repo layout (what matters for docs packets)

```
apython/
├── dictionaries/
│   └── ar-v2.md              ← keyword canon; check this before choosing terms
├── arabicpython/aliases/     ← 40 TOMLs; check arabic_name and entry keys
├── docs/
│   ├── tutorial.md           ← English tutorial (source of truth for B-060)
│   └── ar/                   ← Arabic docs directory (put new files here or
│                                 at docs/ root — mirror the English structure)
├── examples/
│   ├── 01_hello.apy … 07_imports.apy   ← Phase A examples; study for style
│   ├── B10_flask_hello.apy             ← Phase B examples; study for style
│   └── B60_tutorial_excerpts/          ← CREATE THIS for B-060 long examples
├── specs/
│   ├── B-060-tutorial-translation.md   ← Full spec for B-060
│   └── B-061-cookbook-translation.md   ← Full spec for B-061
├── tests/
│   └── test_phase_a_compat.py          ← The existing snapshot test harness
└── CHANGELOG.md
```

---

## How to write `.apy` code (quick reference)

| Python | Arabic (ar-v2) | Notes |
|--------|---------------|-------|
| `import X` | `استورد X` | standalone import |
| `from X import Y` | `من X استورد Y` | from-import |
| `import X as Y` | `استورد X باسم Y` | as-alias |
| `def f():` | `دالة f():` | function definition |
| `class C:` | `صنف C:` | class definition |
| `if / elif / else` | `إذا / إلا_إذا / وإلا` | |
| `for x in y:` | `لكل x في y:` | |
| `while` | `بينما` | |
| `return` | `إرجاع` | |
| `print(x)` | `اطبع(x)` | built-in alias |
| `len(x)` | `طول(x)` | built-in alias |
| `True / False / None` | `صحيح / خطأ / لا_شيء` | |
| `try / except / finally` | `حاول / إلا_إذا / أخيرًا` | |
| `with X as Y:` | `مع X باسم Y:` | |
| `pass` | `مرر` | |
| `assert` | `تأكيد` | |
| `async def` | `دالة غير_متزامنة` | |
| `await` | `تنتظر` | |

**Normalization rules** (apply to TOML keys and `.apy` identifiers):
- `أ / إ / آ` → `ا` (all hamzas become bare alef)
- final `ة` → `ه` (ta-marbuta → heh)
- final `ى` → `ي` (alef-maqsura → yeh)

So write `جلسه` not `جلسة`, `مرتبه` not `مرتبة`, `مبتدي` not `مبتدى`.

**Add the dict directive to every new `.apy` file:**
```
# arabicpython: dict=ar-v2
```

---

## B-060 — Arabic Tutorial Translation

**Full spec**: `specs/B-060-tutorial-translation.md` (read it in full).

### What to produce

| Deliverable | Path | Notes |
|-------------|------|-------|
| Arabic tutorial | `docs/tutorial-ar.md` | Parallel to `docs/tutorial.md`; same sections |
| Glossary | `docs/tutorial-ar-glossary.md` | Every new technical term → Arabic + 1-sentence def |
| Long examples | `examples/B60_tutorial_excerpts/*.apy` | Examples > 30 lines; shorter ones inline |
| Test file | `tests/test_tutorial_ar.py` | 8 specific tests; details in spec |
| README link | `README.md` | One line pointing to `docs/tutorial-ar.md` |
| English cross-link | `docs/tutorial.md` | One line at top: Arabic version link |

### Acceptance checklist (short form)

- [ ] Word count of `tutorial-ar.md` within ±10% of English tutorial
- [ ] Every section in the English tutorial has an Arabic counterpart
- [ ] Every code block tagged `apy` runs via `ثعبان` with exit code 0
      (unless explicitly tagged `<!-- expected-error -->` or `<!-- not-runnable: snippet -->`)
- [ ] All 8 tests in `test_tutorial_ar.py` pass on the full matrix
- [ ] Glossary covers: decorator, iterator, generator, context manager,
      coroutine, module, package, exception, keyword argument, list comprehension
- [ ] Glossary terms match `dictionaries/ar-v2.md` and alias TOMLs where they overlap
- [ ] Cross-links in README.md and docs/tutorial.md added
- [ ] PR includes a GitHub-rendered screenshot (bidi text must look correct)
- [ ] An Arabic-fluent reviewer (not the implementer) signs off on prose quality
- [ ] Delivery note `B-060-tutorial-translation.delivery.md` written

### Style guidelines

- **Language**: Modern Standard Arabic (فصحى). No dialect.
- **Register**: beginner-accessible; short sentences; active voice.
- **Technical terms**: use the dictionary and TOML aliases as the canon.
  When a term has no prior translation in the project, choose one and record
  it in the glossary with rationale. Consult the Microsoft Arabic Style Guide
  (https://learn.microsoft.com/en-us/style-guide/arabic/welcome).
- **Punctuation in prose**: `،` (Arabic comma), `؛` (semicolon), `؟` (question mark).
  Code blocks use ASCII as Python requires.
- **Numbers in prose**: Arabic-Indic digits (٠–٩); ASCII digits in code.
- **No emoji**.
- **No machine translation as the primary source** — MT is a vocabulary aid only.

### Test file skeleton (`tests/test_tutorial_ar.py`)

```python
# tests/test_tutorial_ar.py
# B-060: Arabic tutorial structural and execution tests

import re
import subprocess
import sys
from pathlib import Path

import pytest

TUTORIAL_AR = Path(__file__).parent.parent / "docs" / "tutorial-ar.md"
TUTORIAL_EN = Path(__file__).parent.parent / "docs" / "tutorial.md"
GLOSSARY    = Path(__file__).parent.parent / "docs" / "tutorial-ar-glossary.md"
EXCERPTS    = Path(__file__).parent.parent / "examples" / "B60_tutorial_excerpts"

KEY_TERMS = [
    "decorator", "iterator", "generator", "context_manager",
    "coroutine", "module", "package", "exception",
    "keyword_argument", "list_comprehension",
]


def _headings(path):
    return [l for l in path.read_text(encoding="utf-8").splitlines()
            if l.startswith("#")]


def _code_blocks(path):
    """Yield (line_no, tag, code) for every fenced block."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].startswith("```apy") or lines[i].startswith("```arabicpython"):
            tag = lines[i]
            start = i + 1
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                i += 1
            yield start, tag, "\n".join(lines[start:i])
        i += 1


class TestStructure:
    def test_tutorial_ar_exists(self):
        assert TUTORIAL_AR.exists()

    def test_tutorial_ar_utf8(self):
        TUTORIAL_AR.read_text(encoding="utf-8")

    def test_tutorial_ar_starts_with_heading(self):
        first = TUTORIAL_AR.read_text(encoding="utf-8").lstrip()
        assert first.startswith("# ")

    def test_section_count_matches_english(self):
        en = len(_headings(TUTORIAL_EN))
        ar = len(_headings(TUTORIAL_AR))
        assert abs(ar - en) <= 2, f"English has {en} headings, Arabic has {ar}"


class TestGlossary:
    def test_glossary_exists(self):
        assert GLOSSARY.exists()

    @pytest.mark.parametrize("term", KEY_TERMS)
    def test_key_term_in_glossary(self, term):
        content = GLOSSARY.read_text(encoding="utf-8")
        assert term in content, f"Key term '{term}' not found in glossary"


@pytest.mark.parametrize("lineno,tag,code", list(_code_blocks(TUTORIAL_AR))
                         if TUTORIAL_AR.exists() else [])
def test_tutorial_code_block_runs(tmp_path, lineno, tag, code):
    if "not-runnable" in tag:
        pytest.skip("snippet block")
    apy_file = tmp_path / "block.apy"
    apy_file.write_text(code, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "arabicpython.cli", str(apy_file)],
        capture_output=True, text=True,
    )
    expected_error = "expected-error" in tag
    if expected_error:
        assert result.returncode != 0
    else:
        assert result.returncode == 0, (
            f"Block at line {lineno} failed:\n{result.stderr}"
        )


@pytest.mark.parametrize("apy_file", list(EXCERPTS.glob("*.apy"))
                          if EXCERPTS.exists() else [])
def test_excerpt_runs(apy_file):
    result = subprocess.run(
        [sys.executable, "-m", "arabicpython.cli", str(apy_file)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, (
        f"{apy_file.name} failed:\n{result.stderr}"
    )
```

### Suggested section order for `tutorial-ar.md`

Mirror `docs/tutorial.md` exactly. Typical English tutorial sections:

1. مقدمة (Introduction)
2. تشغيل لغة الثعبان (Running apython)
3. المتغيرات والأنواع الأساسية (Variables and basic types)
4. التحكم في التدفق (Control flow — إذا / بينما / لكل)
5. الدوال (Functions — دالة / إرجاع)
6. الأصناف (Classes — صنف)
7. الاستيراد (Imports — استورد / من … استورد)
8. معالجة الأخطاء (Error handling — حاول / إلا_إذا / أخيرًا)
9. المكتبات (Libraries — alias modules)
10. مشروع كامل (A complete project — e.g. Flask hello-world)

---

## B-061 — Arabic Cookbook Translation

**Full spec**: `specs/B-061-cookbook-translation.md`.

### What to produce

| Deliverable | Path |
|-------------|------|
| Arabic cookbook | `docs/cookbook-ar.md` |
| Glossary | `docs/cookbook-ar-glossary.md` |
| Test file | `tests/test_cookbook_ar.py` |

### Dependency

B-061 **depends on B-060** and on `docs/cookbook.md` existing. If the English
cookbook hasn't been written yet, create it first (it is a non-code packet —
just the English recipes — then translate). Check:

```
ls docs/cookbook.md
```

If the file doesn't exist, create it before starting B-061.

### Test file skeleton (`tests/test_cookbook_ar.py`)

```python
# tests/test_cookbook_ar.py
# B-061: Arabic cookbook code-block tests

import subprocess, sys
from pathlib import Path
import pytest

COOKBOOK_AR = Path(__file__).parent.parent / "docs" / "cookbook-ar.md"


def _code_blocks(path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].startswith("```apy"):
            start = i + 1
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                i += 1
            yield start, "\n".join(lines[start:i])
        i += 1


class TestStructure:
    def test_cookbook_ar_exists(self):
        assert COOKBOOK_AR.exists()

    def test_cookbook_ar_utf8(self):
        COOKBOOK_AR.read_text(encoding="utf-8")


@pytest.mark.parametrize("lineno,code",
    list(_code_blocks(COOKBOOK_AR)) if COOKBOOK_AR.exists() else [])
def test_cookbook_code_block_runs(tmp_path, lineno, code):
    f = tmp_path / "recipe.apy"
    f.write_text(code, encoding="utf-8")
    r = subprocess.run(
        [sys.executable, "-m", "arabicpython.cli", str(f)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, f"Block at line {lineno} failed:\n{r.stderr}"
```

---

## Shared resources

### Looking up the right Arabic term

1. **Dictionary first**: `grep "your_term" dictionaries/ar-v2.md`
2. **Alias TOMLs**: `grep -r "your_term" arabicpython/aliases/`
3. **Existing demos**: `grep -r "your_term" examples/`
4. **Siwar API** (authoritative Arabic terminology from King Salman Arabic
   Language Center): `python tools/siwar_lookup.py <term>`
   Key lexicons: `4cd164a7` (Data & AI), `97ac5360` (Digital Gov),
   `ee392446` (Statistics).

### Running a single `.apy` file

```bash
python -m arabicpython.cli examples/01_hello.apy
```

or

```bash
ثعبان examples/01_hello.apy
```

### Running the full test suite

```bash
pytest                     # full suite (~3 min)
pytest tests/test_foo.py   # one file
pytest -k "tutorial"       # by keyword
```

### Phase A compat suite

The existing snapshot tests live in `tests/test_phase_a_compat.py`.
When adding new example files, add them to `_EXCLUDED` if they:
- make live HTTP calls
- start a blocking server
- produce non-deterministic output (current date/time, random numbers)
- require a CLI argument

Non-excluded examples must have a snapshot in
`tests/snapshots/phase_a/expected_outputs/<filename>.txt`.
Generate one by running the example and capturing stdout+stderr.

### Formatting and linting

```bash
ثعبان نسّق examples/your_new_file.apy    # format in place
ثعبان راجع examples/your_new_file.apy    # lint check
```

---

## Recommended future library alias packets

The table below lists libraries that would give the most value to Arabic
Python learners — prioritised by popularity + educational relevance. Each
would be a self-contained S/M-sized packet following the exact same TOML +
test + demo pattern as the 40 already shipped.

**Already covered** (40 modules): numpy, pandas, flask, django, sqlalchemy,
fastapi, requests, pytest, pillow, seaborn, scipy, aiohttp, asyncio, json,
re, math, os, pathlib, sys, datetime, time, logging, collections, itertools,
functools, csv, sqlite3, subprocess, shutil, argparse, hashlib, io,
contextlib, statistics, random, string, textwrap, secrets, uuid, calendar.

> **Normalization reminder for Arabic names:**
> `أ/إ/آ → ا`, final `ة → ه`, final `ى → ي`, use `_` between words.
> Run `from arabicpython.aliases._loader import load_mapping` on the TOML before
> writing tests — it catches all key errors at once.

---

### Tier 1 — Web / API / Networking

| Library | `python_module` | Arabic name (suggested) | Why | Entries est. |
|---------|----------------|------------------------|-----|:------------:|
| `httpx` | `httpx` | `طلبات_حديثه` | Modern sync+async HTTP; cleaner than requests | ~30 |
| `pydantic` | `pydantic` | `نماذج_بيانات` | Data validation; essential for FastAPI users | ~25 |
| `celery` | `celery` | `مهام_خلفيه` | Background task queues | ~20 |
| `redis` | `redis` | `ذاكره_مؤقته` | In-memory cache + pub/sub + task broker | ~22 |
| `sqlmodel` | `sqlmodel` | `نموذج_قاعده` | SQLAlchemy + Pydantic combo | ~18 |
| `alembic` | `alembic` | `ترحيل_قاعده` | DB migration tool (used with SQLAlchemy) | ~15 |
| `boto3` | `boto3` | `خدمات_سحابيه` | AWS SDK; S3, Lambda, DynamoDB, SQS | ~35 |
| `pymongo` | `pymongo` | `قاعده_وثائق` | MongoDB driver | ~20 |
| `motor` | `motor` | `قاعده_وثائق_غير_متزامنه` | Async MongoDB (built on pymongo) | ~15 |
| `psycopg2` | `psycopg2` | `قاعده_بوستجريس` | PostgreSQL sync adapter | ~15 |
| `asyncpg` | `asyncpg` | `بوستجريس_غير_متزامن` | Async PostgreSQL; fastest driver | ~15 |
| `aiosqlite` | `aiosqlite` | `قاعده_محليه_غير_متزامنه` | Async SQLite | ~10 |
| `websockets` | `websockets` | `مقابس_شبكيه` | WebSocket client + server | ~15 |
| `starlette` | `starlette` | `اطار_خفيف` | ASGI micro-framework; FastAPI's foundation | ~20 |
| `uvicorn` | `uvicorn` | `خادم_asgi` | ASGI server for FastAPI/Starlette | ~10 |
| `gunicorn` | `gunicorn` | `خادم_wsgi` | WSGI server for Flask/Django prod | ~10 |
| `jinja2` | `jinja2` | `قوالب_html` | HTML templating (Flask's engine) | ~20 |
| `authlib` | `authlib` | `مصادقه_متقدمه` | OAuth2, OIDC, JWT library | ~18 |
| `python-jose` | `jose` | `رموز_مشفره` | JWT signing and verification | ~10 |
| `passlib` | `passlib` | `تشفير_كلمات_مرور` | Password hashing (bcrypt, argon2) | ~12 |
| `grpcio` | `grpc` | `استدعاء_بعيد` | gRPC client/server | ~15 |
| `graphene` | `graphene` | `استعلامات_رسوميه` | GraphQL schema builder | ~15 |
| `pika` | `pika` | `طوابير_رسائل` | RabbitMQ / AMQP client | ~12 |
| `kafka-python` | `kafka` | `تدفق_بيانات_حيه` | Apache Kafka client | ~15 |
| `dnspython` | `dns.resolver` | `استعلام_dns` | DNS queries | ~10 |
| `python-multipart` | `multipart` | `بيانات_نماذج` | Multipart form parsing (FastAPI uploads) | ~8 |

### Tier 2 — Databases / ORMs / Storage

| Library | `python_module` | Arabic name (suggested) | Why | Entries est. |
|---------|----------------|------------------------|-----|:------------:|
| `pymysql` | `pymysql` | `قاعده_ميسكول` | MySQL/MariaDB connector | ~12 |
| `elasticsearch` | `elasticsearch` | `محرك_بحث` | Full-text search engine client | ~20 |
| `pymilvus` | `pymilvus` | `قاعده_متجهات` | Vector DB for AI/embedding search | ~15 |
| `pinecone-client` | `pinecone` | `صنوبر_متجهات` | Pinecone vector DB | ~12 |
| `chromadb` | `chromadb` | `قاعده_كروما` | Local vector DB; popular with LangChain | ~12 |
| `influxdb-client` | `influxdb_client` | `قاعده_زمنيه` | Time-series database client | ~15 |
| `cassandra-driver` | `cassandra.cluster` | `قاعده_موزعه` | Apache Cassandra client | ~15 |
| `sqlalchemy-utils` | `sqlalchemy_utils` | `ادوات_قاعده` | Extra SQLAlchemy types and utilities | ~15 |

### Tier 3 — AI / Machine Learning / Deep Learning

| Library | `python_module` | Arabic name (suggested) | Why | Entries est. |
|---------|----------------|------------------------|-----|:------------:|
| `torch` | `torch` | `مشاعل_الذكاء` | PyTorch deep learning | ~40 |
| `torchvision` | `torchvision` | `رؤيه_حاسوبيه_مشاعل` | PyTorch vision models | ~20 |
| `tensorflow` | `tensorflow` | `تدفق_بيانات` | TensorFlow deep learning | ~35 |
| `keras` | `keras` | `واجهه_تعلم_عميق` | High-level DL API (TF backend) | ~25 |
| `transformers` | `transformers` | `محولات_لغويه` | HuggingFace; Arabic BERT/GPT models | ~35 |
| `datasets` | `datasets` | `مجموعات_بيانات` | HuggingFace datasets hub | ~15 |
| `tokenizers` | `tokenizers` | `مقطع_نصوص` | HuggingFace fast tokenizers | ~12 |
| `sentence-transformers` | `sentence_transformers` | `تضمين_جمل` | Sentence embeddings | ~12 |
| `openai` | `openai` | `ذكاء_مفتوح` | OpenAI API (GPT-4, embeddings, Whisper) | ~20 |
| `anthropic` | `anthropic` | `مساعد_كلود` | Claude API (Arabic-capable models) | ~15 |
| `langchain` | `langchain` | `سلسله_لغويه` | LLM orchestration framework | ~30 |
| `langchain-core` | `langchain_core` | `نواه_سلسله_لغويه` | LangChain core abstractions | ~20 |
| `llama-index` | `llama_index` | `فهرس_لغوي` | RAG framework for LLMs | ~20 |
| `sympy` | `sympy` | `رياضيات_رمزيه` | Symbolic math; high educational value | ~45 |
| `networkx` | `networkx` | `شبكات_رياضيه` | Graph theory and network analysis | ~35 |
| `statsmodels` | `statsmodels.api` | `نماذج_احصائيه` | OLS, ARIMA, logistic regression | ~30 |
| `xgboost` | `xgboost` | `تعزيز_متدرج` | Gradient boosting; top Kaggle model | ~20 |
| `lightgbm` | `lightgbm` | `تعزيز_خفيف` | Fast gradient boosting by Microsoft | ~18 |
| `catboost` | `catboost` | `تعزيز_يانديكس` | Categorical feature boosting | ~15 |
| `optuna` | `optuna` | `ضبط_نماذج` | Hyperparameter optimization | ~18 |
| `mlflow` | `mlflow` | `تتبع_تجارب` | ML experiment tracking | ~20 |
| `joblib` | `joblib` | `تنفيذ_موازي` | Parallel loops + caching | ~10 |
| `dask` | `dask` | `بيانات_ضخمه` | Parallel pandas/numpy for big data | ~25 |
| `polars` | `polars` | `اطار_قطبي` | Fast DataFrame library (Rust-backed) | ~40 |
| `pyarrow` | `pyarrow` | `سهم_بيانات` | Arrow columnar format; Parquet I/O | ~25 |
| `xarray` | `xarray` | `مصفوفه_متعدده_الابعاد` | N-dimensional labeled arrays | ~20 |

### Tier 4 — Arabic NLP (highest thematic relevance)

| Library | `python_module` | Arabic name (suggested) | Why | Entries est. |
|---------|----------------|------------------------|-----|:------------:|
| `camel-tools` | `camel_tools` | `ادوات_جمل` | Arabic morphology, POS, NER, diacritization | ~20 |
| `nltk` | `nltk` | `ادوات_لغه_طبيعيه` | NLP toolkit; Arabic tokenizers, stemmer | ~30 |
| `spacy` | `spacy` | `معالجه_نصوص` | Industrial NLP; Arabic model `ar_core_news_sm` | ~20 |
| `arabic-reshaper` | `arabic_reshaper` | `اعاده_رسم_عربي` | Fix Arabic rendering in matplotlib/PDF | ~8 |
| `python-bidi` | `bidi.algorithm` | `ثنائي_الاتجاه` | BiDi algorithm for Arabic+Latin mixing | ~6 |
| `pyarabic` | `pyarabic.araby` | `ادوات_عربيه` | Diacritics, root extraction, stemming | ~20 |
| `farasapy` | `farasa` | `تحليل_فراسه` | KSU Arabic NLP toolkit | ~10 |
| `qalsadi` | `qalsadi` | `تحليل_صرفي` | Arabic morphological analyzer | ~10 |
| `mishkal` | `mishkal` | `تشكيل_نص` | Arabic text diacritization | ~8 |
| `stanza` | `stanza` | `حزمه_لغويه` | Stanford NLP; Arabic pipeline | ~15 |
| `gensim` | `gensim` | `نماذج_دلاليه` | Word2Vec, FastText, LDA topic models | ~20 |
| `hazm` | `hazm` | `معالجه_فارسيه` | Persian NLP (for multilingual projects) | ~15 |

### Tier 5 — Data Visualization

| Library | `python_module` | Arabic name (suggested) | Why | Entries est. |
|---------|----------------|------------------------|-----|:------------:|
| `plotly` | `plotly.express` | `رسوم_تفاعليه` | Interactive charts; RTL Arabic labels | ~30 |
| `plotly-graph-objects` | `plotly.graph_objects` | `كائنات_رسوميه` | Low-level Plotly API | ~25 |
| `bokeh` | `bokeh.plotting` | `رسوم_بوكيه` | Interactive web charts | ~25 |
| `altair` | `altair` | `رسوم_اعلانيه` | Declarative visualization | ~20 |
| `dash` | `dash` | `لوحه_تحكم` | Plotly Dash; interactive web dashboards | ~20 |
| `matplotlib` | `matplotlib.pyplot` | `رسوم_مخططات` | Already exists as `رسم_مخططات` ← verify name | — |
| `folium` | `folium` | `خرائط_تفاعليه` | Leaflet.js maps in Python | ~15 |
| `geopandas` | `geopandas` | `بيانات_جغرافيه` | Geospatial DataFrames | ~20 |
| `pyecharts` | `pyecharts` | `رسوم_صينيه` | Apache ECharts; good RTL support | ~15 |
| `wordcloud` | `wordcloud` | `سحابه_كلمات` | Word cloud generation; great for Arabic text | ~10 |

### Tier 6 — Web UI / Frontend / Automation

| Library | `python_module` | Arabic name (suggested) | Why | Entries est. |
|---------|----------------|------------------------|-----|:------------:|
| `streamlit` | `streamlit` | `واجهه_بيانات` | Fast data app builder; popular in Arabic DS | ~25 |
| `gradio` | `gradio` | `واجهه_تفاعليه` | ML demo UI; HuggingFace demos | ~15 |
| `panel` | `panel` | `لوحه_عرض` | Dashboard framework (hvPlot ecosystem) | ~15 |
| `playwright` | `playwright.sync_api` | `متصفح_الي` | Browser automation; Arabic site testing | ~20 |
| `selenium` | `selenium.webdriver` | `تحكم_متصفح` | Browser automation (legacy; widely known) | ~20 |
| `beautifulsoup4` | `bs4` | `تحليل_html` | HTML/XML parsing | ~15 |
| `lxml` | `lxml.etree` | `تحليل_xml` | Fast XML/HTML parser | ~15 |
| `scrapy` | `scrapy` | `جمع_بيانات` | Industrial web crawler framework | ~20 |
| `pyppeteer` | `pyppeteer` | `متصفح_بايثون` | Headless Chrome (Python puppeteer port) | ~15 |
| `mechanize` | `mechanize` | `تصفح_الي` | Stateful HTTP client (forms, cookies) | ~10 |
| `click` | `click` | `واجهه_اوامر` | CLI builder; decorators-based | ~20 |
| `typer` | `typer` | `اوامر_مكتوبه` | Click with type hints (FastAPI-style CLI) | ~15 |
| `rich` | `rich` | `مخرجات_منسقه` | Rich terminal output; tables, progress, color | ~25 |
| `textual` | `textual` | `واجهه_نصيه` | TUI framework; full-screen terminal apps | ~20 |
| `tqdm` | `tqdm` | `شريط_تقدم` | Progress bars; essential for ML training loops | ~12 |
| `prompt_toolkit` | `prompt_toolkit` | `محرر_اوامر` | Interactive CLI input with history | ~15 |

### Tier 7 — File Formats / Document Processing

| Library | `python_module` | Arabic name (suggested) | Why | Entries est. |
|---------|----------------|------------------------|-----|:------------:|
| `openpyxl` | `openpyxl` | `ملفات_اكسل` | Read/write Excel .xlsx files | ~20 |
| `xlrd` | `xlrd` | `قراءه_اكسل` | Read old Excel .xls files | ~8 |
| `python-docx` | `docx` | `ملفات_وورد` | Read/write Word .docx files | ~20 |
| `pypdf` | `pypdf` | `ملفات_pdf` | PDF reading and manipulation | ~15 |
| `pdfplumber` | `pdfplumber` | `استخراج_pdf` | PDF text/table extraction | ~12 |
| `reportlab` | `reportlab.pdfgen.canvas` | `انشاء_pdf` | PDF generation (Arabic RTL support) | ~20 |
| `weasyprint` | `weasyprint` | `تحويل_html_pdf` | HTML→PDF with CSS (RTL-aware) | ~10 |
| `python-pptx` | `pptx` | `عروض_تقديميه` | Read/write PowerPoint .pptx | ~20 |
| `markdown` | `markdown` | `تحويل_ماركداون` | Markdown→HTML | ~10 |
| `mistune` | `mistune` | `ماركداون_سريع` | Fast Markdown parser | ~10 |
| `pyyaml` | `yaml` | `ملفات_yaml` | YAML read/write | ~10 |
| `toml` / `tomllib` | `tomllib` | built-in (3.11+) | — already available | — |
| `msgpack` | `msgpack` | `تسلسل_سريع` | Fast binary serialization | ~8 |
| `orjson` | `orjson` | `json_سريع` | 10× faster JSON (Rust-backed) | ~8 |
| `python-magic` | `magic` | `كشف_نوع_ملف` | MIME type detection | ~8 |
| `chardet` | `chardet` | `كشف_ترميز` | Character encoding detection (Arabic!) | ~8 |

### Tier 8 — Concurrency / Systems / DevOps

| Library | `python_module` | Arabic name (suggested) | Why | Entries est. |
|---------|----------------|------------------------|-----|:------------:|
| `threading` | `threading` | `خيوط_تنفيذ` | stdlib threading | ~15 |
| `multiprocessing` | `multiprocessing` | `تعدد_معالجات` | stdlib multiprocessing | ~15 |
| `concurrent.futures` | `concurrent.futures` | `مستقبليات` | stdlib thread/process pool | ~10 |
| `trio` | `trio` | `تزامن_ثلاثي` | Structured async concurrency | ~20 |
| `anyio` | `anyio` | `تزامن_موحد` | Backend-agnostic async (asyncio+trio) | ~15 |
| `psutil` | `psutil` | `معلومات_نظام` | CPU, memory, disk, network stats | ~20 |
| `paramiko` | `paramiko` | `اتصال_ssh` | SSH client + SFTP | ~20 |
| `fabric` | `fabric` | `نشر_تلقائي` | Remote server deployment over SSH | ~12 |
| `docker` (SDK) | `docker` | `حاويات_docker` | Docker daemon API | ~15 |
| `cryptography` | `cryptography.fernet` | `تشفير_متقدم` | Fernet, RSA, AES, TLS primitives | ~25 |
| `python-dotenv` | `dotenv` | `متغيرات_بيئه` | Load `.env` files into `os.environ` | ~8 |
| `schedule` | `schedule` | `جدوله_مهام` | Simple cron-like job scheduler | ~10 |
| `apscheduler` | `apscheduler` | `جدوله_متقدمه` | Advanced job scheduling (cron, interval) | ~15 |
| `watchdog` | `watchdog` | `مراقبه_ملفات` | File system change monitoring | ~12 |
| `pywin32` | `win32api` | `واجهه_ويندوز` | Windows API (Windows-only) | ~20 |
| `pyautogui` | `pyautogui` | `تحكم_واجهه` | GUI automation (mouse + keyboard) | ~15 |
| `loguru` | `loguru` | `تسجيل_متقدم` | Better logging (replaces stdlib logging) | ~12 |
| `sentry-sdk` | `sentry_sdk` | `تتبع_اخطاء` | Error monitoring and crash reporting | ~12 |
| `prometheus-client` | `prometheus_client` | `مقاييس_اداء` | Metrics exposition for Prometheus | ~12 |

### Tier 9 — Email / Communication / Notifications

| Library | `python_module` | Arabic name (suggested) | Why | Entries est. |
|---------|----------------|------------------------|-----|:------------:|
| `smtplib` | `smtplib` | `بريد_صادر` | stdlib SMTP (send email) | ~10 |
| `email` | `email.mime.text` | `هيكل_بريد` | stdlib email construction | ~10 |
| `sendgrid` | `sendgrid` | `ارسال_بريد` | SendGrid email API | ~12 |
| `twilio` | `twilio.rest` | `رسائل_نصيه` | SMS + WhatsApp + voice via Twilio | ~15 |
| `slack-sdk` | `slack_sdk` | `رسائل_سلاك` | Slack bot and messaging API | ~15 |
| `python-telegram-bot` | `telegram` | `روبوت_تيليجرام` | Telegram bot framework | ~20 |
| `discord.py` | `discord` | `روبوت_ديسكورد` | Discord bot API | ~20 |
| `firebase-admin` | `firebase_admin` | `قاعده_نار` | Firebase (Firestore, Auth, FCM push) | ~18 |

### Tier 10 — Image / Audio / Video Processing

| Library | `python_module` | Arabic name (suggested) | Why | Entries est. |
|---------|----------------|------------------------|-----|:------------:|
| `opencv-python` | `cv2` | `رؤيه_حاسوبيه` | Computer vision; Arabic OCR pipelines | ~40 |
| `imageio` | `imageio` | `قراءه_صور` | Read/write images + video frames | ~12 |
| `scikit-image` | `skimage` | `معالجه_صور` | Image processing algorithms | ~25 |
| `pytesseract` | `pytesseract` | `تعرف_نصوص` | OCR via Tesseract (Arabic OCR support) | ~10 |
| `easyocr` | `easyocr` | `قراءه_نصوص_سهله` | Deep-learning OCR; Arabic support | ~8 |
| `soundfile` | `soundfile` | `ملفات_صوتيه` | Read/write audio files | ~10 |
| `librosa` | `librosa` | `تحليل_صوت` | Audio analysis and music information | ~20 |
| `pydub` | `pydub` | `تحرير_صوت` | Audio slicing, mixing, format conversion | ~15 |
| `speechrecognition` | `speech_recognition` | `تعرف_كلام` | Speech-to-text (Arabic dialect support) | ~12 |
| `gtts` | `gtts` | `نص_الي_كلام` | Google Text-to-Speech (Arabic voice) | ~8 |
| `moviepy` | `moviepy.editor` | `تحرير_فيديو` | Video editing and composition | ~20 |
| `ffmpeg-python` | `ffmpeg` | `ادوات_ffmpeg` | FFmpeg wrapper; transcoding | ~12 |

### Tier 11 — Finance / Time Series / Geospatial

| Library | `python_module` | Arabic name (suggested) | Why | Entries est. |
|---------|----------------|------------------------|-----|:------------:|
| `yfinance` | `yfinance` | `بيانات_ماليه` | Yahoo Finance stock/crypto data | ~10 |
| `ta` | `ta` | `مؤشرات_فنيه` | Technical analysis indicators (RSI, MACD) | ~20 |
| `pandas-datareader` | `pandas_datareader` | `قارئ_بيانات_ماليه` | Financial data from FRED, World Bank | ~10 |
| `shapely` | `shapely.geometry` | `اشكال_هندسيه` | Geometric shapes and spatial operations | ~20 |
| `pyproj` | `pyproj` | `اسقاط_خرائط` | Map projection and coordinate transforms | ~10 |
| `geopy` | `geopy` | `تحديد_موقع` | Geocoding (address → lat/lon) | ~12 |
| `arrow` | `arrow` | `وقت_سهل` | Better datetime handling than stdlib | ~20 |
| `pendulum` | `pendulum` | `وقت_دقيق` | datetime with timezone + Arabic locale | ~15 |

### Tier 12 — Testing / Quality / Dev Tools

| Library | `python_module` | Arabic name (suggested) | Why | Entries est. |
|---------|----------------|------------------------|-----|:------------:|
| `hypothesis` | `hypothesis` | `اختبار_خصائص` | Property-based testing | ~15 |
| `faker` | `faker` | `بيانات_مزيفه` | Generate fake Arabic names, addresses, text | ~15 |
| `factory-boy` | `factory_boy` | `مصنع_بيانات` | Test fixture factories | ~10 |
| `pytest-asyncio` | `pytest_asyncio` | `اختبار_غير_متزامن` | pytest plugin for async tests | ~8 |
| `pytest-cov` | `pytest_cov` | already in dev deps | — | — |
| `responses` | `responses` | `محاكاه_طلبات` | Mock HTTP responses in tests | ~10 |
| `httpretty` | `httpretty` | `محاكاه_http` | HTTP request interceptor | ~10 |
| `freezegun` | `freezegun` | `تجميد_وقت` | Mock datetime in tests | ~8 |
| `mypy` | `mypy` | type checker | — (dev tool, no alias needed) | — |

### Tier 13 — Configuration / Serialization

| Library | `python_module` | Arabic name (suggested) | Why | Entries est. |
|---------|----------------|------------------------|-----|:------------:|
| `pydantic-settings` | `pydantic_settings` | `اعدادات_بيانات` | Settings management via env vars | ~10 |
| `dynaconf` | `dynaconf` | `اعدادات_ديناميكيه` | Multi-environment config (12-factor) | ~12 |
| `configparser` | `configparser` | `محلل_اعدادات` | stdlib INI file parser | ~10 |
| `marshmallow` | `marshmallow` | `تحقق_بيانات` | Serialization + validation | ~18 |
| `cattrs` | `cattrs` | `تحويل_انواع` | attrs + cattrs data class conversion | ~10 |
| `dacite` | `dacite` | `انشاء_من_قاموس` | dataclass from dict | ~8 |
| `environs` | `environs` | `قراءه_بيئه` | Cleaner env var parsing | ~10 |

### Implementation notes for new packets

Every new alias packet must follow this checklist (same as all 40 existing ones):

1. **Create `arabicpython/aliases/<name>.toml`**
   - `[meta]` section: `arabic_name`, `python_module`, `dict_version = "ar-v1"`, `schema_version = 1`
   - `[entries]` section: `"normalized_arabic_key" = "python_attr"`
   - All keys must pass `normalize_identifier()` (run `python tools/validate_toml.py <file>` if it exists, or load via `_loader.load_mapping()`)
   - No two Arabic keys map to the same Python attribute
   - No collision with existing keys (run cross-consistency test)

2. **Create `tests/aliases/test_<name>.py`**
   - Module-scoped fixture loading the proxy via `AliasFinder`
   - At least one `assert proxy.arabic_key is lib.python_attr` per logical group
   - `TestTomlMeta` class checking `python_module`, `arabic_name`, entry count

3. **Create `tests/aliases/test_stdlib_B0xx_cross_consistency.py`**
   - `EARLIER_MODULES` list = all existing Arabic module names
   - Parametrized test: no overlap between new module and every earlier module

4. **Create `examples/Bxx_<name>_demo.apy`**
   - Uses `استورد <arabic_module_name>` (note: `استورد` not `استيراد`)
   - Adds file to `_EXCLUDED` in `test_phase_a_compat.py` if it has live I/O or non-determinism
   - Otherwise add a snapshot to `tests/snapshots/phase_a/expected_outputs/`

5. **Update `CHANGELOG.md`** — add entry under `## [Unreleased]`

6. **Update `ROADMAP-PHASE-B.md`** — add row in the third-party table, mark merged when done

---

## Large Implementation Packets (non-documentation)

These are self-contained engineering packets — all code, no prose writing. Each
is ready to be claimed and implemented by Claude Code in a single session.
They are ordered by impact × effort ratio (highest first).

---

### B-062 — `pytest-apy` Plugin

**What**: A proper pytest plugin so pytest discovers and runs `.apy` test files
natively — without wrapping via `ثعبان اختبر`. Users write:

```apy
# tests/test_math.apy
استورد pytest

دالة test_addition():
    تأكيد 2 + 2 == 4

دالة test_zero_division():
    مع pytest.raises(ZeroDivisionError):
        1 / 0
```

Then `pytest tests/` picks them up automatically.

**Files to create**:
- `pytest_apy/plugin.py` — register a `pytest_collect_file` hook that returns
  an `ArabyItem` for each `.apy` file; translate source before collection
- `pytest_apy/__init__.py`
- `pytest_apy/conftest.py` — auto-use fixture that installs the import hook
- `pyproject.toml` entry: `pytest11 = { "apy" = "pytest_apy.plugin" }`
- `tests/test_pytest_apy_plugin.py` — run pytest programmatically via
  `pytest.main` against temp `.apy` test files; assert pass/fail counts

**Key technical detail**: Use `pytest`'s `Module` collector. Override
`collect()` to translate the `.apy` source to Python, write to a temp `.py`
file, and delegate to the standard `Module` collector. This avoids re-inventing
test collection logic.

**Size**: M (one session). **Dependencies**: pytest ≥ 8.0, arabicpython.

---

### B-063 — Coverage Integration (`ثعبان غطاء`)

**What**: Make `coverage.py` report line coverage against the **Arabic source**
(`.apy`), not the translated Python. Currently `coverage run ثعبان file.apy`
shows Python line numbers which don't map to the `.apy` file.

**Approach**:
- Implement a `coverage.py` plugin (`CoveragePlugin`) that provides a
  `FileReporter` for `.apy` files
- The `FileReporter` reads the original `.apy` source and maps Python line
  numbers back to `.apy` line numbers using the `tokenize` source map
  (line numbers are 1:1 for most code; the pretokenizer doesn't add/remove lines)
- Register via `coverage_init` entry point

**Files to create**:
- `arabicpython/coverage_plugin.py`
- `tests/test_coverage_plugin.py` — run coverage on a temp `.apy` file,
  assert the report shows `.apy` as the source file and lines covered are correct
- `pyproject.toml` update: add `coverage` to extras; register entry point

**CLI integration**: `ثعبان غطاء` subcommand that calls
`coverage run -m arabicpython.cli <file>` then `coverage report`.

**Size**: M. **Dependencies**: coverage ≥ 7.0.

---

### B-064 — Project Scaffolder (`ثعبان مشروع`)

**What**: `ثعبان مشروع جديد <اسم>` generates a complete, ready-to-run Arabic
Python project directory:

```
<اسم>/
├── pyproject.toml          ← name, deps, scripts
├── README-ar.md            ← Arabic project readme template
├── .gitignore
├── .github/workflows/ci.yml  ← CI that runs pytest on the .apy suite
├── src/
│   └── <اسم>/
│       ├── __init__.apy    ← package init
│       └── رئيسي.apy       ← entry module
├── tests/
│   ├── conftest.py         ← installs arabicpython import hook
│   └── test_رئيسي.apy      ← sample test file
└── examples/
    └── مرحبا.apy           ← hello-world demo
```

**Files to create**:
- `arabicpython/scaffolder.py` — `scaffold_project(name, path)` function with
  Jinja2-free string templates (no extra dep)
- CLI: `ثعبان مشروع` subcommand dispatching to `scaffolder.main()`
- `tests/test_scaffolder.py` — run scaffolder in `tmp_path`, assert all files
  exist, assert the sample test passes when run with pytest

**Size**: S-M. **Dependencies**: none beyond stdlib.

---

### B-065 — REPL v2 (Tab Completion + Syntax Highlight + Multiline)

**What**: Upgrade the existing REPL (`arabicpython/repl.py`) with:

1. **Tab completion** — complete Arabic keywords and alias module names
   using `readline` (Unix) / `pyreadline3` (Windows)
2. **Multiline editing** — detect incomplete input (unclosed `إذا:`/`دالة:`/
   block starters) and show a `... ` continuation prompt, buffering lines
   until the block is complete
3. **Syntax highlight** — optionally colorize keywords, strings, and
   numbers using ANSI escape codes (no external dep; pure stdlib)
4. **History persistence** — save/restore readline history to
   `~/.apython_history`
5. **Arabic banner** — improved startup banner showing version, 40 alias
   modules available, and a tip

**Files to modify**:
- `arabicpython/repl.py` — add `_setup_readline()`, `_is_incomplete()`,
  `_highlight()`, `_banner()` helpers; restructure the input loop
- `tests/test_repl.py` — add tests for `_is_incomplete()` and `_highlight()`
  (readline itself stays untested; it's I/O)

**Size**: M. **Dependencies**: stdlib only (readline/rlcompleter on Unix;
graceful fallback on Windows).

---

### B-066 — Type Checker Shim (`ثعبان تحقق`)

**What**: `ثعبان تحقق file.apy` runs mypy on the **translated Python** output
and maps error line numbers and identifier names back to the Arabic source.

Example:
```bash
$ ثعبان تحقق my_program.apy
my_program.apy:5: خطأ: النوع "str" لا يمكن تعيينه للنوع "int"  [assignment]
```

**Approach**:
1. Translate `.apy` → Python string; write to `tmp` file
2. Run `mypy --show-column-numbers tmp_file.py` via subprocess
3. Parse mypy output; map line numbers back to `.apy` (1:1 unless
   pretokenizer adds lines — handle the offset)
4. Replace Python identifier names with Arabic names using the reverse
   dictionary lookup
5. Print translated diagnostics

**Files to create**:
- `arabicpython/typechecker.py`
- CLI: `ثعبان تحقق` subcommand
- `tests/test_typechecker.py` — translate a deliberately type-incorrect `.apy`
  file; assert the output contains Arabic identifier names and correct line numbers

**Size**: M. **Dependencies**: mypy (optional; graceful error if absent).

---

### B-067 — Arabic Error Message Expansion (Full CPython Coverage)

**What**: The current traceback translator covers 38 exception types and ~30
common error messages. This packet expands coverage to **full CPython 3.11–3.13
message corpus** — all `SyntaxError`, `TypeError`, `ValueError`,
`AttributeError`, `NameError` message templates that CPython generates.

**Scope**: ~200 additional message patterns across 5 exception classes.
Strategy: use the CPython source (`Lib/` and `Objects/`) as the reference;
every message that appears in the test suite gets a template entry.

**Files to modify**:
- `arabicpython/tracebacks.py` — add message templates to the translation table
- `arabicpython/aliases/_proxy.py` — ensure `AttributeError` from alias proxy
  is already Arabic (check existing implementation)
- `tests/test_tracebacks.py` — parametrize over every new template; assert
  the Arabic translation appears in the formatted output

**Size**: L (many templates). **Dependencies**: none.

**Arabic term reference**:
```
object      → كائن
argument    → وسيط / معامل
positional  → موضعي
keyword     → مُفتاحي
expected    → متوقع
got         → تلقّى
is not      → ليس
callable    → قابل_للاستدعاء
subscriptable → قابل_للفهرسه
iterable    → قابل_للتكرار
```

---

### B-068 — Web Playground (Online REPL)

**What**: A self-contained Flask web app that lets anyone run `.apy` code in
a browser — no install required. Serves:
- `GET /` — a single-page app with a textarea (RTL), a Run button, and an
  output area
- `POST /run` — receives `{"code": "..."}`, translates and executes in a
  sandboxed subprocess with a 5-second timeout, returns
  `{"output": "...", "error": "...", "exit_code": 0}`
- `GET /examples` — returns the list of built-in example programs

**Files to create**:
- `playground/app.py` — Flask app
- `playground/templates/index.html` — RTL-first, Arabic UI, CodeMirror with
  Arabic font, dark mode
- `playground/static/style.css`
- `playground/static/main.js`
- `playground/sandbox.py` — subprocess isolation with timeout + memory limit
- `tests/test_playground.py` — Flask test client; assert `/run` with valid
  `.apy` returns exit 0; assert timeout returns error

**Size**: L. **Dependencies**: Flask (already aliased), optional Docker for
deployment.

**Security notes**: subprocess with `timeout=5`; no file system access in
sandbox; no network in sandbox (via `--network none` if Docker, or `ulimit`).

---

### B-069 — PyPI Publication + CI/CD Template

**What**: Two deliverables in one packet:

**1. PyPI-ready package**:
- Clean up `pyproject.toml` for public release (version `0.2.0`, classifiers,
  long description from README)
- Add `MANIFEST.in` to include TOML files
- Verify `pip install apython` (from TestPyPI) installs `ثعبان` console script
  and all 40 alias TOMLs
- GitHub Actions workflow: `.github/workflows/publish.yml` — triggers on tag
  `v*`, builds wheel, publishes to PyPI via trusted publisher

**2. CI template for .apy projects**:
- `.github/workflows/apython-ci-template.yml` — a reusable workflow other
  projects can reference; runs pytest, formatter check, linter check on a
  matrix of Python 3.11/3.12/3.13 × ubuntu/windows

**Files to create/modify**:
- `pyproject.toml` — version bump, classifiers, URLs, long-description
- `MANIFEST.in`
- `.github/workflows/publish.yml`
- `.github/workflows/ci.yml` (or update existing)
- `.github/workflows/apython-ci-template.yml`
- `tests/test_package_metadata.py` — assert `importlib.metadata.metadata("apython")`
  returns correct name, version, license; assert all TOML files are included
  in the installed package

**Size**: M. **Dependencies**: build, twine (dev tools).

---

### B-070 — Pre-commit Hook + Editor Config

**What**: Makes `ثعبان نسّق` and `ثعبان راجع` usable as pre-commit hooks so
every commit is automatically formatted and linted.

**Files to create**:
- `.pre-commit-hooks.yaml` — defines two hooks: `apy-format` and `apy-lint`
- `tests/test_precommit.py` — invoke the hook entry points directly; assert
  they return 0/1 correctly

**`.pre-commit-hooks.yaml` content**:
```yaml
- id: apy-format
  name: Format .apy files
  language: python
  entry: ثعبان نسّق
  types_or: [file]
  files: \.apy$

- id: apy-lint
  name: Lint .apy files
  language: python
  entry: ثعبان راجع
  types_or: [file]
  files: \.apy$
  args: [--no-info]
```

**Size**: S. **Dependencies**: pre-commit (dev only).

---

### B-071 — Sphinx Autodoc Plugin

**What**: Lets Arabic Python projects generate HTML API documentation from
`.apy` docstrings using Sphinx.

**Approach**:
- A Sphinx extension (`arabicpython.sphinx_ext`) that:
  1. Registers `.apy` as a source suffix
  2. Translates `.apy` files to Python before Sphinx parses them
  3. Preserves Arabic docstrings verbatim (they render as RTL in HTML)
  4. Maps autodoc directives: `.. automodule::` works on `.apy` modules

**Files to create**:
- `arabicpython/sphinx_ext.py`
- `docs/sphinx-demo/` — minimal Sphinx project using the extension
- `tests/test_sphinx_ext.py` — build the demo project programmatically;
  assert the output HTML contains the Arabic docstring content

**Size**: M-L. **Dependencies**: Sphinx ≥ 7.0 (optional dep).

---

### B-072 — Jupyter `%%apy` Cell Magic

**What**: Alternative to the full Jupyter kernel — a simpler `%%apy` cell magic
that lets users mix `.apy` cells with Python cells in any kernel:

```python
%load_ext arabicpython.magic
```

```apy
%%apy
دالة فيبوناتشي(ن):
    إذا ن <= 1:
        إرجاع ن
    إرجاع فيبوناتشي(ن-1) + فيبوناتشي(ن-2)

اطبع(فيبوناتشي(10))
```

**Files to create**:
- `arabicpython/magic.py` — `ArabicPythonMagic` class extending `Magics`;
  registers `%%apy` line+cell magic; translates and `exec`s in the kernel
  namespace
- `tests/test_magic.py` — mock IPython shell; assert translation is called
  and result is executed

**Size**: S. **Dependencies**: IPython (optional; graceful if absent).

---

### B-073 — ar-v3 Dialect

**What**: Third generation dictionary with three improvements over ar-v2:

1. **Extended built-in coverage** — translate all 69 Python built-ins that
   ar-v2 leaves in English: `zip`, `enumerate`, `map`, `filter`, `any`, `all`,
   `hasattr`, `getattr`, `setattr`, `delattr`, `vars`, `dir`, `repr`,
   `isinstance`, `issubclass`, `super`, `property`, `staticmethod`,
   `classmethod`, `open`, `format`, `hex`, `oct`, `bin`, `chr`, `ord`, etc.

2. **Operator keywords** — `in`, `not in`, `is`, `is not` get Arabic
   alternatives: `في`, `ليس_في`, `يكون`, `ليس_يكون`

3. **Dunder method aliases** — common dunder methods get Arabic names:
   `__init__` → `__مُهيِّئ__`, `__str__` → `__نص__`, `__len__` → `__طول__`,
   `__repr__` → `__تمثيل__`, etc. (opt-in via `# arabicpython: dunders=on`)

**Files to create**:
- `dictionaries/ar-v3.md` — full keyword + built-in table
- `arabicpython/aliases/_builtins_ar_v3.py` — built-in name injection at
  import time for the new aliases
- `tests/test_dialect_v3.py` — parametrized over every new entry

**Key collision checks**: `في` already used as `in` keyword; `map` / `filter`
get Arabic names; check against all 40 TOMLs.

**Size**: L. **Dependencies**: none.

---

### B-074 — VSCode Debugger Integration

**What**: Extend the VSCode extension (B-053) to support **step-through
debugging** of `.apy` files using the Debug Adapter Protocol (DAP).

**Approach**:
- Add a `debugpy` launch configuration to `package.json`
- The debug adapter translates `.apy` → Python, writes to a temp file,
  launches `debugpy` on the temp file, but intercepts `stackTrace` responses
  to show Arabic source file names and lines
- Breakpoints set in `.apy` files are mapped to the equivalent Python temp
  file line numbers

**Files to create/modify**:
- `editors/vscode/debugAdapter.js` — DAP proxy that wraps debugpy
- `editors/vscode/extension.js` — add `registerDebugAdapterDescriptorFactory`
- `editors/vscode/package.json` — add `debuggers` contribution
- `tests/test_vscode_debug_config.py` — static test: assert `package.json`
  has correct `debuggers` entry with `.apy` file patterns

**Size**: L (DAP is complex). **Dependencies**: debugpy.

---

### B-075 — Interactive Tutorial in the REPL

**What**: `ثعبان تعلّم` launches a guided, interactive tutorial that runs
inside the REPL — like Python's `python -m turtle` demo but for learning
Arabic Python step by step.

```
$ ثعبان تعلّم
╔══════════════════════════════════════╗
║   مرحباً في لغة الثعبان التفاعلية   ║
╚══════════════════════════════════════╝

الدرس 1 من 10: مرحبا بالعالم
══════════════════════════════
اكتب:  اطبع("مرحبا، يا عالم")
[اضغط Enter للمتابعة أو اكتب الكود]
>>>
```

10 lessons progressing from hello-world to importing alias modules.
Each lesson shows the Arabic code, explains it in Arabic prose, then asks
the user to type it themselves and verifies the output.

**Files to create**:
- `arabicpython/tutorial.py` — `TutorialRunner` with 10 lesson dicts
  (prompt, expected_output, hint, explanation_ar)
- CLI: `ثعبان تعلّم` subcommand
- `tests/test_tutorial.py` — mock stdin/stdout; run each lesson
  programmatically; assert correct lessons pass and wrong input gets a hint

**Size**: M. **Dependencies**: none beyond stdlib.

---

### B-076 — `ثعبان ترجم` Bidirectional Translator (Show Mode)

**What**: A tool that shows the translation side-by-side — useful for
learners and for debugging:

```bash
$ ثعبان ترجم my_program.apy
```

Output:
```
السطر ١  │  دالة مرحبا(اسم):          │  def مرحبا(اسم):
السطر ٢  │      اطبع(f"مرحبا {اسم}")  │      print(f"مرحبا {اسم}")
السطر ٣  │  مرحبا("عالم")              │  مرحبا("عالم")
```

Also: `ثعبان ترجم --reverse` takes Python and shows what Arabic keywords map
to it (useful for contributors writing new demos).

**Files to create**:
- `arabicpython/show_translation.py`
- CLI: `ثعبان ترجم` subcommand
- `tests/test_show_translation.py`

**Size**: S. **Dependencies**: none.

---

### Summary table

| Packet | Name | Type | Size | Depends on |
|--------|------|------|------|------------|
| B-062 | pytest-apy plugin | tooling | M | pytest ≥ 8, arabicpython |
| B-063 | Coverage integration | tooling | M | coverage ≥ 7 |
| B-064 | Project scaffolder | tooling | S-M | stdlib only |
| B-065 | REPL v2 | tooling | M | readline/pyreadline3 |
| B-066 | Type checker shim | tooling | M | mypy (optional) |
| B-067 | Error message expansion | core | L | none |
| B-068 | Web playground | app | L | Flask |
| B-069 | PyPI + CI/CD | infra | M | build, twine |
| B-070 | Pre-commit hooks | tooling | S | pre-commit |
| B-071 | Sphinx autodoc | tooling | M-L | Sphinx ≥ 7 |
| B-072 | Jupyter `%%apy` magic | tooling | S | IPython |
| B-073 | ar-v3 dialect | core | L | none |
| B-074 | VSCode debugger | editor | L | debugpy, B-053 |
| B-075 | Interactive tutorial REPL | app | M | none |
| B-076 | Bidirectional translator | tooling | S | none |
| B-057–B-059 | seaborn, scipy, aiohttp | aliases | done | — |
| B-0xx | All 195 library packets | aliases | S each | arabicpython |

**Recommended order for maximum value per session**:
1. B-076 (translator show mode) — S, high visibility, easy win
2. B-072 (Jupyter magic) — S, complements existing kernel
3. B-070 (pre-commit) — S, makes formatter/linter production-ready
4. B-064 (scaffolder) — S-M, directly useful for new Arabic Python projects
5. B-062 (pytest plugin) — M, eliminates the test-runner workaround
6. B-065 (REPL v2) — M, biggest UX improvement to the interactive mode
7. B-067 (error messages) — L, full Arabic error coverage
8. B-073 (ar-v3) — L, biggest language improvement
9. B-068 (playground) — L, community/education impact
10. B-069 (PyPI) — M, needed before any public launch

## Contact / questions

Open a GitHub issue tagged `packet:B-060` or `packet:B-061`. Tag the planner
(`@GalaxyRuler`) for any question about Arabic terminology choices or spec
interpretation.
