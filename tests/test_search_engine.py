import sys
import os
import subprocess
import pytest

import arabicpython

arabicpython.install()

import apps.search_engine.normalizer as normalizer
import apps.search_engine.indexer as indexer
import apps.search_engine.ranker as ranker

DOCS_DIR = "apps/search_engine/docs"


def test_normalizer_strips_harakat():
    assert normalizer.طبع("الكِتَابُ") == "الكتاب"


def test_normalizer_folds_hamza():
    assert normalizer.طبع("إذا") == "اذا"


def test_normalizer_folds_ta_marbuta():
    assert normalizer.طبع("قيمة") == "قيمه"


def test_index_loads_six_documents():
    idx = indexer.فهرس(DOCS_DIR)
    assert len(idx) == 6


def test_index_contains_expected_term():
    idx = indexer.فهرس(DOCS_DIR)
    normalized_term = normalizer.طبع("الجبر")
    assert normalized_term in idx.الفهرس_المعكوس


def test_search_returns_results():
    idx = indexer.فهرس(DOCS_DIR)
    rank = ranker.باحث(idx)
    results = rank.تنفيذ_البحث("الجبر")
    assert len(results) > 0

    first_doc_id = results[0][0]
    assert idx.الوثائق[first_doc_id]["الاسم"] == "الخوارزمي.txt"


def test_search_ranking_order():
    idx = indexer.فهرس(DOCS_DIR)
    rank = ranker.باحث(idx)
    results = rank.تنفيذ_البحث("الطب")
    first_doc_id = results[0][0]
    assert idx.الوثائق[first_doc_id]["الاسم"] == "ابن_سينا.txt"


def test_search_no_results():
    idx = indexer.فهرس(DOCS_DIR)
    rank = ranker.باحث(idx)
    results = rank.تنفيذ_البحث("بيتزا برغر كولا")
    assert len(results) == 0


def test_snippet_contains_brackets():
    idx = indexer.فهرس(DOCS_DIR)
    rank = ranker.باحث(idx)
    results = rank.تنفيذ_البحث("الرياضيات")
    snippet = results[0][2]
    assert "【" in snippet
    assert "】" in snippet


def test_arabic_indic_in_output():
    result = subprocess.run(
        [sys.executable, "-m", "arabicpython.cli", "apps/search_engine/cli.apy", "الجبر"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert "١" in result.stdout
