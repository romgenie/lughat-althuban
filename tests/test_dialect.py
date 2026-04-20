import keyword
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from arabicpython.dialect import DialectError, load_dialect
from arabicpython.normalize import normalize_identifier


# Group: Load and shape
def test_load_ar_v1_succeeds():
    d = load_dialect("ar-v1")
    assert d is not None


def test_dialect_is_frozen():
    d = load_dialect("ar-v1")
    with pytest.raises(FrozenInstanceError):
        d.name = "ar-v2"


def test_mappings_are_read_only():
    d = load_dialect("ar-v1")
    with pytest.raises(TypeError):
        d.names["new"] = "x"


def test_name_attribute():
    d = load_dialect("ar-v1")
    assert d.name == "ar-v1"


# Group: Entry counts
def test_total_entry_count():
    d = load_dialect("ar-v1")
    assert len(d.names) + len(d.attributes) >= 187


def test_attributes_nonempty():
    d = load_dialect("ar-v1")
    assert len(d.attributes) >= 42


def test_names_nonempty():
    d = load_dialect("ar-v1")
    assert len(d.names) >= 120


# Group: Forward lookup (names map)
def test_keyword_if():
    d = load_dialect("ar-v1")
    assert d.names[normalize_identifier("إذا")] == "if"


def test_keyword_def():
    d = load_dialect("ar-v1")
    assert d.names[normalize_identifier("دالة")] == "def"


def test_keyword_class():
    d = load_dialect("ar-v1")
    assert d.names[normalize_identifier("صنف")] == "class"


def test_literal_true():
    d = load_dialect("ar-v1")
    assert d.names[normalize_identifier("صحيح")] == "True"


def test_type_str():
    d = load_dialect("ar-v1")
    assert d.names[normalize_identifier("نص")] == "str"


def test_function_print():
    d = load_dialect("ar-v1")
    assert d.names[normalize_identifier("اطبع")] == "print"


def test_exception_value_error():
    d = load_dialect("ar-v1")
    assert d.names[normalize_identifier("خطا_قيمة")] == "ValueError"


def test_filter_resolved():
    d = load_dialect("ar-v1")
    assert d.names[normalize_identifier("فلتر")] == "filter"


# Group: Forward lookup (attributes map)
def test_method_append():
    d = load_dialect("ar-v1")
    assert d.attributes[normalize_identifier("اضف")] == "append"


def test_method_keys():
    d = load_dialect("ar-v1")
    assert d.attributes[normalize_identifier("مفاتيح")] == "keys"


def test_method_encode_resolved():
    d = load_dialect("ar-v1")
    assert d.attributes[normalize_identifier("رمز_بايتات")] == "encode"


def test_method_values_resolved():
    d = load_dialect("ar-v1")
    assert d.attributes[normalize_identifier("قيم_القاموس")] == "values"


# Group: Normalization is applied
def test_lookup_with_harakat():
    d = load_dialect("ar-v1")
    assert d.names[normalize_identifier("إِذَا")] == "if"


def test_lookup_with_tatweel():
    d = load_dialect("ar-v1")
    assert d.names[normalize_identifier("إـذا")] == "if"


def test_lookup_via_folded_hamza():
    d = load_dialect("ar-v1")
    assert d.names[normalize_identifier("اذا")] == "if"


# Group: Reverse lookup
def test_reverse_name_keyword():
    d = load_dialect("ar-v1")
    assert d.reverse_names["if"] == "إذا"


def test_reverse_attribute_method():
    d = load_dialect("ar-v1")
    assert d.reverse_attributes["append"] == "اضف"


def test_reverse_preserves_hamza():
    d = load_dialect("ar-v1")
    assert d.reverse_names["print"] == "اطبع"


# Group: Categories
def test_category_keyword():
    d = load_dialect("ar-v1")
    assert d.categories[normalize_identifier("إذا")] == "keyword"


def test_category_type():
    d = load_dialect("ar-v1")
    assert d.categories[normalize_identifier("نص")] == "type"


def test_category_function():
    d = load_dialect("ar-v1")
    assert d.categories[normalize_identifier("اطبع")] == "function"


def test_category_exception():
    d = load_dialect("ar-v1")
    assert d.categories[normalize_identifier("خطا_قيمة")] == "exception"


def test_category_method():
    d = load_dialect("ar-v1")
    assert d.categories[normalize_identifier("اضف")] == "method"


def test_category_literal():
    d = load_dialect("ar-v1")
    assert d.categories[normalize_identifier("صحيح")] == "literal"


# Group: Cross-map coexistence (collision context)
def test_cross_map_allowed(tmp_path: Path):
    fixture = tmp_path / "cross_map.md"
    fixture.write_text(
        "## 1. Control-flow keywords\n"
        "| `if` | عد | — | | \n"
        "## 6. Common methods on built-in types\n"
        "| `.count` | عد | — | | \n"
        + "".join(f"| `dummy{i}` | دممي{i} | — | | \n" for i in range(150)),
        encoding="utf-8",
    )
    d = load_dialect("malformed", path=fixture)
    norm_ad = normalize_identifier("عد")
    assert norm_ad in d.names
    assert norm_ad in d.attributes


# Group: Cache
def test_load_is_cached():
    d1 = load_dialect("ar-v1")
    d2 = load_dialect("ar-v1")
    assert d1 is d2


def test_load_with_path_cached(tmp_path: Path):
    fixture = tmp_path / "cache_fixture.md"
    fixture.write_text(
        "## 1. Control-flow keywords\n"
        + "".join(f"| `dummy{i}` | دممي{i} | — | | \n" for i in range(150)),
        encoding="utf-8",
    )
    d1 = load_dialect("cache_fixture", path=fixture)
    d2 = load_dialect("cache_fixture", path=fixture)
    assert d1 is d2


# Group: Malformed dictionary errors


def create_fixture(tmp_path: Path, content: str) -> Path:
    fixture = tmp_path / "dialect_malformed.md"
    # Ensure minimum 150 entries unless specified otherwise by the test
    padding = "".join(f"| `dummy{i}` | دممي{i} | — | | \n" for i in range(150))
    fixture.write_text(content + padding, encoding="utf-8")
    return fixture


def test_missing_backticks_raises(tmp_path: Path):
    content = "## 1. Control-flow keywords\n| if | إذا | — | | \n"
    fixture = create_fixture(tmp_path, content)
    with pytest.raises(DialectError) as exc:
        load_dialect("malformed", path=fixture)
    assert "Line 2" in str(exc.value)


def test_empty_canonical_raises(tmp_path: Path):
    content = "## 1. Control-flow keywords\n| `if` |  | — | | \n"
    fixture = create_fixture(tmp_path, content)
    with pytest.raises(DialectError):
        load_dialect("malformed", path=fixture)


def test_duplicate_normalized_key_raises(tmp_path: Path):
    content = "## 1. Control-flow keywords\n" "| `if` | إذا | — | | \n" "| `else` | إذا | — | | \n"
    fixture = create_fixture(tmp_path, content)
    with pytest.raises(DialectError) as exc:
        load_dialect("malformed", path=fixture)
    assert "if" in str(exc.value)
    assert "else" in str(exc.value)


def test_row_before_section_raises(tmp_path: Path):
    content = "| `if` | إذا | — | | \n## 1. Control-flow keywords\n"
    fixture = create_fixture(tmp_path, content)
    with pytest.raises(DialectError):
        load_dialect("malformed", path=fixture)


def test_insufficient_entries_raises(tmp_path: Path):
    fixture = tmp_path / "dialect_malformed.md"
    fixture.write_text("## 1. Control-flow keywords\n| `if` | إذا | — | | \n", encoding="utf-8")
    with pytest.raises(DialectError) as exc:
        load_dialect("malformed", path=fixture)
    assert "150" in str(exc.value)


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_dialect("malformed", path=Path("does_not_exist.md"))


# Group: Cross-check
def test_all_python_targets_are_identifiers():
    d = load_dialect("ar-v1")
    for norm_key, py_sym in d.names.items():
        assert py_sym.isidentifier(), f"'{py_sym}' is not a valid identifier"
        is_kw = keyword.iskeyword(py_sym)
        if is_kw:
            assert d.categories[norm_key] in (
                "keyword",
                "literal",
            ), f"'{py_sym}' is a Python keyword but not in keyword category"
        else:
            assert not is_kw

    for _norm_key, py_sym in d.attributes.items():
        assert py_sym.isidentifier(), f"'{py_sym}' is not a valid identifier"
        assert not keyword.iskeyword(
            py_sym
        ), f"'{py_sym}' is a Python keyword but used as attribute"


# Group: v1.1 additions (Category C — no ADR required per ADR 0003)

def test_builtin_breakpoint():
    d = load_dialect("ar-v1")
    assert d.names[normalize_identifier("نقطة_توقف")] == "breakpoint"


# Set methods
def test_method_set_add():
    d = load_dialect("ar-v1")
    assert d.attributes[normalize_identifier("ضم")] == "add"


def test_method_set_discard():
    d = load_dialect("ar-v1")
    assert d.attributes[normalize_identifier("أسقط")] == "discard"


def test_method_set_union():
    d = load_dialect("ar-v1")
    assert d.attributes[normalize_identifier("اتحاد")] == "union"


def test_method_set_intersection():
    d = load_dialect("ar-v1")
    assert d.attributes[normalize_identifier("تقاطع")] == "intersection"


def test_method_set_difference():
    d = load_dialect("ar-v1")
    assert d.attributes[normalize_identifier("فرق")] == "difference"


# String methods (new)
def test_method_str_title():
    d = load_dialect("ar-v1")
    assert d.attributes[normalize_identifier("عنوان")] == "title"


def test_method_str_capitalize():
    d = load_dialect("ar-v1")
    assert d.attributes[normalize_identifier("كبر_الأول")] == "capitalize"


def test_method_str_swapcase():
    d = load_dialect("ar-v1")
    assert d.attributes[normalize_identifier("عكس_الحالة")] == "swapcase"


def test_method_str_zfill():
    d = load_dialect("ar-v1")
    assert d.attributes[normalize_identifier("مل_بأصفار")] == "zfill"


def test_method_str_center():
    d = load_dialect("ar-v1")
    assert d.attributes[normalize_identifier("توسط")] == "center"


def test_method_str_ljust():
    d = load_dialect("ar-v1")
    assert d.attributes[normalize_identifier("ضبط_يسار")] == "ljust"


def test_method_str_rjust():
    d = load_dialect("ar-v1")
    assert d.attributes[normalize_identifier("ضبط_يمين")] == "rjust"


# Dict methods (new)
def test_method_dict_popitem():
    d = load_dialect("ar-v1")
    assert d.attributes[normalize_identifier("انتزع_زوج")] == "popitem"


def test_method_dict_pop_via_existing_mapping():
    # dict.pop and list.pop share the Python name "pop"; انتزع already covers both
    d = load_dialect("ar-v1")
    assert d.attributes[normalize_identifier("انتزع")] == "pop"
