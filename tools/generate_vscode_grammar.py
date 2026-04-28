#!/usr/bin/env python3
# tools/generate_vscode_grammar.py
# B-053: Generate the VSCode TextMate grammar for apython (.apy files).
#
# Usage:
#   python tools/generate_vscode_grammar.py [dialect] [--output PATH]
#
# dialect: ar-v2 (default) — Arabic keyword set

from __future__ import annotations
import argparse
import json
from pathlib import Path

KEYWORDS_AR_V2 = [
    "إذا", "وإلا", "إلا_إذا", "إلا",
    "بينما", "لكل", "في",
    "دالة", "صنف", "إرجاع", "ناتج",
    "حاول", "أخيرًا", "إثارة", "مع", "كـ",
    "استيراد", "من",
    "و", "أو", "ليس",
    "مرر", "تابع", "اكسر", "احذف", "عالمي", "غير_محلي",
    "لامدا", "تأكيد", "منتج",
    "صحيح", "خطأ", "لا_شيء",
]

BUILTIN_FUNCTIONS_AR = [
    "اطبع", "مدخل", "نطاق", "طول", "نوع", "قائمة", "مجموعة", "قاموس",
    "صحيح_أم_خطأ", "رقم_صحيح", "رقم_عشري", "نص", "مجموعة_مرتبة",
    "مرتب", "معكوس", "مجموع", "أقصى", "أدنى", "مطلق", "تعداد",
    "مضغوط", "خريطة", "فلتر", "مُقيَّم", "تنفيذ", "مساعدة",
    "معرف", "هاش", "موجود_في", "استدعاء",
    "print", "input", "range", "len", "type", "list", "set", "dict",
    "bool", "int", "float", "str", "sorted", "reversed", "sum",
    "max", "min", "abs", "enumerate", "zip", "map", "filter",
    "eval", "exec", "help", "id", "hash", "callable",
]

BUILTIN_TYPES_AR = [
    "صحيح_أم_خطأ", "رقم_صحيح", "رقم_عشري", "نص", "قائمة", "مجموعة",
    "قاموس", "مجموعة_مرتبة", "شريحة", "نوع", "كائن",
    "bool", "int", "float", "str", "list", "set", "dict",
    "tuple", "slice", "type", "object", "bytes", "bytearray",
]

BUILTIN_EXCEPTIONS_AR = [
    "خطأ_عام", "خطأ_قيمة", "خطأ_نوع", "خطأ_اسم", "خطأ_مفتاح",
    "خطأ_فهرس", "خطأ_نطاق", "خطأ_إيقاف", "خطأ_ذاكرة",
    "خطأ_تكرار", "خطأ_إدخال_إخراج", "خطأ_توقف_تكرار",
    "Exception", "ValueError", "TypeError", "NameError", "KeyError",
    "IndexError", "AttributeError", "RuntimeError", "StopIteration",
    "OSError", "IOError", "MemoryError", "RecursionError",
    "NotImplementedError", "KeyboardInterrupt", "SystemExit",
    "BaseException", "ImportError", "ModuleNotFoundError",
    "ZeroDivisionError", "OverflowError", "FileNotFoundError",
    "PermissionError",
]


def _alt(*words: str) -> str:
    return "|".join(sorted(set(words), key=len, reverse=True))


def build_grammar(dialect: str = "ar-v2") -> dict:
    if dialect not in ("ar-v2",):
        raise ValueError(f"Unknown dialect: {dialect!r}")

    keywords = KEYWORDS_AR_V2
    kw_alt = _alt(*keywords)
    kw_match = rf"(?<![ء-يa-zA-Z_٠-٩0-9])({kw_alt})(?![ء-يa-zA-Z_٠-٩0-9])"

    bf_alt = _alt(*BUILTIN_FUNCTIONS_AR)
    bf_match = rf"(?<![ء-يa-zA-Z_٠-٩0-9])({bf_alt})(?![ء-يa-zA-Z_٠-٩0-9])"

    bt_alt = _alt(*BUILTIN_TYPES_AR)
    bt_match = rf"(?<![ء-يa-zA-Z_٠-٩0-9])({bt_alt})(?![ء-يa-zA-Z_٠-٩0-9])"

    be_alt = _alt(*BUILTIN_EXCEPTIONS_AR)
    be_match = rf"(?<![ء-يa-zA-Z_٠-٩0-9])({be_alt})(?![ء-يa-zA-Z_٠-٩0-9])"

    return {
        "$schema": "https://raw.githubusercontent.com/martinring/tmlanguage/master/tmlanguage.json",
        "name": "apython",
        "scopeName": "source.apy",
        "fileTypes": ["apy"],
        "patterns": [
            {"include": "#comment"},
            {"include": "#string-triple-double"},
            {"include": "#string-triple-single"},
            {"include": "#string-double"},
            {"include": "#string-single"},
            {"include": "#builtin-exception"},
            {"include": "#builtin-type"},
            {"include": "#builtin-function"},
            {"include": "#keyword"},
            {"include": "#literal"},
            {"include": "#number"},
            {"include": "#operator"},
        ],
        "repository": {
            "comment": {
                "name": "comment.line.number-sign.apy",
                "match": "#.*$",
            },
            "keyword": {
                "name": "keyword.control.apy",
                "match": kw_match,
            },
            "literal": {
                "name": "constant.language.apy",
                "match": r"(?<![ء-يa-zA-Z_٠-٩0-9])(صحيح|خطأ|لا_شيء|True|False|None)(?![ء-يa-zA-Z_٠-٩0-9])",
            },
            "builtin-function": {
                "name": "support.function.builtin.apy",
                "match": bf_match,
            },
            "builtin-type": {
                "name": "support.type.apy",
                "match": bt_match,
            },
            "builtin-exception": {
                "name": "support.class.exception.apy",
                "match": be_match,
            },
            "number": {
                "name": "constant.numeric.apy",
                "match": r"(?<!\w)([٠-٩]+\.?[٠-٩]*|[0-9]+\.?[0-9]*([eE][+-]?[0-9]+)?|0[xX][0-9a-fA-F]+|0[bB][01]+|0[oO][0-7]+)(?!\w)",
            },
            "operator": {
                "name": "keyword.operator.apy",
                "match": r"[+\-*/%&|^~<>=!@]+|//|<<|>>|\*\*",
            },
            "string-triple-double": {
                "name": "string.quoted.triple.double.apy",
                "begin": '"""',
                "end": '"""',
                "patterns": [{"include": "#string-escape"}],
            },
            "string-triple-single": {
                "name": "string.quoted.triple.single.apy",
                "begin": "'''",
                "end": "'''",
                "patterns": [{"include": "#string-escape"}],
            },
            "string-double": {
                "name": "string.quoted.double.apy",
                "begin": '"',
                "end": '"',
                "patterns": [{"include": "#string-escape"}],
            },
            "string-single": {
                "name": "string.quoted.single.apy",
                "begin": "'",
                "end": "'",
                "patterns": [{"include": "#string-escape"}],
            },
            "string-escape": {
                "name": "constant.character.escape.apy",
                "match": r"\.",
            },
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate apy.tmLanguage.json")
    parser.add_argument("dialect", nargs="?", default="ar-v2")
    parser.add_argument("--output", "-o", type=Path, default=None)
    args = parser.parse_args()

    grammar = build_grammar(args.dialect)
    if args.output is None:
        out = Path(__file__).parent.parent / "editors" / "vscode" / "syntaxes" / "apy.tmLanguage.json"
    else:
        out = args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(grammar, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Written: {out}")


if __name__ == "__main__":
    main()
