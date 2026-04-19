"""Unit tests for Python 3.11 f-string interior rewriter."""

import sys

import pytest

from arabicpython._fstring_311 import rewrite_fstring_literal
from arabicpython.dialect import load_dialect
from arabicpython.normalize import normalize_identifier


@pytest.fixture(scope="module")
def dialect():
    return load_dialect("ar-v1")


# All tests in this file are for the 3.11 code path specifically.
# On 3.12+, PEP 701 tokens make this helper unnecessary.
pytestmark = pytest.mark.skipif(
    sys.version_info >= (3, 12), reason="3.11-specific rewriter path not used on 3.12+"
)


def test_non_fstring_passes_through(dialect):
    assert rewrite_fstring_literal('"hello"', dialect) == '"hello"'
    assert rewrite_fstring_literal("'x'", dialect) == "'x'"
    assert rewrite_fstring_literal('r"raw"', dialect) == 'r"raw"'
    assert rewrite_fstring_literal('"""triple"""', dialect) == '"""triple"""'


def test_fstring_no_expressions_passes_through(dialect):
    assert rewrite_fstring_literal('f"no expressions here"', dialect) == 'f"no expressions here"'


def test_fstring_simple_keyword_rewrite(dialect):
    # اطبع maps to print
    res = rewrite_fstring_literal('f"{اطبع}"', dialect)
    assert "{print}" in res


def test_fstring_normalizes_ta_marbuta(dialect):
    # فاكهة -> فاكهه
    res = rewrite_fstring_literal('f"{فاكهة}"', dialect)
    assert "فاكهه" in res


def test_fstring_subscript_with_arabic_names(dialect):
    # f"{الأسعار[فاكهة]}"
    res = rewrite_fstring_literal('f"{الأسعار[فاكهة]}"', dialect)
    norm_prices = normalize_identifier("الأسعار")
    norm_fruit = normalize_identifier("فاكهة")
    assert f"{{{norm_prices}[{norm_fruit}]}}" in res


def test_fstring_doubled_braces_are_literal(dialect):
    assert rewrite_fstring_literal('f"{{اطبع}}"', dialect) == 'f"{{اطبع}}"'


def test_fstring_mixed_literal_and_expr(dialect):
    res = rewrite_fstring_literal('f"before {فاكهة} after"', dialect)
    assert res.startswith('f"before ')
    assert res.endswith(' after"')
    assert "فاكهه" in res


def test_fstring_conversion_marker_preserved(dialect):
    res = rewrite_fstring_literal('f"{اطبع!r}"', dialect)
    assert "{print!r}" in res


def test_fstring_format_spec_preserved(dialect):
    res = rewrite_fstring_literal('f"{x:>10}"', dialect)
    assert "{x:>10}" in res  # x is ASCII, so normalized to x


def test_fstring_nested_format_spec_with_expression(dialect):
    # عرض maps to width (if in dict) or just normalized عرض -> عرضه
    res = rewrite_fstring_literal('f"{x:>{عرض}}"', dialect)
    norm_width = normalize_identifier("عرض")
    assert f"{{x:>{{{norm_width}}}}}" in res


def test_fstring_self_documenting_equals(dialect):
    res = rewrite_fstring_literal('f"{فاكهة=}"', dialect)
    assert "{فاكهه=}" in res


def test_fstring_nested_expression_with_dict(dialect):
    # 3.11 f-strings can have dicts if they use different quotes
    # Must have space to not be seen as {{ literal escape
    literal = "f\"{ {'a': 1}['a'] }\""
    res = rewrite_fstring_literal(literal, dialect)
    assert "{'a':1}['a']" in res.replace(" ", "")


def test_fstring_triple_quoted(dialect):
    literal = "f'''line1\\n{فاكهة}\\nline2'''"
    res = rewrite_fstring_literal(literal, dialect)
    assert res.startswith("f'''")
    assert "فاكهه" in res


def test_fstring_raw_prefix_rf(dialect):
    literal = 'rf"{فاكهة}"'
    res = rewrite_fstring_literal(literal, dialect)
    assert res.startswith('rf"')
    assert "فاكهه" in res


def test_fstring_attribute_access_inside(dialect):
    # اضف is in dialect.attributes for append
    literal = 'f"{obj.اضف}"'
    res = rewrite_fstring_literal(literal, dialect)
    assert "{obj.append}" in res


def test_fstring_unbalanced_raises(dialect):
    with pytest.raises(SyntaxError, match="f-string"):
        rewrite_fstring_literal('f"{x"', dialect)


def test_fstring_single_closing_brace_raises(dialect):
    with pytest.raises(SyntaxError, match="single"):
        rewrite_fstring_literal('f"oops }"', dialect)


def test_fstring_strict_mode_skips_fold(dialect):
    # فاكهة normally folds to فاكهه. In strict mode it should stay فاكهة (after NFKC)
    res = rewrite_fstring_literal('f"{فاكهة}"', dialect, strict=True)
    assert "فاكهة" in res
    assert "فاكهه" not in res


def test_non_fstring_with_braces_untouched(dialect):
    assert rewrite_fstring_literal('"{اطبع}"', dialect) == '"{اطبع}"'


def test_byte_preservation_outside_expressions(dialect):
    literal = 'f"  spaces\\ttab {x}"'
    res = rewrite_fstring_literal(literal, dialect)
    # The literal part '  spaces\\ttab ' should be preserved
    assert "  spaces\\ttab " in res
