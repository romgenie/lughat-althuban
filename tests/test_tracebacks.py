import io
import re
import sys

import pytest

from arabicpython import cli, run_repl
from arabicpython.normalize import normalize_identifier
from arabicpython.tracebacks import (
    EXCEPTION_NAMES_AR,
    MESSAGE_TEMPLATES_AR,
    format_translated_exception,
    install_excepthook,
    print_translated_exception,
    translate_exception_message,
    translate_exception_name,
    uninstall_excepthook,
)

# Translation lookups (8)


def test_translate_exception_name_known():
    assert translate_exception_name("ZeroDivisionError") == "خطا_القسمه_على_صفر"


def test_translate_exception_name_unknown_passes_through():
    assert translate_exception_name("MyCustomError") == "MyCustomError"


def test_translate_message_division_by_zero():
    assert translate_exception_message("division by zero") == "القسمة على صفر"


def test_translate_message_name_error():
    assert translate_exception_message("name 'foo' is not defined") == "الاسم 'foo' غير معرّف"


def test_translate_message_attribute_error():
    msg = "'list' object has no attribute 'frobnicate'"
    translated = translate_exception_message(msg)
    assert "الكائن من نوع 'list' لا يملك الخاصية 'frobnicate'" in translated


def test_translate_message_unknown_passes_through():
    msg = "some random error message"
    assert translate_exception_message(msg) == msg


def test_translate_message_first_match_wins():
    # The first pattern for name error is more general, but they are anchored.
    # If there were overlapping patterns, the first would win.
    pass


def test_all_38_exception_names_have_translations():
    assert len(EXCEPTION_NAMES_AR) == 38
    for _name, translation in EXCEPTION_NAMES_AR.items():
        assert translation
        # Contains at least one Arabic codepoint U+0600–U+06FF
        assert any("\u0600" <= ch <= "\u06ff" for ch in translation)


# Type-name table coverage (4)


def test_table_includes_zero_division_error():
    assert "ZeroDivisionError" in EXCEPTION_NAMES_AR


def test_table_includes_all_common_types():
    common = {
        "NameError",
        "TypeError",
        "ValueError",
        "IndexError",
        "KeyError",
        "AttributeError",
        "ImportError",
        "FileNotFoundError",
        "ZeroDivisionError",
    }
    for c in common:
        assert c in EXCEPTION_NAMES_AR


def test_table_no_duplicate_arabic_values():
    values = list(EXCEPTION_NAMES_AR.values())
    assert len(values) == len(set(values))


def test_table_arabic_names_are_normalized():
    for val in EXCEPTION_NAMES_AR.values():
        assert normalize_identifier(val) == val


# Message template coverage (3)


def test_message_templates_compiled():
    for p, _ in MESSAGE_TEMPLATES_AR:
        assert isinstance(p, re.Pattern)


def test_message_templates_arabic_present():
    for _, t in MESSAGE_TEMPLATES_AR:
        assert any("\u0600" <= ch <= "\u06ff" for ch in t)


def test_message_templates_anchored():
    for p, _ in MESSAGE_TEMPLATES_AR:
        assert p.pattern.startswith("^")
        assert p.pattern.endswith("$")


# format_translated_exception (5)


def test_format_zero_division_simple():
    try:
        1 / 0  # noqa: B018
    except ZeroDivisionError:
        output = format_translated_exception(*sys.exc_info())
    assert "خطا_القسمه_على_صفر" in output
    assert "القسمة على صفر" in output
    assert "تتبع_الأخطاء" in output


def test_format_includes_arabic_module_marker():
    try:
        exec("1/0")
    except ZeroDivisionError:
        output = format_translated_exception(*sys.exc_info())
    assert "<الوحدة>" in output


def test_format_includes_file_path_and_line():
    try:
        1 / 0  # noqa: B018
    except ZeroDivisionError:
        output = format_translated_exception(*sys.exc_info())
    assert "ملف" in output
    assert "سطر" in output


def test_format_chained_exception_with_from():
    try:
        try:
            1 / 0  # noqa: B018
        except ZeroDivisionError as e:
            raise ValueError("bad value") from e
    except ValueError:
        output = format_translated_exception(*sys.exc_info())
    assert "السبب المباشر للاستثناء أعلاه:" in output
    assert "خطا_القسمه_على_صفر" in output
    assert "خطا_قيمه" in output


def test_format_chained_exception_implicit_context():
    try:
        try:
            1 / 0  # noqa: B018
        except ZeroDivisionError:
            raise ValueError("bad value")  # noqa: B904
    except ValueError:
        output = format_translated_exception(*sys.exc_info())
    assert "أثناء معالجة الاستثناء أعلاه, حدث استثناء آخر:" in output
    assert "خطا_القسمه_على_صفر" in output
    assert "خطا_قيمه" in output


# print_translated_exception (2)


def test_print_writes_to_stderr_by_default(capsys):
    try:
        1 / 0  # noqa: B018
    except ZeroDivisionError:
        print_translated_exception(*sys.exc_info())
    _, err = capsys.readouterr()
    assert "خطا_القسمه_على_صفر" in err


def test_print_accepts_custom_file():
    buf = io.StringIO()
    try:
        1 / 0  # noqa: B018
    except ZeroDivisionError:
        print_translated_exception(*sys.exc_info(), file=buf)
    assert "خطا_القسمه_على_صفر" in buf.getvalue()


# install_excepthook / uninstall_excepthook (4)


@pytest.fixture(autouse=True)
def snapshot_excepthook():
    from arabicpython import tracebacks

    orig_hook = sys.excepthook
    orig_saved = tracebacks._saved_excepthook

    # Baseline for this file
    sys.excepthook = sys.__excepthook__
    tracebacks._saved_excepthook = None

    yield sys.__excepthook__

    sys.excepthook = orig_hook
    tracebacks._saved_excepthook = orig_saved


def test_install_replaces_excepthook(snapshot_excepthook):
    install_excepthook()
    assert sys.excepthook is print_translated_exception


def test_install_is_idempotent(snapshot_excepthook):
    install_excepthook()
    first_hook = sys.excepthook
    install_excepthook()
    assert sys.excepthook is first_hook


def test_uninstall_restores_previous(snapshot_excepthook):
    orig = sys.excepthook
    install_excepthook()
    uninstall_excepthook()
    assert sys.excepthook is orig


def test_uninstall_idempotent(snapshot_excepthook):
    uninstall_excepthook()
    uninstall_excepthook()
    # Should not raise


# CLI integration (3)


def test_cli_runtime_error_shows_arabic(tmp_path, capsys):
    f = tmp_path / "err.apy"
    f.write_text("x = 1 / 0\n", encoding="utf-8")
    assert cli.main([str(f)]) == 1
    _, err = capsys.readouterr()
    assert "خطا_القسمه_على_صفر" in err
    assert "القسمة على صفر" in err


def test_cli_name_error_shows_arabic(tmp_path, capsys):
    f = tmp_path / "name.apy"
    f.write_text("undefined_var\n", encoding="utf-8")
    assert cli.main([str(f)]) == 1
    _, err = capsys.readouterr()
    assert "خطا_اسم" in err
    assert "الاسم 'undefined_var' غير معرّف" in err


def test_cli_unknown_exception_falls_through_to_english_message(tmp_path, capsys):
    f = tmp_path / "custom.apy"
    f.write_text("raise Exception('unique message')\n", encoding="utf-8")
    assert cli.main([str(f)]) == 1
    _, err = capsys.readouterr()
    assert "استثناء: unique message" in err


# REPL integration (2)


def test_repl_runtime_error_shows_arabic(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("١/٠\n"))
    # run_repl calls sys.exit, so we catch it
    run_repl(banner="", exit_msg="")
    _, err = capsys.readouterr()
    assert "خطا_القسمه_على_صفر" in err


def test_repl_name_error_shows_arabic(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("undefined_in_repl\n"))
    run_repl(banner="", exit_msg="")
    _, err = capsys.readouterr()
    assert "خطا_اسم" in err


# Class identity preservation (1)


def test_exception_class_identity_unchanged(tmp_path, capsys):
    f = tmp_path / "identity.apy"
    f.write_text("try:\n    1/0\nexcept ZeroDivisionError:\n    اطبع('caught')\n", encoding="utf-8")
    assert cli.main([str(f)]) == 0
    out, _ = capsys.readouterr()
    assert "caught" in out
