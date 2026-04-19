import sys

import pytest

from arabicpython.dialect import load_dialect
from arabicpython.translate import translate


# Identity on pure ASCII Python (5)
def test_empty_string():
    res = translate("")
    assert res in ("", "\n")
    assert compile(res, "<test>", "exec") is not None


def test_pure_ascii_passthrough():
    src = "x = 1\nprint(x)\n"
    assert translate(src) == src


def test_ascii_function_def():
    src = "def foo(x):\n    return x + 1\n"
    assert translate(src) == src


def test_ascii_class_def():
    src = "class C:\n    def m(self):\n        pass\n"
    assert translate(src) == src


def test_ascii_with_comment():
    src = "# hello\nx = 1\n"
    assert translate(src) == src


# Single keyword translation (10)
def test_translate_if():
    res = translate("إذا x: pass\n")
    assert "if " in res
    compile(res, "<test>", "exec")


def test_translate_else():
    res = translate("إذا x: pass\nوإلا: pass\n")
    assert "else:" in res
    compile(res, "<test>", "exec")


def test_translate_while():
    res = translate("طالما x: pass\n")
    assert "while " in res
    compile(res, "<test>", "exec")


def test_translate_for():
    res = translate("لكل x in y: pass\n")
    assert "for " in res
    compile(res, "<test>", "exec")


def test_translate_def():
    res = translate("دالة foo(): pass\n")
    assert "def " in res
    compile(res, "<test>", "exec")


def test_translate_class():
    res = translate("صنف C: pass\n")
    assert "class " in res
    compile(res, "<test>", "exec")


def test_translate_return():
    res = translate("def foo():\n    ارجع 1\n")
    assert "return " in res
    compile(res, "<test>", "exec")


def test_translate_pass():
    res = translate("def foo():\n    مرر\n")
    assert "pass" in res
    compile(res, "<test>", "exec")


def test_translate_True_literal():
    res = translate("x = صحيح\n")
    assert "True" in res
    compile(res, "<test>", "exec")


def test_translate_None_literal():
    res = translate("x = لاشيء\n")
    assert "None" in res
    compile(res, "<test>", "exec")


# Built-in function translation (5)
def test_translate_print():
    res = translate("اطبع(1)\n")
    assert "print" in res
    compile(res, "<test>", "exec")


def test_translate_len():
    res = translate("طول([1])\n")
    assert "len" in res
    compile(res, "<test>", "exec")


def test_translate_range():
    res = translate("نطاق(5)\n")
    assert "range" in res
    compile(res, "<test>", "exec")


def test_translate_input():
    res = translate("ادخل()\n")
    assert "input" in res
    compile(res, "<test>", "exec")


def test_translate_isinstance():
    res = translate("من_نوع(1, int)\n")
    assert "isinstance" in res
    compile(res, "<test>", "exec")


# Built-in type translation (3)
def test_translate_list():
    res = translate("قائمة()\n")
    assert "list" in res
    compile(res, "<test>", "exec")


def test_translate_dict():
    res = translate("قاموس()\n")
    assert "dict" in res
    compile(res, "<test>", "exec")


def test_translate_str():
    res = translate("نص()\n")
    assert "str" in res
    compile(res, "<test>", "exec")


# Exception translation (3)
def test_translate_exception_keyword():
    res = translate("try: pass\nاستثناء KeyError: pass\n")
    assert "except " in res
    compile(res, "<test>", "exec")


def test_translate_exception_class():
    res = translate("raise استثناء_عام()\n")
    assert "Exception" in res
    compile(res, "<test>", "exec")


def test_translate_value_error():
    res = translate("raise خطا_قيمة()\n")
    assert "ValueError" in res
    compile(res, "<test>", "exec")


# Method/attribute translation (5)
def test_translate_str_method():
    res = translate("s.كبير()\n")
    assert ".upper" in res
    compile(res, "<test>", "exec")


def test_translate_list_method():
    res = translate("lst.اضف(x)\n")
    assert ".append" in res
    compile(res, "<test>", "exec")


def test_translate_dict_method():
    res = translate("d.اجلب(k)\n")
    assert ".get" in res
    compile(res, "<test>", "exec")


def test_translate_chained_attributes():
    res = translate("a.b.كبير()\n")
    assert ".upper" in res
    assert "a.b" in res
    compile(res, "<test>", "exec")


def test_attribute_does_not_match_name():
    # اطبع maps to print in names, but it shouldn't translate when accessed as attribute
    res = translate("obj.اطبع()\n")
    assert ".اطبع" in res
    compile(res, "<test>", "exec")


# Normalization in translation (3)
@pytest.mark.skipif(
    sys.version_info < (3, 12),
    reason="Python 3.11 tokenizer does not accept Arabic harakat in identifiers (fixed in 3.12)",
)
def test_translate_with_harakat():
    res = translate("إِذا x: pass\n")
    assert "if " in res
    compile(res, "<test>", "exec")


def test_translate_hamza_variant():
    res = translate("اذا x: pass\n")
    assert "if " in res
    compile(res, "<test>", "exec")


@pytest.mark.skipif(
    sys.version_info < (3, 12),
    reason="Python 3.11 tokenizer does not accept Arabic harakat in identifiers (fixed in 3.12)",
)
def test_unknown_identifier_normalized():
    # كَلب is normalized to كلب
    res = translate("كَلب = 1\nكلب = 2\n")
    assert "كلب = 1" in res
    assert "كلب = 2" in res
    compile(res, "<test>", "exec")


# Pretokenize integration (3)
def test_translate_with_arabic_digits():
    res = translate("x = ٥\n")
    assert "5" in res
    compile(res, "<test>", "exec")


def test_translate_with_arabic_punct():
    res = translate("foo(a، b)\n")
    assert "foo(a, b)" in res
    compile(res, "<test>", "exec")


def test_translate_combined_keyword_and_digit():
    res = translate("إذا x > ٥: pass\n")
    assert "if " in res
    assert "5" in res
    compile(res, "<test>", "exec")


# Unknown identifiers preserved (3)
def test_unknown_arabic_name_preserved():
    res = translate("كلب = 1\n")
    assert "كلب = 1" in res
    compile(res, "<test>", "exec")


def test_user_function_def():
    res = translate("def دالتي(): pass\n")
    assert "دالتي" in res
    compile(res, "<test>", "exec")


def test_unknown_attribute_preserved():
    res = translate("obj.صفتي\n")
    assert "obj.صفتي" in res
    compile(res, "<test>", "exec")


# String preservation (3)
def test_arabic_keyword_inside_string_not_translated():
    res = translate('x = "إذا"\n')
    assert '"إذا"' in res
    compile(res, "<test>", "exec")


def test_arabic_method_inside_string_not_translated():
    res = translate('x = "obj.قراءة()"\n')
    assert '"obj.قراءة()"' in res
    compile(res, "<test>", "exec")


def test_triple_string_preserved():
    res = translate("'''multi\\nline\\nإذا'''\n")
    assert "إذا" in res
    compile(res, "<test>", "exec")


# Comment preservation (2)
def test_arabic_keyword_in_comment_not_translated():
    res = translate("# إذا x: pass\nx = 1\n")
    assert "# إذا x: pass" in res
    compile(res, "<test>", "exec")


def test_inline_comment_with_arabic_keyword():
    res = translate("x = 1  # إذا\n")
    assert "# إذا" in res
    compile(res, "<test>", "exec")


# Combined real-world programs (5)
def test_program_factorial():
    src = """دالة fact(n):
    إذا n == 0:
        ارجع 1
    وإلا:
        ارجع n * fact(n - 1)
"""
    res = translate(src)
    assert "def " in res
    assert "if " in res
    assert "else:" in res
    assert "return " in res
    code = compile(res, "<test>", "exec")
    ns = {}
    exec(code, ns)
    assert ns["fact"](5) == 120


def test_program_fizzbuzz(capsys):
    src = """دالة fizzbuzz(n):
    لكل i in نطاق(1, n + 1):
        إذا i % 15 == 0:
            اطبع("FizzBuzz")
        وإلا_إذا i % 3 == 0:
            اطبع("Fizz")
        وإلا_إذا i % 5 == 0:
            اطبع("Buzz")
        وإلا:
            اطبع(i)

fizzbuzz(5)
"""
    res = translate(src)
    code = compile(res, "<test>", "exec")
    ns = {}
    exec(code, ns)
    captured = capsys.readouterr()
    assert captured.out == "1\n2\nFizz\n4\nBuzz\n"


def test_program_class_with_method():
    src = """صنف MyClass:
    دالة __init__(self, val):
        self.val = val
    دالة get_val(self):
        ارجع self.val

obj = MyClass(42)
res = obj.get_val()
"""
    res = translate(src)
    code = compile(res, "<test>", "exec")
    ns = {}
    exec(code, ns)
    assert ns["res"] == 42


def test_program_try_except():
    src = """res = لاشيء
try:
    raise خطا_قيمة("test")
استثناء خطا_قيمة as e:
    res = e.args[0]
"""
    res = translate(src)
    code = compile(res, "<test>", "exec")
    ns = {}
    exec(code, ns)
    assert ns["res"] == "test"


def test_program_for_loop_with_range():
    src = """total = 0
لكل i in نطاق(5):
    total += i
"""
    res = translate(src)
    code = compile(res, "<test>", "exec")
    ns = {}
    exec(code, ns)
    assert ns["total"] == 10


# F-string handling (5)
def test_fstring_text_preserved():
    src = 'f"hello {x}"\n'
    res = translate(src)
    assert 'f"hello {x}"' in res


@pytest.mark.skipif(
    sys.version_info < (3, 12), reason="F-string interior tokens only available in 3.12+"
)
def test_fstring_arabic_expr_312_plus_translates():
    src = 'f"{اطبع}"\n'
    res = translate(src)
    assert "print" in res


def test_translate_fstring_arabic_expr_on_311():
    # Renamed/new; no skipif. Tests that f-strings translate on any version.
    res = translate('x = 1\nاطبع(f"{x}")\n')
    assert "print" in res
    compile(res, "<test>", "exec")


def test_translate_fstring_arabic_identifier_normalized_on_311():
    # فاكهة = 1
    # print(f"{فاكهة}")
    # both should normalize to فاكهه
    src = 'فاكهة = 1\nاطبع(f"{فاكهة}")\n'
    res = translate(src)
    assert "فاكهه = 1" in res
    assert "{فاكهه}" in res
    ns = {}
    exec(compile(res, "<test>", "exec"), ns)


def test_translate_fstring_subscript_regression_packet_0010(capsys):
    # The exact program from examples/05_data_structures.apy
    src = """# القوائم والقواميس
الفواكه = ["تفاح", "موز", "برتقال"]
الأسعار = {"تفاح": 3, "موز": 2, "برتقال": 4}

لكل فاكهة في الفواكه:
    اطبع(f"{فاكهة}: {الأسعار[فاكهة]} ريال")
"""
    res = translate(src)
    exec(compile(res, "<test>", "exec"), {})
    out, _ = capsys.readouterr()
    expected = "تفاح: 3 ريال\nموز: 2 ريال\nبرتقال: 4 ريال\n"
    assert out == expected


# Whitespace and structure preservation (3)
def test_indentation_preserved():
    src = "def foo():\n    pass\n"
    res = translate(src)
    assert "    pass" in res


def test_blank_lines_preserved():
    src = "x = 1\n\ny = 2\n"
    res = translate(src)
    assert "\n\n" in res


def test_line_count_within_one():
    src = "\n".join(f"x_{i} = {i}" for i in range(20)) + "\n"
    res = translate(src)
    assert abs(res.count("\n") - src.count("\n")) <= 1


# Error propagation (2)
def test_bidi_error_propagates():
    with pytest.raises(SyntaxError) as exc:
        translate("x = \u202e\n")
    assert "bidi control" in str(exc.value)


def test_unclosed_string_raises_syntax_error():
    with pytest.raises(SyntaxError):
        translate('x = "unclosed\n')


# Custom dialect parameter (2)
def test_custom_dialect_used(tmp_path):
    fixture = tmp_path / "custom.md"
    fixture.write_text(
        "## 1. Control-flow keywords\n"
        "| `if` | customif | — | | \n"
        + "".join(f"| `dummy{i}` | دممي{i} | — | | \n" for i in range(150)),
        encoding="utf-8",
    )
    d = load_dialect("custom", path=fixture)
    res = translate("customif x: pass\n", dialect=d)
    assert "if " in res


def test_default_dialect_is_ar_v1():
    # It defaults to ar-v1, which we can test by translating something specific
    res = translate("إذا x: pass\n")
    assert "if " in res
