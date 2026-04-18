import io
import subprocess
import sys

from arabicpython import __version__
from arabicpython.cli import main


# Help and version (3)
def test_help_flag_exits_zero(capsys):
    ret = main(["-h"])
    assert ret == 0
    out, err = capsys.readouterr()
    assert "usage:" in out or "usage:" in err


def test_version_flag_prints_version(capsys):
    # argparse.version action typically exits with 0
    # but some versions might raise SystemExit.
    # The spec says main returns int.
    try:
        ret = main(["--version"])
    except SystemExit as e:
        ret = e.code
    assert ret == 0
    out, err = capsys.readouterr()
    assert f"apython {__version__}" in out or f"apython {__version__}" in err


def test_cli_no_args_drops_into_repl(monkeypatch, capsys):
    """main([]) drops into REPL; we feed an immediate EOF to exit cleanly."""
    monkeypatch.setattr("sys.stdin", io.StringIO(""))
    ret = main([])
    assert ret == 0
    out, err = capsys.readouterr()
    assert "apython" in out or "apython" in err


def test_cli_repl_executes_piped_arabic(monkeypatch, capsys):
    """Pipe an Arabic command into apython with no args; it should run and exit."""
    monkeypatch.setattr("sys.stdin", io.StringIO("اطبع('cli_repl')\n"))
    ret = main([])
    assert ret == 0
    out, err = capsys.readouterr()
    assert "cli_repl" in out


# File mode — golden path (5)
def test_run_simple_arabic_file(tmp_path, capsys):
    f = tmp_path / "hello.apy"
    f.write_text('اطبع("مرحبا")\n', encoding="utf-8")
    ret = main([str(f)])
    assert ret == 0
    out, err = capsys.readouterr()
    assert "مرحبا" in out


def test_run_pure_ascii_file(tmp_path, capsys):
    f = tmp_path / "ascii.apy"
    f.write_text('print("hi")\n', encoding="utf-8")
    ret = main([str(f)])
    assert ret == 0
    out, err = capsys.readouterr()
    assert "hi" in out


def test_run_arabic_keywords_and_digits(tmp_path, capsys):
    f = tmp_path / "keywords.apy"
    # if x > 5: print(x)
    f.write_text("x = ١٠\nإذا x > ٥:\n    اطبع(x)\n", encoding="utf-8")
    ret = main([str(f)])
    assert ret == 0
    out, err = capsys.readouterr()
    assert "10" in out


def test_run_function_def_and_call(tmp_path, capsys):
    f = tmp_path / "func.apy"
    f.write_text("دالة جمع(أ، ب):\n    ارجع أ + ب\n\nاطبع(جمع(١، ٢))\n", encoding="utf-8")
    ret = main([str(f)])
    assert ret == 0
    out, err = capsys.readouterr()
    assert "3" in out


def test_run_class_with_method(tmp_path, capsys):
    f = tmp_path / "class.apy"
    # class C: def m(self): return 42
    f.write_text(
        "صنف ص:\n    دالة م(الذات):\n        ارجع ٤٢\n\nكائن = ص()\nاطبع(كائن.م())\n",
        encoding="utf-8",
    )
    ret = main([str(f)])
    assert ret == 0
    out, err = capsys.readouterr()
    assert "42" in out


# Inline mode (2)
def test_inline_arabic_code(capsys):
    ret = main(["-c", "اطبع('xy')"])
    assert ret == 0
    out, err = capsys.readouterr()
    assert "xy" in out


def test_inline_with_forwarded_args(capsys):
    ret = main(["-c", "import sys; print(sys.argv)", "a", "b"])
    assert ret == 0
    out, err = capsys.readouterr()
    # sys.argv inside should be ["-c", "a", "b"]
    assert "['-c', 'a', 'b']" in out


# Stdin mode (2)
def test_stdin_arabic_code(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("اطبع('from_stdin')\n"))
    ret = main(["-"])
    assert ret == 0
    out, err = capsys.readouterr()
    assert "from_stdin" in out


def test_stdin_with_forwarded_args(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("import sys; print(sys.argv)\n"))
    ret = main(["-", "extra_arg"])
    assert ret == 0
    out, err = capsys.readouterr()
    assert "['-', 'extra_arg']" in out


# __name__, __file__, sys.argv (4)
def test_dunder_name_is_main(tmp_path, capsys):
    f = tmp_path / "test_name.apy"
    f.write_text("print(__name__)\n", encoding="utf-8")
    ret = main([str(f)])
    assert ret == 0
    out, err = capsys.readouterr()
    assert "__main__" in out


def test_dunder_file_is_absolute_path(tmp_path, capsys):
    f = tmp_path / "test_file.apy"
    f.write_text("print(__file__)\n", encoding="utf-8")
    ret = main([str(f)])
    assert ret == 0
    out, err = capsys.readouterr()
    assert out.strip() == str(f.absolute())


def test_sys_argv_in_file_mode(tmp_path, capsys):
    f = tmp_path / "test_argv.apy"
    f.write_text("import sys; print(sys.argv)\n", encoding="utf-8")
    ret = main([str(f), "alpha", "beta"])
    assert ret == 0
    out, err = capsys.readouterr()
    # Using repr() on the list elements escapes backslashes on Windows.
    # We construct the expected list string to match.
    expected = str([str(f), "alpha", "beta"])
    assert expected in out or str([str(f.absolute()), "alpha", "beta"]) in out


def test_sys_argv_restored_after_run(tmp_path, capsys):
    f = tmp_path / "nop.apy"
    f.write_text("pass\n", encoding="utf-8")
    original_argv = sys.argv[:]
    ret = main([str(f)])
    assert ret == 0
    assert sys.argv == original_argv


# Error reporting (6)
def test_missing_file_prints_error_exits_one(capsys):
    ret = main(["non_existent.apy"])
    assert ret == 1
    out, err = capsys.readouterr()
    assert "can't open file" in err
    assert "non_existent.apy" in err


def test_directory_instead_of_file(tmp_path, capsys):
    ret = main([str(tmp_path)])
    assert ret == 1
    out, err = capsys.readouterr()
    assert "can't open file" in err
    assert str(tmp_path) in err


def test_bidi_in_source_reports_syntax_error(tmp_path, capsys):
    f = tmp_path / "bidi.apy"
    # U+202E is RIGHT-TO-LEFT OVERRIDE
    f.write_text("\u202e", encoding="utf-8")
    ret = main([str(f)])
    assert ret == 1
    out, err = capsys.readouterr()
    assert "bidi control" in err
    assert "trojansource.codes" in err


def test_mixed_digit_in_source_reports_error(tmp_path, capsys):
    f = tmp_path / "mixed.apy"
    f.write_text("x = ١2\n", encoding="utf-8")
    ret = main([str(f)])
    assert ret == 1
    out, err = capsys.readouterr()
    assert "mixed digit" in err


def test_translated_python_syntax_error(tmp_path, capsys):
    f = tmp_path / "bad_python.apy"
    # إذا x: (missing pass/body)
    f.write_text("إذا صحيح:\n", encoding="utf-8")
    ret = main([str(f)])
    assert ret == 1
    out, err = capsys.readouterr()
    assert "خطا" in err or "تتبع_الأخطاء" in err


def test_runtime_exception_prints_traceback(tmp_path, capsys):
    f = tmp_path / "runtime_err.apy"
    f.write_text("x = 1 / 0\n", encoding="utf-8")
    ret = main([str(f)])
    assert ret == 1
    out, err = capsys.readouterr()
    assert "خطا_القسمه_على_صفر" in err
    assert "تتبع_الأخطاء" in err


# sys.exit and KeyboardInterrupt (3)
def test_program_calls_sys_exit_zero(tmp_path):
    f = tmp_path / "exit0.apy"
    f.write_text("import sys; sys.exit(0)\n", encoding="utf-8")
    ret = main([str(f)])
    assert ret == 0


def test_program_calls_sys_exit_nonzero(tmp_path):
    f = tmp_path / "exit7.apy"
    f.write_text("import sys; sys.exit(7)\n", encoding="utf-8")
    ret = main([str(f)])
    assert ret == 7


def test_keyboard_interrupt_exits_130(tmp_path, capsys):
    f = tmp_path / "ki.apy"
    f.write_text("raise KeyboardInterrupt\n", encoding="utf-8")
    ret = main([str(f)])
    assert ret == 130
    out, err = capsys.readouterr()
    assert "KeyboardInterrupt" in err


# File encoding (2)
def test_utf8_with_bom_handled(tmp_path, capsys):
    f = tmp_path / "bom.apy"
    # UTF-8 with BOM
    f.write_bytes(b"\xef\xbb\xbf" + 'اطبع("bom")\n'.encode())
    ret = main([str(f)])
    assert ret == 0
    out, err = capsys.readouterr()
    assert "bom" in out


def test_non_utf8_file_clean_error(tmp_path, capsys):
    f = tmp_path / "latin1.apy"
    # Some invalid UTF-8 bytes
    f.write_bytes(b"\xe0\xe1\xe2")
    ret = main([str(f)])
    assert ret == 1
    out, err = capsys.readouterr()
    assert "invalid UTF-8 encoding" in err


# Subprocess smoke (1)
def test_subprocess_end_to_end():
    # Use actual Arabic for print: اطبع
    res = subprocess.run(
        [sys.executable, "-m", "arabicpython.cli", "-c", "اطبع('ok')"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert res.returncode == 0
    assert "ok" in res.stdout


# UTF-8 stream configuration (4)
def test_configure_utf8_reconfigures_stdout(monkeypatch):
    from arabicpython.cli import _configure_utf8_streams

    buf = io.BytesIO()
    fake = io.TextIOWrapper(buf, encoding="cp1252")
    monkeypatch.setattr(sys, "stdout", fake)
    _configure_utf8_streams()
    assert sys.stdout.encoding.lower().replace("-", "") == "utf8"


def test_configure_utf8_safe_with_non_reconfigurable_stream(monkeypatch):
    from arabicpython.cli import _configure_utf8_streams

    monkeypatch.setattr(sys, "stdout", io.StringIO())
    monkeypatch.setattr(sys, "stderr", io.StringIO())
    _configure_utf8_streams()  # must not raise


def test_configure_utf8_safe_with_none_stream(monkeypatch):
    from arabicpython.cli import _configure_utf8_streams

    monkeypatch.setattr(sys, "stdout", None)
    _configure_utf8_streams()  # must not raise


def test_main_recovers_from_cp1252_stdout(tmp_path, monkeypatch):
    f = tmp_path / "h.apy"
    f.write_text('اطبع("مرحبا")\n', encoding="utf-8")
    buf = io.BytesIO()
    fake = io.TextIOWrapper(buf, encoding="cp1252", write_through=True)
    monkeypatch.setattr(sys, "stdout", fake)
    rc = main([str(f)])
    fake.flush()
    assert rc == 0
    assert "مرحبا" in buf.getvalue().decode("utf-8")
