import io
import sys

import pytest

from arabicpython import __version__
from arabicpython.repl import ArabicConsole, run_repl


@pytest.fixture
def console():
    """Fresh ArabicConsole with isolated locals and stderr captured to a StringIO."""
    c = ArabicConsole(locals={})
    err_buf = io.StringIO()
    c.write = err_buf.write  # InteractiveConsole writes errors via self.write
    c._test_err = err_buf
    return c


@pytest.fixture(autouse=True)
def isolate_history(monkeypatch, tmp_path):
    """Redirect history file to tmp_path so tests don't touch ~/.apython_history."""
    monkeypatch.setattr(
        "os.path.expanduser",
        lambda p: str(tmp_path / p.lstrip("~/")) if p.startswith("~/") else p,
    )


# runsource — basic execution (5)


def test_runsource_executes_arabic_print(console, capsys):
    ret = console.runsource("اطبع('hi')")
    assert ret is False
    out, err = capsys.readouterr()
    assert "hi\n" in out


def test_runsource_executes_arabic_assignment(console):
    ret = console.runsource("س = ٥")
    assert ret is False
    assert console.locals["س"] == 5
    # persistence
    ret = console.runsource("اطبع(س)")
    assert ret is False


def test_runsource_returns_true_for_incomplete_block(console):
    ret = console.runsource("إذا صحيح:")
    assert ret is True


def test_runsource_returns_true_for_unclosed_triple_string(console):
    ret = console.runsource('س = """unclosed')
    assert ret is True


def test_runsource_handles_pure_ascii(console, capsys):
    ret = console.runsource("print('ascii')")
    assert ret is False
    out, err = capsys.readouterr()
    assert "ascii\n" in out


# Multi-line constructs (4)


def test_multiline_function_def(console, capsys):
    assert console.push("دالة f():") is True
    assert console.push("    اطبع('inside')") is True
    assert console.push("") is False
    assert "f" in console.locals
    console.push("f()")
    out, err = capsys.readouterr()
    assert "inside\n" in out


def test_multiline_class_def(console, capsys):
    assert console.push("صنف C:") is True
    assert console.push("    دالة m(الذات):") is True
    assert console.push("        اطبع('meth')") is True
    assert console.push("") is False  # exit block
    assert "C" in console.locals
    console.push("C().m()")
    out, err = capsys.readouterr()
    assert "meth\n" in out


def test_multiline_for_loop(console, capsys):
    assert console.push("لكل i in [١, ٢]:") is True
    assert console.push("    اطبع(i)") is True
    assert console.push("") is False
    out, err = capsys.readouterr()
    assert "1\n2\n" in out


def test_multiline_with_arabic_keywords_and_digits(console, capsys):
    console.locals["x"] = 10
    assert console.push("إذا x > ٥:") is True
    assert console.push("    اطبع('كبير')") is True
    assert console.push("") is False
    out, err = capsys.readouterr()
    assert "كبير\n" in out


# Error handling — translate-time (3)


def test_bidi_in_input_clean_error_no_traceback(console):
    # U+202E is RIGHT-TO-LEFT OVERRIDE
    ret = console.runsource("\u202e")
    assert ret is False
    err_text = console._test_err.getvalue()
    assert "bidi control" in err_text
    assert "Traceback" not in err_text


def test_mixed_digit_clean_error(console):
    ret = console.runsource("x = ١2")
    assert ret is False
    err_text = console._test_err.getvalue()
    assert "mixed digit" in err_text
    assert "Traceback" not in err_text


def test_buffer_resets_after_translate_error(console, capsys):
    console.runsource("\u202e")
    # Buffer should be reset, next command works
    ret = console.runsource("اطبع('after')")
    assert ret is False
    out, err = capsys.readouterr()
    assert "after\n" in out


# Error handling — runtime (3)


def test_zero_division_shows_traceback(console):
    ret = console.runsource("١/٠")
    assert ret is False
    err_text = console._test_err.getvalue()
    assert "خطا_القسمه_على_صفر" in err_text
    assert "تتبع_الأخطاء" in err_text


def test_name_error_shows_traceback(console):
    ret = console.runsource("undefined_name")
    assert ret is False
    err_text = console._test_err.getvalue()
    assert "خطا_اسم" in err_text
    assert "تتبع_الأخطاء" in err_text


def test_runtime_error_does_not_clear_state(console, capsys):
    console.runsource("س = ٤٢")
    console.runsource("١/٠")
    # State should be preserved
    console.runsource("اطبع(س)")
    out, _ = capsys.readouterr()
    assert "42\n" in out


# State persistence (3)


def test_imports_persist_across_calls(console, capsys):
    console.runsource("import math")
    console.runsource("اطبع(math.pi)")
    out, err = capsys.readouterr()
    assert "3.14" in out


def test_function_defined_then_called_separately(console, capsys):
    # A one-line def in REPL still needs a blank line if using push,
    # but runsource("def...") should return True.
    assert console.runsource("دالة foo(): اطبع('foo')") is True
    # If we want it executed, we need to complete the block
    console.runsource("دالة foo(): اطبع('foo')\n")  # Some versions might accept this,
    # but InteractiveConsole.push ensures it's joined.

    # Let's use push to be safe
    console.push("دالة foo(): اطبع('foo')")
    console.push("")  # complete it
    console.push("foo()")
    out, err = capsys.readouterr()
    assert "foo\n" in out


def test_class_defined_then_instantiated(console, capsys):
    console.push("صنف K: pass")
    console.push("")  # complete
    console.push("k = K()")
    console.push("اطبع(type(k).__name__)")
    out, err = capsys.readouterr()
    assert "K\n" in out


# run_repl — entry point (4)


def test_run_repl_immediate_eof_exits_zero(monkeypatch):
    monkeypatch.setattr("sys.stdin", io.StringIO(""))
    ret = run_repl(banner="", exit_msg="")
    assert ret == 0


def test_run_repl_banner_includes_version(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO(""))
    run_repl()
    out, err = capsys.readouterr()
    assert f"apython {__version__}" in out or f"apython {__version__}" in err


def test_run_repl_executes_piped_input(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("اطبع('piped')\n"))
    ret = run_repl(banner="", exit_msg="")
    assert ret == 0
    out, err = capsys.readouterr()
    assert "piped\n" in out


def test_run_repl_sys_exit_propagates(monkeypatch):
    monkeypatch.setattr("sys.stdin", io.StringIO("import sys; sys.exit(7)\n"))
    ret = run_repl(banner="", exit_msg="")
    assert ret == 7


# Environment overrides (2)


def test_apython_ps1_env_override(monkeypatch):
    monkeypatch.setenv("APYTHON_PS1", "آب> ")
    monkeypatch.setattr("sys.stdin", io.StringIO(""))
    run_repl(banner="", exit_msg="")
    assert sys.ps1 == "آب> "


def test_apython_ps2_env_override(monkeypatch):
    monkeypatch.setenv("APYTHON_PS2", "صص> ")
    monkeypatch.setattr("sys.stdin", io.StringIO(""))
    run_repl(banner="", exit_msg="")
    assert sys.ps2 == "صص> "


# Readline graceful fallback (2)


def test_readline_unavailable_does_not_crash(monkeypatch):
    import builtins

    real_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if name == "readline":
            raise ImportError("mocked")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", mock_import)
    monkeypatch.setattr("sys.stdin", io.StringIO(""))
    ret = run_repl(banner="", exit_msg="")
    assert ret == 0


def test_history_file_used_when_readline_present(monkeypatch, tmp_path):
    try:
        import readline  # noqa: F401
    except ImportError:
        pytest.skip("readline not available")

    monkeypatch.setattr("sys.stdin", io.StringIO("x = 1\n"))
    run_repl(banner="", exit_msg="")
    history_file = tmp_path / ".apython_history"
    assert history_file.exists()


# KeyboardInterrupt (1)


def test_keyboard_interrupt_does_not_exit_repl(console, capsys):
    # ArabicConsole uses runcode for execution, which should catch KeyboardInterrupt
    # and print a traceback.
    ret = console.runsource("raise KeyboardInterrupt")
    assert ret is False
    err_text = console._test_err.getvalue()
    assert "مقاطعه_لوحه_المفاتيح" in err_text
